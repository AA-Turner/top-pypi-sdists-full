#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kaiyuan
# @Time         : 2024/12/18 16:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import hmac
import zlib
import hashlib

from meutils.pipe import *
from meutils.caches.redis_cache import cache
from meutils.io.files_utils import to_bytes
from meutils.apis.jimeng.common import get_upload_token, get_headers, BASE_URL, FEISHU_URL, check_token
from meutils.notice.feishu import send_message_for_images
from meutils.config_utils.lark_utils import get_next_token_for_polling


def random_str(n):
    return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', n))


def hash256(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def hmac_hash256(key, msg):
    if type(key) == str:
        return hmac.new(key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256)
    elif type(key) == hmac.HMAC:
        return hmac.new(key.digest(), msg.encode('utf-8'), hashlib.sha256)


def fileCRC32(file_buffer):
    return hex(zlib.crc32(file_buffer) & 0xFFFFFFFF)[2:]


def u(params):
    new_params = sorted(params.items(), key=lambda x: x[0])
    new_params = [f"{k}={v}" for k, v in new_params]
    return "&".join(new_params)


class JJRequest:
    def __init__(self, e, t, api, method="GET", params=None, data=None, serviceName="imagex"):
        self.t = t
        self.e = e
        self.api = api
        self.method = method
        self.params = params
        self.data = data

        self.serviceName = serviceName

    def getAuthorization(self):
        return f"AWS4-HMAC-SHA256 Credential={self.e['access_key_id']}/{self.t[:8]}/cn-north-1/{self.serviceName}/aws4_request, SignedHeaders=x-amz-date;x-amz-security-token, Signature={self.signature()}"

    def signature(self):
        r = self.getSigningKey()
        return hmac_hash256(r, self.stringToSign()).hexdigest()

    def getSigningKey(self, r="cn-north-1"):
        n = self.serviceName

        o = hmac_hash256("AWS4" + self.e['secret_access_key'], str(self.t[0:8]))
        i = hmac_hash256(o, str(r))
        s = hmac_hash256(i, str(n))
        return hmac_hash256(s, "aws4_request")

    def stringToSign(self):
        t = []
        t.append("AWS4-HMAC-SHA256")
        t.append(self.t)
        t.append(self.credentialString())
        t.append(hash256(self.canonicalString()))
        return "\n".join(t)

    def credentialString(self, region="cn-north-1"):
        return "/".join([self.t[0:8], region, self.serviceName, "aws4_request"])

    def canonicalString(self):
        e = []
        e.append(self.method)
        e.append("/")
        e.append(u(self.params))
        e.append(self.canonicalHeaders())
        e.append(self.signedHeaders())
        e.append(self.hexEncodedBodyHash())
        return "\n".join(e)

    def canonicalHeaders(self):
        return f"x-amz-date:{self.t}\nx-amz-security-token:{self.e['session_token']}\n"

    def signedHeaders(self):
        return "x-amz-date;x-amz-security-token"

    def hexEncodedBodyHash(self):
        return hash256("")


# @cache(ttl=15 * 60)
async def upload(image: bytes, upload_token: dict):  # oss 跨账号不知道是否可以使用
    # e = auth = upload_token['data']['auth'] # 豆包
    data = upload_token['data']
    # service_id = data.get('service_id', '3jr8j4ixpe')  # 即梦 3jr8j4ixpe 豆包 a9rns2rl98

    service_id = data.get('space_name') or "3jr8j4ixpe"  # 即梦视频 tb4s082cfz

    if 'auth' in data:
        data = data['auth']

    session_token = data['session_token']

    t = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    # "ServiceId": "tb4s082cfz",
    params = {
        "Action": "ApplyImageUpload",
        "Version": "2018-08-01",
        "ServiceId": service_id,
        "s": random_str(10),

        # "FileExtension": ".png",  #####
        "FileSize": len(image),
    }

    r = JJRequest(data, t, "https://imagex.bytedanceapi.com/", method="GET", params=params)
    headers = {
        'authorization': r.getAuthorization(),
        'x-amz-date': t,
        'x-amz-security-token': session_token,
    }
    # logger.debug(headers)
    response = requests.get(r.api, params=params, headers=headers)
    response.raise_for_status()
    logger.debug(response.status_code)
    response = response.json()

    logger.debug(bjson(response))
    if "Result" not in response:
        return

    store_info = response['Result']['UploadAddress']['StoreInfos'][0]
    logger.debug(bjson(store_info))

    oss_uri = store_info['StoreUri']
    oss_token = store_info['Auth']

    headers = {
        "authorization": oss_token,
        "content-length": str(len(image)),
        "content-Type": "image/jpeg",
        "content-crc32": fileCRC32(image),
    }

    # oss_url = f"https://{resp['Result']['UploadAddress']['UploadHosts'][0]}/{oss_uri}"

    # image_resp = requests.put(  # post
    #     oss_url,
    #     headers=headers,
    #     data=image,
    # )
    # logger.debug(image_resp.json())

    # return get_url(StoreUri)

    # upload_url = f"https://tos-hl-x.snssdk.com/upload/v1/{oss_uri}"
    upload_url = f"https://{response['Result']['UploadAddress']['UploadHosts'][0]}/upload/v1/{oss_uri}"

    # response = requests.post(upload_url, headers=headers, data=image)
    # response.raise_for_status()
    # response = response.json()
    # logger.debug(response)

    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        response = await client.post(upload_url, content=image)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    return oss_uri


async def upload_for_vod(image: bytes, upload_token: dict):  # oss 跨账号不知道是否可以使用
    """
                    "UploadHost": "tos-lf-x.snssdk.com",
                    "UploadHost": "tos-hl-x.snssdk.com",

    :param image:
    :param upload_token:
    :return:
    """
    # e = auth = upload_token['data']['auth'] # 豆包
    data = upload_token['data']
    service_id = data.get('space_name', 'tb4s082cfz')  # 即梦 3jr8j4ixpe 豆包 a9rns2rl98

    if 'auth' in data:
        data = data['auth']

    session_token = data['session_token']

    t = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    params = {
        "Action": "ApplyUploadInner",
        "Version": "2020-11-19",

        "ServiceId": service_id,
        # "SpaceName": "artist_op",
        # "SpaceName": "dreamina",

        "IsInner": "1",

        "FileType": "video",
        "FileSize": len(image),

        "s": random_str(10),

    }

    r = JJRequest(data, t, "https://vod.bytedanceapi.com/", method="GET", params=params, serviceName="vod")
    headers = {
        'authorization': r.getAuthorization(),
        'x-amz-date': t,
        'x-amz-security-token': session_token,
    }
    # logger.debug(headers)
    # response = requests.get(r.api, params=params, headers=headers)
    # response.raise_for_status()
    # logger.debug(response.status_code)
    # response = response.json()
    # logger.debug(bjson(response))

    async with httpx.AsyncClient(headers=headers, params=params, timeout=120) as client:
        response = await client.get(r.api)
        response.raise_for_status()
        response = response.json()
        logger.debug(bjson(response))

    if "Result" not in response:
        return

    upload_node = response['Result']['InnerUploadAddress']['UploadNodes'][0]
    store_info = upload_node['StoreInfos'][0]
    logger.debug(bjson(store_info))

    vid = upload_node['Vid']
    upload_host = upload_node['UploadHost']

    oss_uri = store_info['StoreUri']
    oss_token = store_info['Auth']

    headers = {
        "authorization": oss_token,
        "content-length": str(len(image)),
        "content-Type": "application/octet-stream",
        "content-crc32": fileCRC32(image),
    }

    # upload_url = f"https://tos-hl-x.snssdk.com/upload/v1/{oss_uri}"
    upload_url = f"https://{upload_host}/upload/v1/{oss_uri}"

    # response = requests.post(upload_url, headers=headers, data=image)
    # response.raise_for_status()
    # response = response.json()
    # logger.debug(response)

    async with httpx.AsyncClient(headers=headers, timeout=120) as client:
        response = await client.post(upload_url, content=image)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    return vid, oss_uri


async def upload_for_image(image, token, biz: Optional[str] = None):  # todo: 跨账号token
    """image url base64 bytes"""
    if not image: return

    upload_token = await get_upload_token(token, biz)
    image_uri = await upload(await to_bytes(image), upload_token)
    return image_uri


async def upload_for_video(video, token):  # 跨账号token
    """video url base64 bytes
    """
    if not video: return

    upload_token = await get_upload_token(token)
    vid, uri = await upload_for_vod(await to_bytes(video), upload_token)
    return vid, uri


async def face_recognize(image, token: Optional[str] = None):
    """
    图片识别
    """
    # token = "1c21a9fe6a4230609d7ff13e5cec41ec"  # 跨账号测试

    token = token or await get_next_token_for_polling(FEISHU_URL, check_token)

    url = "/mweb/v1/face_recognize"
    headers = get_headers(url, token)

    image_uri = await upload_for_image(image, token)
    payload = {
        "image_uri_list": [
            image_uri
        ]
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=120) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        try:
            data['data']['image_uri'] = image_uri
            data['data']['face_recognize_list'][0][0]['type'] = ""
            data['data']['face_recognize_list'][0][0]['id'] = str(uuid.uuid4())
            data['data']['face_recognize_list'][0][0]['is_selected'] = True
        except Exception as e:
            logger.error(e)
            send_message_for_images(f"图片识别失败 {bjson(data)}", __name__)

        return data


if __name__ == "__main__":
    # 豆包
    token = "de2215a7bb8e442774cf388f03fac84c"

    # jimeng
    token = "ffeee346fbd19eceebb79a7bfbca4bfe"
    token = "34438eb03d165737122180caf62a8058"
    #
    # upload_token = arun(get_upload_token(token))

    #
    # with open("test.jpg", "rb") as f:
    #     file = image = f.read()
    #
    #     print(upload(image, upload_token))
    # print(upload_for_vod(image, upload_token))
    #
    # with timer():
    #     arun(upload_for_video("https://fal.media/files/koala/8teUPbRRMtAUTORDvqy0l.mp4", token))

    # with timer():
    #     arun(upload_for_image("https://oss.ffire.cc/files/kling_watermark.png", token))

    # with timer():
    #     url = "https://oss.ffire.cc/files/lipsync.mp3"
    #     # arun(upload_for_video("https://oss.ffire.cc/files/lipsync.mp3", token))
    #     arun(upload_for_video(url, token))
    image_url = "https://oss.ffire.cc/files/kling_watermark.png"
    # arun(face_recognize(image_url, token))
    # arun(face_recognize(image_url))

    token = "ed16bb360a4744696f88a7b52b7c10a3"

    arun(upload_for_image(image_url, token, "video"))
