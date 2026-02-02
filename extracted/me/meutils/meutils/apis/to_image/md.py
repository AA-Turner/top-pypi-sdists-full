#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : md
# @Time         : 2024/11/25 15:33
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://readpo.com/en/poster#%201
# https://readpo.com/zh/poster

from meutils.pipe import *
from urllib.parse import quote


@background_task
def get(url):
    resp = httpx.get(url, timeout=30)
    # Path('x.png').write_bytes(resp.content)
    # logger.debug(resp.text)
    logger.debug(resp.status_code)


def markdown2poster(title="MarkdownTest", content="# fire"):
    content = f"""https://readpo.com/p/{quote(content)}"""

    # content = f"""https://md.chatfire.cn/{quote(content)}"""
    get(content)

    return f"![{title}]({content})"

if __name__ == '__main__':
    title = "🔥最新功能"
    content = """
    # 最新通知
> 支持超多模型：`对话` `图片` `视频` `语音` `音乐` `变清晰` `去水印` `文档解析` `联网API`
---

## 2025.02.21
> jina-deepsearch 满血r1 `推理` `搜索`


> Grok-3 是马斯克旗下xAI公司开发的人工智能模型，具备128,000个Token的上下文处理能力，支持函数调用和系统提示，并计划推出多模态版本以处理图像。
  - grok-3
  - grok-3-reasoner `推理`
  - grok-3-deepsearch `搜索`



    """.strip()
    print(markdown2poster(title, content))
