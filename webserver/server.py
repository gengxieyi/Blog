from flask import Flask
from flask import request
import os
import sys
import json
import time
import markdown
app = Flask(__name__)

if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')

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
        f = {"title":os.path.splitext(filename)[0],"date":ctime,"snapshot":open(workdir+filename).read(100)+"......"}
        result.append(f)
    print result
    return json.dumps(result)

@app.route('/article/<name>',methods=['GET'])
def preview(name):
    md_text = open("/mnt/webfile/" + name + ".md").read()
    html = markdown.markdown(md_text)
    return '<h1 class="blog-title">' + name + '</h1>' + html

@app.route('/update',methods=['POST'])
def update():
    os.system("bash /mnt/webdata/Blog/webserver/script/update.sh")
    return ""

def preview(name):
    md_text = open("/mnt/webfile/" + name + ".md").read()
    html = markdown.markdown(md_text)
    return '<h1 class="blog-title">' + name + '</h1>' + html
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
