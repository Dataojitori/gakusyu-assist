# -*- coding:utf-8 -*-
import os
import shutil
import myfunction


#读取数据
datas = read


f = open("my.dat", "wb")
pickle.dump(mystr, f)
f.close()

datas = {}
mypath = os.getcwd()
#读取数据存档
def get_big_number():
	#获取问题文件夹里数值最大的文件名编号。如果没有文件则为0
	names = os.listdir(mypath + "\\questiondata")

	maxnumber = 0
	for name in names:
		maxnumber = max(maxnumber, int(str.split(name,'.')[0]))
	return maxnumber

	
def move_file(fileder, newfileder, newname):
	"获取等待文件夹的文件并改名放入归档文件夹"
	"返回更改后文件名"
	#获取图片文件名
	if os.listdir(mypath + "\\" + fileder):
		oldname = os.listdir(mypath + "\\" + fileder)[0]
		#获取图像后缀
		imgtypeq = str.split(oldname,'.')[1]
		#生成新文件名
		newname = newname + '.' + imgtypeq
		#切换工作目录
		os.chdir(mypath + "\\" + fileder)
		#重命名
		os.rename(oldname, newname)
		#移动文件归档
		shutil.move(mypath + "\\" + fileder + "\\" + newname, mypath + "\\" + newfileder) 
		return newname
	

a = raw_input("出题还是交卷？c/j")
if a == "j":
	a = raw_input("把问题和答案（非必须）放在文件夹\n这是一个新问题吗？y/n")
	if a == 'n':
		number = input("请输入问题编号")
		question = datas.get(number)
	elif a == 'y':
		#计算配给编号
		number = get_big_number() + 1
		#归档文件
		newname = move_file("questionwaiting", "questiondata", str(number))
		move_file("answerwaiting", "answerdata", str(number))
		#生成新类
		question = mondai(newname, newname)
		datas[number] = question

	point = raw_input("请输入你的得分")
	question.score(point)
	a = raw_input("要记录笔记说明吗？y/n")
	if a == "y":
		memo = raw_input("写下你的笔记")
		question.write_memo(memo)



f=open("my.dat", "rb")
mystr = pickle.load(f)
print mystr