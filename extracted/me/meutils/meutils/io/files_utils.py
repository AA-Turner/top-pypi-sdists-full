#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : file
# @Time         : 2022/7/5 下午3:31
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import mimetypes

import shortuuid

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.caches import rcache, cache
from meutils.oss.minio_oss import Minio

# from fastapi import UploadFile 有点区别
from starlette.datastructures import UploadFile
from contextlib import asynccontextmanager
from httpx import AsyncClient


def guess_mime_type(file):
    mime_type = None
    if isinstance(file, str):
        mime_type, _ = mimetypes.guess_type(file)
    return mime_type or "application/octet-stream"


def file_append_firstline(line):
    with open('untitled.txt', "r+") as f:
        old = f.read()

        f.seek(0)
        f.write(line)
        f.write(old)


def base64_to_bytes(base64_image_string):
    """
    # 将字节数据写入图片文件
    image_data = base64_to_bytes(...)
    with open(filename, 'wb') as file:
        file.write(image_data)
    """
    return base64.b64decode(base64_image_string.split(",", 1)[-1])


async def to_bytes(
        file: Union[UploadFile, str, bytes],
        headers: Optional[dict] = None
):
    """

    :param file: 文件对象、路径、base64、url
    :param headers: httpx

    :return: todo: bytes、filepath、io.BytesIO
    """
    # assert file

    if isinstance(file, bytes):
        logger.debug(f"FileType: BYTES")

        return file

    elif isinstance(file, str):
        if file.startswith('http'):
            logger.debug(f"FileType: HTTP")

            async with AsyncClient(headers=headers or {}, timeout=300) as cilent:  # todo: 缓存 根据大小
                resp = await cilent.get(file)
                file_bytes = resp.content

        elif file.startswith('data:') and ";base64," in file or len(file) > 1024:
            logger.debug(f"FileType: BASE64")

            file_bytes = base64_to_bytes(file)

        elif Path(file).is_file():  # file
            logger.debug(f"FileType: PATH")

            file_bytes = Path(file).read_bytes()

        else:
            logger.debug(f"FileType: MAY BASE64")

            file_bytes = base64_to_bytes(file)

        return file_bytes

    elif isinstance(file, UploadFile):
        file_bytes = await file.read()
        return file_bytes


@asynccontextmanager
async def to_tempfile(file: Union[UploadFile, str]):
    """

    :param file: 文件对象、路径、base64、url
    :return: todo: bytes、filepath、io.BytesIO
    """
    file_bytes = await to_bytes(file)

    with tempfile.NamedTemporaryFile(mode='wb+') as temp:
        temp.write(file_bytes)
        temp.seek(0)

        logger.debug(temp.name)

        yield temp.name


async def to_url_fal(
        file: Union[str, bytes, List],
        filename: Optional[str] = None,
        headers: Optional[dict] = None,
        content_type: str = "application/octet-stream",
):
    """对象存储 todo: minio"""
    if isinstance(file, list):
        tasks = [to_url_fal(_, filename, headers, content_type) for _ in file]
        urls = await asyncio.gather(*tasks)
        return urls

    if not file: return

    if isinstance(file, str) and file.startswith("http"):  # 转存： todo: base64
        content_type = mimetypes.guess_type(file)[0] or content_type

    file = await to_bytes(file, headers=headers)
    content_type = (
            mimetypes.guess_type(filename or '')[0]
            or mimetypes.guess_type(f"x.{content_type}")[0]  # format: image/png
            or content_type
    )

    import fal_client

    url = await fal_client.upload_async(data=file, content_type=content_type, file_name=filename)
    return url


async def to_url(
        file: Union[str, bytes, List],
        filename: Optional[str] = None,
        headers: Optional[dict] = None,

        content_type: Optional[str] = None,
        mime_type: Optional[str] = None
):
    content_type = content_type or mime_type

    if isinstance(file, list):
        tasks = [to_url(_, f"{shortuuid.random()}_{filename}", headers, content_type=content_type) for _ in file]
        urls = await asyncio.gather(*tasks)
        return urls

    if not file: return

    file = await to_bytes(file, headers=headers)
    file_url = await Minio().upload(file, filename, content_type=content_type)
    return file_url


async def to_base64(file: Union[UploadFile, str, bytes, list], content_type: Optional[str] = None):
    if isinstance(file, list):
        tasks = [to_base64(_, content_type) for _ in file]
        return await asyncio.gather(*tasks)

    if not file: return

    # logger.debug(file)
    _ = base64.b64encode(await to_bytes(file)).decode('utf-8')

    if content_type:  # "image/png"
        _ = f"data:{content_type};base64,{_}"

    return _


def base64_to_file(base64_image_string, filename):
    image_data = base64_to_bytes(base64_image_string)
    with open(filename, 'wb') as file:
        file.write(image_data)


def file_to_base64(file):
    _ = base64.b64encode(Path(file).read_bytes()).decode('utf-8')
    content_type = mimetypes.guess_type('img.webp')[0] or "data:image/jpeg"

    return f"data:{content_type},{_}"


async def to_file(file: Union[UploadFile, str, bytes], filename: Optional[str] = None):
    file = await to_bytes(file)
    if not filename:  # 临时文件
        with tempfile.NamedTemporaryFile(mode='wb+', delete=False) as temp:
            temp.write(file)
            temp.seek(0)
            return temp.name
    else:
        Path(filename).write_bytes(file)
        return Path(filename).resolve()


async def markdown_base64_to_url(text, pattern=r'!\[Image_\d+\]\((.+?)\)'):
    base64_strings = re.findall(pattern, text)

    tasks = [to_url(base64_string, filename=f"{shortuuid.random()}.png") for base64_string in base64_strings]
    urls = await asyncio.gather(*tasks)

    for base64_string, url in zip(base64_strings, urls):
        text = text.replace(base64_string, url)
    return text


if __name__ == '__main__':
    # import tempfile
    #
    # # 使用上下文管理器自动处理文件的关闭和删除
    # with tempfile.NamedTemporaryFile(mode='wb+') as temp:
    #     temp.write(b"This is a temporary file.")
    #     temp.seek(0)
    #     print(f"文件内容: {temp.read()}")
    #     print(f"临时文件名: {temp.name}")
    # 文件在这里自动关闭和删除

    # arun(to_bytes(''))

    # arun(to_url("x.png"))

    # url = "https://storage.googleapis.com/bsp-remini-image-in-web-us-central1-autodelete/54a2d77f-3070-4a95-8a1b-906ac1c74d44/64439c90-c628-47e0-9e1b-36dbbbd06664/ba502f58/input.jpg?X-Goog-Algorithm=GOOG4-HMAC-SHA256&X-Goog-Credential=GOOG1ETQDJI557KBP4YD5TQG6FMZHVKCP3S53FHI6XLBYYMT24W3PZAZNZZWQ%2F20241014%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241014T060335Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=b7745e3639a1cb81465409bfa7ed20801c5b997945739810c32cb4af02304893"

    # arun(to_base64(url))[:100]

    url = "https://oss.ffire.cc/files/kling_watermark.png"

    # arun(to_file(url, filename='x.jpg'))

    file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/x.py").read_bytes()

    # arun(to_url_fal([file] * 1))

    # print(mimetypes.guess_type("http://url"))
    # print(mimetypes.guess_type("http://url.pdf"))
    # print(mimetypes.guess_type("http://url.php"))
    #
    # print(mimetypes.guess_type("xx.txt"))
    # print(mimetypes.guess_type("xx.html"))
    # print(mimetypes.guess_type("xx.mp3"))
    # print(mimetypes.guess_type("xx.mp4"))

    # print(guess_mime_type("http://url")) # application # msword

    # arun(to_bytes(None))

    # print(mimetypes.guess_type("x.jpg"))
    # print(mimetypes.guess_type("x.png"))
    # print(mimetypes.guess_type("x.jpg"))

    # print(mimetypes.guess_extension("x.mp4", False))

    # arun(to_url(
    #     "https://cdn.hailuoai.video/moss/prod/2024-11-11-09/video/1731287464150180347-video_raw_8ba15c5c206f8d393a9248f4f9215ed8_312186282087260162.mp4",
    #     content_type=None))

    # arun(to_url_fal(url))
    # print(guess_mime_type(b"base64xxxxxxxxxxxxxxxxxx.mp4"))

    # arun(to_url([Path('img_1.png').read_bytes()], filename='x.png'))
    file = "/Users/betterme/PycharmProjects/AI/ppt.txt"
    # arun(to_url(Path(file).read_bytes(), filename='ppt.txt'))

    # arun(markdown_base64_to_url("![Image_0](data:image)"))

    # arun(to_bytes("https://oss.ffire.cc/files/kling_watermark.png"))

    file = "https://v3.fal.media/files/penguin/Rx-8V0MVgkVZM6PJ0RiPD_douyin.mp4"
    arun(to_bytes(file))
