#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : minio_utils
# @Time         : 2024/1/3 14:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/fanpiao/p/17603553.html
from minio import Minio
from meutils.pipe import *

minioClient = Minio(
    endpoint=os.getenv('MINIO_ENDPOINT'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    # secure=False
)

# Make a bucket with the make_bucket API call.
bucket_name = 'bname'
# minioClient.make_bucket(bucket_name)

print(minioClient.list_buckets())
# Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.

# minioClient.fput_object(bucket_name, 'object_name', 'x.yml')
#
# minioClient.fput_object(bucket_name, 'img.png', 'img.png')
#
# minioClient.fput_object(bucket_name, 'file.py', 'file.py')


# minioClient.fput_object(bucket_name, 'x/img','img.png')


# url = minioClient.get_presigned_url(
#     "GET",
#     bucket_name,
#     'img.png',
# )
# print(url)

# url = minioClient.presigned_get_object(bucket_name, 'img.png', )
# print(url)
#
# response = minioClient.get_object(bucket_name, 'img.png', )
# print(len(response.read()))