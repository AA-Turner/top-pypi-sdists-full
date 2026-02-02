#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/11/24 11:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest, CompletionUsage
import replicate


class Completions(object):

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        api_key = api_key or os.getenv("REPLICATE_API_KEY")
        self.client = replicate.client.Client(api_token=api_key)

    async def create(self, request: CompletionRequest):

        payload = {
            # "audio": "https://replicate.delivery/pbxt/O5Vw2eTOp7z4V27QYXqEUQZ5OvwTEKj2TVf3syi4dTJpvUG9/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3",
            "top_p": request.top_p,
            "images": [],
            "prompt": request.last_user_content,
            "videos": [],
            "temperature": request.temperature,
            "thinking_level": request.reasoning_effort or "low",
            "max_output_tokens": request.max_completion_tokens or 64000
        }

        if image_urls := request.last_urls.get("image_url"):
            payload["images"] += image_urls
        elif audio_urls := request.last_urls.get("audio_url"):
            payload["audio"] = audio_urls[0]
        elif video_urls := request.last_urls.get("video_url"):
            payload["videos"].append(video_urls[0])  # 默认第一个

        logger.debug(bjson(payload))

        if request.stream:
            chunks = await self.client.async_stream(request.model, input=payload, wait=False)
            async for chunk in chunks:
                yield str(chunk)
        else:
            chunks = await self.client.async_run(request.model, input=payload, wait=False)
            _ = ''.join(chunks)
            logger.debug(_)
            yield _


if __name__ == '__main__':
    url = "https://lmdbk.com/5.mp4"
    request = CompletionRequest(
        model="google/gemini-3-pro",
        stream=True,
        messages=[{"role": "user", "content": "你好"}])

    arun(Completions().create(request))
