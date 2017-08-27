# -*- coding:utf-8 -*-

from myfunction import *


dataname = "his.txt"
#定义路径
mypath = "static"
#读取数据
datas = readfile(mypath, dataname)
sysdatas = readfile(mypath, "data.txt")

def onekilled_a_qus():
	"当初次做对一道题时.在sysdatas记录初答正确数"
	sysdatas["onekill"] += 1
	#存档
	writefile(mypath, "data.txt", sysdatas)

def what_is_hp():
	#每多一道题库+1hp.每初次做对一道题+1hp
	hp = len(datas) + sysdatas["onekill"]	
	#随着时间经过-hp
	hp -= (time.time() - sysdatas["starttime"])/3600
	#根据目前题库的理解度+hp
	points = map(lambda q :q.understand, datas.values())	
	hp += sum(points)
	return round(hp, 2)

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
	try :
		shutil.move(mypath + "\\" + "answerdata" + "\\" + imgname, mypath + "\\" + "answerwaiting") 
	except IOError:
		print "没有答案图片"

def search_qus():
	"查找特定科目的问题并用来展示"
	"返回图片路径"
	qus = datas_to_issue(datas)			
	imgname = qus.imgnum
	#问题图片的地址
	quspath = mypath + "\\" + "questiondata" + "\\" + imgname
	return quspath

def back(point):
	"记录分数并返还问题图片"
	qus.write_history(point)
	imgname = qus.imgnum
	shutil.move(mypath + "\\" + "questionwaiting" + "\\" + imgname, mypath + "\\" + "questiondata") 
	shutil.move(mypath + "\\" + "answerwaiting" + "\\" + imgname, mypath + "\\" + "answerdata") 
	writefile(mypath, dataname, datas)


