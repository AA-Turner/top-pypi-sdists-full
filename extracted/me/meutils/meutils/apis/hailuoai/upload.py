import os
import oss2
import json
import time
import uuid
import requests
from datetime import datetime
import hashlib
from meutils.pipe import *
from meutils.hash_utils import md5

BASE_URL = "https://hailuoai.video"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM1NjI3ODcsInVzZXIiOnsiaWQiOiIzMDI4MzM4Njc3NzE5NDkwNTgiLCJuYW1lIjoibWUgYmV0dGVyIiwiYXZhdGFyIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSWdTU0NoczFENHNUajFTVGs3UHNUbTd5NTNKRFg5OW84QnhwWmNWNjU2MEFKYlJnPXM5Ni1jIiwiZGV2aWNlSUQiOiIifX0.6RgLLZGa_zFYWW0e_thcfBWWrZIS8KuBkyd6AkNZSEE"
# TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM0MDY1MzUsInVzZXIiOnsiaWQiOiIzMDI4MzM4Njc3NzE5NDkwNTgiLCJuYW1lIjoibWUgYmV0dGVyIiwiYXZhdGFyIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSWdTU0NoczFENHNUajFTVGs3UHNUbTd5NTNKRFg5OW84QnhwWmNWNjU2MEFKYlJnPXM5Ni1jIiwiZGV2aWNlSUQiOiIifX0.mcozMacSciz0MORdleOMS_uhrixhIlpQmFmUwvn81I4"
# TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM1MzMwNTAsInVzZXIiOnsiaWQiOiIzMDI4MzM4Njc3NzE5NDkwNTgiLCJuYW1lIjoibWUgYmV0dGVyIiwiYXZhdGFyIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSWdTU0NoczFENHNUajFTVGs3UHNUbTd5NTNKRFg5OW84QnhwWmNWNjU2MEFKYlJnPXM5Ni1jIiwiZGV2aWNlSUQiOiIifX0.R1wHnd5LZ3uuvEqMV5nodHjzksrJ5RVaSaqjnt_dfDQ"
# BASE_URL = "https://hailuoai.com"
# TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMwMTkwMDcsInVzZXIiOnsiaWQiOiIyMjkwODQ3NTA2MDEzODgwMzciLCJuYW1lIjoi5bCP6J665bi9ODAzNyIsImF2YXRhciI6Imh0dHBzOi8vY2RuLnlpbmdzaGktYWkuY29tL3Byb2QvdXNlcl9hdmF0YXIvMTcwNjI2NzcxMTI4Mjc3MDg3Mi0xNzMxOTQ1NzA2Njg5NjU4OTZvdmVyc2l6ZS5wbmciLCJkZXZpY2VJRCI6IjI0MzcxMzI1MjU0NTk4NjU2MiIsImlzQW5vbnltb3VzIjpmYWxzZX19.dZwNcZfVnHHWYJRiv3wOrD2LSM3X9jzof6jxH2OcZOI"
# TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM1MzI3NjUsInVzZXIiOnsiaWQiOiIyNDM3MTMyNTI3OTc2NDA3MDgiLCJuYW1lIjoi5bCP6J665bi9NzA4IiwiYXZhdGFyIjoiaHR0cHM6Ly9jZG4ueWluZ3NoaS1haS5jb20vcHJvZC91c2VyX2F2YXRhci8xNzA2MjY3MzY0MTY0NDA0MDc3LTE3MzE5NDU3MDY2ODk2NTg5Nm92ZXJzaXplLnBuZyIsImRldmljZUlEIjoiMjQzNzEzMjUyNTQ1OTg2NTYyIiwiaXNBbm9ueW1vdXMiOmZhbHNlfX0.7Twuu96zja8htvqY0Psm3bJV8sHAVIBke79JR-5YW4Y"
USER_ID = "3de88ad0-8a38-48a9-8ed3-0d63f9c71296"
DEVICE_ID = "302833759512764417"

headers = {
    "token": TOKEN,
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}


def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:  # 打开文件，以二进制读取模式
        for chunk in iter(lambda: f.read(4096), b""):  # 读取文件的块
            hash_md5.update(chunk)  # 更新哈希值
    logger.debug(hash_md5.hexdigest()) # 5d850db413c9b55eff61d47cbec208e7
    return hash_md5.hexdigest()


def upload_path(image_path):
    tt = "{}000".format(int(time.time()))
    url = "https://hailuoai.video/v1/api/files/request_policy?device_platform=web&app_id=3001&version_code=22201&uuid={}&device_id={}&os_name=Windows&browser_name=chrome&device_memory=8&cpu_core_num=20&browser_language=zh-CN&browser_platform=Win32&screen_width=2560&screen_height=1440&unix={}".format(
        USER_ID, DEVICE_ID, tt)

    url = f"{BASE_URL}/v1/api/files/request_policy?device_platform=web&app_id=3001&version_code=22201&uuid={USER_ID}&device_id={DEVICE_ID}&os_name=Windows&browser_name=chrome&device_memory=8&cpu_core_num=20&browser_language=zh-CN&browser_platform=Win32&screen_width=2560&screen_height=1440&unix={tt}"
    res = requests.get(url, headers=headers)
    data = res.json()["data"]

    print(data)
    # 提供的认证信息
    access_key_id = data["accessKeyId"]
    access_key_secret = data["accessKeySecret"]
    security_token = data["securityToken"]
    bucket_name = data["bucketName"]
    endpoint = data["endpoint"]
    dir_name = data["dir"]

    # 创建OSS客户端
    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 要上传的文件路径和文件名
    obj_name = "{}.{}".format(str(uuid.uuid4()), image_path.split(".")[-1])
    object_name = f"{dir_name}/{obj_name}"

    # 上传文件
    bucket.put_object_from_file(object_name, image_path)
    # bucket.put_object(object_name, Path(image_path).read_bytes())


    print(dir_name, obj_name)
    print("File uploaded successfully")
    origin_name = image_path.split("/")[-1]
    size = str(os.path.getsize(image_path))
    h_md5 = calculate_md5(image_path)
    mini_type = image_path.split(".")[-1]
    up_tt = "{}000".format(int(time.time()))
    up_url = "https://hailuoai.video/v1/api/files/policy_callback?device_platform=web&app_id=3001&version_code=22201&uuid={}&device_id={}&os_name=Windows&browser_name=chrome&device_memory=8&cpu_core_num=20&browser_language=zh-CN&browser_platform=Win32&screen_width=2560&screen_height=1440&unix={}".format(
        USER_ID, DEVICE_ID, up_tt)

    print(up_url)

    up_url = f"{BASE_URL}/v1/api/files/policy_callback?device_platform=web&app_id=3001&version_code=22201&uuid={USER_ID}&device_id={DEVICE_ID}&os_name=Windows&browser_name=chrome&device_memory=8&cpu_core_num=20&browser_language=zh-CN&browser_platform=Win32&screen_width=2560&screen_height=1440&unix={up_tt}"

    payload = json.dumps({
        "fileName": obj_name,
        "originFileName": origin_name,
        "dir": dir_name,
        "endpoint": endpoint,
        "bucketName": bucket_name,
        "size": size,
        "mimeType": mini_type,
        "fileMd5": h_md5
    })

    # {
    #     "fileName": "db884a7c-99a4-40f5-929e-db8769dbf64a.png",
    #     "originFileName": "503af3b5-9c3b-4bdc-a6d4-256debce3dd5_00001_.png",
    #     "dir": "cdn-yingshi-ai-com/prod/2024-10-28-09/user/multi_chat_file",
    #     "endpoint": "oss-cn-wulanchabu.aliyuncs.com",
    #     "bucketName": "minimax-public-cdn",
    #     "size": "1681865",
    #     "mimeType": "png",
    #     "fileMd5": "923e10167a2d7b36e866319dad738b1e",
    #     "fileScene": 10
    # }

    res = requests.post(up_url, data=payload, headers=headers)
    print(res.text)
    print(payload)
    print(res.json())


upload_path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/data/cowboy-hat-face.webp")


# print(md5(Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/data/cowboy-hat-face.webp").read_bytes()))
