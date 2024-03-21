# -*- coding:utf-8 -*-
import os,time, pickle
from flask import Flask, request, redirect, url_for
from flask import render_template
from myfunction import *

#UPLOAD_FOLDER = '/uploads'

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dataname = "his.txt"
#定义路径
mypath = os.path.join( os.path.dirname(__file__), "static")
datas = readfile(os.path.dirname(__file__), dataname)
#writefile(mypath, dataname, datas)
##myfile=open("his.txt", "r")
##datas = pickle.load(myfile)
##myfile.close()
print os.path.join( os.path.dirname(__file__), "134.jpg")

@app.route('/')
def hello_world():
    
        #f = request.files['the_file']
        #f.save('/uploads/' + secure_filename(f.filename))   
	#	return render_template('index.html', name=None)
	#if request.method == 'GET':
	#	return render_template('index.html', name=None)

	#	return render_template('index.html', name=None)
		
    img_stream = search_qus()
    #img_stream =  os.path.join( os.path.dirname(__file__), "134.jpg")
    return render_template('index.html', img_stream = img_stream)
    #return "hello"
    #return img_stream

def search_qus():
	"查找特定科目的问题并用来展示"
	"返回图片路径"
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	#问题图片的地址
	quspath = os.path.join(mypath, "questiondata", imgname)
	return quspath

    
if __name__ == '__main__':
    app.debug = True
    app.run()
