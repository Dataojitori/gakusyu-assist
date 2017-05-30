# -*- coding:utf-8 -*-
import time, math
import pickle

def readfile(filename):
	"读取文件内数据"
	myfile=open(filename, "rb")
	datas = pickle.load(f)
	myfile.close()
	return datas

def writefile(filename, datas):
	"向文件内写入"
	myfile = open(filename, "wb")
	pickle.dump(datas, myfile)
	myfile.close()

class mondai:
	"""问题类，每个类存放一个问题的数据"""
	"""公式为e^-(t/(3^n))。知识度n是3的指数。t时间单位是天"""
	"""每个类的计算区别只取决于lasttime上次做题时间，以及understand理解度"""
	def __init__(self, qus_img, ans_img):
		self.qus_img = qus_img #♥
		self.ans_img = ans_img #♥
		self.tag = []
		self.memo = []
		self.history = [] #♥记录列表，包含子列表[时间，分数]
		self.lasttime = 0 #♥最后一次学习的时间，单位为1970以来的秒
		self.understand = 0 #♥理解度,0~正无穷
		self.remember = 0 #记忆度,0~1

	def write_memo(self, memo):
		"记录文字笔记"
		self.memo.append([self.lasttime, self.wordtime, memo])

	def whatis_remenber(self):
		"返回现在的记忆程度百分比"
		t = (time.time() - self.lasttime) / 86400 #自最后一次学习以来的天数
		knowledge = 3^self.understand
		self.remember = math.e^(-t / knowledge)

	def return_time(self):
		"返回多少时间后应该出题"
		"返回值可正可负，单位秒"
		pass

	def next_time(self):
		"根据history记录更新下一次出题时间self.time"
		"不返回值。出题时间的类型是自1970年秒数"
		pass

	def score(self, point):
		"解题后进行评分以及归档，根据评分更新self.understand理解度"
		"point范围0~1，是正答率的百分比"
		"point大于0.5，记忆度越低，理解度增加越高；point小于0.5，记忆度越高，理解度降低越大"
		# if point > 0.5:
		# 	zen = (1 - self.remember) * point 
		# else :
		# 	zen = -self.remember * (1 - point)
		self.understand += point - self.remember	
		self.wordtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		machinetime = time.time()
		self.history.append([machinetime, self.wordtime, point])
		self.lasttime = machinetime