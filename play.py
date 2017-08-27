# -*- coding:utf-8 -*-

from myfunction import *


dataname = "his.txt"
#定义路径
mypath = "static"
#读取数据
datas = readfile(mypath, dataname)
sysdatas = readfile(mypath, "data.txt")

def onekilled_a_qus(sysdatas, num):
	"当初次做对一道题时.在sysdatas记录初答正确数"
	sysdatas["onekill"] += num
	#存档
	writefile(mypath, "data.txt", sysdatas)

def read_chapter(sysdatas, num):
	sysdatas["novel"] += num
	#存档
	writefile(mypath, "data.txt", sysdatas)

def what_is_progress(sysdatas, rate = False):
	"进度如何.返回题库数量+理解度+一次做对数"
	#每多一道题库+1分.每初次做对一道题+1分
	score = len(datas) + sysdatas["onekill"]	
	#+总理解度
	points = map(lambda q :q.understand, datas.values())	
	score += sum(points)
	if rate :
		if score < 500 :
			progress = score / 500. * 100
			return round(progress, 2)
	else :
		return round(score, 2)

def what_is_hp(sysdatas):
	score = what_is_progress(sysdatas)
	#随着时间经过-hp
	hp = score - (time.time() - sysdatas["starttime"])/1800
	hp -= sysdatas["novel"]*2
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


