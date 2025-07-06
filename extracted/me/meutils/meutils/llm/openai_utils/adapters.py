#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : adapters
# @Time         : 2025/5/30 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_url_fal
from meutils.str_utils.json_utils import json_path
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.image_types import ImageRequest
from meutils.llm.openai_utils import chat_completion, chat_completion_chunk, create_chat_completion_chunk


async def stream_to_nostream(
        request: CompletionRequest,
):
    pass


async def chat_for_image(
        generate: Callable,
        request: CompletionRequest,
        api_key: Optional[str] = None,
):
    generate = partial(generate, api_key=api_key)

    if not request.stream or request.last_user_content.startswith(  # 跳过nextchat
            (
                    "hi",
                    "使用四到五个字直接返回这句话的简要主题",
                    "简要总结一下对话内容，用作后续的上下文提示 prompt，控制在 200 字以内"
            )):
        chat_completion.choices[0].message.content = "请设置`stream=True`"
        return chat_completion

    prompt = request.last_user_content
    if request.last_urls:  # image_url
        urls = await to_url_fal(request.last_urls["image_url"], content_type="image/png")
        prompt = "\n".join(urls + [prompt])

    request = ImageRequest(
        model=request.model,
        prompt=prompt,
    )

    future_task = asyncio.create_task(generate(request))  # 异步执行

    async def gen():
        for i in f"> 🖌️正在绘画\n\n```json\n{request.model_dump_json(exclude_none=True)}\n```\n\n":
            await asyncio.sleep(0.05)
            yield i

        response = await future_task

        for image in response.data:
            yield f"![{image.revised_prompt}]({image.url})\n\n"

    chunks = create_chat_completion_chunk(gen(), redirect_model=request.model)
    return chunks


async def chat_for_video(
        get_task: Callable,  # response
        taskid: str,
):
    """异步任务"""

    async def gen():

        # 获取任务
        for i in f"""> VideoTask(id={taskid})\n""":
            await asyncio.sleep(0.03)
            yield i

        yield f"[🤫 任务进度]("
        for i in range(60):
            await asyncio.sleep(3)
            response = await get_task(taskid)  # 包含  "status"

            logger.debug(response)
            if response.get("status", "").lower().startswith(("succ", "fail")):

                yield ")🎉🎉🎉\n\n"

                yield f"""```json\n{json.dumps(response, indent=4, ensure_ascii=False)}\n```"""

                if urls := json_path(response, expr='$..[url,image_url,video_url]'):  # 所有url
                    for i, url in enumerate(urls, 1):
                        yield f"\n\n[下载链接{i}]({url})\n\n"

                break

            else:
                yield "🚀"

    chunks = create_chat_completion_chunk(gen())
    return chunks


if __name__ == '__main__':
    request = CompletionRequest(
        model="deepseek-r1-Distill-Qwen-1.5B",
        messages=[
            {"role": "user", "content": "``hi"}
        ],
        stream=False,
    )
    arun(chat_for_image(None, request))
