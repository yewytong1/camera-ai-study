'''
为什么是 (高, 宽, 3) 不是 (宽, 高, 3)？
numpy的行列顺序，"一行"就是横向的一排像素，行数就是画面的高度
第三个数字 3 是什么，为什么顺序是 BGR 不是 RGB？
3是3个色彩通道，BGR 的来源是历史兼容（早期相机硬件和 Windows 位图用 BGR 排列），
跟 C 语言语法没关系。OpenCV 官方也没给过硬性出处，公认说法就是“当年就这么存的，现在改不动了”。
uint8 和 0~255 意味着什么？
uint8是数据类型，0~255是色彩从淡到深的区间
'''
'''
C:\Windows\Web\Wallpaper\Windows\img0.jpg
这张壁纸 → 打印 shape、dtype
转灰度 → 存成 shots\gray_01.png
再用 save_image（你的 img_io）存一次，验证中文路径确实能存
'''
import os
import cv2
from img_io import save_image        # 文件顶部，和 import cv2 放一起

img = cv2.imread(r"C:\Windows\Web\Wallpaper\Windows\img0.jpg")

if img is None:
    raise FileNotFoundError
else:
    print("形状/尺寸",img.shape)
    print("数据类型",img.dtype)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots","gray_01.png")
if save_image(path, gray):
    print("已保存：", path)
else:
    print("保存失败：", path)