# -*- coding:utf-8 -*-

from myfunction import *





dataname = "his.txt"
#定义路径
mypath = os.getcwd()
#读取数据
datas = readfile(mypath, dataname)
#计算新文件名编号
maxnum = get_big_number(mypath) + 1
#把问题归档
#newname = move_file(mypath, "questionwaiting", "questiondata", str(maxnum))
#move_file(mypath, "answerwaiting", "answerdata", str(maxnum))
qus = make_question(mypath, datas) #一个问题类对象
qus.write_history(0)
#writefile(mypath, dataname, datas)

def datas_to_issue():
	"从数据集里找出记忆度最低的问题"
	def whoisbig(q1, q2):
		if q1.whatis_remenber() < q2.whatis_remenber():
			return q1
		else :
			return q2
	question = reduce(whoisbig, datas.values())
	return question
		
