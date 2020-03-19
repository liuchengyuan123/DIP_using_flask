## DIP_using_flask

Digital Image Process website

## What did I do

### `ImageOP`

一个包含主要图像处理函数和功能的**裸**图像处理类，不包含任何GUI成分。

- `photoOpen`打开一张图片，`change`参数决定是否打开的是原图。

- `ColorspaceChange`色彩空间转换功能。

- `FftDct`画对应图像

- `Hist`画直方图

- `HistLinear`直方图线性拉伸

- `Hist_gama/sigmoid/log`直方图非线性拉伸（三种不同函数）

- `Hist_equlizate`直方图均衡

- `RotateOP`旋转

- `WordAdd`添加文字

- `BSCenhence`可以增强对比度、亮度和锐化

- `filters`滤镜

### `forms`

声明了前端html代码所需要用户填写的参数表单格式。
如线性拉伸操作需要填写*斜率*和*截距*等。
**特点**：
- 可以进行输入数值检查是否合法 validators，包括输入旋转角度的范围$angle \in [-180, 180]$，以及输入类型检查（是否为浮点数等）。

### `app`

前端接收数据后，返回给后端的`app`代码，该文件响应前端的操作。在`app`中导入了`ImageOP`作为`self.iop`，可以处理前端要求的图像。如：

- 前端发送了“打开文件”请求，那么会上传一张照片到服务器，文件名为`/static/img/test.png`，然后调用`self.iop.PhotoOpen("/static/img/test.png")`方法。

- 前端发送滤镜操作，并用`POST`方法传递了滤镜选项，则调用`self.iop.filters(filter)`操作。

### templates

#### `navbar`

导航栏，可以添加一些其他功能，如搜索等。可以拓展。

#### `base`

所有前端的基础样式，规定了图片位置，和`nav tab`的样式。包括了所有鼠标控制拖动、放大缩小的JavaScript代码。

#### `index`

实现快捷操作按钮的前端代码和向后端发送请求的JavaScript代码。实现了打开图片、原图、撤销、重做和分享功能。

#### `base`

实现基础操作按钮的前端代码和向后端发送请求的JavaScript代码。实现了旋转、缩放和添加文字功能。

#### `dip`

实现其他数图功能，详细请看演示视频。


## Install & Run

### git
```bash
git clone https://github.com/liuchengyuan123/DIP_using_flask/

sudo pip install -r .\requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```

### run
```bash
python3 app.py
```
