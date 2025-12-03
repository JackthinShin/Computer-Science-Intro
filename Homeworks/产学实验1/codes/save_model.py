# -*- coding: utf-8 -*-
import os

import tensorflow as tf
import json
from tensorflow.keras.optimizers import Adam as adam
from moxing.framework import file

from train import model_fn


def load_weights(model, weighs_file_path):
    if os.path.isfile(weighs_file_path):
        print('load weights from %s' % weighs_file_path)
        if weighs_file_path.startswith('s3://'):
            weighs_file_name = weighs_file_path.rsplit('/', 1)[1]
            file.copy(weighs_file_path, '/cache/tmp/' + weighs_file_name)
            weighs_file_path = '/cache/tmp/' + weighs_file_name
            model.load_weights(weighs_file_path)
            os.remove(weighs_file_path)
        else:
            model.load_weights(weighs_file_path)
        print('load weights success')
    else:
        print('load weights failed! Please check weighs_file_path')



def save_pb_model(FLAGS, model, acc):    
    if FLAGS.mode == 'train':
        pb_save_dir_local = FLAGS.train_local
        pb_save_dir_obs = FLAGS.train_url
    elif FLAGS.mode == 'save_pb':
        freeze_weights_file_dir = FLAGS.freeze_weights_file_path.rsplit('/', 1)[0]
        if freeze_weights_file_dir.startswith('s3://'):
            pb_save_dir_local = '/cache/tmp'
            pb_save_dir_obs = freeze_weights_file_dir
        else:
            pb_save_dir_local = freeze_weights_file_dir
            pb_save_dir_obs = pb_save_dir_local

    tf.saved_model.save(model, os.path.join(pb_save_dir_local, 'model'))
    print('save pb to local path success')

    if pb_save_dir_obs.startswith('s3://'):
        file.copy_parallel(os.path.join(pb_save_dir_local, 'model'),
                               os.path.join(pb_save_dir_obs, 'model'))
        print('copy pb to %s success' % pb_save_dir_obs)
    config_path = os.path.join(FLAGS.deploy_script_path, 'config.json')
    
    
    with open(config_path, 'r') as json_file:
        config_json = json.load(json_file)
    config_json['metrics']['accuracy'] = acc.item()

    with open(os.path.join(pb_save_dir_obs, 'model/config.json'), 'w') as json_file:
        json.dump(config_json, json_file, indent=4)

    file.copy(os.path.join(FLAGS.deploy_script_path, 'customize_service.py'),
                  os.path.join(pb_save_dir_obs, 'model/customize_service.py'))
    if file.exists(os.path.join(pb_save_dir_obs, 'model/config.json')) and \
            file.exists(os.path.join(pb_save_dir_obs, 'model/customize_service.py')):
        print('copy config.json and customize_service.py success')
    else:
        print('copy config.json and customize_service.py failed')


def load_weights_save_pb(FLAGS):
    optimizer = adam(lr=FLAGS.learning_rate, clipnorm=0.001)
    objective = 'binary_crossentropy'
    metrics = ['accuracy']
    model = model_fn(FLAGS, objective, optimizer, metrics)
    load_weights(model, FLAGS.freeze_weights_file_path)
    save_pb_model(FLAGS, model)
