#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : fileparser
# @Time         : 2025/1/7 17:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://bigmodel.cn/dev/activities/freebie/fileextracion
import asyncio

from meutils.pipe import *
from meutils.io.files_utils import to_bytes, guess_mime_type
from meutils.llm.clients import moonshot_client, zhipuai_client, APIStatusError
from meutils.notice.feishu import send_message as _send_message, FILES
from meutils.caches.redis_cache import cache

send_message = partial(
    _send_message,
    title=__name__,
    url=FILES
)
"""

# 智谱
# 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF

# kimi todo: 定期删除文件
文件接口与 Kimi 智能助手中上传文件功能所使用的相同，支持相同的文件格式，它们包括 
.pdf .txt .csv .doc .docx .xls .xlsx .ppt .pptx .md .jpeg .png .bmp .gif .svg .svgz .webp .ico .xbm .dib .pjp .tif 
.pjpeg .avif .dot .apng .epub .tiff .jfif .html .json .mobi .log .go .h .c .cpp .cxx .cc .cs .java .js .css .jsp .php 
.py .py3 .asp .yaml .yml .ini .conf .ts .tsx 等格式。

# todo: 
+ .sh
"""


@cache(ttl=24 * 3600)
async def file_extract(
        file,
        provider: Union[str, Literal['kimi', 'moonshot', 'zhipu']] = 'moonshot'
):
    """todo 定时删除文件
    todo: 兼容下 url bytes path

    # moonshot_client.files.

# len(moonshot_client.files.list().data)

    """
    mime_type = guess_mime_type(file)
    if mime_type == "application/octet-stream": return  # 不解析

    logger.debug(f"file_extract: {mime_type}")

    if provider == "zhipu":
        client = zhipuai_client
    else:
        client = moonshot_client  # 默认

    filename = Path(file).name
    file_bytes: bytes = await to_bytes(file)

    # todo: zhipu兜底
    try:
        file_object = await client.files.create(
            # file=file,
            # file=("filename.pdf", file),
            file=(filename, file_bytes, mime_type),
            purpose="file-extract"
        )

        if isinstance(file, str) and file.startswith('http'):
            file_object.url = file
        send_message(file_object)

        response = await client.files.content(file_id=file_object.id)  # 抛错处理
        return response.json()
    except APIStatusError as e:
        logger.debug(e)
        _ = e.response.json()
        if isinstance(file, str) and file.startswith('http'):
            _['url'] = file
        send_message(_)
        return _


if __name__ == '__main__':
    # file = "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
    file = "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf"
    "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 这个文件讲了什么？"
    # file = "https://oss.ffire.cc/files/百炼系列手机产品介绍.docx"
    # file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/llm/completions/rag/百炼系列手机产品介绍.docx")

    # file = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/img_1.png"

    # openai.BadRequestError: Error code: 400 - {'error': {'message': 'text extract error: 没有解析出内容', 'type': 'invalid_request_error'}}
    # file = "https://oss.ffire.cc/files/kling_watermark.png"

    # with timer():
    #     r = arun(file_extract(file, moonshot_client))

    # with timer():
    #     r = arun(file_extract(file, provider='kimi'))

    # with timer():
    #     arun(file_extract(file))

    print(guess_mime_type('x.sh'))
