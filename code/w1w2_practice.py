# -*- coding: utf-8 -*-
"""
W1 + W2 巩固练习（Day 1）
==========================================================================
把两周学的东西串成一个程序：
    摄像头 → 转灰度 → 缩一半 → 双窗口显示 → 显示 FPS → 按 s 存图 → 按 q 退出

本次练习真正要掌握的三件事：
    1) 彩色图是 3 维 (高, 宽, 3)，灰度图是 2 维 (高, 宽)，两者要分开处理
    2) resize 用 fx/fy（按比例）时，dsize 必须传 None
    3) putText 要画在彩色原图上；灰度图上写字颜色参数没有意义

顺手修掉的 5 个坑（都是踩过的）：
    1. cap.isOpened() 失败必须 return，否则后面 read() 会静默失败
    2. 帧间隔 delta 可能等于 0，做除法前先判断
    3. 文件名只写日期会互相覆盖，要带时分秒
    4. 保存要检查返回值，失败得看得见
    5. 变量名不要只靠大小写区分（now / Now 迟早写错）

运行：python w1w2_practice.py
"""

# 标准库：os 拼路径，time 算帧率，datetime 起文件名
import os
import time
from datetime import datetime

import cv2

# 自己写的工具：能处理中文路径的保存函数（路径换成中文目录也照样能用）
from img_io import save_image

# 截图目录：用 __file__ 定位，不受"从哪个目录运行"影响
SHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")


def main() -> None:
    """程序入口：打开摄像头，循环读帧、处理、显示，按 q 退出。"""

    os.makedirs(SHOT_DIR, exist_ok=True)

    # 打开摄像头。0 = 第一个摄像头；CAP_DSHOW 是 Windows 专用，比默认方式快
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # 坑 1：打不开就直接结束。不 return 的话，后面 read() 会一直返回 False，
    #       程序静默卡死，你还以为是别的问题
    if not cap.isOpened():
        print("摄像头打开失败，检查：")
        print("  1. 是不是被微信 / 腾讯会议 / 相机占用了？关掉它们")
        print("  2. 把 VideoCapture(0, ...) 里的 0 改成 1 再试")
        print("  3. 笔记本有没有物理摄像头开关没打开")
        return

    print("已打开。按键：q=退出  s=保存当前灰度图")

    prev_time = time.time()   # 上一帧的时间（注意：叫 prev_time，不叫 now）
    fps = 0.0

    while True:
        # 读一帧。ok=False 表示这一帧没读到（掉线、被占用等）
        ok, frame = cap.read()
        if not ok:
            print("读不到画面，退出。")
            break

        # ---- 算帧率：1 / 两帧时间差 ----
        cur_time = time.time()
        delta = cur_time - prev_time      # 坑 2：delta 有可能正好是 0
        prev_time = cur_time
        if delta > 0:                     # 先判断再除法，否则 ZeroDivisionError
            # 平滑：新值只占 10%，避免数字乱跳
            fps = fps * 0.9 + (1.0 / delta) * 0.1

        # ---- 图像处理：彩色 → 灰度 → 缩小一半 ----
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # (720, 1280) 两维
        small_gray = cv2.resize(gray, None, fx=0.5, fy=0.5)  # (360, 640) 两维
        # 注意：dsize 传 None 才能用 fx/fy；两个同时给，fx/fy 会被忽略

        # ---- 在彩色原图上写 FPS ----
        # 参数：图像, 文字, 左下角坐标, 字体, 字号, 颜色(B,G,R), 线宽
        cv2.putText(frame, f"FPS={fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # ---- 显示两个窗口 ----
        cv2.imshow("original", frame)          # 1280×720 彩色
        cv2.imshow("gray_half", small_gray)    # 640×360 灰度

        # ---- 按键处理：waitKey(1) = 等 1 毫秒，返回按下的键；-1 表示没按 ----
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("已退出。")
            break

        elif key == ord("s"):
            # 坑 3：文件名带时分秒，同一天按多少次都不会覆盖
            # 前缀用 gray_，和 w01 存的彩色 shot_ 区分开
            base = datetime.now().strftime("gray_%Y%m%d_%H%M%S")
            path = os.path.join(SHOT_DIR, base + ".png")
            n = 2
            while os.path.exists(path):        # 同一秒内连按，补 _2 _3
                path = os.path.join(SHOT_DIR, f"{base}_{n}.png")
                n += 1

            # 坑 4：保存要看返回值。save_image 成功返回 True
            if save_image(path, small_gray):
                print("已保存：", path, "| 尺寸:", small_gray.shape)
            else:
                print("保存失败：", path)

    # ---- 收尾：不释放的话，下次运行会报"摄像头被占用" ----
    cap.release()
    cv2.destroyAllWindows()


# 只有直接运行本文件才执行 main()；被 import 时不会自动跑
if __name__ == "__main__":
    main()
