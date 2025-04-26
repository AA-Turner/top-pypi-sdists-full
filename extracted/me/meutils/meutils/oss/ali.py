#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ali
# @Time         : 2025/4/11 19:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import oss2

# params = {
#     "access_key_id": "STS.NWwe4G59dgRocw4eRdfCXvCrV",
#     "access_key_secret": "FXZPFZ9fJxkwHQbcfMbW6pSy9bFmb3xsSYWjxvTfnx3u",
#     "security_token": "CAISvgN1q6Ft5B2yfSjIr5TCLo7z2OZF0JCEYVGFgVIxasx0mYbZtDz2IHhMeXZqAuEcs/8znGlU6/gYlqRtT6h+SFffbMx24plJqado/UdL4Z7b16cNrbH4M8L6aXeirhu7AYjQSNfaZY3iCTTtnTNyxr3XbCirW0ffX7SClZ9gaKZwPGy/diEUPMpKAQFgpcQGT5q4V5CXPwXtn3DbAWdxpwN4khkf06mkxdCG4ResiT/5w+QO9YPqOcrmPYs+JYhyVZKq0eZrd+/ZyilcrEMTrKx8gKVKvGyY443YXwcI6FCPaOTat4xiJ18hPvVhQf9P/b+iz/Em5+Ddy8GpwkhAeL0FDyiaFdCtkI6bE7z0bocyeev2Yiv6i5aNLpbXy1p8Pi9Kb1gRIoJ6eiQtU0cWJ2uEevP9yjfjeRy+TqWJ6qYy3Kduwk/gldjwfADXHurDindCZ8RgNxp0akBMxw37e6oBaBdAfk13zDVs0w7K8Hm0wIafXm26PkUIphk/NM0lZWRslY41fWSSjD/XHMdspXXr/rnEdS6D75iEJCl62qLrD8iYHifDx+FBhpFLooGxJdqiIJRhHj3m9p+H/kLlIRqAAURdoxHCj+ca+GZXLN76Ae2FqVmunalPJWbb/DlgSSH4hk4uIaIQzX6NRfHMrfK/xFw++ykKEr27uA/whIn+xvmyuPrgssyHDlN8kS3lHjmsB72OX1YQRFLa3fHCy8wZalhfpDKAsSkI/FT+HDPu8EV5f+t8pdw5ZFHJFJyp7xlsIAA=",
#     "file_url": "https://cdn.qwenlm.ai/310cbdaf-3754-461c-a3ff-9ec8005329c9/62d65df4-6a6e-484d-98e8-7c7509cd5e17_1.jpg?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV91c2VyX2lkIjoiMzEwY2JkYWYtMzc1NC00NjFjLWEzZmYtOWVjODAwNTMyOWM5IiwicmVzb3VyY2VfaWQiOiI2MmQ2NWRmNC02YTZlLTQ4NGQtOThlOC03Yzc1MDljZDVlMTciLCJyZXNvdXJjZV9jaGF0X2lkIjpudWxsfQ.1lc6X4KJsAyqV71cdIjkeazPEOKYNtF5rgtiGuu_iFI",
#     "file_path": "310cbdaf-3754-461c-a3ff-9ec8005329c9/62d65df4-6a6e-484d-98e8-7c7509cd5e17_1.jpg",
#     "file_id": "62d65df4-6a6e-484d-98e8-7c7509cd5e17",
#     "bucketname": "qwen-webui-prod",
#     "region": "oss-ap-southeast-1"
# }


url = "https://chat.qwen.ai/api/v1/files/getstsToken"


def get_sts_token(filename):
    payload = {
        "filename": filename,
        "filetype": "image"  # file video audio
    }

    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNzY1N2Y1LTgxN2ItNDg5Yi1iNjk4LWFhZjAyM2EwZTE4MyIsImV4cCI6MTc0NjI5NTAwNH0.D1uJN44NHiEt6URce4upbHvs7v73_Vd0V1s3T_JzclI',

    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response.json()


def qwenai_upload(file, filetype: str = 'image'):  # todo: 自动猜测类型
    params = get_sts_token(file_name)

    access_key_id = params['access_key_id']
    access_key_secret = params['access_key_secret']
    security_token = params['security_token']

    endpoint = "oss-ap-southeast-1.aliyuncs.com"
    bucket_name = params["bucketname"]

    # 创建OSS客户端
    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 要上传的文件路径和文件名
    file_path = params.get("file_path")
    file_url = params.get("file_url")

    # 上传文件
    if isinstance(file, bytes):
        bucket.put_object(file_path, file)
    else:
        bucket.put_object_from_file(file_path, file)

    return file_url


if __name__ == '__main__':
    # qwenai_upload(params['file_path'], params)
    file_name = "/Users/betterme/PycharmProjects/AI/QR.png"
    # file_url = qwenai_upload(file_name)

    get_sts_token(file_name)
