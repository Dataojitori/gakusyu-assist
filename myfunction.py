# -*- coding:utf-8 -*-

import time
import math
import pickle
import os,re
import shutil
import numpy as np


def readfile(mypath, filename):
    "读取文件内数据"
    filename = os.path.join(mypath, filename)
    myfile=open(filename, "r")
    datas = pickle.load(myfile)
    myfile.close()
    return datas

def writefile(mypath, filename, datas):
    "向文件内写入"
    filename = os.path.join(mypath, filename)
    myfile = open(filename, "w")
    pickle.dump(datas, myfile)
    myfile.close()

def move_file(mypath, fileder, newfileder, newname, use_old_name = False):
    "获取等待文件夹的文件并改名放入归档文件夹"
    "返回更改后文件名"
    #获取图片文件名
    if os.listdir( os.path.join(mypath, fileder) ):
        oldname = os.listdir( os.path.join(mypath, fileder) )[0]
        #获取图像后缀
        imgtypeq = str.split(oldname,'.')[1]
        #生成新文件名
        if use_old_name == True :
            newname = newname
        else :
            newname = newname + '.' + imgtypeq
        #切换工作目录
        os.chdir(os.path.join(mypath, fileder))
        #重命名
        os.rename(oldname, newname)
        #移动文件归档
        shutil.move(os.path.join(mypath, fileder, newname), os.path.join(mypath, newfileder)) 
        return newname

def get_big_number(mypath):
    "获取问题文件夹里数值最大的文件名编号。如果没有文件则为0"
    names = os.listdir( os.path.join(mypath, "questiondata") )
    maxnumber = 0
    for name in names:
        maxnumber = max(maxnumber, int(str.split(name,'.')[0]))
    return maxnumber

def make_question(mypath, datas, number=None):
    "获取或生成问题对象"
    if datas.get(number):#如果是已存在的问题
        question = datas.get(number)
    else :
        if not number:
            #计算配给编号
            number = get_big_number(mypath) + 1                                     
        #归档文件
        newname = move_file(mypath, "questionwaiting", "questiondata", str(number))
        move_file(mypath, "answerwaiting", "answerdata", str(number))
        #生成新类
        question = mondai(newname)
        datas[number] = question
    return question
    
def datas_to_issue(datas, tag = False, rank = False):
    "从数据集里找出记忆度最低的问题"
    if not rank:
        rank = 0
        
    sort_datas = sort_issue(datas, tag)
    question = sort_datas[rank]
    # else :
        # def whoisbig(q1, q2):    
            # if tag :
                # if (tag in q1.tag) == 0 :
                    # "如果q1不包含所找标签"
                    # return q2
                # if (tag in q2.tag) == 0 :
                    # "如果q2不包含所找标签"
                    # return q1
            # if q1.whatis_remenber() < q2.whatis_remenber():
                # return q1
            # else :
                # return q2
        # quses = filter(lambda x: "hold" not in x.tag, datas.values())
        # question = reduce(whoisbig, quses)
        
    return question

def sort_issue(datas, tag = False, view = False):
    "排序问题"
    def match_memo(q):        
        for list in q.memo:
            for m in list:             
                if pattern.match(m):
                    return True
                
    quses = filter(lambda x: "hold" not in x.tag, datas.values())
    if tag :        
        if tag == "mathtit":
            #正则表达式筛选memo
            tag = "TIT"
            pattern = re.compile(r'H..')
            quses = filter(match_memo, quses)            
        elif tag == "chemistrytit":
            #正则表达式筛选memo
            tag = "chemistry"
            pattern = re.compile(r'H..')
            quses = filter(match_memo, quses)                    
        quses = filter(lambda x: tag in x.tag, quses)
    sort_datas = sorted( quses, key = lambda x: x.whatis_remenber() )
    
    if view :
        ranks = [a.whatis_remenber() for a in sort_datas]
        return ranks
    return sort_datas
    
class mondai:
    """问题类，每个类存放一个问题的数据"""
    """公式为e^-(t/(3^n))。知识度n是3的指数。t时间单位是天"""
    """每个类的计算区别只取决于lasttime上次做题时间，以及understand理解度"""
    def __init__(self, imgnum):
        self.imgnum = imgnum #♥图片编号
        self.tag = []
        self.memo = []
        self.history = [] #♥记录列表，包含子列表(时间，分数)
        self.lasttime = 0. #♥最后一次学习的时间，单位为1970以来的秒
        self.understand = 0. #♥理解度,0~正无穷
        self.remember = 0. #记忆度,0~1.不需要保存,即用即算
        self.qusnum = 0#所包含的问题个数                

    def write_memo(self, memo):
        "记录文字笔记"
        self.memo.append([self.wordtime, memo])
    def culc_knowledge(self):
        "计算知识度"        
        self.knowledge = 0
        weight = 5        
        if len(self.history) == 1:
            self.knowledge = self.history[-1][2]
        else :
            only_num = [0,0,0,0] + [x[2] for x in self.history]
            for i in range(len(self.history))[1:]:
                aver = np.average(only_num[i-1:weight-1+i],weights=[1,1.5,2,2.5,3])                
                self.knowledge += only_num[i+weight-1] - aver                           
        
    def whatis_remenber(self):        
        "返回现在的记忆程度百分比"
        self.culc_knowledge()
        t = (time.time() - self.lasttime) / 86400 #自最后一次学习以来的天数
        knowledge = 3**self.knowledge
        self.remember = math.e**(-t / knowledge)
        return self.remember

    def return_time(self):
        "返回多少时间后应该出题"
        "返回值可正可负，单位秒"
        pass

    def next_time(self):
        "根据history记录更新下一次出题时间self.time"
        "不返回值。出题时间的类型是自1970年秒数"
        pass

    def write_history(self, point):
        "向历史里记录成绩，根据评分更新self.understand理解度"
        "point范围0~1，是正答率的百分比"
        "point大于0.5，记忆度越低，理解度增加越高；point小于0.5，记忆度越高，理解度降低越大"
        # if point > 0.5:
        #   zen = (1 - self.remember) * point 
        # else :
        #   zen = -self.remember * (1 - point)
        self.whatis_remenber() #更新现在记忆度 
        self.understand += point - self.remember    
        self.wordtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        machinetime = time.time()
        self.history.append([machinetime, self.wordtime, point])
        self.lasttime = machinetime
