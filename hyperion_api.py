from flask import Flask
from flask import request
from werkzeug.exceptions import HTTPException, NotFound
from flask import send_file
import cv2
import subprocess
import uuid
import cairosvg
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
            file_name_svg2png = file_name_in+'.png'
            file_name_out = file_name_in+'.png'
            f.save(file_name_in)
            file_name_pgm = file_name_in+'.pgm'
            file_name_svg = file_name_pgm+'.svg'

            image_in = cv2.imread(file_name_in)
            gray = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(file_name_pgm, gray)

            res = subprocess.getstatusoutput('./elsd ' + file_name_pgm)

            # convert svg2png using cairo
            cairosvg.svg2png(url=file_name_svg, write_to=file_name_svg2png)

            # apply HoughCircles on svg image
            image = cv2.imread(file_name_svg2png)
            target_size = size = 300
            # 300/x
            r = float(target_size) / image.shape[0] 
            dim = (int(image.shape[1] * r), size)
            image = cv2.resize (image, dim) #(x*r,300))
            image_in = cv2.resize (image_in, dim)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.bilateralFilter(gray, 9, 75, 75)
            circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=9, minDist=10, minRadius=4, maxRadius=15)

            if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                # loop over the (x, y) coordinates and radius of the HoughCircles
                for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(image_in, (x, y), r, (64, 255, 64), 1)
                cv2.imwrite(file_name_out, image_in)

            else:
                return 'No circles'
            # return str(res)
            return send_file(file_name_out, mimetype='image/png')
        except HTTPException as e:
            return str(e)
    else:
        return 'GET RESULT'