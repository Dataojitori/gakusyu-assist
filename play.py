# -*- coding:utf-8 -*-

from myfunction import *


dataname = "his.txt"
#定义路径
mypath = os.getcwd()
#读取数据
datas = readfile(mypath, dataname)
#计算新文件名编号
def new(point, tag = None):
	"新建一个问题并写入得分"
	maxnum = get_big_number(mypath) + 1
	global qus
	qus = make_question(mypath, datas) #一个问题类对象
	qus.write_history(point)
	if tag :
		qus.tag.append(tag)
	writefile(mypath, dataname, datas)

def give():
	"给我出一道题"
	"问题会被放在等待文件夹里,问题变量是qus"
	global qus
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	shutil.move(mypath + "\\" + "questiondata" + "\\" + imgname, mypath + "\\" + "questionwaiting") 
	shutil.move(mypath + "\\" + "answerdata" + "\\" + imgname, mypath + "\\" + "answerwaiting") 

def back(point):
	"记录分数并返还问题图片"
	qus.write_history(point)
	imgname = qus.imgnum
	shutil.move(mypath + "\\" + "questionwaiting" + "\\" + imgname, mypath + "\\" + "questiondata") 
	shutil.move(mypath + "\\" + "answerwaiting" + "\\" + imgname, mypath + "\\" + "answerdata") 
	writefile(mypath, dataname, datas)


