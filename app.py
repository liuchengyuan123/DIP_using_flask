from flask import Flask, render_template, url_for, request, flash, redirect
from flask_bootstrap import Bootstrap
from forms import *
import os
from werkzeug.utils import secure_filename
from ImageOP import ImageProcess
import numpy as np

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "A-VERY-LONG-SECRET-KEY"
filename = ""
iop = ImageProcess()

@app.route("/", methods=["POST", "GET"])
def index():
    form = UpLoadFileForm()
    global filename
    print("in index")
    if form.validate_on_submit():
        f = form.photo.data
        filename = os.path.join('static/Image', secure_filename(f.filename))
        f.save(os.path.join(
            basedir, filename
        ))
        print(filename)
        try:
            iop.PhotoOpen(filename, change=True)
            flash("上传成功: " + filename, category="success")
        # return redirect(url_for('index'))
        except Exception as e:
            flash("文件打开失败", category="danger")
            flash(e, category="danger")
    if filename == "":
        flash("请打开图片", category="warning")
    if filename:
        iop.PhotoOpen(filename)
    print("index filename", filename)
    return render_template("index.html", upload_file_form=form, filename=filename + "?randomstr=" + str(np.random.rand()))

@app.route("/basic", methods=["POST", "GET"])
def basic():
    global filename
    if filename == "":
        return redirect(url_for("index"))
    rotate_form = RotateForm()
    if rotate_form.validate_on_submit():
        pass
    if filename:
        iop.PhotoOpen(filename)
    return render_template("basic.html", filename=filename + "?randomstr=" + str(np.random.rand()), rotate_form=rotate_form)

@app.route("/dip", methods=["POST", "GET"])
def dip():
    global filename
    if filename == "":
        return redirect(url_for("index"))
    sharpen_form = SharpenForm()
    if sharpen_form.validate_on_submit():
        if sharpen_form.operation.data == 0:
            filename = iop.BSCenhance(sharp_factor=sharpen_form.factor.data, choice="sharp")
        elif sharpen_form.operation.data == 1:
            filename = iop.BSCenhance(bright_factor=sharpen_form.factor.data, choice="bright")
        else:
            filename = iop.BSCenhance(contrast_factor=sharpen_form.factor.data, choice="contrast")
    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        # filter_form.filtername.data
        arr = ["guassian", "emboss", "edge", "sharp", "rect"]
        filename = iop.filters(arr[filter_form.filtername.data])
    linear_form = LinearForm()
    if linear_form.validate_on_submit():
        filename = iop.Hist_linear(a=linear_form.slope.data, b=linear_form.bias.data)
    unlinear_form = UnLinearForm()
    if unlinear_form.validate_on_submit():
        if unlinear_form.function.data == 0:
            filename = iop.Hist_gamma(1.2)
        elif unlinear_form.function.data == 1:
            filename = iop.Hist_sigmoid()
        else:
            filname = iop.Hist_log()
    color_space_reverse_form = ColorSpaceReverseForm()
    if color_space_reverse_form.validate_on_submit():
        arr = ['RGB', 'HSV', 'RGB CIE', 'XYZ', 'YUV', 'YIQ', 'YPbPr', 'YCbCr']
        filename = iop.ColorSpaceChange(arr[color_space_reverse_form.toSpace.data])
    if filename:
        iop.PhotoOpen(filename)
    return render_template("dip.html", filename=filename + "?randomstr=" + str(np.random.rand()), 
                    sharpen_form=sharpen_form, filter_form=filter_form, 
                    linear_form=linear_form, unlinear_form=unlinear_form,
                    color_space_reverse_form=color_space_reverse_form)

@app.route("/equalization", methods=["POST", "GET"])
def equalization():
    global filename
    filname = iop.Hist_equalize()
    return redirect(url_for("dip"))

@app.route("/smooth", methods=["POST", "GET"])
def smooth():
    global filename
    filename = iop.filters("rect")
    return redirect(url_for("dip"))

@app.route("/histogram", methods=['POST', 'GET'])
def histogram():
    print("in histogram")
    hist = iop.Hist()
    return hist + "?randomstr=" + str(np.random.rand())

@app.route("/FFTDCT", methods=["POST", "GET"])
def FFTDCT():
    print("in fft dct", request.form.get("operation"))
    ret = iop.FftDct(request.form.get("operation"))
    print(ret)
    return ret + "?randomstr=" + str(np.random.rand())

@app.route("/org", methods=["GET"])
def org():
    global filename
    print(filename)
    filename = iop.orgFile
    print(filename)
    iop.PhotoOpen(filename, change=True)
    return redirect(url_for("index"))

@app.route("/undo", methods=["GET", "POST"])
def undo():
    global filename
    if iop.temp == 1:
        filename = iop.orgFile
        iop.PhotoOpen(iop.orgFile)
    else:
        iop.temp -= 1
        filename = iop.base_dir + 'temp'+str(iop.temp)+'.'+iop.format
        print("in undo")
        print(filename)
        iop.PhotoOpen(filename)
    return redirect(url_for("index"))

@app.route("/redo", methods=["GET", "POST"])
def redo():
    try:
        global filename
        iop.temp += 1
        iop.PhotoOpen(iop.base_dir + 'temp'+str(iop.temp)+'.'+iop.format)
        filename = iop.base_dir + 'temp'+str(iop.temp)+'.'+iop.format
    except:
        iop.temp -= 1
        flash("已经是最新操作！", category="warning")
    return redirect(url_for("index"))

@app.route("/rotate1")
def rotate1():
    global filename
    filename = iop.RotateOP(90)
    return redirect(url_for("basic"))

@app.route("/rotate2")
def rotate2():
    global filename
    filename = iop.RotateOP(-90)
    return redirect(url_for("basic"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
