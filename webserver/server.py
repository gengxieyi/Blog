#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask import request
import os
import sys
import json
import time
import markdown
import urllib
app = Flask(__name__)

@app.route('/upload',methods=['POST'])
def upload():
    f = request.files['file']
    f.save('/mnt/webfile/' + f.filename)
    return "error test",200

@app.route('/articles',methods=['GET'])
def getFileItems():
    ext = (".md")
    workdir = "/mnt/webfile/"
    result=[]
    for filename in os.listdir(workdir):
        if not filename.endswith(ext):
            continue
        ctime = os.path.getctime(workdir + filename)
        ctime = time.strftime("%B %d,%Y %H:%M",time.localtime(ctime))
        snapshot = getsnapshot(workdir+filename,40)
        f = {"title":os.path.splitext(filename)[0],"date":ctime,"snapshot":snapshot+"......"}
        result.append(f)
    print result
    return json.dumps(result)

@app.route('/article/<name>',methods=['GET'])
def preview(name):
    md_text = open("/mnt/webfile/" + name + ".md").read().decode("utf-8")
    html = markdown.markdown(md_text)
    return html

@app.route('/update',methods=['POST'])
def update():
    os.system("bash /mnt/webdata/Blog/webserver/script/update.sh")
    return ""

@app.route('/remove/<name>',methods=['POST'])
def remove(name):
    os.remove("/mnt/webfile/" + name + ".md")
    return ""

def preview(name):
    md_text = open("/mnt/webfile/" + name + ".md").read()
    html = markdown.markdown(md_text)
    return html

def getsnapshot(filename,count):
    f = open(filename).read()
    result = []
    offset = 0
    while count > 0 and offset < len(f):
        ch = f[offset]
        result.append(ch)
        if ord(ch) >> 4 == 14:
            result.append(f[offset+1])
            result.append(f[offset+2])
            offset += 3
        else :
            offset += 1
        count -= 1
    return "".join(result)
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
