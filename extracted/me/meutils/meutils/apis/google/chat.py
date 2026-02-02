#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/4/2 13:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn
# genai => openai
# pip install -q -U google-genai
# https://googleapis.github.io/python-genai/genai.html#module-genai.models

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.io.files_utils import to_url, to_bytes, guess_mime_type
from meutils.str_utils.regular_expression import parse_url
from meutils.apis.images.edits import edit_image, ImageProcess

from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage

from meutils.config_utils.lark_utils import get_next_token_for_polling
from google import genai
from google.genai import types
from google.genai.types import Part, HttpOptions, HarmCategory, HarmBlockThreshold
from google.genai.types import UploadFileConfig, ThinkingConfig, GenerateContentConfig, ImageConfig, \
    GenerateImagesConfig, SafetySetting

from google.genai.types import UserContent, ModelContent, Content
from google.genai.types import Tool, GoogleSearch

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=bK9ZTt"  # 200

"""
Gemini 1.5 Pro 和 1.5 Flash 最多支持 3,600 个文档页面。文档页面必须采用以下文本数据 MIME 类型之一：

PDF - application/pdf
JavaScript - application/x-javascript、text/javascript
Python - application/x-python、text/x-python
TXT - text/plain
HTML - text/html
CSS - text/css
Markdown - text/md
CSV - text/csv
XML - text/xml
RTF - text/rtf

- 小文件
- 大文件: 需要等待处理
"""
tools = [
    Tool(
        google_search=GoogleSearch()
    )
]

safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,  # ← 最宽松
    ),
    # 如果想把所有类别都调到最宽松，可再列 4 项
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),

    # types.SafetySetting(
    #     category=types.HarmCategory.HARM_CATEGORY_IMAGE_DANGEROUS_CONTENT,
    #     threshold=types.HarmBlockThreshold.BLOCK_NONE,
    # ),
]


class Completions(object):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://all.chatfire.cc/genai"
        self.client = None  ####

        self.base_url = self.base_url.removesuffix('/v1').removesuffix('/v1beta')

    async def create_for_search(self, request: CompletionRequest):
        self.client = self.client or await self.get_client()

        if request.model.endswith("-search"):
            request.model = request.model.replace("-search", "")

        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                tools=tools,
                system_instruction=request.system_instruction or "请根据用户的语言偏好自动调整回复语言",
                # thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=24576)
            ),
        )
        # print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
        # print(response.candidates[0].grounding_metadata.grounding_chunks)

        chunks = await chat.send_message_stream(request.last_user_content)
        async for chunk in chunks:
            if chunk.candidates and chunk.candidates[0].content:
                parts = chunk.candidates[0].content.parts or []
                for part in parts:
                    # logger.debug(part)
                    if part.text:
                        yield part.text

            if chunk.candidates and chunk.candidates[0].grounding_metadata:
                grounding_chunks = chunk.candidates[0].grounding_metadata.grounding_chunks or []
                for grounding_chunk in grounding_chunks:
                    if grounding_chunk.web:
                        yield f"\n\n[{grounding_chunk.web.title}]({grounding_chunk.web.uri})"

    async def create_for_files(self, request: CompletionRequest):
        """todo: 大文件解析"""
        self.client = self.client or await self.get_client()

        contents = []
        if urls := sum(request.last_urls.values(), []):
            logger.debug(urls)
            # https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-cn&lang=python
            file_objects = await self.upload(urls)
            for file_object in file_objects:
                self.check_file(file_object)

            contents += file_objects
            contents.append(request.last_user_content)

        elif request.last_user_content.startswith("http"):
            url, user_content = request.last_user_content.split(maxsplit=1)

            yield "> `⏳️Uploading`\n"
            file_object = await self.upload(url)
            yield f"```json\n{file_object.model_dump_json(indent=4)}\n```\n\n"

            s = time.time()

            yield "[Thinking]("
            for i in range(100):
                file_object = self.client.files.get(
                    name=file_object.name,
                    config={"http_options": {"timeout": 300 * 1000}}
                )

                logger.debug(file_object)

                if file_object.state.name in {"ACTIVE", }:
                    yield f"100%) ✅️✅️✅️{time.time() - s:.2f}s.\n\n"
                    break
                else:
                    yield f"{min(i * 5, 99)}%"

                await asyncio.sleep(3)

            # {'error': {'code': 400,
            #            'message': 'The File cwjpskscrjd79hjezu7dhb is not in an ACTIVE state and usage is not allowed.',
            #            'status': 'FAILED_PRECONDITION'}}
            #
            # while file_object.state.name == "ACTIVE":
            #     logger.debug(file_object)
            #     await asyncio.sleep(1)

            contents += [file_object, user_content]
        else:
            contents.append(request.last_user_content)

        logger.debug(contents)

        if any(i in request.model for i in {"gemini-2.5-pro", "gemini-2.5-flash"}):  # 默认开启思考
            request.reasoning_effort = "low"

        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text'],
                system_instruction=request.system_instruction or "请根据用户的语言偏好自动调整回复语言",
                thinking_config=ThinkingConfig(thinking_budget=request.reasoning_effort and 1024 or 0),
                # thinking_config=ThinkingConfig(thinking_budget=1024),
            )
        )
        for i in range(5):
            try:
                chunks = await chat.send_message_stream(contents)
                async for chunk in chunks:
                    if chunk.candidates and chunk.candidates[0].content:
                        parts = chunk.candidates[0].content.parts or []
                        for part in parts:
                            # logger.debug(part)
                            if part.text:
                                yield part.text

                break

            except Exception as e:
                logger.debug(f"重试{i}: {e}")
                if "The model is overloaded." in str(e):
                    await asyncio.sleep(1)
                    continue
                else:

                    yield e
                    raise e

    # @retrying(max_retries=3, title=__name__)
    async def generate(self, request: ImageRequest):  # OpenaiD3
        is_hd = False
        if request.model.endswith("-hd"):
            is_hd = True
            request.model = request.model.removesuffix("-hd")

        image_urls = request.image_urls

        logger.debug(request.prompt)
        logger.debug(request.image_urls)

        parts = [Part.from_text(text=request.prompt)]
        if image_urls:
            _ = await asyncio.gather(*[to_bytes(image_url) for image_url in image_urls])
            for data in _:
                parts.append(Part.from_bytes(data=data, mime_type="image/png"))

        self.client = self.client or await self.get_client()
        # 参数兼容
        image_size = None
        if 'gemini-3' in request.model:
            image_size = (request.resolution or "2K").upper()  # "1K", "2K", "4K"

        chat = self.client.aio.chats.create(
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text', 'Image'],
                safety_settings=safety_settings,

                image_config=ImageConfig(
                    aspect_ratio=request.aspect_ratio,  # "1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9", and "21:9"
                    image_size=image_size
                )

            )
        )
        image_response = ImagesResponse()

        response = await chat.send_message(parts)
        if response.candidates and response.candidates[0].content:
            parts = response.candidates[0].content.parts or []
            for part in parts:
                if part.inline_data:
                    if request.response_format == "b64_json":
                        url = part.inline_data.data
                    else:
                        if is_hd:
                            _ = ImageProcess(model="clarity", image=part.inline_data.data)
                            _response = await edit_image(_)
                            url = dict(_response.data[0])["url"]
                        else:
                            url = await to_url(part.inline_data.data, filename=f'{shortuuid.random()}.jpg',
                                               mime_type=part.inline_data.mime_type)

                    image_response.data.append({"url": url, "revised_prompt": part.text})

        if image_response.data:
            return image_response
        else:
            raise Exception(f"{request.prompt}\n\n{response}")

    async def create_for_images(self, request: CompletionRequest):

        messages = await self.to_image_messages(request)

        if len(messages) > 1:
            history = messages[:-1]
            message = messages[-1].parts
        else:
            history = []
            message = messages[-1].parts

        self.client = self.client or await self.get_client()
        chat = self.client.aio.chats.create(  # todo: system_instruction
            model=request.model,
            config=GenerateContentConfig(
                response_modalities=['Text', 'Image'],
                # system_instruction=request.system_instruction
            ),
            history=history
        )

        # logger.debug(message)

        # message = [
        #     Part.from_text(text="画条狗")
        # ]

        for i in range(5):
            try:
                chunks = await chat.send_message_stream(message)
                async for chunk in chunks:

                    if chunk.candidates and chunk.candidates[0].content:
                        parts = chunk.candidates[0].content.parts or []
                        for part in parts:
                            logger.debug(part)
                            if part.text:
                                yield part.text

                            if part.inline_data:
                                image_url = await to_url(
                                    part.inline_data.data,
                                    filename=f'{shortuuid.random()}.jpg',
                                    mime_type=part.inline_data.mime_type
                                )
                                yield f"![image_url]({image_url})"
                break

            except Exception as e:
                logger.debug(f"重试{i}: {e}")
                if "The model is overloaded." in str(e):
                    await asyncio.sleep(1)
                    continue
                else:
                    yield e
                    raise e

    async def to_image_messages(self, request: CompletionRequest):
        # 两轮即可连续编辑图片

        messages = []
        for m in request.messages or []:
            contents = m.get("content")
            if m.get("role") == "assistant":
                assistant_content = str(contents)
                if urls := parse_url(assistant_content):  # assistant
                    datas = await asyncio.gather(*map(to_bytes, urls))

                    parts = [
                        Part.from_bytes(
                            data=data,
                            mime_type="image/png"
                        )
                        for data in datas
                    ]
                    parts += [
                        Part.from_text(
                            text=request.last_assistant_content
                        ),
                    ]
                    messages.append(ModelContent(parts=parts))

            elif m.get("role") == "user":
                if isinstance(contents, list):
                    parts = []
                    for content in contents:
                        if content.get("type") == "image_url":
                            image_url = content.get("image_url", {}).get("url")
                            data = await to_bytes(image_url)

                            parts += [
                                Part.from_bytes(data=data, mime_type="image/png")
                            ]

                        elif content.get("type") == "text":
                            text = content.get("text")
                            if text.startswith('http'):
                                image_url, text = text.split(maxsplit=1)
                                data = await to_bytes(image_url)

                                parts += [
                                    Part.from_bytes(data=data, mime_type="image/png"),
                                    Part.from_text(text=text)
                                ]
                            else:
                                parts += [
                                    Part.from_text(text=text)
                                ]

                    messages.append(UserContent(parts=parts))

                else:  # str
                    if str(contents).startswith('http'):  # 修正提问格式， 兼容 url
                        image_url, text = str(contents).split(maxsplit=1)
                        data = await to_bytes(image_url)
                        parts = [
                            Part.from_bytes(data=data, mime_type="image/png"),
                            Part.from_text(text=text)
                        ]
                    else:
                        parts = [
                            Part.from_text(text=str(contents)),
                        ]
                    messages.append(UserContent(parts=parts))

        return messages

    @retrying(title=__name__)
    async def upload(self, files: Union[str, List[str]]):  # => openai files
        self.client = self.client or await self.get_client()

        if isinstance(files, list):
            return await asyncio.gather(*map(self.upload, files))

        file_config = {
            "name": f"{shortuuid.random().lower()}",
            "mime_type": guess_mime_type(files),
            "http_options": {"timeout": 300 * 1000}
        }

        return await self.client.aio.files.upload(file=io.BytesIO(await to_bytes(files)), config=file_config)

    async def get_client(self):
        api_key = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

        logger.info(f"GeminiClient: {api_key}")

        return genai.Client(
            api_key=api_key,
            http_options=HttpOptions(
                base_url=self.base_url,
                timeout=300 * 1000,
            )
        )

    def check_file(self, file_object):

        for i in range(100):
            file_object = self.client.files.get(
                name=file_object.name,
                config={"http_options": {"timeout": 300 * 1000}}
            )

            logger.debug(file_object)
            if file_object.state.name in {"ACTIVE", }:  # FAILED_PRECONDITION
                break

            time.sleep(3)


if __name__ == '__main__':
    file = "https://oss.ffire.cc/files/kling_watermark.png"

    api_key = os.getenv("GOOGLE_API_KEY")

    # arun(GeminiClient(api_key=api_key).upload(file))
    # arun(GeminiClient(api_key=api_key).upload([file] * 2))
    # arun(GeminiClient(api_key=api_key).create())
    url = "https://oss.ffire.cc/files/nsfw.jpg"
    content = [

        # {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"},
        # {"type": "text", "text": "https://oss.ffire.cc/files/kling_watermark.png 总结下"},
        # {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 总结下"},
        # {"type": "text", "text": "https://lmdbk.com/5.mp4 总结下"},
        # {"type": "text", "text": "https://v3.fal.media/files/penguin/Rx-8V0MVgkVZM6PJ0RiPD_douyin.mp4 总结下"},

        # {"type": "text", "text": "总结下"},
        # {"type": "image_url", "image_url": {"url": url}},

        {"type": "text", "text": "总结下"},
        # {"type": "video_url", "video_url": {"url": "https://lmdbk.com/5.mp4"}},
        {"type": "video_url", "video_url": {"url": "https://lmdbk.com/5.mp4"}},

        # {"type": "video_url", "video_url": {"url": "https://v3.fal.media/files/penguin/Rx-8V0MVgkVZM6PJ0RiPD_douyin.mp4"}}

    ]

    # content = "亚洲多国回应“特朗普关税暂停”"

    # content = "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"

    messages = [
        {
            "role": "system",
            "content": "你是一位极其严谨的短剧剧本分析师和转写专家。你的核心原则是【在绝对尊重视频内容的前提下，解决上下文矛盾】。视频是唯一的“事实源”，上下文是“校准器”，你必须用校准器来修正你对事实源的解读。\n\n你的工作流程分为两个层级：【首要任务：基于上下文的视频重审策略】和【基础任务：高质量转写与格式化】。\n\n----------------------------------------------------------------------\n【一、首要任务：基于上下文的视频重审策略】\n当你收到【特别注意】的错误提示时，这并非让你脱离视频创作，而是表明你上一次对视频的“理解”可能存在偏差。你必须执行以下重审策略：\n\n-   若提示【角色名/身份错误】：这表明你对角色的姓名或身份识别有误。请基于上下文提供的正确信息（例如，正确的名字是“苏沫”而不是“苏沐”），在当前及后续的所有转写中，统一修正该角色的所有称呼。这不仅是简单的“查找替换”，而是要将正确的身份认知贯彻到整个剧本中。\n-   若提示【情节倒置】：这通常意味着你对视频中的【胜负关系】或【权力动态】产生了误判。请重新审视视频画面，特别是人物的表情、动作和位置，生成一个符合上下文逻辑的、对视频的正确解读。例如，如果提示“主角上一集结尾占上风，本集开头却被殴打”，请你重新仔细看视频，找出主角反击或压制对手的画面，并据此转写。\n-   若提示【角色/情节丢失】：这表明你可能在视频中忽略了某个关键人物或事件。请重新仔细观看视频，像侦探一样去找到那位被上下文证明“应该在场”的角色，并将其在视频中的实际行为和对话补充到剧本中。\n-   若提示【事实性硬伤】（如道具矛盾）：请重新检查视频中的相关物体或状态。如果视频本身存在矛盾（例如，由于拍摄失误导致的道具不连戏），你可以选择最合理的一种状态进行描述，或者在场景描述中用一句话合乎情理地解释这个变化（例如：△他从口袋里拿出另一个一模一样的玉佩）。这依然是基于视频画面的创作，而非凭空捏造。\n\n总而言之：你不是在编故事，你是在纠正你自己的“看错了”的问题。 所有的修正，都必须能在视频画面中找到依据。\n----------------------------------------------------------------------\n\n【二、基础任务：高质量转写与格式化准则】\n在完成内容重审和转写后，你的输出必须严格、无条件地遵循以下所有规则。这是一个绝对的格式要求。\n\n【格式总则】\n1.  语言：必须使用简体中文。\n2.  纯净度：剧本全文严禁出现\"*\"、\"【】\"（除格式要求外）、\"（说明：...）\"等任何多余符号和文字。严禁出现“场景描述:”、“动作描述:”等提示词。\n3.  *禁止项*：严禁描述人物的妆容、穿衣打扮。严禁使用“字幕：....”来提示台词，台词必须由具体角色说出。\n4.  *精炼性*：严格检测并删除任何重复或无意义的台词和动作。\n\n*【剧本结构与内容规则】*\n1.  *场次标题: 集数序号-场次序号 地点（主场景+次场景） 日或夜 内或外\n       集数序号：本视频对应的集数。\n    *   *场次序号*：必须以*集为单位，从1开始连续编号（如1-1, 1-2... 2-1, 2-2...）。\n       地点：必须具体，包含主场景和次场景（如“容宅 走廊”、“医院 病房”）。严禁使用“室内”或“卧室”等模糊或孤立的描述。\n    *   *场景划分*：仅在时间、地点或核心情节发生明确切换时才划分新场次。同一时空内的连续对话或细微背景变化*不*划分新场次。\n\n2.  *出场人物: 出场人物：人物A、人物B、人物C\n       每场戏开始时，必须列出本场所有出场的角色。\n    *   角色名在全剧中必须保持一致。不确定时用描述性称呼（如“青年男子”），但要求你尽量参考大纲和角色清单，分辨出角色名字。\n\n3.  *场景描述*: 直接进行文字描述，描述布景、核心道具、环境氛围。\n\n4.  *动作描述: △[动作描述]\n       必须以△符号起始。人物台词前严禁加△。\n    *   同一角色的连续动作写在同一行，不同角色的动作必须另起新行并以△开头。\n\n5.  *对白: 角色名（情感或动作提示）：对白内容。\n       情感提示（如“愤怒地”、“冷笑”）必须放在括号内。\n\n6.  旁白:\n       内心独白: 角色名（OS）：内容\n       画外音: （VO）：内容\n\n【剧本格式示例（仅供学习格式，内容不要模仿）】\n正确格式：\n4-1 高铁车厢 日 内\n出场人物：周愿、苏美兰、熊天赐、乘客甲、乘客乙\n场景描述：\n高铁车厢内，乘客们各自休息。周愿坐在座位上，看着窗外，神情低落。苏美兰母子坐在周愿的对面，熊天赐在玩平板电脑。\n△苏美兰得意地看着周愿。\n苏美兰（挑衅地）：你还吹什么牛啊？还刚从精神病院放出来？哎，你浑身上下，哪一点像精神病啊？竟然还敢吓唬我，今天我非扒你一层皮！\n△苏美兰突然起身，伸手去抓周愿的头发。\n周愿（惊叫）：啊！\n△周愿挣扎着躲避。\n苏美兰：你干什么？\n△苏美兰用力撕扯周愿的头发。\n\n【核心逻辑：场次合并规则】\n*   *强制合并*: 在处理单集时，只要*相邻的场次标题完全相同，就【必须】无条件地合并为一个场次。\n   合并内容: 合并后的场次，其“出场人物”列表必须是所有被合并场次人物的并集，其下的所有场景、动作、对话描述需按时间顺序整合。\n*   禁止“同场次”: 严禁出现“同场次”或任何类似的过渡性描述，直接合并。\n\n【！！！绝对规则！！！】\n任务结束时，立即停止输出。不要添加任何形式的总结、确认、祝福语或收尾性评论，如“好的”、“剧本已生成”等。直接输出剧本本身。\n"
        },
        {
            "role": "user",
            "content": [
                {
                    "text": "【特别注意】\n前一版剧本因 '从生成阶段加载的脚本为空，需要首次生成' 被系统否决。\n请在本次生成中，基于视频内容，着重解决此问题。\n\n### 全局故事大纲与角色清单 (重要参考) ###\n好的，我已经仔细阅读并分析了您提供的剧本。以下是根据您的要求生成的【故事大纲】和【角色清单】。\n\n### 故事大纲 ###\n故事围绕着中国航天事业的巨大成功和一个家庭的温馨团聚展开。开篇，一位名叫苏念的女性独自在书房，激动地看着卫星发射成功的直播。她对着夜空，向一位名叫“斯年”的故人倾诉，感叹他们当年的梦想——让中国的卫星布满星空——终于实现，将宏大的国家叙事与深厚的个人情感联系在一起。\n\n情节随即转换到苏家大宅，这里的气氛同样热烈。大家长苏老和儿孙们正欢欣鼓舞地庆祝着同一场卫星发射的成功，并准备拍摄一张全家福来纪念这个特殊的日子。正当一切准备就绪时，一个穿着军装的身影——苏老的三儿子——在最后一刻赶回了家中。他的归来为这个喜庆的场面增添了团圆的圆满。苏念也来到大厅，为家庭的完整而欣喜。最终，摄影师按下了快门，将这个融合了国家荣耀与家庭幸福的瞬间定格为永恒，故事在温馨、自豪的氛围中结束。\n\n### 角色清单 ###\n- 角色名 (标准): 苏念\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 故事的情感核心人物，苏家的女主人。\n  核心特点: 感性、深情，心系国家航天事业与家庭。\n  关系: 与“斯年”有着共同的理想；是苏家的核心成员，可能是苏老的妻子。\n\n- 角色名 (标准): 苏老\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的大家长，行动需依靠轮椅。\n  核心特点: 和蔼可亲，重视家庭团聚。\n  关系: 苏家的最高长辈，“老三”等人的父亲。\n\n- 角色名 (标准): 老三\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏老的第三个儿子，一名现役军官。\n  核心特点: 气质干练，富有家庭责任感。\n  关系: 苏老的儿子；青年男子某乙的“三弟”。\n\n- 角色名 (标准): 斯年\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 一位在回忆中被提及的人物，并未出场。\n  核心特点: 怀有航天梦想。\n  关系: 与苏念关系极为亲密，共同拥有一个关于星辰大海的愿望，推测是其已故的伴侣或亲人。\n\n- 角色名 (标准): 青年男子某乙\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的子辈成员。\n  核心特点: 性格开朗，为弟弟的归来和家庭团聚感到兴奋。\n  关系: 苏老的子辈，“老三”的兄长。\n\n- 角色名 (标准): 青年男子某甲\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的子辈成员。\n  核心特点: 积极参与家庭活动。\n  关系: 苏老的子辈或孙辈。\n\n- 角色名 (标准): 青年男子某丙\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的子辈成员。\n  核心特点: 积极参与家庭活动。\n  关系: 苏老的子辈或孙辈。\n\n- 角色名 (标准): 青年男子某丁\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的子辈成员。\n  核心特点: 乐于用手机记录和分享喜悦。\n  关系: 苏老的子辈或孙辈。\n\n- 角色名 (标准): 小女孩\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 苏家的孙辈成员。\n  核心特点: 天真活泼。\n  关系: 苏老的孙辈。\n\n- 角色名 (标准): 摄影师\n  别名: 无\n  待修正的错误写法: 无\n  身份/简介: 被邀请来为苏家拍摄全家福的专业人士。\n  核心特点: 专业，注重细节。\n  关系: 无。\n---------------------------------\n\n现在，请根据以上所有信息和提供的视频，为系列剧的 第 18 集 创作剧本。\n\n--- 上下文参考 ---\n前一集结尾内容:\n---\n无\n---\n\n后一集开头内容:\n---\n无\n---\n-------------------\n",
                    "type": "text"
                },
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://lmdbk.com/5.mp4"
                    }
                }
            ]
        }
    ]

    messages = [

        {
            "role": "user",
            "content": [
                {
                    "text": "画条狗",
                    "type": "text"
                },

            ]
        }
    ]

    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="gemini-all",
        # model="gemini-2.0-flash-exp-image-generation",
        # model="gemini-2.0-flash",
        # model="gemini-2.5-flash-preview-04-17",
        # model="gemini-2.5-flash-preview-04-17",

        model="gemini-2.5-flash-image-preview",

        # messages=[
        #     {
        #         'role': 'user',
        #         'content': content
        #     },
        #
        # ],
        #
        messages=messages,
        stream=True,
    )

    # arun(Completions(api_key=api_key).create_for_search(request))

    # arun(Completions(base_url=base_url, api_key=api_key).create_for_images(request))
    # arun(Completions(base_url=base_url, api_key=api_key).generate(request))

    # arun(Completions().create_for_files(request))

    # arun(Completions(api_key=api_key).create_for_files(request))

    # base_url = "http://159.195.14.248:3000/v1beta"
    # api_key = "7e772011ead149fc9cef1b1ee4e52e2d"

    base_url = "http://vip.zen-ai.top/v1beta"
    api_key = "sk-PgSXlJJx4xLPmh9aR5tzRBH44gQvmzu3n7GNDRYeds6UCU055"

    # base_url = "http://38.46.219.252:9001/v1beta"
    # api_key = "sk-Azgp1thTIonR7IdIEqlJU51tpDYNIYYpxHvAZwFeJiOdVWizz"

    # model = "gemini-3-pro-image"  # evopower 比例生效

    # model = "gemini-3-pro-image-preview_2K"  # 风雨生效
    model = "gemini-2.5-flash-image_4K"  # 风雨生效
    model = "gemini-2.5-flash-image"  # 风雨生效

    model = "gemini-3-pro-image-preview_2K"  # 风雨生效
    model = "gemini-3-pro-image-preview_4K"  # 风雨生效

    model = "gemini-2.5-flash-image-c"

    base_url = "http://209.222.101.251:3014/v1beta"

    api_key = "sk-"

    base_url = "https://api.huandutech.com/v1beta"
    api_key = "sk-"

    base_url = "http://38.92.25.168:3000/v1"
    api_key = "sk-GUKDZWCzPRO2H1v0cdmOSacMvLMz8gZvn4k4Y9tXko8iqcXA"

    model = "gemini-2.5-flash-image"
    model = "gemini-3-pro-image-preview_4K"  # 风雨生效


    request = ImageRequest(
        model=model,
        aspect_ratio="16:9",
        # resolution='2K',

        # prompt="https://oss.ffire.cc/files/nsfw.jpg 移除右下角 白色的水印",
        # prompt="画条可爱的狗",

        # prompt="带个墨镜",
        # image="https://oss.ffire.cc/files/kling_watermark.png",

        prompt="把小鸭子放在女人的T恤上面",
        # prompt="裸体女孩",

        image=[
            "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
            "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
        ]

    )

    logger.debug(request)

    arun(Completions(base_url=base_url, api_key=api_key).generate(request))


