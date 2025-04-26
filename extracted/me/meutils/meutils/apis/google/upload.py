#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : upload
# @Time         : 2025/4/21 16:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
import asyncio
import httpx
import os
import mimetypes
import json
import sys
from pathlib import Path

mime_type = mimetypes.guess_type("x.html")[0] or "application/octet-stream"

print(mime_type)

num_bytes = len(Path("x.html").read_bytes())

headers = {
    "X-Goog-Upload-Protocol": "resumable",
    "X-Goog-Upload-Command": "start",
    "X-Goog-Upload-Header-Content-Length": str(num_bytes),
    "X-Goog-Upload-Header-Content-Type": mime_type,
    "Content-Type": "application/json",



}
# payload = {'file': {'display_name': "TEXT"}}
payload = {}
base_url = "https://all.chatfire.cc/genai"

client = httpx.Client(base_url=base_url, headers=headers)

response = client.post("/upload/v1beta/files", params={"key": os.getenv("GOOGLE_API_KEY")}, json=payload)

print(dict(response.headers))
upload_url = response.headers.get("x-goog-upload-url")
print(upload_url)

headers = {"X-Goog-Upload-Offset": "0",
    "X-Goog-Upload-Command": "upload, finalize", **headers}

response = httpx.post(url=upload_url, headers=headers, content=Path("x.html").read_bytes())
