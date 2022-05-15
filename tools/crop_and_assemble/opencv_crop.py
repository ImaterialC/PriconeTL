# -*- coding: UTF-8 -*-  
import cv2
import json 

print("Crop images")
imageSource=input("Source image name:")
jsonSource=input("JSON file name:")
outputChoice=input("Output to JP[1] or zh_TW[2]:")
print(imageSource)
img = cv2.imread(imageSource, cv2.IMREAD_UNCHANGED)



with open(jsonSource) as f:
    data = json.load(f)

print(type(data))

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

    # 裁切圖片
    crop_img = img[y:y+h, x:x+w]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(500)
    
    #alpha2048=cv2.imread("Alpha2048.png")
    #alpha2048[y:y+h, x:x+w]=crop_img

    #cv2.imwrite('Alpha2048.png', alpha2048)
    #cv2.imshow('alpha2048', alpha2048)
    #cv2.waitKey(1000)
    if outputChoice=="1":
        cv2.imwrite("JP/"+i['name']+'.png', crop_img)
    else:
        cv2.imwrite("zh_TW/"+i['name']+'.png', crop_img)
    
    print("--------------------------")