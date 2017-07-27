# -*- coding:utf-8 -*-

from flask import Flask,render_template,jsonify,request,redirect,url_for
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER='questionwaiting'
UPLOAD_FOLDER2='answerwaiting'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','JPG','PNG','gif','GIF'])
#----------------------------------------------------------------------------------
#主程序部分
from myfunction import *

dataname = "his.txt"
#定义路径
#mypath = os.getcwd() + "\\static"
mypath = "static"
#读取数据
datas = readfile(mypath, dataname)
#计算新文件名编号
#----------------------------------------------------------------------------------

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/')  
def hello_world():  
    img_stream = search_qus()	
    return render_template('index.html',  
                           img_stream=img_stream)  

# 上传文件
@app.route('/api/upload',methods=['GET', 'POST'],strict_slashes=False)
def api_upload():
	if request.method == 'GET':
		img_stream = search_qus()
		return render_template('index.html', img_stream=img_stream)

	elif request.method == 'POST':
		file_dir = mypath + "\\questionwaiting"
		file2_dir = mypath + "\\answerwaiting"
		#file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER'])
		#file2_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER2'])
		
		f=request.files['qus']  # 从表单的file字段获取文件，myfile为该表单的name值
		f2=request.files['ans']
		if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
			f.save(os.path.join(file_dir,f.filename))  #保存文件到upload目录
			if f2 and allowed_file(f2.filename):#如果有答案图片
				f2.save(os.path.join(file2_dir,f2.filename)) 
			
			tag = request.values.get("kamoku") #问题标签.数学物理化学
			point = float(request.values.get("point"))
			#开始主程序
			new(point, tag)
			
			img_stream = search_qus()
			return render_template('index.html', img_stream=img_stream)
		else:
			return jsonify({"errno":1001,"errmsg":"上传失败"})
#----------------------------------------------------------------------------------

def new(point, tag = None):
	"新建一个问题并写入得分"
	maxnum = get_big_number(mypath) + 1
	global qus
	qus = make_question(mypath, datas) #一个问题类对象
	qus.write_history(point)
	if tag :
		qus.tag.append(str(tag))
	writefile(mypath, dataname, datas)

def search_qus():
	"查找特定科目的问题并用来展示"
	"返回图片路径"
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	#问题图片的地址
	quspath = "/static/questiondata/" + imgname
	return quspath
	
def give():
	"给我出一道题"
	"问题会被放在等待文件夹里,问题变量是qus"
	global qus
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	shutil.move(mypath + "\\" + "questiondata" + "\\" + imgname, mypath + "\\" + "questionwaiting") 
	try :
		shutil.move(mypath + "\\" + "answerdata" + "\\" + imgname, mypath + "\\" + "answerwaiting") 
	except IOError:
		print "没有答案图片"

def back(point):
	"记录分数并返还问题图片"
	qus.write_history(point)
	imgname = qus.imgnum
	shutil.move(mypath + "\\" + "questionwaiting" + "\\" + imgname, mypath + "\\" + "questiondata") 
	shutil.move(mypath + "\\" + "answerwaiting" + "\\" + imgname, mypath + "\\" + "answerdata") 
	writefile(mypath, dataname, datas)



if __name__ == '__main__':
    app.run(debug=True)
