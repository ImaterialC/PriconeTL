from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from UI import Ui_Dialog
from PyQt5.QtWidgets import (QFileDialog,QApplication, QMessageBox)
import cv2
import json 
import os, shutil
import sys

class MainWindow_controller(QtWidgets.QMainWindow):
    imageSource="0"
    jsonSource="0"
    folder='JP/'

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.chooseTexture.clicked.connect(self.open_texture) 
        self.ui.chooseJSON.clicked.connect(self.open_json)
        self.ui.Run.clicked.connect(self.sliceTexture)
        self.ui.zh_TW.toggled.connect(self.onClicked)
        self.ui.JP.toggled.connect(self.onClicked)
    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_Image.setPixmap(QPixmap.fromImage(self.qimg))
    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            radioBtn.text
            if radioBtn.text=="JP":
                self.folder = 'JP/'
            else:
                self.folder = 'zh_TW/'
    def drawSquare(self,x,y,sx,sy):
        left_up = (x, y)
        right_down =  (sx, sy)
        color = (0, 0, 255) # red
        thickness = 5 # 寬度 (-1 表示填滿)
        
        self.display_img =cv2.rectangle(self.img, left_up,right_down, color, thickness) 
        height, width, channel = self.display_img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.display_img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_Image.setPixmap(QPixmap.fromImage(self.qimg))
    def open_texture(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./",'Image Files (*.png)')                 # start path
        print(filename, filetype)
        if filename:
            self.imageSource=filename
            self.img_path = self.imageSource
            self.display_img()
            self.ui.chooseJSON.setEnabled(True)

    def open_json(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./",'JSON file (*.json)')                  # start path
        #print(filename, filetype)
        if filename:
            self.jsonSource=filename
            with open(self.jsonSource) as f:
                    data = json.load(f)
            for i in data['mSprites']:
                #print(i)
                #print("name:" + i['name'])
                #print("x:" + str(i["x"]))
                #print("y:" + str(i["y"]))
                #print("width:" + str(i['width']))
                #print("height:" + str(i['height']))
                # 裁切區域的 x 與 y 座標（左上角）
                x = i["x"]
                y = i["y"]

                # 裁切區域的長度與寬度
                w = i['width']
                h = i['height']
                self.drawSquare(x,y,x+w,y+h)
            self.ui.Run.setEnabled(True)
        
        
    def sliceTexture(self):
        #print("***************")
        #print(self.imageSource)
        #print(self.jsonSource)
        
        if self.imageSource=="0" or self.jsonSource=="0":
            print("Not Yet")
        else:
            imgTemp = cv2.imread(self.img_path, cv2.IMREAD_UNCHANGED)
            with open(self.jsonSource) as f:
                data = json.load(f)
            for filename in os.listdir(self.folder):
                file_path = os.path.join(self.folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))



            #print(type(data))

            for i in data['mSprites']:
                #print(i)
                #print("name:" + i['name'])
                #print("x:" + str(i["x"]))
                #print("y:" + str(i["y"]))
                #print("width:" + str(i['width']))
                #print("height:" + str(i['height']))
                # 裁切區域的 x 與 y 座標（左上角）
                x = i["x"]
                y = i["y"]

                # 裁切區域的長度與寬度
                w = i['width']
                h = i['height']

                # 裁切圖片
                crop_img = imgTemp[y:y+h, x:x+w]
                #cv2.imshow("cropped", crop_img)
                #cv2.waitKey(500)
                
                #alpha2048=cv2.imread("Alpha2048.png")
                #alpha2048[y:y+h, x:x+w]=crop_img

                #cv2.imwrite('Alpha2048.png', alpha2048)
                #cv2.imshow('alpha2048', alpha2048)
                #cv2.waitKey(1000)
                cv2.imwrite(self.folder+i['name']+'.png', crop_img)
                
                #print("--------------------------")
            app = QApplication(sys.argv)
            QMessageBox.information(None, '通知', '完成')