#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tin
# @Time         : 2025/7/8 13:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from tinytag import TinyTag
import requests
from io import BytesIO

url = "https://lmdbk.com/5.mp4"
# url = "https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-1-0-pro/02175195186682100000000000000000000ffffac15f035b51e5d.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYjg3ZjNlOGM0YzQyNGE1MmI2MDFiOTM3Y2IwMTY3OTE%2F20250708%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250708T051814Z&X-Tos-Expires=86400&X-Tos-Signature=7c8be9f1694e7a437bd7263ad7ddee42c642de190c1919f0bd776e6416cb1772&X-Tos-SignedHeaders=host"
# 下载文件到内存
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Range': 'bytes=0-8191'  # 请求文件的前 8192 字节 (8KB)，通常足够了
}


# # 发起流式请求，只获取部分内容
# response = requests.get(url, headers=headers, stream=False, timeout=10)
# response.raise_for_status()  # 如果请求失败 (如 404), 会抛出异常
# # 读取响应的前 8KB 内容
# video_data = response.content
#
# len(response.content)
#
#
#
#
# response = requests.get(url, stream=True)
# audio_data = BytesIO(response.content)

# 解析时长
# tag = TinyTag.get(filename='.mp4', file_obj=audio_data)
# duration = tag.duration  # 单位：秒
# print(f"音频时长：{duration:.2f}秒")

# filename = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/y5-1YTGpun17eSeggZMzX_video-1733468228.mp4"
#
# # 解析时长
# tag = TinyTag.get(filename)
# duration = tag.duration  # 单位：秒
# print(f"音频时长：{duration:.2f}秒")

#
async def get_duration(url, filename: str = ".mp4"):
    # Path(url.split('?')[0]).name
    headers = {
        "Range": "bytes=0-8191"
    }
    async with httpx.AsyncClient(headers=headers, timeout=100) as client:
        response = await client.get(url=url)
        response.raise_for_status()

        chunk = io.BytesIO(response.content)
        tag = TinyTag.get(filename=filename, file_obj=chunk, ignore_errors=False)
        return np.ceil(tag.duration or 10)


if __name__ == '__main__':
    with timer():
        arun(get_duration(url))
