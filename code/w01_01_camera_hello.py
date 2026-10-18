# -*- coding: utf-8 -*-
"""
第 1 课 · 打开摄像头，把画面显示出来
=========================================================
你要做的只有三步：
  1) 装依赖（命令行里执行一次）：  pip install opencv-python
  2) 运行本文件：                  python w01_01_camera_hello.py
  3) 按需按键，玩一玩参数

按键说明：
  q 或 ESC  → 退出
  s         → 把当前原始画面截图保存到 shots/ 目录
  e         → 开关"边缘检测"窗口（打开后能看到画面的轮廓）
  + / -     → 调整边缘检测的灵敏度

小提示：窗口要先点一下，键盘按键才会被程序收到。
"""

# 标准库：os 用来建文件夹，time 用来算帧率
import os
import time

# 第三方库：OpenCV 的包名叫 cv2（历史原因，记住就行）
import cv2

# 截图保存目录（和本脚本同级的 shots 文件夹）
SHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")


def main() -> None:
    """程序入口：打开摄像头，循环读帧、处理、显示。"""
    os.makedirs(SHOT_DIR, exist_ok=True)

    # 打开摄像头。
    # 0 = 第一个摄像头（笔记本自带的那个）。如果打不开，把 0 改成 1 再试。
    # cv2.CAP_DSHOW 是 Windows 专用的打开方式，比默认方式快很多。
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # 设置分辨率（摄像头不支持时会自动选最接近的，不会报错）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # 检查是否真的打开了，打不开就直接告诉用户原因，别让它默默失败
    if not cap.isOpened():
        print("打不开摄像头，按顺序检查：")
        print("  1. 摄像头是不是被微信 / 腾讯会议 / 相机 占用了？关掉它们")
        print("  2. 把代码里的 cv2.VideoCapture(0, ...) 改成 cv2.VideoCapture(1, ...) 再试")
        print("  3. 笔记本是否有物理摄像头开关 / 隐私开关没打开")
        return

    print("摄像头已打开。按键：q=退出  s=截图  e=开关边缘窗口  +/-=调灵敏度")

    show_edges = False     # 是否显示边缘检测窗口
    low_threshold = 80     # Canny 边缘检测的低阈值（越小越敏感）
    shot_index = 1         # 截图编号

    # 用于算帧率的变量：记录上一次循环的时间
    prev_time = time.time()
    fps = 0.0

    while True:
        # 读一帧画面。ok=False 表示这一帧没读到（摄像头掉线等）
        ok, frame = cap.read()
        if not ok:
            print("读不到画面了，摄像头可能被拔掉或被占用，程序退出。")
            break

        # 算帧率：1 / (这一帧和上一帧的时间差)
        now = time.time()
        delta = now - prev_time
        prev_time = now
        if delta > 0:
            # 做个平滑，避免数字乱跳
            fps = 0.9 * fps + 0.1 * (1.0 / delta)

        # 在画面左上角写帧率（参数：图像, 文字, 坐标, 字体, 字号, 颜色BGR, 线宽）
        cv2.putText(
            frame, f"FPS: {fps:.1f}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2,
        )

        # 显示原始彩色画面
        cv2.imshow("Camera (original)", frame)

        # 灰度 = 把彩色图变成黑白图，很多算法都要求输入灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if show_edges:
            # 先模糊一下再找边缘，能少很多噪点（新手最容易漏的一步）
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            # Canny：经典的边缘检测算法，两个阈值控制"多明显才算边缘"
            edges = cv2.Canny(blurred, low_threshold, low_threshold * 2)
            cv2.imshow("Camera (edges)", edges)

        # 等 1 毫秒接收键盘输入；返回 -1 表示这段时间没按键
        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):        # q 或 ESC 退出
            break
        elif key == ord("s"):            # 截图
            path = os.path.join(SHOT_DIR, f"shot_{shot_index:03d}.png")
            cv2.imwrite(path, frame)
            print("已保存：", path)
            shot_index += 1
        elif key == ord("e"):            # 开关边缘窗口
            show_edges = not show_edges
            if not show_edges:
                cv2.destroyWindow("Camera (edges)")
            print("边缘窗口：", "开" if show_edges else "关")
        elif key in (ord("+"), ord("=")):  # 更敏感（阈值变小）
            low_threshold = max(10, low_threshold - 10)
            print("低阈值 =", low_threshold)
        elif key == ord("-"):              # 更迟钝（阈值变大）
            low_threshold = min(240, low_threshold + 10)
            print("低阈值 =", low_threshold)

    # 收尾：释放摄像头、关掉所有窗口
    cap.release()
    cv2.destroyAllWindows()
    print("已退出。")


# 这行的意思是：直接运行本文件时才执行 main()，
# 被别人 import 时不会自动跑（正规写法，先养成习惯）
if __name__ == "__main__":
    main()
