#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : luma
# @Time         : 2024/7/22 11:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.luma_types import BASE_URL, LumaRequest, EXAMPLES
from meutils.schemas.task_types import Task

from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=RsoADK"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


def refresh_token():
    import requests

    url = "https://lumalabs.ai/?_rsc=1ovtp"

    payload = {}
    headers = {
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'Cookie': '_clck=1pg7ir3%7C2%7Cfno%7C0%7C1664; _ga=GA1.1.708578083.1721630345; luma_session=SkMABQUEQBc6TA4PUVoaD0ERUEsvDFFxUFl6Cyl4Zk14UC8PLxJ6CjcNAid9AnFeEWtjcS9dHVNKek8GNHhaeF8SCAI-L18HCQFQAGNYU3wLXFxrMQdKe2R2WDsZaEduZQUKKA9RAykycgwoYFxQbyVQQXwyMll7d2JYLydaSm4DNwwvDxZaPVdAET5jAQhtU19eew8URlJkSEYEMEZabWkJFi8MDksqH3EZKl55QXgLWE9UNEpJBVVUUS5XdV5RegsSAlNWWA5UUVQJRkMVAjd3dnhUVQFsA15xDSUBVkJaQ01GRBNWAhddEgxrQFdeBF0XCEVGVk95WFclAFh8XnsoNBwvUH0NLEsoCmYBW3YoBXxZFTxldXkJGwcae0lTZigIKQgSWgA9dg0HWA0JUTZfXnsPC1pvZ1NMLzR3Xm5LOBU_MgVYKgwIUSljflV5NVtdaCEHR3hkZl8vJ2NeenUKGD9UN14tDE8IPQZMSG82BgVqVwhYf1lAQAY0SUBRYhYIPD4JRC0PVxkqTn1BeAt-BH8PD0lQYh5wDjNXR050BVFfAgJ3MA5sJAZCZ0tWFmV9XQkqC0JRRGM4FWFabn47CFYzQx9ER1sNDVFaTGoIVxcIRQpGWl9N; _clsk=k5j7yi%7C1721631686971%7C7%7C0%7Cw.clarity.ms%2Fcollect; _ga_67JX7C10DX=GS1.1.1721630344.1.1.1721631758.0.0.0',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    #
    # print(response.cookies)
    # print(response.cookies.values())
    # print(response.headers)
    #
    # print(response.text)


@retrying(max_retries=6, predicate=lambda r: not r)
async def create_task(request: Union[dict, LumaRequest], token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)
    logger.debug(token)

    headers = {
        'Cookie': token,
    }

    payload = request if isinstance(request, dict) else request.model_dump(exclude_none=True)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/generations/", json=payload)
        # [
        #     {
        #         "id": "82507194-91c0-4fe3-ad12-f459acbcf3a5",
        #         "prompt": "清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K",
        #         "state": "pending",
        #         "created_at": "2024-07-22T05:26:20.871974Z",
        #         "video": null,
        #         "liked": null,
        #         "estimate_wait_seconds": null,
        #         "thumbnail": null,
        #         "last_frame": null
        #     }
        # ]

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            data = response.json()
            send_message(bjson(data))
            data = data[0]

            return Task(id=data.get("id"), data=data, system_fingerprint=token)

        response.raise_for_status()


# @retrying(predicate=lambda r: not r)  # 触发重试
# @retrying()  # 触发重试
async def get_task(task_id: str, token: str):  # 1ee02f7b-42df-4926-b034-f56e4c4e2d31

    headers = {
        'Cookie': token,
    }
    params = {
        'offset': 0,
        'limit': 32
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        # response = await client.get(f"/user/generations/", params=params)
        # if response.is_success:
        #     data = response.json()
        #     return list(filter(lambda x: x.get("id") == task_id, data))
        response = await client.get(f"/generations/{task_id}", params=params)

        logger.debug(response.text)
        logger.debug(response.status_code)
        if response.is_success:
            return response.json()

        response.raise_for_status()


if __name__ == '__main__':
    pass
    # cookie = "_clck=1tbe3d1%7C2%7Cfno%7C0%7C1664; _ga=GA1.1.1897085930.1721613998; luma_session=SkMABQUEQBc6TA4PUVoaD0ERUEsvDFFxUFl6Cyl4Zk14UC8PLxJ6CjcNAid9AnFeEWtjcS9dHVNKek8GNHhaeF8SCAI-L18HCQFQAGNYU3wLXFxrMQdKe2R2WDsZaEduZQUKKA9RAykycgwoYFxQbyVQQXwyMll7d2JYLydaSm4DNwwvDxZaPVdAET5jAQhtU19eew8URlJkSEYEMEZabWkJFi8MDksqH3EZKl59C3glWExUNEpccnsHWS8wB3lffhIoLQRTWDYDdwpVGXJ8TS93b3QREFlGRARmASxCAmEFQ01GRBNWAhddEgxrQFdeBF0XCEVGVk95WFclAFh8XnsoNBwvUH0NLEsoCmYBW3YoBXxZFTxldXkJGwcae0lTZigIKQgSWgA9dg0HWA0JUTZfXnsPC1pvZ1NMLzR3Xm5LOBU_MgVYKgwIUSljflV5NVtdaCEHR3hkZl8vJ2NeenUKGD9UN14tDE8IPQZMSG82BgVqVwhYf1lAQAY0SUBRYhYIPD4JRC0PVxkqTn1BeAt-Qn8hD0pQYh5tVTtZYlIDDjlTKAVhNgxJJzMBXwENUB5AcC8NYH1-YQdbAAN9TWMbGAUNQx9ER1sNDVFaTGoIVxcIRQpGWl9N"
    # cookie = "_clck=1tbe3d1%7C2%7Cfno%7C0%7C1664; _ga=GA1.1.1897085930.1721613998; luma_session=SkMABQUEQBc6TA4PUVoaD0ERUEsvDFFxUFl6Cyl4Zk14UC8PLxJ6CjcNAid9AnFeEWtjcS9dHVNKek8GNHhaeF8SCAI-L18HCQFQAGNYU3wLXFxrMQdKe2R2WDsZaEduZQUKKA9RAykycgwoYFxQbyVQQXwyMll7d2JYLydaSm4DNwwvDxZaPVdAET5jAQhtU19eew8URlJkSEYEMEZabWkJFi8MDksqH3EZKl59DHo1dkxUNEpqZVJldgA1WmZ8QxUAIycRchwHcCUmfwEJAwBnAgM1MFp_QXFjKFpHSQV8Q01GRBNWAhddEgxrQFdeBF0XCEVGVk95WFclAFh8XnsoNBwvUH0NLEsoCmYBW3YoBXxZFTxldXkJGwcae0lTZigIKQgSWgA9dg0HWA0JUTZfXnsPC1pvZ1NMLzR3Xm5LOBU_MgVYKgwIUSljflV5NVtdaCEHR3hkZl8vJ2NeenUKGD9UN14tDE8IPQZMSG82BgVqVwhYf1lAQAY0SUBRYhYIPD4JRC0PVxkqTn1BeAt-TX0xIUpQYh5TByJhAn5wODYsCTIHLhB6DFZNUWsYE3sAZB0gBA9ydVInDFZyRGYAUgIrQx9ER1sNDVFaTGoIVxcIRQpGWl9N"
    arun(create_task(EXAMPLES[0]))
    # arun(get_task("6de49fdc-f3ed-4590-8a1a-0c53cfca055b", cookie))
    # print(refresh_token())
