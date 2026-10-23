'''
读那张 3840×2400 的壁纸，做四件事，每张都存到 shots\，都打印 shape：

#	裁什么	你要自己算坐标
A	左上角 1/4	从 (0,0) 开始，裁到一半
B	正中间 800×800	先算中心点，再向上下左右各推 400
C	把 B 放大 2 倍	resize(B, None, fx=2, fy=2)
D	右下角 1/4	换个方向再裁一次
期望值（自己算，跑完对答案）

A -> (1200, 1920, 3)
B -> (800, 800, 3)
C -> (1600, 1600, 3)
D -> (1200, 1920, 3)
如果 A 的 shape 变成 (1920, 1200, 3)，说明宽高又反了，这次反在切片里。

第二个任务：一个必须自己验证的实验
裁出 img[0:10, 0:10]（左上角 10×10 的小块），把这一小块全部改成 0（黑色），然后问你两个问题：

原图的左上角黑了吗？
如果黑了，怎么改才不影响到原图？
把答案写进代码注释。 这两个问题的答案，决定了你以后画人脸框时，会不会把原图弄花。今天先别问我，自己跑一遍看结果。

验收
四张图都存下来，四个 shape 都对'''

import cv2
import os
# 自己写的工具：能处理中文路径的保存函数（路径换成中文目录也照样能用）
from img_io import save_image

img = cv2.imread(r"C:\Windows\Web\Wallpaper\Windows\img0.jpg")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots")

#A
img_A =img[0:1200,0:1920]

#B
img_B =img[800:1600,1520:2320]

#C
img_C =cv2.resize(img_B, None, fx=2, fy=2)

#D
img_D =img[1200:2400,1920:3840]

for name,IMG in [("img_A",img_A),("img_B",img_B),("img_C",img_C),("img_D",img_D)]:
    Path =os.path.join(path,f"{name}.png")
    
    if save_image(Path,IMG ):
        print("已保存：", Path, "| 尺寸:", IMG.shape)
    else:
        print("保存失败：", Path)

uple =img[0:10,0:10].copy()
uple[:]=0
if save_image(os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots","uple.png"),uple):
    print("| 尺寸:", uple.shape)
else:
    print("保存失败")
# 实验结论：不加 .copy() 时，uple[:]=0 会让原图左上角从 [200 171 127] 变成 [0 0 0]
# 加了 .copy() 后原图保持 [200 171 127]。切片是视图，不是拷贝。

print(img[0, 0])