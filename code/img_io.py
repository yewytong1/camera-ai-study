# -*- coding: utf-8 -*-
"""
中文路径也能用的图像读写。
OpenCV 自带的 imread / imwrite 不支持中文路径：
  - imread 返回 None（不报错）
  - imwrite 返回 False（不报错）
这里用 numpy 自己写文件，绕过这个限制。
"""
import numpy as np
import cv2


def save_image(path: str, img) -> bool:
    """保存图片，支持中文路径。成功返回 True。"""
    ok, buf = cv2.imencode(".png", img)
    if not ok:
        print("编码失败，没存上：", path)
        return False
    buf.tofile(path)
    return True


def load_image(path: str):
    """读取图片，支持中文路径。失败返回 None。"""
    data = np.fromfile(path, dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)