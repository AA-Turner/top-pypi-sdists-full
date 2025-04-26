#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : fileparser
# @Time         : 2025/1/7 17:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://bigmodel.cn/dev/activities/freebie/fileextracion

from meutils.pipe import *
from meutils.io.files_utils import to_bytes, guess_mime_type
from meutils.llm.clients import moonshot_client, zhipuai_client, APIStatusError
from meutils.notice.feishu import send_message as _send_message, FILES
from meutils.caches import cache, rcache
from meutils.apis.jina import url_reader

# from openai.types.file_object import FileObject

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


async def delete_files(client, threshold: int = 666):
    _ = await client.files.list()
    file_objects = _.data

    logger.debug(len(file_objects))

    if len(file_objects) > threshold:
        tasks = [client.files.delete(file.id) for file in file_objects]
        await asyncio.gather(*tasks)


@rcache(ttl=7 * 24 * 3600)
async def file_extract(file):
    """

    :param file: url bytes path
    :return:
    """
    # url
    if isinstance(file, list):
        return await asyncio.gather(*map(file_extract, file))

    filename = Path(file).name if isinstance(file, str) else 'untitled'
    mime_type = guess_mime_type(file)

    if str(file).startswith("http") and mime_type in {"application/octet-stream", "text/html"}:
        logger.debug(f"jina reader")
        markdown_content = await url_reader(file)
        return {
            'filename': filename,
            'type': 'file',
            'file_type': "text/plain",
            'content': markdown_content,
        }

    file: bytes = await to_bytes(file)

    for i, client in enumerate([moonshot_client, zhipuai_client]):

        try:
            # 1 / 0
            file_object = await client.files.create(
                file=(filename, file, mime_type),
                purpose="file-extract"
            )
            logger.debug(file_object)

            response = await client.files.content(file_id=file_object.id)

            return response.json()

        except Exception as e:
            logger.debug(e)
            if i == 1:
                await delete_files(moonshot_client)

    # 兜底
    data = {
        'filename': filename,

        'type': 'file',
        'file_type': mime_type,
        'content': '',
    }
    try:
        data['content'] = file.decode('utf-8')

    except Exception as e:
        logger.debug(e)
    return data


# http://admin.ilovechatgpt.top/file/boshihouyanjiurenyuankaitipingshenbiaochugaofanyidocx_88256801.docx

# async def file_extract(files):
#     if isinstance(files, str):
#         return await _file_extract(files)
#
#     tasks = [_file_extract(file) for file in files]
#     return await asyncio.gather(*tasks)


# FileObject(id='1741136989_8dd96cbee6274251b7e4c9568779bd6a', bytes=82947, created_at=1741136989, filename='kling_watermark.png', object='file',  status=None, status_details=None)

if __name__ == '__main__':
    # file = "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf"
    file = "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf"
    "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 这个文件讲了什么？"
    file = "https://oss.ffire.cc/files/百炼系列手机产品介绍.docx"
    # file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/llm/completions/rag/百炼系列手机产品介绍.docx")

    # file = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/img_1.png"

    # openai.BadRequestError: Error code: 400 - {'error': {'message': 'text extract error: 没有解析出内容', 'type': 'invalid_request_error'}}
    # file = "https://oss.ffire.cc/files/kling_watermark.png"
    file = "/Users/betterme/PycharmProjects/AI/xx.sh"

    file = [file] * 10
    file = []

    # print(Path(file).read_text())

    # with timer():
    #     r = arun(file_extract(file, moonshot_client))

    # with timer():
    #     r = arun(file_extract(file, provider='kimi'))

    # with timer():
    #     arun(file_extract(file))

    # with timer():
    #     arun(file_extract("https://top.baidu.com/board?tab=realtime"))

    with timer():
        file = "https://top.baidu.com/board?tab=realtime"
        file = "http://admin.ilovechatgpt.top/file/yuzhicaizaibutongnianlingquntixiaofeixingweijishichangdiaochawenjuanweishanjianbanpptx_59787479.pptx"
        file = "https://oss.ffire.cc/files/百炼系列手机产品介绍.docx"
        # file = "https://app.yinxiang.com/fx/8b8bba1e-b254-40ff-81e1-fa3427429efe"
        file = "http://admin.ilovechatgpt.top/file/boshihouyanjiurenyuankaitipingshenbiaochugaofanyidocx_88256801.docx"

        print(guess_mime_type(file))

        arun(file_extract(file))

        # arun(file_extract("/Users/betterme/PycharmProjects/AI/data/041【精选】海门招商重工5G+智慧工厂解决方案.pptx"))
        # arun(file_extract("/Users/betterme/PycharmProjects/AI/data/098【采集】基于室内定位导航的医院解决方案.pdf"))
        # arun(file_extract("//Users/betterme/PycharmProjects/AI/data/《 纺织行业场景化解决方案-客户介绍材料》.pptx"))
