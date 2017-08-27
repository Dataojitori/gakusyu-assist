# -*- coding:utf-8 -*-

from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request,redirect,url_for
import time
import os

app = Flask(__name__)
MainPath = 'static'
app.config['MainPath'] = MainPath

UPLOAD_FOLDER='static/questiondata'
UPLOAD_FOLDER2='static/answerdata'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
QUS_folder = '\static\questiondata'
app.config['QUS_folder'] = QUS_folder
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','JPG','PNG','gif','GIF'])
#----------------------------------------------------------------------------------
#主程序部分
from myfunction import *
from play import *

dataname = "his.txt"
#定义路径
mypath = app.config['MainPath']
#读取数据
datas = readfile(mypath, dataname)
sysdatas = readfile(mypath, "data.txt")
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
		qus_dir = os.path.join( mypath, "questionwaiting")
		ans_dir = os.path.join( mypath, "answerwaiting")		
		
		qus_img=request.files['qus']  # 从表单的file字段获取文件，myfile为该表单的name值
		ans_img=request.files['ans']
		if qus_img :#and allowed_file(qus_img.filename):  # 判断是否是允许上传的文件类型
			#生成新文件名
			namenum = get_big_number(mypath) + 1			
			imgtypeq = qus_img.filename.rsplit('.',1)[1]					
			newname = str(namenum) + '.' + imgtypeq
			#保存问题文件到questiondata
			qus_img.save( os.path.join(app.config['UPLOAD_FOLDER'] ,newname) ) 
			
			if ans_img and allowed_file(ans_img.filename):#如果有答案图片
				ans_img.save( os.path.join(app.config['UPLOAD_FOLDER2'] ,newname) ) 
			
			tag = request.values.get("kamoku") #问题标签.数学物理化学
			point = float(request.values.get("point"))
			memo = str(request.values.get("memo"))#笔记
			#开始主程序
			new(point, memo, namenum, tag, newname)
			
			img_stream = search_qus()
			return render_template('index.html', img_stream=img_stream)
		else:
			return jsonify({"errno":1001,"errmsg":"上传失败"})
#----------------------------------------------------------------------------------

def new(point, memo, number, tag = None, newname=None):
	"新建一个问题并写入得分"	
	global qus
	qus = make_question(mypath, datas, number) #一个问题类对象
	qus.write_history(point)
	if tag :
		qus.tag.append(str(tag))
	if memo != "0":
		qus.memo.append(memo)
	if newname :
            #如果给了文件名就重新命名
            qus.imgnum = str(newname)
	writefile(mypath, dataname, datas)

def search_qus():
	"查找特定科目的问题并用来展示"
	"返回图片路径"
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	#问题图片的地址
	#quspath = os.path.join(mypath, "questiondata", imgname)
	quspath = os.path.join(app.config['QUS_folder'], imgname)
	return quspath
	
def give():
	"给我出一道题"
	"问题会被放在等待文件夹里,问题变量是qus"
	global qus
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	shutil.move(os.path.join(mypath, "questiondata", imgname),os.path.join(mypath, "questionwaiting"))                    
	try :
		shutil.move(os.path.join(mypath, "answerdata", imgname), os.path.join(mypath, "answerwaiting"))
	except IOError:
		print "没有答案图片"

def back(point):
	"记录分数并返还问题图片"
	qus.write_history(point)
	imgname = qus.imgnum
	shutil.move(os.path.join(mypath, "questionwaiting", imgname),os.path.join(mypath, "questiondata")) 
	shutil.move(os.path.join(mypath, "answerwaiting", imgname), os.path.join(mypath, "answerdata")) 
	writefile(mypath, dataname, datas)


print search_qus()
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',debug=True)
