'''
W2 结业项目：九宫格拆解 + 还原
这是 W2 真正能拿出去说的东西，做完 W2 就打勾。

任务：新建 code\w02_04_grid.py

把 3840×2400 切成 3×3，每块单独存成 shots\grid_0_0.png … grid_2_2.png
再按原位置拼回去，存成 shots\grid_back.png
自测：np.array_equal(原图, 拼回的图) 打印出来必须是 True
只给你三个提示：

提示	内容
尺寸自己算	3840÷3 = 1280（列方向），2400÷3 = 800（行方向），所以每块是 (800, 1280, 3)
拼回去怎么搞	先建一张同样大小的空图（np.zeros_like(img) 或 img.copy()），再用同样的切片位置把块写进去
别用 .copy() 在拼图上	先用 img.copy() 当画布，往上面贴块；贴的时候直接赋值即可
验收三条：

9 个文件都存下来，每个打印 shape = (800, 1280, 3)
grid_back.png 和原图像素完全一致（array_equal 为 True）
打开 grid_back.png 看，和壁纸一模一样，接缝处没有黑边、没有错位
'''
import os
import numpy as np
import cv2
# 自己写的工具：能处理中文路径的保存函数（路径换成中文目录也照样能用）
from img_io import save_image

img = cv2.imread(r"C:\Windows\Web\Wallpaper\Windows\img0.jpg")
path =os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots")

h =int(img.shape[0]/3)
w =int(img.shape[1]/3)

new =np.zeros_like(img)
for i in range(3):
    for j in range(3):
        part =img[i*h:i*h+h,j*w:j*w+w]
        Path =os.path.join(path,f"grid_{i}_{j}.png")
        if save_image(Path,part):
            print("已保存:",Path,"大小形状：",part.shape)
        else:
            print("保存失败")
        new[i*h:i*h+h,j*w:j*w+w] =part

save_image(os.path.join(path,"grid_back.png"),new)
print(np.array_equal(img,new))


