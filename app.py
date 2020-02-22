from flask import Flask, render_template, url_for, request, flash, redirect
from flask_bootstrap import Bootstrap
from forms import *
import os
from werkzeug.utils import secure_filename
# from ImageOP import ImageProcess

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "A-VERY-LONG-SECRET-KEY"
filename = ""
# iop = ImageProcess()

@app.route("/", methods=["POST", "GET"])
def index():
    form = UpLoadFileForm()
    global filename
    if form.validate_on_submit():
        f = form.photo.data
        filename = os.path.join('static/Image', secure_filename(f.filename))
        f.save(os.path.join(
            basedir, filename
        ))
        print(filename)
        try:
            # iop.PhotoOpen(filename)
            flash("上传成功: " + filename, category="success")
        # return redirect(url_for('index'))
        except:
            flash("文件打开失败", category="danger")
            return render_template("index.html", upload_file_form=form, filename=filename)
    if filename == "":
        flash("请打开图片", category="warning")
    return render_template("index.html", upload_file_form=form, filename=filename)

@app.route("/basic", methods=["POST", "GET"])
def basic():
    global filename
    if filename == "":
        return redirect(url_for("index"))
    rotate_form = RotateForm()
    if rotate_form.validate_on_submit():
        pass
    
    return render_template("basic.html", filename=filename, rotate_form=rotate_form)

hist = ""

@app.route("/dip", methods=["POST", "GET"])
def dip():
    global filename
    if filename == "":
        return redirect(url_for("index"))
    sharpen_form = SharpenForm()
    if sharpen_form.validate_on_submit():
        pass
    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        pass
    linear_form = LinearForm()
    if linear_form.validate_on_submit():
        pass
    unlinear_form = UnLinearForm()
    if unlinear_form.validate_on_submit():
        pass
    color_space_reverse_form = ColorSpaceReverseForm()
    if color_space_reverse_form.validate_on_submit():
        pass
    return render_template("dip.html", filename=filename, 
                    sharpen_form=sharpen_form, filter_form=filter_form, 
                    linear_form=linear_form, unlinear_form=unlinear_form,
                    color_space_reverse_form=color_space_reverse_form)

@app.route("/histogram", methods=['POST', 'GET'])
def histogram():
    print("in histogram")
    # hist = iop.Hist()
    # hist = os.path.join(basedir, "static/Image", hist)
    return "Hello, I am Histogram"

@app.route("/FFTDCT", methods=["POST", "GET"])
def FFTDCT():
    print("in fft dct")
    return "Hello, I am " + request.form.get("operation") + " result"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
