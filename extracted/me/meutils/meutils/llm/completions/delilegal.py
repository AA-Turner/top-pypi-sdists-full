#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : delilegal
# @Time         : 2024/9/20 17:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.pandas_utils import to_html_plus

from meutils.notice.feishu import send_message as _send_message
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling

from meutils.llm.utils import oneturn2multiturn
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage
from meutils.schemas.oneapi import REDIRECT_MODEL

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)

BASE_URL = "https://www.delilegal.com"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=DtiUmU"


async def check_token(token: Optional[str] = None):
    headers = {
        "authorization": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.get("/ai/api/v1/gptIm/getLimitUser")

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            return response.json()['body']  #####


@alru_cache(ttl=3600)
@retrying(predicate=lambda r: r is None)
async def create_session(token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    headers = {
        "authorization": token
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/ai/api/v1/gptIm/createSession")

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            return response.json()["body"]["sessionId"]


async def create(request: ChatCompletionRequest, token: Optional[str] = None, answer_again: bool = False):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)

    sessionId = await create_session(token)

    headers = {
        "authorization": token,
    }
    payload = {
        "sessionId": sessionId,
        "question": request.last_content,
        # "question": oneturn2multiturn(request.messages),

        "answerAgain": answer_again,
        "qaId": "",
        "tabType": "lawQa" if 'viewpoint' not in request.model else "viewpointQa"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        async with client.stream("POST", "/ai/api/v1/gptIm/sendGptMessageStreamV3", json=payload) as response:
            yield "\n"  # 提升首字速度

            logger.debug(response.status_code)
            # logger.debug(response.text)

            _chunk = ""
            async for chunk in response.aiter_lines():
                if (chunk := chunk.strip("data:")) and chunk.startswith("{"):
                    # logger.debug(chunk)
                    try:
                        chunk = json.loads(chunk)
                        data = chunk.get("data", {})
                        chunk = data.get("lawQaText", "") or data.get("viewpointQaText", "")

                        for i in ["lawQaRelatedLaws", "lawQaRelatedCases", "viewpointQaRelatedArticles"]:
                            if data.get(i):
                                chunk = ""  # 最好不返回
                                df = pd.DataFrame(data[i])
                                filename = to_html_plus(
                                    df,
                                    title=i,
                                    subtitle="ChatfireLaw",
                                    return_filename=True
                                )
                                yield f"\n\n[{i}](https://api.chatfire.cn/render/{filename})"

                        yield chunk.replace(_chunk, "")
                        _chunk = chunk
                    except Exception as e:
                        _ = f"{e}\n{chunk}"
                        logger.error(_)
                        send_message(_)
                        yield ""
                # else:
                #     logger.debug(chunk)


if __name__ == '__main__':
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmbm9wc3J6eHFvY3V2Y2ZtY3BwZGNpcW54eWFzY25sYSIsIm5iZiI6MTcyNjgyMzgyNCwiZXhwIjoxNzI3NDI4NjI0LCJpYXQiOjE3MjY4MjM4MjQsImp0aSI6IlppbERZaElKZXF4RFRncnMifQ.tbx8XW9sEOz1bY-c0JrKMJBd3mAoTBRXhvGIotmPiR4"

    # arun(create_session(token))
    # arun(check_token(token))

    model = "viewpointQaText"
    model = ""

    request = ChatCompletionRequest(model=model, messages=[
        {'role': 'user',
         'content': '客人吃出苍蝇超出十倍的赔偿怎么办?\n\n先给出准确答案➕原因理由➕再法律依据➕再相关延伸'}
    ])

    arun(create(request))
