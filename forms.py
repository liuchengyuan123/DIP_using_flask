from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, SelectField, IntegerField, validators, FloatField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, NumberRange, ValidationError

class UpLoadFileForm(FlaskForm):
    photo = FileField("图片", validators=[FileRequired()])
    submit = SubmitField("确认")

class RotateForm(FlaskForm):
    angle = FloatField("角度", validators=[NumberRange(min=-180, max=180)])
    submit = SubmitField("确认")

class SharpenForm(FlaskForm):
    operation = SelectField("锐化操作", coerce=int, choices=[(0, "sharpen"), (1, "contrast"), (2, "bright")])
    factor = FloatField("锐化倍数", validators=[NumberRange(min=0.1, max=10)])
    submit = SubmitField("确认")

class FilterForm(FlaskForm):
    filtername = SelectField("滤镜", coerce=int, choices=[(0, "guassian"), (1, "emboss"), (2, "edge"), (3, "sharp"), (4, "rect")])
    submit = SubmitField("确认")

class ColorSpaceReverseForm(FlaskForm):
    toSpace = SelectField("色彩空间", coerce=int, choices=[(0, 'RGB'), (1, 'HSV'), (2, 'RGB CIE'), (3, 'XYZ'), (4, 'YUV'), (5, 'YIQ'), (6, 'YPbPr'), (7, 'YCbCr')])
    submit = SubmitField("确认")

class LinearForm(FlaskForm):
    slope = FloatField("斜率", validators=[NumberRange()])
    bias = FloatField("截距", validators=[NumberRange()])
    submit = SubmitField("确认")

class UnLinearForm(FlaskForm):
    function = SelectField("非线性函数", coerce=int, choices=[(0, "gamma"), (1, "sigmoid"), (2, "log")])
    submit = SubmitField("确认")

