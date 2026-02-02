#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : elevenlabs
# @Time         : 2025/7/14 16:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.apis.utils import make_request_httpx

UPSTREAM_BASE_URL = "https://api.elevenlabs.io/v1"
UPSTREAM_API_KEY = "sk_9e7ce9190f85579b527beb6e673eb350db9c0cbfe2c7334b"
headers = {
    "xi-api-key": UPSTREAM_API_KEY
}

path = "/text-to-speech/JBFqnCBsd6RMkjVDRZzb"

params = {
    "output_format": "mp3_44100_128"
}
payload = {
    "text": "The first move is what sets everything in motion.",
    "model_id": "eleven_multilingual_v2"
}

path = "speech-to-text"

data = {
    'model_id': "scribe_v1",
}
files = {
    'file': ('xx.mp3', open("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/x1.wav", 'rb'))

}

arun(make_request_httpx(
    base_url=UPSTREAM_BASE_URL,
    path=path,
    # payload=payload,
    data=data,
    files=files,
    headers=headers,
    params=params,
    # debug=True,
))
