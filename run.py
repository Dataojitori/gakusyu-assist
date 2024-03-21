#! python2
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
ANS_folder = "\\static\\answerdata"
Qwating_folder = '\static\questionwaiting'
Awating_folder = '/static/answerwaiting'
app.config['QUS_folder'] = QUS_folder
app.config['ANS_folder'] = ANS_folder
app.config['Qwating_folder'] = Qwating_folder
app.config['Awating_folder'] = Awating_folder
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
def hello_world(qus_type = False, rank = False, start_rank = 0):  
    img_stream, remenber = search_qus(needremenber = True, qus_type = qus_type, rank = rank) 
    hp = what_is_hp(sysdatas)
    onekill = sysdatas["onekill"]
    progress = what_is_progress(sysdatas, rate = True)
    total_qus = len( sort_issue(datas) )
    print "进度".decode('utf-8').encode('gbk'), what_is_progress(sysdatas)
    print "是否存在未解决问题".decode('utf-8').encode('gbk'), \
          os.listdir("C:/Users/niwatori/OneDrive/code/gakusyu assist/static/questionwaiting")
    print "目前问题编号".decode('utf-8').encode('gbk'), img_stream    
    return render_template('index.html', remenber = remenber, start_rank = start_rank, 
                           img_stream=img_stream, hp = hp, onekill = onekill, progress = progress, total_qus = total_qus)  
                           
@app.route('/old_qus')  
def give_me_qus(qus_type, rank = False):
    if not os.listdir("C:/Users/niwatori/OneDrive/code/gakusyu assist/static/questionwaiting"):
        "如果是空文件夹"
        give(qus_type, rank)          
    #else :#如果存在未解决问题就不要出题
     #   return jsonify({"errno":1002,"errmsg":"看看你文件夹"})
        #global qus
        #qus = datas_to_issue(datas, qus_type)           
    time.sleep(0.1)
    img_stream = os.path.join(app.config['Qwating_folder'], qus.imgnum)
    print "解答历史".decode('utf-8').encode('gbk'), qus.history
    try :
        contain = qus.qusnum
    except AttributeError:
        qus.qusnum = 0
    return render_template('oldqus.html', img_stream=img_stream, contain = qus.qusnum, tag = qus.tag)  

@app.route('/old_ans')  
def give_me_ans():          
    memo = qus.memo
    img_stream = os.path.join(app.config['Awating_folder'], qus.imgnum)    
    try :
        contain = qus.qusnum
    except AttributeError:
        qus.qusnum = 0
    return render_template('oldans.html', img_stream=img_stream, memo = memo, contain = qus.qusnum, tag = qus.tag)  

# 上传文件
@app.route('/api/upload',methods=['GET', 'POST'],strict_slashes=False)
def api_upload():
    if request.method == 'GET':
        img_stream = search_qus()
        return render_template('index.html', img_stream=img_stream)

    elif request.method == 'POST':
        qus_dir = os.path.join( mypath, "questionwaiting")
        ans_dir = os.path.join( mypath, "answerwaiting")        
        
        #锁定问题的type类型和rank排序
        qus_type = str(request.values.get("qus_type"))      
        if qus_type == "--all--":
            qus_type = False
        rank = int(request.values.get("rank"))#找排名第几的问题
        
        if request.form["button"] == "imgupload":
            qus_img=request.files['qus']  # 从表单的file字段获取文件，myfile为该表单的name值
            ans_img=request.files['ans']
            if qus_img :#and allowed_file(qus_img.filename):  # 判断是否是允许上传的文件类型
                #生成新文件名
                namenum = get_big_number(mypath) + 1            
                imgtypeq = qus_img.filename.rsplit('.',1)[1]                    
                newname = str(namenum) + '.' + imgtypeq
                #保存问题文件到questiondata
                qus_img.save( os.path.join(app.config['UPLOAD_FOLDER'] ,newname) ) 
                
                if ans_img:#如果有答案图片
                    ans_img.save( os.path.join(app.config['UPLOAD_FOLDER2'] ,newname) ) 
                
                tag = request.values.get("kamoku") #问题标签.数学物理化学
                containqus = request.values.get("containqus")
                point = float(request.values.get("point"))
                memo = str(request.values.get("memo"))#笔记
                #开始主程序
                new(point, memo, namenum, tag, newname, containqus)
                return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)
                
        elif request.form["button"] == "onekill":
            #初次做对了一道题
            num = request.values.get("onekillnum")
            onekilled_a_qus(sysdatas, int(num))
            writefile(mypath, dataname, datas)          
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)                       
                        
        elif request.form["button"] == "-1":
            rank -= 1
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)          
        elif request.form["button"] == "+1":
            rank += 1
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)          
        elif request.form["button"] == "old":
            #出旧题                                
            return give_me_qus(qus_type, rank)
        elif request.form["button"] == "show_img":                        
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)
        elif request.form["button"] == "skip":            
            qus = datas_to_issue(datas, qus_type, rank)       
            point = qus.whatis_remenber()
            qus.write_history(point)
            writefile(mypath, dataname, datas)          
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)
        elif request.form["button"] == "hold":          
            qus = datas_to_issue(datas, qus_type, rank)
            qus.tag.append("hold")
            writefile(mypath, dataname, datas)          
            return hello_world(qus_type = qus_type, rank = rank, start_rank = rank)
        else:
            return jsonify({"errno":1001,"errmsg":"上传失败"})

@app.route('/api/upload2',methods=['GET', 'POST'],strict_slashes=False)
def api_upload2():
    if request.method == 'GET':
        give_me_qus()

    elif request.method == 'POST':      
        if request.form["button"] == "show_answer":         
            return give_me_ans()                    
        elif request.form["button"] == "show_qus":
            return give_me_qus(qus.tag[-1])
        elif request.form["button"] == "dataupload":                    
            #获取表单
            point = float(request.values.get("point"))
            contain = int(request.values.get("contain"))                
            memo = str(request.values.get("memo"))#笔记            
            #记录
            qus.write_history(point)#记录history
            qus.qusnum = contain#记录问题数
            if memo != "0":
                qus.write_memo(memo)
            imgname = qus.imgnum
            shutil.move(mypath + "\\" + "questionwaiting" + "\\" + imgname, mypath + "\\" + "questiondata") 
            if os.path.isfile(mypath + "\\" + "answerwaiting" + "\\" + imgname):                    
                shutil.move(mypath + "\\" + "answerwaiting" + "\\" + imgname, mypath + "\\" + "answerdata") 
            #写文件
            writefile(mypath, dataname, datas)
            return hello_world()        
        else:
            return jsonify({"errno":1001,"errmsg":"上传失败"})
#----------------------------------------------------------------------------------

def new(point, memo, number, tag = None, newname=None, containqus =None):
        "新建一个问题并写入得分"   
        qus = make_question(mypath, datas, number) #一个问题类对象
        qus.write_history(point)
        if tag :
                if str(tag) in ["TIT", "YNU"] :
                        qus.tag.append("math")
                qus.tag.append(str(tag))
        if containqus :
                qus.qusnum = int(containqus)
        if memo != "0":
                qus.write_memo(memo)
        if newname :
                #如果给了文件名就重新命名
                qus.imgnum = str(newname)
        writefile(mypath, dataname, datas)

def search_qus(needremenber = False, qus_type = False, rank = False):
    "查找特定科目的问题并用来展示"
    "返回图片路径"    
    qus = datas_to_issue(datas, qus_type, rank)           
    imgname = qus.imgnum
    #问题图片的地址
    quspath = os.path.join(app.config['QUS_folder'], imgname)
    if needremenber == True :
        return quspath, qus.whatis_remenber()
    else :
        return quspath
    
def give(qus_type, rank = False):
    "给我出一道题"
    "问题会被放在等待文件夹里,问题变量是qus"
    global qus
    qus = datas_to_issue(datas, qus_type, rank)           
    imgname = qus.imgnum
    shutil.move(os.path.join(mypath, "questiondata", imgname),os.path.join(mypath, "questionwaiting"))                    
    try :
        shutil.move(os.path.join(mypath, "answerdata", imgname), os.path.join(mypath, "answerwaiting"))
    except IOError:
        print "没有答案图片"
        
        
print search_qus()
if __name__ == '__main__':
    app.run(debug=True) 
    #app.run(host='0.0.0.0',debug=True)
