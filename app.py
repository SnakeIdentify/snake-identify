from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re

import numpy
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from PIL import Image
import numpy as np
from skimage import transform

def load(filename):
   np_image = Image.open(filename)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (100, 100, 1))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image







# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model'

# Load your trained model
model = load_model(MODEL_PATH)
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    # img = image.load_img(img_path, target_size=(100, 100,1))
    #
    # # Preprocessing the image
    # x = image.img_to_array(img)
    # # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)
    #
    # # Be careful how your trained model deals with the input
    # # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    #
    # preds = model.predict(x)
    preds = model.predict(load(img_path))
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        print("##################################")
        print(basepath)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)
        # Simple argmax
        max_ped = max(preds[0])
        i = 0
        found = 0
        for p in preds[0]:
            print("P value")
            print(p)
            if p == max_ped:
                found = i
            i=i+1
        print("INDEX ||||||||||||||||||||||||||||")

        print(found)
        names = ['Geradiya','Naya',"Nayi Hami",'Geradiya','Naya',"Nayi Hami",'Geradiya','Naya',"Nayi Hami"]
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # result = str(pred_class[0][1])               # Convert to string
        return names[found]


if __name__ == '__main__':
    app.run(debug=True)

