#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : adapters
# @Time         : 2025/5/30 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import shortuuid
from aiostream import stream

from meutils.pipe import *
from meutils.io.files_utils import to_url, to_url_fal
from meutils.str_utils.json_utils import json_path
from meutils.llm.openai_utils import create_chat_completion
from meutils.schemas.openai_types import CompletionRequest, ChatCompletion
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.llm.openai_utils import chat_completion, chat_completion_chunk, create_chat_completion_chunk
from meutils.str_utils import parse_url, parse_command_string


async def stream_to_nostream(
        request: CompletionRequest,
):
    pass


async def chat_for_image(
        generate: Optional[Callable],
        request: CompletionRequest,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        http_url: Optional[Any] = None,
):
    generate = generate and partial(generate, api_key=api_key, base_url=base_url, http_url=http_url)

    image = None
    prompt = request.last_user_content
    if image_urls := request.last_urls.get("image_url"):  # image_url
        if request.model.startswith('fal'):
            urls = await to_url_fal(image_urls, content_type="image/png")  # 国外友好
            image = urls

        elif request.model.startswith("doubao-seed"):
            image = image_urls  # b64

        else:
            urls = await to_url(image_urls, ".png", content_type="image/png")  # b64 转 url
            image = urls

    image_request = ImageRequest(
        model=request.model,
        prompt=prompt,
        image=image
    )
    if not image_request.image:
        image_request.image, image_request.prompt = image_request.image_and_prompt

    if '--' in image_request.prompt:
        prompt_dict = parse_command_string(image_request.prompt)
        # 缩写补充
        prompt_dict['aspect_ratio'] = prompt_dict.get('aspect_ratio') or prompt_dict.get('ar')

        data = {
            **image_request.model_dump(exclude_none=True, exclude={"extra_fields", "aspect_ratio"}),
            **prompt_dict
        }
        image_request = ImageRequest(**data)
        logger.debug(image_request)

    # 非流式
    if not request.stream:
        if request.last_user_content.startswith(  # 跳过nextchat
                (
                        "hi",
                        "使用四到五个字直接返回这句话的简要主题",
                        "简要总结一下对话内容，用作后续的上下文提示 prompt，控制在 200 字以内"
                )):
            return chat_completion

        response = await generate(image_request)  # None

        if not response:
            raise Exception(f"image generate error: {str(request)[:1000]}")

        if not isinstance(response, dict):
            response = response.model_dump()

        content = ""
        for image in response['data']:
            content += f"""![{image.get("revised_prompt")}]({image['url']})\n\n"""

        chat_completion.choices[0].message.content = content
        chat_completion.usage = image_request.usage
        return chat_completion

    # 流式
    if not generate: return

    future_task = asyncio.create_task(generate(image_request))  # 异步执行

    async def gen():
        exclude = None
        if len(str(image_request.image)) > 1000:
            exclude = {"image"}

        text = image_request.model_dump_json(exclude_none=True, exclude=exclude).replace("free", "")
        for i in f"""> 🖌️正在绘画\n\n```json\n{text}\n```\n\n""":
            await asyncio.sleep(0.05)
            yield i

        try:
            response = await future_task
            # response = await response  # 注意

            if not isinstance(response, dict):
                response = response.model_dump()

            for image in response['data']:
                yield f"""![{image.get("revised_prompt")}]({image['url']})\n\n"""


        except Exception as e:
            # yield f"```error\n{e}\n```\n"
            raise e

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
        for i in range(100):
            await asyncio.sleep(3)
            response = await get_task(taskid)  # 包含  "status"

            logger.debug(response)
            if isinstance(response, BaseModel):
                response = response.model_dump(exclude_none=True)

            if response.get("status", "").lower().startswith(("comp", "succ", "fail")):

                yield ")🎉🎉🎉\n\n"

                yield f"""```json\n{json.dumps(response, indent=4, ensure_ascii=False)}\n```"""

                if urls := json_path(response, expr='$..[url,image_url,video_url]'):  # 所有url
                    for i, url in enumerate(urls, 1):
                        yield f"\n\n[下载链接{i}]({url})\n\n"

                break

            else:
                yield "🚀"

    chunks = create_chat_completion_chunk(gen(), chat_id=taskid)
    return chunks


if __name__ == '__main__':
    from meutils.apis.images.generations import generate

    request = CompletionRequest(
        model="deepseek-r1-Distill-Qwen-1.5B",
        messages=[
            {"role": "user", "content": "``hi --a 1"}
        ],
        stream=True,
    )
    arun(chat_for_image(None, request))

    request = CompletionRequest(
        model="gemini-2.5-flash-image-preview",
        messages=[
            {"role": "user", "content": "画条狗"}
        ],
        # stream=True,
    )
    api_key = "sk-MAZ6SELJVtGNX6jgIcZBKuttsRibaDlAskFAnR7WD6PBSN6M-openai"
    base_url = "https://new.yunai.link/v1"
    arun(chat_for_image(generate, request, api_key, base_url))
