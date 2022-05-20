from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from UI_Make import Ui_Dialog
from PyQt5.QtWidgets import (QFileDialog,QApplication, QMessageBox)
import cv2
import json 
import os, shutil
import numpy as np
import sys
import ntpath
import subprocess
import time
#圖片等比縮放
def img_resize(image,h,w):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = w
    height_new = h
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new
#圖片增加透明邊框
def img_border(img,h,w):
    borderValue1=0
    borderValue2=0
    borderValue3=0
    borderValue4=0
    size = img.shape
    img_w= size[1]
    img_h= size[0]
    if (h-img_h)%2 ==0:
        borderValue1=int((h-img_h)/2)
        borderValue2=int((h-img_h)/2)
    else:
        borderValue1=int((h-img_h)/2+0.5)
        borderValue2=int((h-img_h)/2-0.5)
    if (w-img_w)%2 ==0:
        borderValue3=int((w-img_w)/2)
        borderValue4=int((w-img_w)/2)
    else:
        borderValue3=int((w-img_w)/2+0.5)
        borderValue4=int((w-img_w)/2-0.5)
    img_with_border = cv2.copyMakeBorder(img, borderValue1, borderValue2,borderValue3,borderValue4, cv2.BORDER_CONSTANT, value=[0,0,0,0])#上,下,左,右
    return img_with_border

class MainWindow_controller(QtWidgets.QMainWindow):
    TemplateImageSource="0"
    imgT_name="0"
    ImageMakeSource="0"
    jsonSource="0"
    folder="JP/"
    img_height=0
    img_width =0
    
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()


    def setup_control(self):
        self.ui.chooseTexture.clicked.connect(self.open_texture) 
        self.ui.chooseJSON.clicked.connect(self.open_json)
        self.ui.Run.clicked.connect(self.MakeTexture)
        self.ui.zh_TW.toggled.connect(self.onClicked)
        self.ui.JP.toggled.connect(self.onClicked)
        self.ui.EN.toggled.connect(self.onClicked)

        
        
        
        
    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.folder = str(radioBtn.text())+'/'
            print(self.folder)
    def open_texture(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./",'Image Files (*.png)')
        img_name=ntpath.basename(self.TemplateImageSource)
        if filename:
            print(filename)
            #
            imgTemp = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            sizeTemp = imgTemp.shape
            self.img_height=sizeTemp[0]
            self.img_width =sizeTemp[1]
            print(self.img_height)
            print(self.img_width)
            print(ntpath.basename(filename))
            self.imgT_name=ntpath.basename(filename)
            n_channels = 4
            transparent_img = np.zeros((int(self.img_height), int(self.img_width), n_channels), dtype=np.uint8)
            cv2.imwrite("output/"+self.imgT_name, transparent_img)
            self.ImageMakeSource="output/"+self.imgT_name
            
            self.ui.chooseJSON.setEnabled(True)

    def open_json(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./",'JSON file (*.json)') 
        if filename:
            print(filename)
            self.jsonSource=filename
            self.ui.Run.setEnabled(True)
        
    def MakeTexture(self):
        if self.ImageMakeSource=="0" or self.jsonSource=="0":
            print("Not Yet")  
        else:
            writeName=self.ImageMakeSource
            OutputImage=cv2.imread(writeName, cv2.IMREAD_UNCHANGED)
            with open(self.jsonSource) as f:
                data = json.load(f)
            for i in data['mSprites']:
                #print(i)
                print("name:" + i['name'])
                print("x:" + str(i["x"]))
                print("y:" + str(i["y"]))
                print("width:" + str(i['width']))
                print("height:" + str(i['height']))
                # 裁切區域的 x 與 y 座標（左上角）
                x = i["x"]
                y = i["y"]

                # 裁切區域的長度與寬度
                w = i['width']
                h = i['height']
                
                img = cv2.imread(self.folder+i['name']+".png", cv2.IMREAD_UNCHANGED)
                
                size = img.shape
                img_w= size[1]
                img_h= size[0]
                
                if w==img_w and h==img_h:
                    OutputImage[y:y+h, x:x+w]=img
                    #cv2.imwrite(writeName, OutputImage)
                else:
                    print("diff")
                    print("img_w="+str(img_w))
                    print("img_h="+str(img_h))
                    print("w="+str(w))
                    print("h="+str(h))
                    
                    if img_w<=w and img_h<=h:
                        #圖片皆小於等於JSON紀載
                        OutputImage[y:y+h, x:x+w]=img_border(img,h,w)
                        #cv2.imwrite(writeName, OutputImage)
                    else:
                        print("---")
                        #圖片長度或寬度大於JSON紀載，先等比縮小
                        imageProcessed = img_resize(img,h,w)
                        if w==img_w and h==img_h:
                            OutputImage[y:y+h, x:x+w]=imageProcessed
                            #cv2.imwrite(writeName, OutputImage)
                        else:
                            OutputImage[y:y+h, x:x+w]=img_border(imageProcessed,h,w)
                            #cv2.imwrite(writeName, OutputImage)
                #cv2.imshow('alpha2048', alpha2048)
                #cv2.waitKey(1000)
                
                
                print("--------------------------")
            cv2.imwrite(self.ImageMakeSource, OutputImage)
            print("make")
            
            app = QApplication(sys.argv)
            QMessageBox.information(None, 'Notification', 'Compelte')
            subprocess.Popen('explorer '+os.path.dirname(os.path.abspath(self.ImageMakeSource)))