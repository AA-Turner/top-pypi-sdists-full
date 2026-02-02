#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : yuanbao
# @Time         : 2024/6/11 18:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from aiostream import stream

from meutils.pipe import *
from meutils.io.image import image2nowatermark_image

from meutils.llm.utils import oneturn2multiturn
from meutils.schemas.openai_types import CompletionRequest
from meutils.schemas.image_types import HunyuanImageRequest

from meutils.schemas.yuanbao_types import FEISHU_URL, SSEData, YUANBAO_BASE_URL, API_CHAT, API_GENERATE_ID, \
    API_DELETE_CONV, \
    GET_AGENT_CHAT
from meutils.config_utils.lark_utils import get_next_token_for_polling, aget_spreadsheet_values


# import rev_HunYuan


class Completions(object):

    @classmethod
    async def generate(cls, request: HunyuanImageRequest):
        response = cls().create(image_request=request)
        urls = await stream.list(response)
        urls = await asyncio.gather(*map(image2nowatermark_image, urls))

        return {
            "data": [{"url": url} for url in urls]
        }

    async def create(
            self,
            request: Optional[CompletionRequest] = None,
            image_request: Optional[HunyuanImageRequest] = None,
            token: Optional[str] = None
    ):
        token = token or await get_next_token_for_polling(FEISHU_URL, check_token=check_token)

        logger.debug(token)

        prompt = request and oneturn2multiturn(request.messages) or (image_request and image_request.prompt)

        if isinstance(prompt, list):
            prompt = prompt[-1].get("text", "")  # [{'type': 'text', 'text': 'hi'}]

        payload = {
            "model": "gpt_175B_0404",
            "chatModelId": request.model,
            "version": "v2",
            "supportHint": 2,  # 1

            "prompt": prompt,
            # "displayPrompt": "画条可爱的狗狗",
            # "displayPromptType": 1,
            "multimedia": [],
            # "agentId": "gtcnTp5C1G",

            "plugin": "Adaptive",

            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True,
                    "userIntention": {
                        "resolution": "1280x1280",
                    }
                }
            },

        }
        if "search" in request.model:
            # deep_seek deep_seek_v3 hunyuan_t1 hunyuan_gpt_175B_0404
            payload['chatModelId'] = request.model.replace('-search', '')
            payload['supportFunctions'] = ["supportInternetSearch"]

        if image_request:
            payload["displayImageIntentionLabels"] = [
                {"type": "resolution", "disPlayValue": "超清", "startIndex": 0, "endIndex": 1}
            ]
            payload["options"]["imageIntention"]["userIntention"].update(
                {
                    "style": image_request.style,

                    "scale": image_request.size,

                    # todo: 默认四张 不生效
                    # "N": image_request.n,
                    # "num": image_request.n,
                    # "Count": image_request.n,

                }
            )

        # logger.debug(bjson(payload))
        headers = {
            'cookie': token
        }
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=300) as client:
            # chatid = (await client.post(API_GENERATE_ID)).text
            chatid = uuid.uuid4()
            # https://yuanbao.tencent.com/api/chat/90802631-22dc-4d5d-9d3f-f27f57d5fec8'
            async with client.stream(method="POST", url=f"{API_CHAT}/{chatid}", json=payload) as response:
                logger.debug(response.status_code)
                response.raise_for_status()

                references = []
                reasoning = "<think>\n"  # </think>
                async for chunk in response.aiter_lines():
                    sse = SSEData(chunk=chunk)
                    if image_request and sse.image:
                        logger.debug(sse.image)
                        yield sse.image

                    if request:
                        if sse.reasoning_content:
                            yield reasoning
                            yield sse.reasoning_content
                            reasoning = ""
                        elif sse.content and reasoning == "":
                            reasoning = "\n</think>"
                            yield reasoning

                        if sse.search_content:
                            # references
                            df = pd.DataFrame(sse.search_content).fillna('')
                            df['icon'] = "![" + df['sourceName'] + "](" + df['icon_url'] + ")"
                            df['web_site_name'] = df['icon'] + df['web_site_name'] + ": "
                            df['title'] = df['web_site_name'] + "[" + df['title'] + "](" + df['url'] + ")"

                            for i, ref in enumerate(df['title'], 1):
                                references.append(f"[^{i}]: {ref}\n")
                        if sse.content:
                            yield sse.content

                            # logger.debug(sse.content)
                if references:
                    yield '\n\n'
                    for ref in references:
                        yield ref

    def generate_id(self, random: bool = True):
        if random:
            return f'{uuid.uuid4()}'
        return httpx.post(API_GENERATE_ID).text

    def delete_conv(self, chatid):
        response = httpx.post(f"{API_DELETE_CONV}/{chatid}")
        return response.status_code == 200


async def check_token(token):
    headers = {
        "cookie": token
    }
    try:
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=10) as client:
            response = await client.get("/api/info/general")
            response.raise_for_status()
            logger.debug(response.status_code)
            return True
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    # chatid = generate_id()
    # print(chatid)
    # print(delete_conv(chatid))
    # payload = {
    #     # "model": "gpt_175B_0404",
    #     # "prompt": "1+1",
    #     "prompt": "错了",
    #
    #     # "plugin": "Adaptive",
    #     # "displayPrompt": "1+1",
    #     # "displayPromptType": 1,
    #     # "options": {},
    #     # "multimedia": [],
    #     # "agentId": "naQivTmsDa",
    #     # "version": "v2"
    # }
    # chat(payload)

    # async2sync_generator(Completions(api_key).achat('画条狗')) | xprint
    # request = HunyuanImageRequest(prompt='画条狗', size='16:9')
    # deep_seek deep_seek_v3 hunyuan_t1 hunyuan_gpt_175B_0404
    # model = 'deep_seek_v3-search'
    # model = 'deep_seek-search'
    model = 'deep_seek'
    model = 'hunyuan_t1'
    # model = 'hunyuan_t1-search'
    # model = 'deep_seek-search'
    


    arun(Completions().create(
        CompletionRequest(
            model=model,
            messages=[{'role': 'user', 'content': '南京天气如何'}],
            stream=True
        ),
        # image_request=request,
        # token=token
    ))
    # arun(Completions.generate(request))

    # df = arun(aget_spreadsheet_values(feishu_url=FEISHU__URL, to_dataframe=True))
    #
    # for i in df[0]:
    #     if not arun(check_token(i)):
    #         print(i)
    #

    # token="""_ga_RPMZTEBERQ=GS2.1.s1750752972$o9$g1$t1750752995$j37$l0$h0;_qimei_q36=;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%223133038818%22%2C%22first_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%2C%22%24search_keyword_id%22%3A%22c8f5e19c000022920000000268799a56%22%2C%22%24search_keyword_id_type%22%3A%22baidu_seo_keyword_id%22%2C%22%24search_keyword_id_hash%22%3A4558975629240447%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE5OGM3YjJkNTItMGZjY2E4ZDczMWNiOWI4LTE4NTI1NjM3LTIwNzM2MDAtMTkxYjE5OGM3YjMxZmQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzEzMzAzODgxOCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223133038818%22%7D%2C%22%24device_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%7D;_qimei_i_3=4dfa758b920b50d2c9c5fe365ad77ae6f6bda2a2135d578ab5dc280d219a713a676061973989e285d096;_ga=GA1.2.981511920.1725261466;qcloud_from=qcloud.baidu.seo-1752799836749;web_uid=ac283ec7-4bf6-40c9-a0ce-5a2e0cd7db06;_gcl_au=1.1.295860038.1750044382;_qimei_i_1=53c92ed79c5c53d997c6a830538677e2f7bdf0f51209518bb38e2f582593206c616336913980e4ddd6f3eec5;hy_source=web;_qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba;_qimei_h38=e9632faf082420cd40bb971703000001419610;_qimei_uuid42=18c0310102d1002a082420cd40bb9717523c3c7e12;hy_token=8tE8bq6InCxff5mUqQZfc9aGHP6NPD80Cr/k258SiLJ0SRKVmpnUylkLLyDfCVTF9ODHgBEHyOLIcel29d1mX0kymysiIaZYSDr6Xzq5lVMpsKUcFcSvEUaC7i7OWJLxaG2UHBpv1r6rzNJ1AK/vdJB/JgR+VfBuyHcBAhZvFjI+SK5/XXKJHVlQUSk0sDcCKUoLec4xWHnRXFsGT+xcy8LTSuM0rD2AtdD1SIHpuk4H5mCnFHzFJZki+Zm2BLnGRhOqCEjD1GTT1fh8a5H2aGRG1wLSdZEkxtUN2JfwC9005MvGjklEVpb+Vjuhkj8yxQveWM38lQ6s+4eZ5RXM4RBvjWe/IcVXqbSEhkLFKaHED/pVIxDXgjRWJhcRXo36w5VWzc7XO6/qJRouVj6/VpHFNYBtaIR25SC3itS138QdEo5EDEHQtGap/R0jxaiPKSqnDQ70Uzwd4ORrdBE31eCQqK1oyiG5KmPFj4azXTJKn+VejoUJxBBXqMPMtsv+b9e8Plh2dpW3vNepa9nMOQ9gJVynX6KJdgMKP4Ea5W1UOuUW8P/MHR787PpxwyRRz6D7ZDs2RhSvNvmCJzG6Cw==;hy_user=1bc4978e537649caae881f86ba807bca"""
    # arun(check_token(token))
