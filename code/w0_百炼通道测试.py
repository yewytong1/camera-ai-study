# -*- coding: utf-8 -*-
"""
百炼（阿里云大模型服务）通道测试脚本
用途：确认你的账号能不能正常调通阿里云百炼的大模型 API。
      跑通了，再往 Camera AI Assistant 的 D3「能回应」环节里接。

运行前提：
    1. pip install -U openai
    2. 设好 API Key 环境变量（只在这个窗口有效，不写进代码）：
         PowerShell 7:   $env:DASHSCOPE_API_KEY = "sk-xxxx"
         CMD:            set DASHSCOPE_API_KEY=sk-xxxx
       注意：Key 按地域绑定，北京地域的 Key 只能配北京地域的地址。

用法：
    python w0_百炼通道测试.py
    python w0_百炼通道测试.py --model qwen-max
    python w0_百炼通道测试.py --base-url https://<你的业务空间ID>.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
"""

import argparse
import os
import sys

# 老域名，仍然可用；换成你自己业务空间的专属域名更稳（见 --base-url）
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen-plus"

# 退出码约定：0 成功 / 1 调用失败 / 2 环境没配好
EXIT_OK, EXIT_CALL_FAIL, EXIT_ENV_FAIL = 0, 1, 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="测试阿里云百炼 OpenAI 兼容通道是否可用")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"模型名，默认 {DEFAULT_MODEL}")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="接口地址，默认北京地域老域名")
    parser.add_argument("--prompt", default="只回四个字：通道正常", help="测试用的提示词")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # 1. 先检查环境，别等报错才发现 Key 没配
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("[X] 没找到环境变量 DASHSCOPE_API_KEY。")
        print('    PowerShell 7 里这样设（只对当前窗口有效）：')
        print('    $env:DASHSCOPE_API_KEY = "sk-你的Key"')
        return EXIT_ENV_FAIL

    try:
        from openai import OpenAI
    except ImportError:
        print("[X] 没装 openai 库，先跑：pip install -U openai")
        return EXIT_ENV_FAIL

    print(f"[i] 接口地址：{args.base_url}")
    print(f"[i] 模型    ：{args.model}")
    print(f"[i] Key 前缀：{api_key[:6]}...(只显示前 6 位，别把完整 Key 贴到任何地方)")

    client = OpenAI(api_key=api_key, base_url=args.base_url)

    # 2. 发一次最小请求
    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
            timeout=30,
        )
    except Exception as exc:  # 网络、鉴权、模型名都会落到这里
        msg = str(exc)
        print(f"[X] 调用失败：{msg[:400]}")
        # 把最常见的几种错误翻成人话
        if "401" in msg or "invalid_api_key" in msg or "Incorrect API key" in msg:
            print("    → Key 无效，或者 Key 和接口地域不匹配（北京 Key 必须配北京地址）。")
        elif "404" in msg or "model" in msg.lower():
            print("    → 模型名或地址不对，先用默认 qwen-plus 和默认地址试。")
        elif "403" in msg:
            print("    → 没有开通该模型/该服务的权限，去百炼控制台开通后再试。")
        elif "timeout" in msg.lower() or "connect" in msg.lower():
            print("    → 网络问题：代理、防火墙，或者本机没网。")
        return EXIT_CALL_FAIL

    # 3. 成功，打印结果和用量（用量用来估算券烧得快不快）
    print("[OK] 通道正常，模型回复：")
    print("    " + (resp.choices[0].message.content or "").strip())
    usage = getattr(resp, "usage", None)
    if usage:
        print(f"[i] 本次用量：输入 {usage.prompt_tokens} tokens，输出 {usage.completion_tokens} tokens")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
