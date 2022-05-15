import cv2
import json 
import time
import numpy as np
from datetime import datetime

print("Assamable images")
img_height=input("Output image height:")
img_width =input("Output image weight:")
img_name=input("Output image name:")
n_channels = 4
transparent_img = np.zeros((int(img_height), int(img_width), n_channels), dtype=np.uint8)
# Save the image for visualization
cv2.imwrite(img_name, transparent_img)
json_file=input("Json file:")
folderchoice=input("Use JP[1] or zh_TW[2] to make:")
if folderchoice =="1":
    folderUSE="JP"
else:
    folderUSE="zh_TW"



with open(json_file) as f:
    data = json.load(f)

print(type(data))
file = open('manual-image-list.txt','w')
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
    img = cv2.imread(folderUSE+"/"+i['name']+".png", cv2.IMREAD_UNCHANGED)
    OutputImage=cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
    size = img.shape
    img_w= size[1]
    img_h= size[0]
    if w==img_w and h==img_h:
        OutputImage[y:y+h, x:x+w]=img
        cv2.imwrite(img_name, OutputImage)
    else:
        print("diff")
        
        print("img_w="+str(img_w))
        print("img_h="+str(img_h))
        print("w="+str(w))
        print("h="+str(h))
        if img_w<=w and img_h<=h:
            borderValue1=0
            borderValue2=0
            borderValue3=0
            borderValue4=0
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
            OutputImage[y:y+h, x:x+w]=img_with_border
            cv2.imwrite(img_name, OutputImage)
            time.sleep(1)
        else:
            print("---")
            print("Sorry, you will handle this on your own.")
            print("filename:"+i['name']+".png")
            
            file.write(i['name']+".png"+"\n")
            time.sleep(3)
    #cv2.imshow('alpha2048', alpha2048)
    #cv2.waitKey(1000)
    
    
    print("--------------------------")
file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n----------\n")
file.close() 