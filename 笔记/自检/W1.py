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
import os
import time
import cv2

SHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")

def main():
  os.makedirs(SHOT_DIR, exist_ok=True)

  cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

  if not cap.isOpened():
    print("摄像头打开失败，请自己检查问题")
    return
  print("摄像头打开成功")

  now = time.time()

  fps = 0
  count = 1
  threshold = 80
  show_edge = False
  while True:
    ok,frame =cap.read()
    if not ok:
      print("没有读取成功")
      break

    neonew =time.time()
    delay = neonew-now
    now = neonew
    if delay >0:
        fps =0.9*fps+(1/delay)*0.1
   
    cv2.putText(frame,f"FPS={fps:.1f}",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("original",frame)
    gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    if show_edge:
      blur =cv2.GaussianBlur(gray,(5,5),0)
      edge = cv2.Canny(blur,threshold,threshold*2)
      cv2.imshow("Finish",edge)
    
    key = cv2.waitKey(1) & 0xFF
    if key in (ord("q"),27):
      break
    elif key == ord("s"):
      path = os.path.join(SHOT_DIR,f"shots_{count:03d}.png")
      cv2.imwrite(path,frame)
      print("已保存",path)
      count+=1
    elif key == ord("e"):
      show_edge = not show_edge
      if not show_edge:
        cv2.destroyWindow("Finish")
    elif key in (ord("+"),ord("=")):
      threshold=max(10,threshold-10)
    elif key == ord("-"):
      threshold=min(240,threshold+10)
    

  cap.release()
  cv2.destroyAllWindows()
  print("已退出")

if __name__=="__main__":
  main()
