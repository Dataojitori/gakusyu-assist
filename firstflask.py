import os
from flask import Flask, request, redirect, url_for
from flask import render_template
from werkzeug import secure_filename

#UPLOAD_FOLDER = '/uploads'

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        f = request.files['the_file']
        #f.save('/uploads/' + secure_filename(f.filename))   
	#	return render_template('index.html', name=None)
	#if request.method == 'GET':
	#	return render_template('index.html', name=None)

	#	return render_template('index.html', name=None)
		
	return render_template('index.html', name=None)

if __name__ == '__main__':
    app.debug = True
    app.run()
