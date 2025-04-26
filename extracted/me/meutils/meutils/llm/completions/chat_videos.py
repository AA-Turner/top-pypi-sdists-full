#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_videos
# @Time         : 2025/3/20 10:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.apis.chatglm import glm_video_api  # VideoRequest, create_task, get_task
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self,
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None
                 ):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def create(self, request: CompletionRequest):

        image_url = None
        prompt = request.last_user_content
        if urls := parse_url(prompt):
            image_url = urls[0]
            prompt = prompt.replace(image_url, "")

        # 创建任务
        video_request = glm_video_api.VideoRequest(image_url=image_url, prompt=prompt)
        response = await glm_video_api.create_task(video_request)
        taskid = response.id
        system_fingerprint = response.system_fingerprint

        # 获取任务
        for i in f"""> VideoTask(id={taskid.split('-')[-1]}, image_url={image_url}, prompt={prompt})\n""":
            await asyncio.sleep(0.03)
            yield i

        yield f"[🤫 任务进度]("
        for i in range(60):
            await asyncio.sleep(3)
            response = await glm_video_api.get_task(taskid, system_fingerprint)

            logger.debug(response)
            if response.task_status == "SUCCESS" or response.video_result:
                yield ")🎉🎉🎉\n\n"
                for video in response.video_result or []:
                    yield f"[^1]: [封面]({video.cover_image_url})\n\n"
                    yield f"[^2]: [视频]({video.url})\n\n"

                    yield f"[视频]({video.url})[^1][^2]\n\n"
                    yield f"![视频]({video.url})[^1][^2]\n\n"

                break
            else:
                yield "🔥"


if __name__ == '__main__':
    url = "https://oss.ffire.cc/files/lipsync.mp3"
    url = "https://lmdbk.com/5.mp4"
    content = [
        {"type": "text", "text": "总结下"},
        # {"type": "image_url", "image_url": {"url": url}},

        {"type": "video_url", "video_url": {"url": url}}

    ]
    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        model="gemini-all",
        # model="qwen-plus-latest",

        messages=[
            {
                'role': 'user',

                'content': content
            },

        ],
        stream=False,
    )
    arun(Completions().create(request))
