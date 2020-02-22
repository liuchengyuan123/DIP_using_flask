#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Tyler%13 time:2019/12/5

import numpy as np
import cv2
from PIL import Image,ImageEnhance,ImageDraw,ImageFont
from skimage import io,color,transform,img_as_float,img_as_ubyte,img_as_uint
from skimage.exposure import histogram,adjust_gamma,adjust_log,adjust_sigmoid,equalize_hist
import matplotlib.pyplot as plt

class ImageProcess():
    def __init__(self):
        self.img = []
        self.im = []
        self.img_cv = []
        self.format = None
        self.fromspace = None
        self.temp = 0
        self.orgFile = None

    def PhotoOpen(self,filename, change=False):
        if change:
            self.orgFile = filename
        self.img = io.imread(filename)
        self.im = Image.open(filename)
        self.img_cv = cv2.imread(filename)
        self.format = self.im.format
        self.fromspace = self.im.mode

    def ColorSpaceChange(self,toSpace):
        self.temp = self.temp + 1
        img = self.img
        if self.fromspace == 'RGBA':
            img = color.rgba2rgb(self.img)
            self.fromspace = 'RGB'
        converted_image = color.convert_colorspace(img,self.fromspace,toSpace) # having limits
        io.imsave('temp'+str(self.temp)+'.'+self.format,converted_image)
        return 'temp'+str(self.temp)+'.'+self.format

    def FftDct(self,op):
        print('in ImageOP.FftDct')
        if op == 'fft':
            self.temp = self.temp + 1
            img = color.rgb2gray(self.img)
            img = np.float32(img)
            fft_img = np.fft.fftshift(np.fft.fft2(img))
            fft_img = np.log(np.abs(fft_img)+1)
            io.imsave('temp'+ str(self.temp)+'.'+self.format, fft_img)
        elif op == 'dct':
            self.temp = self.temp + 1
            img_cv = cv2.cvtColor(self.img_cv,cv2.COLOR_BGRA2GRAY)
            img_cv = img_cv.astype(np.float32)
            dct_img = cv2.dct(img_cv)
            dct_img = np.log(np.abs(dct_img)+1e-5)
            io.imsave('temp'+ str(self.temp)+'.'+self.format, dct_img)
        return 'temp' + str(self.temp) + '.' + self.format

    def Hist(self):
        self.temp = self.temp + 1
        if len(self.img.shape) == 2:
            hist, hist_centers = histogram(self.img)
            print(hist_centers)
            plt.plot(hist_centers * 255, hist, lw=2)
        else:
            for i in range(3):
                hist, hist_centers = histogram(self.img[ :, :,i])
                plt.plot(hist_centers,hist,lw=2)
        plt.savefig('temp'+str(self.temp)+'.'+self.format)
        plt.clf()
        return 'static/Image/temp'+str(self.temp)+'.'+self.format

    def Hist_linear(self,a,b):
        if len(self.img.shape) == 2:
            img = self.img
            for i in range(self.img.shape[0]):
                for j in range(self.img.shape[1]):
                    if (a * img[i,j] + b) > 255:
                        img[i,j] = 255
                    else:
                        img[i,j] = a * img[i,j] + b
                    img[i,j] = np.uint8(img[i,j])
            io.imsave('temp'+str(self.temp)+'.'+self.format, img)
        else:
            img = self.img
            for i in range(self.img.shape[2]):
                for j in range(self.img.shape[0]):
                    for k in range(self.img.shape[1]):
                        if (a * img[j, k,i] + b) > 255:
                            img[j,k,i] = 255
                        else:
                            img[j,k,i] = a * img[j,k,i] + b
                        img[j,k,i] = np.uint8(img[j,k,i])
            io.imsave('temp'+str(self.temp)+'.'+self.format, img)
        return 'temp' + str(self.temp) + '.' + self.format

    def Hist_gamma(self,gamma,gain = 1):
        self.temp = self.temp + 1
        img = img_as_float(self.img)
        gamma_corrected = adjust_gamma(img,gamma,gain)
        io.imsave('temp'+ str(self.temp)+'.'+self.format, gamma_corrected)
        return 'temp'+str(self.temp)+'.'+self.format
    def Hist_sigmoid(self):
        self.temp = self.temp + 1
        img = img_as_float(self.img)
        sigmoid_corrected = adjust_sigmoid(img)
        io.imsave('temp'+ str(self.temp)+'.'+ self.format, sigmoid_corrected)
        return 'temp'+str(self.temp)+'.'+self.format
    def Hist_log(self):
        self.temp = self.temp + 1
        img = img_as_float(self.img)
        log_corrected = adjust_log(img)
        io.imsave('temp'+ str(self.temp)+'.'+self.format, log_corrected)
        return 'temp'+str(self.temp)+'.'+self.format
    def Hist_equalize(self):
        self.temp = self.temp + 1
        img = img_as_ubyte(self.img)
        img = equalize_hist(img)
        io.imsave('temp'+ str(self.temp)+'.'+self.format, img)
        return 'temp'+str(self.temp)+'.'+self.format

    def RotateOP(self,anger = 90):
        self.temp = self.temp + 1
        img = transform.rotate(self.img,anger)
        io.imsave('temp'+ str(self.temp)+'.'+self.format, img)
        return 'temp'+str(self.temp)+'.'+self.format
    def ResizeOP(self,size):
        self.temp = self.temp + 1
        img = transform.resize(self.img,size)
        io.imsave('temp'+str(self.temp)+'.'+self.format,img)
        return 'temp'+str(self.temp)+'.'+self.format

    def WordAdd(self,area,contend,color,size):
        self.temp = self.temp + 1
        setFont = ImageFont.truetype('simfang.ttf',size)
        im = self.im
        draw = ImageDraw.Draw(im)
        draw.text(area,contend,color,font =setFont)
        im.save('temp'+str(self.temp)+'.'+self.format)
        return 'temp'+str(self.temp)+'.'+self.format

    def BSCenhance(self,bright_factor = 1.2, sharp_factor = 1.2, contrast_factor = 1.2, choice = 'bright'):
        self.temp = self.temp+1
        if choice == 'sharp':
            Simg = ImageEnhance.Sharpness(self.im)
            Simg = Simg.enhance(sharp_factor)
            Simg.save('temp' + str(self.temp) + '.' + self.format)
        elif choice == 'contrast':
            Cimg = ImageEnhance.Contrast(self.im)
            Cimg = Cimg.enhance(contrast_factor)
            Cimg.save('temp' + str(self.temp) + '.' + self.format)
        elif choice == 'bright':
            Bimg = ImageEnhance.Brightness(self.im)
            Bimg = Bimg.enhance(bright_factor)
            Bimg.save('temp' + str(self.temp) + '.' + self.format)

        return 'temp'+ str(self.temp)+'.'+self.format

    def filters(self,filtername):
        kernel1 = np.array([[.11,.11,.11],[.11,.11,.11],[.11,.11,.11]])
        kernel_gaussian = np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]]) / 273
        kernel_emboss = np.array([[-2,-2,-2,-2,0],[-2,-2,-2,0,2],[-2,-2,0,2,2],[-2,0,2,2,2],[0,2,2,2,2]])
        kernel_edge = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
        kernel_sharp = np.array([[0,-2,0],[-2,9,-2],[0,-2,0]])

        if filtername == 'gaussian':
            self.temp = self.temp + 1
            gaussian = cv2.filter2D(self.img_cv, -1, kernel_gaussian)
            cv2.imwrite('temp'+ str(self.temp)+'.'+self.format, gaussian)
        elif filtername == 'emboss':
            self.temp = self.temp + 1
            emboss = cv2.filter2D(self.img_cv, -1, kernel_emboss)
            emboss = cv2.cvtColor(emboss, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('temp'+ str(self.temp)+'.'+self.format, emboss)
        elif filtername == 'edge':
            self.temp = self.temp + 1
            edge = cv2.filter2D(self.img_cv, -1, kernel_edge)
            cv2.imwrite('temp'+ str(self.temp)+'.'+self.format, edge)
        elif filtername == 'sharp':
            self.temp = self.temp + 1
            sharp = cv2.filter2D(self.img_cv, -1, kernel_sharp)
            cv2.imwrite('temp'+ str(self.temp)+'.'+ self.format, sharp)
        elif filtername == 'rect':
            self.temp = self.temp + 1
            rect = cv2.filter2D(self.img_cv,-1,kernel1)
            cv2.imwrite('temp'+ str(self.temp)+'.'+self.format,rect)
        else:
            pass
        return 'temp'+ str(self.temp)+'.'+self.format

# if __name__ == '__main__':
#     c = ImageProcess()
#     c.PhotoOpen('./image/1.png')
#     c.ColorSpaceChange('hsv')
#     c.FftDct('dct')
#     c.Hist()
#     c.BSCenhance(1,10,1,'sharp')
#     #c.Hist_linear(3,6)
#     c.filters('emboss')
#     c.Hist_equalize()
#     c.WordAdd((40,40),'HAPPY',(255,255,255),50)
