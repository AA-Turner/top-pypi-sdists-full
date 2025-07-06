#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : minio_oss
# @Time         : 2024/3/14 17:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import datetime
import mimetypes

from meutils.pipe import *

from minio import Minio as _Minio
from openai.types.file_object import FileObject
from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request, status
from asgiref.sync import sync_to_async


class Minio(_Minio):

    def __init__(self, endpoint: Optional[str] = None,
                 access_key: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 **kwargs):
        self.endpoint = endpoint or os.getenv('MINIO_ENDPOINT', 's3.ffire.cc')
        access_key = access_key or os.getenv('MINIO_ACCESS_KEY', 'minio')
        secret_key = secret_key or os.getenv('MINIO_SECRET_KEY')

        secure = False if ":" in self.endpoint else True

        super().__init__(endpoint=self.endpoint, access_key=access_key, secret_key=secret_key, secure=secure, **kwargs)

    # def list_bucket_objects(self):
    #     super().list_buckets()
    #     super().list_objects('中职职教高考政策解读.pdf')
    #     return super().list_buckets()
    async def upload(
            self,
            file: bytes,
            filename: Optional[str] = None,

            content_type: Optional[str] = None,

            bucket_name: str = "cdn",

    ):
        file_name = filename or shortuuid.random()

        content_type = (
                content_type
                or mimetypes.guess_type(file_name)[0]
                or "application/octet-stream"
        )

        object_name = f"""{datetime.datetime.now().strftime("%Y%m%d")}/{file_name}"""
        _ = await self.aput_object(
            bucket_name,
            object_name=object_name,
            content_type=content_type,

            data=io.BytesIO(file),
            length=len(file),
        )

        return f"https://{self.endpoint}/{bucket_name}/{object_name}"

    async def put_object_for_openai(
            self,
            file: Union[str, bytes, UploadFile],

            bucket_name: str = "cdn",
            purpose: str = "oss",

            filename: Optional[str] = None,  # 预生成：提前生成链接返回 适用于异步任务

            headers: Optional[dict] = None,
            follow_redirects: bool = False,

            content_type: Optional[str] = "application/octet-stream",

    ):
        """
        FileObject(id='ZDcQjHb9nsmwnYXaw8eKem.docx', bytes=55563, created_at=1710729984, filename='ZDcQjHb9nsmwnYXaw8eKem.docx', object='file', purpose='file-upload', status='processed', status_details=None)

        """
        # self.make_bucket(bucket_name, object_lock=True)

        # file 标准化为 UploadFile
        if isinstance(file, str) and file.startswith("http"):  # todo: url2UploadFile 从网络下载
            async with httpx.AsyncClient(timeout=300, headers=headers, follow_redirects=follow_redirects) as client:
                for i in range(3):
                    response = await client.get(url=file)
                    if response.is_success: break

                file = UploadFile(
                    file=io.BytesIO(response.content),
                    filename=filename or Path(file).name,
                    size=len(response.content),
                    headers=response.headers,  # content_type
                )
                logger.debug(file)

        elif isinstance(file, bytes):
            file = UploadFile(
                file=io.BytesIO(file),
                size=len(file),

                filename=filename,
            )
        file_name = filename or file.filename or shortuuid.random()

        content_type = (
                file.content_type
                or mimetypes.guess_type(file_name)[0]
                or content_type
                or "application/octet-stream"
        )

        logger.debug(f"content_type: {content_type}")
        object_name = f"""{datetime.datetime.now().strftime("%Y%m%d")}/{file_name}"""
        _ = await self.aput_object(
            bucket_name,
            object_name=object_name,
            data=file.file,
            length=file.size,  # 不能为None
            content_type=content_type
        )

        # construct 创建实例，跳过验证
        file_object = FileObject.construct(
            id=object_name,
            bytes=file.size,
            created_at=int(time.time()),
            filename=f"https://{self.endpoint}/{bucket_name}/{object_name}",
            # file_url: oss.chatfire.cn/files/{file_id}

            object='file',

            purpose=purpose,

            status='processed' if _ else "error",  # todo: 抛错处理

        )

        logger.debug(file_object)

        return file_object

    @sync_to_async(thread_sensitive=False)
    def aget_object(self, *args, **kwargs):
        return self.get_object(*args, **kwargs)

    # async def aget_object(self, *args, **kwargs):
    #     return sync_to_async(thread_sensitive=False)(self.get_object)(*args, **kwargs)

    @sync_to_async(thread_sensitive=False)
    def aput_object(self, *args, **kwargs):
        return self.put_object(*args, **kwargs)

    def get_file_url(self, filename, bucket_name='files'):
        return f"https://{self.endpoint}/{bucket_name}/{filename}"


# minio_client.put_object(OPENAI_BUCKET, f"{api_key}/{file.filename}", data=file.file, length=file.size)

# # Make a bucket with the make_bucket API call.
# bucket_name = 'bname'
# # minioClient.make_bucket(bucket_name)
#
# print(client.list_buckets())

if __name__ == '__main__':
    client = Minio()
    # bucket_name = 'test'
    # prefix = 'prefix'
    # filename = Path('minio_oss.py').name
    # data = Path('minio_oss.py').read_bytes()
    #
    # extension = Path("xx.x").suffix
    #
    # file_url = Path(f"{bucket_name}/{prefix}/xxxxxxxx{extension}")  # base url
    #
    # print(file_url)
    #
    # obj = client.put_object(bucket_name, f"{prefix}/{filename}", data=io.BytesIO(data), length=len(data),
    #                         metadata={"url": str(file_url), "content_type": "application/octet-stream"}
    #                         )
    #
    # print(obj)

    # _ = client.put_object_for_openai(
    #     "https://sfile.chatglm.cn/chatglm4/82834747-0fcf-4ecb-94b0-92e5e749798b.docx",
    #     bucket_name="files",
    #     file_id='xx.docx'
    # )

    url = "https://sfile.chatglm.cn/testpath/4f520e7f-c2f5-5555-8d1f-4fda0fec0e9d_0.png"
    # url = "https://cdn1.suno.ai/bb10a2e9-3543-4ddc-aad1-2c7ca95bfa7c.mp3"
    # url = "https://p1.a.kwimgs.com/bs2/upload-ylab-stunt/special-effect/output/HB1_PROD_ai_web_31199871/685408188778288330/output_ffmpeg.mp4"
    # url = 'https://klingai.com/api/works/batch_download?workIds=58740791&fwm=false'
    # _ = client.put_object_for_openai(
    #     url,
    #     bucket_name="caches",
    #     filename='cff.png'
    # )
    # print(arun(_, debug=True))

    # _ = client.put_object_for_openai(
    #     url,
    #     filename='cff.png'
    # )
    # arun(_)

    f = client.upload(Path("/Users/betterme/PycharmProjects/AI/qun.png").read_bytes(), filename='x.png')
