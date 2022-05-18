import cv2
import json 
import time
import numpy as np
from datetime import datetime
import ntpath

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



folderUSE=""



print("Assamable images_new")
TemplateImageSource=input("Output image Template:")
imgTemp = cv2.imread(TemplateImageSource, cv2.IMREAD_UNCHANGED)
sizeTemp = imgTemp.shape
img_height=sizeTemp[0]
img_width =sizeTemp[1]

print(ntpath.basename(TemplateImageSource))
img_name=ntpath.basename(TemplateImageSource)
n_channels = 4
transparent_img = np.zeros((int(img_height), int(img_width), n_channels), dtype=np.uint8)
# Save the image for visualization
cv2.imwrite("output/"+img_name, transparent_img)
json_file=input("Json file:")
folderchoice=input("Use JP[1] or zh_TW[2] to make:")
if folderchoice =="1":
    folderUSE="JP"+"/"
else:
    folderUSE="zh_TW"+"/"



with open(json_file) as f:
    data = json.load(f)
    
    
    

writeName="output/"+img_name
OutputImage=cv2.imread(writeName, cv2.IMREAD_UNCHANGED)




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
    
    img = cv2.imread(folderUSE+i['name']+".png", cv2.IMREAD_UNCHANGED)
    
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
cv2.imwrite(writeName, OutputImage)