#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_files
# @Time         : 2025/3/4 18:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.files_utils import to_bytes
from meutils.llm.clients import moonshot_client, zhipuai_client


async def file_extract(file):  # "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
    """todo 定时删除文件"""
    filename = Path(file).name
    mime_type, _ = mimetypes.guess_type(filename)  # mime_type = "application/octet-stream"
    file: bytes = await to_bytes(file)

    file_object = await moonshot_client.files.create(
        # file=file,
        # file=("filename.pdf", file),
        file=(filename, file, mime_type),
        purpose="file-extract"
    )
    logger.debug(file_object)

    response = await moonshot_client.files.content(file_id=file_object.id)
    return response.text
