#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/11/24 11:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo 适配
import os

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest, CompletionUsage, ChatCompletion, ChatCompletionChunk, \
    chat_completion, chat_completion_chunk
import replicate


def get_usage_from_logs(logs: str) -> CompletionUsage:
    if logs:
        matches = re.findall(r'(Input|Output) token count: (\d+)', logs)
        tokens = {k: int(v) for k, v in matches}
        usage = CompletionUsage(
            prompt_tokens=tokens.get("Input", 1000),
            completion_tokens=tokens.get("Output", 1000),
        )
        return usage


class Completions(object):

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        api_key = api_key or os.getenv("REPLICATE_API_KEY")
        self.client = replicate.client.Client(api_token=api_key)

    async def create(self, request: CompletionRequest):

        payload = {
            # "audio": "https://replicate.delivery/pbxt/O5Vw2eTOp7z4V27QYXqEUQZ5OvwTEKj2TVf3syi4dTJpvUG9/Never%20Gonna%20Give%20You%20Up%20-%20Rick%20Astley.mp3",
            "top_p": request.top_p,
            "prompt": request.last_user_content,
            "images": [],
            "videos": [],
            "temperature": request.temperature,

            "max_output_tokens": request.max_completion_tokens or 65535,

            "thinking_level": request.thinking_budget or "low",
        }
        if request.system_instruction:
            payload["system_instruction"] = request.system_instruction

        if urls := request.last_urls.get("image_url"):
            payload["images"] = urls
        elif urls := request.last_urls.get("audio_url"):
            payload["audio"] = urls[0]
        elif urls := request.last_urls.get("video_url"):
            payload["videos"] = urls  # 默认第一个

        logger.debug(bjson(payload))

        # 创建任务
        response = await self.client.predictions.async_create(
            request.model,
            input=payload,
            stream=request.stream,
            # wait=False,
            webhook=f"""{os.getenv('WEBHOOK_URL')}/replicate"""
        )

        # 轮询任务
        content = ""
        for i in range(100):
            await asyncio.sleep(0.05 if content else 3)
            if prediction := await self.client.predictions.async_get(response.id):
                logger.debug(f"Status: {prediction.status}")

                if request.stream:
                    chat_completion_chunk.id = prediction.id
                    chat_completion_chunk.usage = get_usage_from_logs(prediction.logs)

                    content = ''.join(prediction.output or []).replace(content, "").strip()
                    chat_completion_chunk.choices[0].delta.content = content
                    logger.debug(chat_completion_chunk)

                    if prediction.status in ["succeeded", "failed"]:
                        break

                if prediction.status in ["succeeded", "failed"]:
                    logger.debug(prediction)

                    chat_completion.id = prediction.id
                    chat_completion.usage = get_usage_from_logs(prediction.logs)

                    content = ''.join(prediction.output or []).replace(content, "")
                    chat_completion.choices[0].message.content = content
                    logger.debug(chat_completion)

                    break

        # if request.stream:
        #     chunks = await self.client.async_stream(request.model, input=payload, wait=False)
        #
        #     logger.debug(self.client.predictions.async_create() )
        #     # todo 监控状态
        #     async for chunk in chunks:
        #         yield str(chunk)
        # else:
        #     chunks = await self.client.async_run(request.model, input=payload, wait=False)
        #     _ = ''.join(chunks)
        #     logger.debug(_)
        #     yield _


if __name__ == '__main__':
    polling_url = "https://oneapi.chatfire.cn/sys/webhook/replicate?task_id=t4117wzm91rmt0cw9hwt197br0"
    url = "https://lmdbk.com/5.mp4"
    model = "google/gemini-3-pro"
    model = "google/gemini-3-flash"
    request = CompletionRequest(
        model=model,
        stream=True,
        messages=[{"role": "user", "content": "9.11 9.8哪个大"}])


    arun(Completions(api_key=api_key).create(request))
