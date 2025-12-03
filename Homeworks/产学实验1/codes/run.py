# -*- coding: utf-8 -*-
'''
基于resnet50实现的垃圾分类代码
使用方法：
（1）训练
cd {run.py所在目录}
python run.py --data_url='../datasets/garbage_classify/train_data' --train_url='../model_snapshots' 
--num_classes=43 --deploy_script_path='./deploy_scripts' --test_data_url='../datasets/test_data' 
--max_epochs=10

（2）转pb
cd {run.py所在目录}
python run.py --mode=save_pb --deploy_script_path='./deploy_scripts' 
--freeze_weights_file_path='../model_snapshots/weights_000_0.9811.h5' --num_classes=43

（3）评价
cd {run.py所在目录}
python run.py --mode=eval --eval_pb_path='../model_snapshots/model' --num_classes=43
--test_data_url='../datasets/test_data'
'''
import os
import tensorflow as tf
from moxing.framework import file
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="基于ResNet50的手势识别")
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'save_pb', 'eval'],
                        help='可选: train, save_pb, eval')
    parser.add_argument('--local_data_root', type=str, default='/cache/',
                        help='用于在本地路径和OBS路径之间传输数据的目录')
    # 训练参数
    parser.add_argument('--data_url', type=str, default='', help='训练数据路径')
    parser.add_argument('--weights', type=str, default='', help='ResNet50预训练权重路径')
    parser.add_argument('--restore_model_path', type=str, default='',
                        help='历史模型路径，可以加载并继续训练')
    parser.add_argument('--train_url', type=str, default='', help='保存训练输出的路径')
    parser.add_argument('--keep_weights_file_num', type=int, default=20,
                        help='保持的最大权重文件数，-1表示无限')
    parser.add_argument('--num_classes', type=int, default=43, help='分类任务的类别数')
    parser.add_argument('--input_size', type=int, default=224, help='模型输入图像大小')
    parser.add_argument('--batch_size', type=int, default=16, help='批处理大小')
    parser.add_argument('--learning_rate', type=float, default=1e-4, help='学习率')
    parser.add_argument('--max_epochs', type=int, default=5, help='最大训练轮数')

    # 转换为pb模型参数
    parser.add_argument('--deploy_script_path', type=str, default='',
                        help='包含config.json和customize_service.py的路径')
    parser.add_argument('--freeze_weights_file_path', type=str, default='',
                        help='要转换为pb模型的h5权重文件路径，仅在mode=save_pb时有效')

    # 评估参数
    parser.add_argument('--eval_weights_path', type=str, default='', help='需要评估的权重文件路径')
    parser.add_argument('--eval_pb_path', type=str, default='', help='需要评估的pb文件路径')
    parser.add_argument('--test_data_url', type=str, default='', help='测试数据路径')

    # 本地缓存路径
    parser.add_argument('--data_local', type=str, default='', help='本地训练数据路径')
    parser.add_argument('--train_local', type=str, default='', help='本地训练输出结果路径')
    parser.add_argument('--test_data_local', type=str, default='', help='本地测试数据路径')
    parser.add_argument('--tmp', type=str, default='', help='本地临时路径')

    return parser.parse_args()

def check_args(args):
    if args.mode not in ['train', 'save_pb', 'eval']:
        raise Exception('args.mode error, should be train, save_pb or eval')
    if args.num_classes <= 0:
        raise Exception('args.num_classes error, should be a positive number associated with your classification task')

    if args.mode == 'train':
        if args.data_url == '':
            raise Exception('you must specify args.data_url')
        if not file.exists(args.data_url):
            raise Exception('args.data_url: %s is not exist' % args.data_url)
        if args.restore_model_path != '' and (not file.exists(args.restore_model_path)):
            raise Exception('args.restore_model_path: %s is not exist' % args.restore_model_path)
        if file.is_directory(args.restore_model_path):
            raise Exception('args.restore_model_path must be a file path, not a directory, %s' % args.restore_model_path)
        if args.train_url == '':
            raise Exception('you must specify args.train_url')
        elif not file.exists(args.train_url):
            file.make_dirs(args.train_url)
        if args.deploy_script_path != '' and (not file.exists(args.deploy_script_path)):
            raise Exception('args.deploy_script_path: %s is not exist' % args.deploy_script_path)
        if args.deploy_script_path != '' and file.exists(args.train_url + '/model'):
            raise Exception(args.train_url +
                            '/model is already exist, only one model directory is allowed to exist')
        if args.test_data_url != '' and (not file.exists(args.test_data_url)):
            raise Exception('args.test_data_url: %s is not exist' % args.test_data_url)

    if args.mode == 'save_pb':
        if args.deploy_script_path == '' or args.freeze_weights_file_path == '':
            raise Exception('you must specify args.deploy_script_path '
                            'and args.freeze_weights_file_path when you want to save pb')
        if not file.exists(args.deploy_script_path):
            raise Exception('args.deploy_script_path: %s is not exist' % args.deploy_script_path)
        if not file.is_directory(args.deploy_script_path):
            raise Exception('args.deploy_script_path must be a directory, not a file path, %s' % args.deploy_script_path)
        if not file.exists(args.freeze_weights_file_path):
            raise Exception('args.freeze_weights_file_path: %s is not exist' % args.freeze_weights_file_path)
        if file.is_directory(args.freeze_weights_file_path):
            raise Exception('args.freeze_weights_file_path must be a file path, not a directory, %s ' % args.freeze_weights_file_path)
        if file.exists(args.freeze_weights_file_path.rsplit('/', 1)[0] + '/model'):
            raise Exception('a model directory is already exist in ' + args.freeze_weights_file_path.rsplit('/', 1)[0]
                            + ', please rename or remove the model directory ')

    if args.mode == 'eval':
        if args.eval_weights_path == '' and args.eval_pb_path == '':
            raise Exception('you must specify args.eval_weights_path '
                            'or args.eval_pb_path when you want to evaluate a model')
        if args.eval_weights_path != '' and args.eval_pb_path != '':
            raise Exception('you must specify only one of args.eval_weights_path '
                            'and args.eval_pb_path when you want to evaluate a model')
        if args.eval_weights_path != '' and (not file.exists(args.eval_weights_path)):
            raise Exception('args.eval_weights_path: %s is not exist' % args.eval_weights_path)
        if args.eval_pb_path != '' and (not file.exists(args.eval_pb_path)):
            raise Exception('args.eval_pb_path: %s is not exist' % args.eval_pb_path)
        if not file.is_directory(args.eval_pb_path) or (not args.eval_pb_path.endswith('model')):
            raise Exception('args.eval_pb_path must be a directory named model '
                            'which contain saved_model.pb and variables, %s' % args.eval_pb_path)
        if args.test_data_url == '':
            raise Exception('you must specify args.test_data_url when you want to evaluate a model')
        if not file.exists(args.test_data_url):
            raise Exception('args.test_data_url: %s is not exist' % args.test_data_url)

def main(args):
    check_args(args)

    # 创建一些本地缓存目录，用于在本地路径和OBS路径之间传输数据
    if not args.data_url.startswith('s3://'):
        args.data_local = args.data_url
    else:
        args.data_local = os.path.join(args.local_data_root, 'train_data/')
        if not os.path.exists(args.data_local):
            file.copy_parallel(args.data_url, args.data_local)
        else:
            print('args.data_local: %s is already exist, skip copy' % args.data_local)
        
    if not args.train_url.startswith('s3://'):
        args.train_local = args.train_url
    else:
        args.train_local = os.path.join(args.local_data_root, 'model_snapshots/')
        if not os.path.exists(args.train_local):
            os.mkdir(args.train_local)
    
    if not args.test_data_url.startswith('s3://'):
        args.test_data_local = args.test_data_url
    else:
        args.test_data_local = os.path.join(args.local_data_root, 'test_data/')
        if not os.path.exists(args.test_data_local):
            file.copy_parallel(args.test_data_url, args.test_data_local)
        else:
            print('args.test_data_local: %s is already exist, skip copy' % args.test_data_local)
    
    args.tmp = os.path.join(args.local_data_root, 'tmp/')
    if not os.path.exists(args.tmp):
        os.mkdir(args.tmp)

    if args.mode == 'train':
        from train import train_model
        train_model(args)
    elif args.mode == 'save_pb':
        from save_model import load_weights_save_pb
        load_weights_save_pb(args)
    elif args.mode == 'eval':
        from eval import eval_model
        eval_model(args)

if __name__ == '__main__':
    args = parse_args()
    main(args)