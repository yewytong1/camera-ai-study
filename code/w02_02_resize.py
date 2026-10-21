'''
用那张 3840×2400 的壁纸做三件事，都存到 shots\，都要打印 shape：

做法	目标
A. 按比例缩到一半	用 fx=0.5, fy=0.5，dsize 传 None
B. 缩到宽度 = 800，高度跟着等比变	先用原宽度算比例，再把同一个比例传给 fx 和 fy
C. 强制拉成 800 × 600	直接用 dsize=(800, 600)
只给你一个函数：
cv2.resize(图像, dsize, fx=..., fy=..., interpolation=...)
'''

import cv2
import os 
from img_io import save_image        # 文件顶部，和 import cv2 放一起

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots","gray_01.png")
img =cv2.imread(path)
if img is None:
    raise FileNotFoundError
#A
A = cv2.resize(img,dsize=None,fx=0.5,fy=0.5)

#B
W = 800
H = int(2400/(3840/W))
B = cv2.resize(img,None,fx =W/3840,fy =H/2400)

#C
C = cv2.resize(img,(800,600))
for name,img_out in [("A",A),("B",B),("C",C)] :
    Path =os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots",f"{name}.png")
    if save_image(Path, img_out):
        print("已保存：", Path)
        print(f"{name}_shape",img_out.shape)
    else:
        print("保存失败：", Path)
    