import sys
import os
sys.path.append(os.path.join(os.path.abspath('.'), 'venv/Lib/site-packages'))
from flask import Flask, request
app = Flask(__name__)
@app.route('/')
def index():
    return 'It doesn\'t work!'
