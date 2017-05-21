from flask import Flask
from flask import request
from werkzeug.exceptions import HTTPException, NotFound
from flask import send_file
import cv2
import subprocess
import uuid
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_hyperion():
    return 'Hello, Hyperion!'

@app.route('/logs', methods =['GET', 'POST'])
def logs():
    if request.method=='POST':
        try:
            f = request.files['logs_image']
            file_name_in = '/tmp/hyperion_in_' + str(uuid.uuid4())[:8]
            file_name_out = file_name_in+'.png'
            f.save(file_name_in)

            image_in = cv2.imread(file_name_in)
            gray = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(file_name_out, gray)


            return send_file(file_name_out, mimetype='image/png')
        except HTTPException as e:
            return str(e)
    else:
        return 'Only POST method can be used'
