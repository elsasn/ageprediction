import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

import cv2 as cv
import math
import time
import argparse

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')