#coding:utf-8
from flask import Flask, render_template, request, send_from_directory, send_file, redirect
import os
import showVlanRange as svr

from models.forms import UploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/index/<msg>", methods=["GET", "POST"])
@app.route("/index/", defaults={"msg":None}, methods=["GET", "POST"])
@app.route("/<msg>", methods=["GET", "POST"])
@app.route("/", defaults={"msg":None}, methods=["GET", "POST"])
def index(msg):
    form = UploadForm()
    return render_template('index.html', msg=msg, form=form)

@app.route("/upload", methods=["POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        print(form.listInterfaces.data)
    else:
        return render_template('index.html', msg="msg6", form=form)

    target = os.path.join(APP_ROOT, 'files/')
    print("target: "+target)
    if os.path.isdir(target):
        os.system('rm -rf '+target)
    if not os.path.isdir(target):
        os.mkdir(target)

    if not request.files.getlist("txtFiles"):
        return render_template('index.html', msg="msg4", form=form)
    if not request.files.getlist("csvFiles"):
        return render_template('index.html', msg="msg4", form=form)

    # arquivos txt
    for upload in request.files.getlist("txtFiles"):
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if ext == ".txt":
            destination = "/".join([target, filename])
            upload.save(destination)
        else:
            return render_template('index.html', msg="msg2", form=form)

    #arquivo csv
    destinationCsv = ""
    for upload in request.files.getlist("csvFiles"):
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if ext == ".csv":
            destination = "/".join([target, filename])
            upload.save(destination)
            destinationCsv = destination
        else:
            return render_template('index.html', msg="msg3", form=form)

    svr.main(target, destinationCsv, form.listInterfaces.data)
    return redirect("vlans.xls")

@app.route("/vlans.xls")
def downloadFile():
    form = UploadForm()
    target = os.path.join(APP_ROOT, 'files/vlans.xls')
    try:
        return send_file(target)
    except Exception as e:
        return render_template('index.html', msg="msg5-Não foi possivel fazer o download do arquivo. Erro: "+str(e), form=form)



if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='192.168.0.40', debug=False)
