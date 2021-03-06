#coding=utf-8
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask import render_template
import json

#模型部分
import os
import tensorflow as tf
from numpy.random import RandomState
import numpy as np
import operator
import string


def outputByChinese(outputArray,sess):
    if sess.run(outputArray)[0][0] == 1:
        return 0
    if sess.run(outputArray)[0][1] == 1:
        return 1        
    if sess.run(outputArray)[0][2] == 1:
        return 2        
    if sess.run(outputArray)[0][3] == 1:
        return 3        
    if sess.run(outputArray)[0][4] == 1:
        return 4        

app = Flask(__name__)
#@app.route('/api/hello', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template("homepage.html")

@app.route('/', methods=['POST'])
def start():
    return json.dumps(
        'Welcome my friends, use URL to play with my AI.try this:http://47.101.152.193/0000210.Encode your URL last six number as follow. weather(0-3)(very bad -> very good),fatigue degree(0-3)(very tired -> very relaxed),weekday(0-6),taste(0-3)(bad->good),price(0-3)(cheap->expensive),distance(0-3)(far away->close), So AI could Guess whether you like to go to that place for lunch'
    )


@app.route('/<strD>',methods=['GET','POST'])
def create_app(strD):
    MODEL_SAVE_PATH = "model/"
    MODEL_NAME = "model.ckpt"
    INPUT_NODE_NUM = 7
    
    x = tf.placeholder(tf.float32, shape = (None,INPUT_NODE_NUM), name = 'x-input')
    y_ = tf.placeholder(tf.float32, shape = (None, 5), name = 'y-input')

    rdm = RandomState(1)
    dataset_size = 101

    w1 = tf.Variable(tf.random_normal([INPUT_NODE_NUM,20],stddev = 1))                       
    w2 = tf.Variable(tf.random_normal([20,20],stddev = 1))                           
    w3 = tf.Variable(tf.random_normal([20,5],stddev = 1))                            
    #w4 = tf.Variable(tf.random_normal([3,1],stddev = 1))
    saver = tf.train.Saver() 
    x_w1 = tf.matmul(x, w1)
    x_w1 = tf.sigmoid(x_w1)
    w1_w2 = tf.matmul(x_w1, w2)
    w1_w2 = tf.sigmoid(w1_w2)
    y = tf.matmul(w1_w2, w3)
    y = tf.sigmoid(y)

    InputX = rdm.rand(1,INPUT_NODE_NUM)
    if len(strD) != 7:
        return json.dumps(
            'em...try to keep it in 7 numbers'
        )
    if strD.isdigit():
        pass
    else:
        return json.dumps(
            'please use int number'
        )

    with tf.Session() as sess:
    #读取模型
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            pass    
        InputX[0][0] = strD[0]
        InputX[0][1] = strD[1]
        InputX[0][2] = strD[2]
        InputX[0][3] = strD[3]
        InputX[0][4] = strD[4]
        InputX[0][5] = strD[5]   
        InputX[0][6] = strD[6] 
        #print("x :")
        #print(InputX)
        
        predict_output = sess.run(y,{x:InputX})
        #print("predict_output :")
        #print(predict_output)
        predict_outputInt = tf.round(predict_output)
        #print("predict_outputInt :")
        #print(predict_outputInt)
        output_num = outputByChinese(predict_outputInt,sess)
        #print("output_num:")
        #print(output_num)
        
    if output_num == 0:
        #return render_template('homepage.html',file=file)
        return render_template("veryBad.html")
        return json.dumps(
            'I don\'t want to go to this place at all'
        )
    if output_num == 1:
        return render_template("Bad.html")
        return json.dumps(
            'well,I just don\'t like there'
        )

    if output_num == 2:
        return render_template("justSoSo.html")
        #return json.dumps(
            #'Just so so, Would you like to send an e-mail to explain the detail? 310244098@qq.com'
        #)

    if output_num == 3:
        return render_template("goodOption.html")
        #return json.dumps(
            #'It\'s a good oppotunity,contact me with 15365180821'
        #)

    if output_num == 4:
        return render_template("veryInterested.html")
        #return json.dumps(
            #'I am very interested in it,please contact me with 15365180821'
        #)

    return render_template("confused.html")
    #return json.dumps(
         #'I am not sure, please change condition and try again'
    #)
   

@app.route('/signin' , methods=['GET'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

@app.route('/robot.gif', methods=['GET'])
def mainpage():
	root_dir = os.path.abspath(os.path.dirname(__file__))
	img_path=root_dir+'/templates'+'/static'+'/images'#图片文件存储在static文件夹下的images文件夹内
	files = os.listdir(img_path)#获取图片文件名字
	
	#if id==len(files):
        #    id=0
        file= "/static/images/robot.gif"
	return render_template('homepage.html',file=file)    
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)

