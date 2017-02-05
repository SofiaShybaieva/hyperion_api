from flask import Flask
from flask import request
from werkzeug.exceptions import HTTPException, NotFound

import uuid

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Hyperion!'

@app.route('/logs', methods =['GET', 'POST'])
def logs():
    if request.method=='POST':
        try:
            f = request.files['logs_image']
            file_name_in = '/tmp/hyperion_in_' + str(uuid.uuid4())[:8]
            app.logger.debug('Got ' + file_name_in)
            f.save(file_name_in)
            return file_name_in
        except HTTPException as e:
            return str(e)
    else:
        return 'GET RESULT'