import ast
import numpy as np
from PIL import Image
import tensorflow as tf
from collections import OrderedDict
from tensorflow.python.saved_model import tag_constants
from model_service.tfserving_model_service import TfServingBaseService
import threading
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class gesture_classify_service(TfServingBaseService):
    def __init__(self, model_name, model_path):
        # these three parameters are no need to modify
        self.model = None
        self.predict = None
        self.model_name = model_name
        self.model_path = model_path
        self.signature_key = 'predict_images'

        self.input_size = 224  # the input image size of the model
        self.load_model()

        self.label_id_name_dict = \
        {
            "0": "Background",
            "1": "Great",
            "2": "OK",
            "3": "Other",
            "4": "Rock",
            "5": "Yeah"
        }

    def load_model(self):
        # load saved_model 格式的模型
        self.model = tf.saved_model.load(self.model_path)

        signature_defs = self.model.signatures.keys()
        signature = []
        # only one signature allowed
        for signature_def in signature_defs:
            signature.append(signature_def)

        if len(signature) == 1:
            model_signature = signature[0]
        else:
            model_signature = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY

        self.predict = self.model.signatures[model_signature]

    def center_img(self, img, size=None, fill_value=255):
        """
        center img in a square background
        """
        h, w = img.shape[:2]
        if size is None:
            size = max(h, w)
        shape = (size, size) + img.shape[2:]
        background = np.full(shape, fill_value, np.uint8)
        center_x = (size - w) // 2
        center_y = (size - h) // 2
        background[center_y:center_y + h, center_x:center_x + w] = img
        return background

    def preprocess_img(self, img):
        """
        image preprocessing
        you can add your special preprocess method here
        """
        resize_scale = self.input_size / max(img.size[:2])
        img = img.resize((int(img.size[0] * resize_scale), int(img.size[1] * resize_scale)))
        img = img.convert('RGB')
        img = np.array(img)
        img = img[:, :, ::-1]
        img = self.center_img(img, self.input_size)
        return img

    def _preprocess(self, data):
        preprocessed_data = {}
        for k, v in data.items():
            for file_name, file_content in v.items():
                img = Image.open(file_content)
                img = self.preprocess_img(img)
                preprocessed_data[k] = img
        return preprocessed_data

    def _inference(self, data):
        """
        model inference function
        Here are a inference example of resnet, if you use another model, please modify this function
        """
        img = data['input_img']
        img = img[np.newaxis, :, :, :]  # the input tensor shape of resnet is [?, 224, 224, 3]
        img = tf.convert_to_tensor(img, dtype=tf.float32)
        pred_score = self.predict(img)
        if pred_score is not None:
            output = pred_score['output']
            pred_label = np.argmax(output, axis=1)[0]
            result = {'result': self.label_id_name_dict[str(pred_label)]}
        else:
            result = {'result': 'predict score is None'}
        return result

    def _postprocess(self, data):
        return data
