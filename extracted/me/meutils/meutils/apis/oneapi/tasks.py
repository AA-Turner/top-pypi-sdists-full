#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tasks
# @Time         : 2025/7/11 13:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.apis.utils import make_request_httpx
from meutils.apis.oneapi.log import get_logs
from meutils.apis.oneapi.user import update_user_for_refund, get_user

# headers
ACTIONS = {
    # 按量计费的异步任务
    "async": "https://api.chatfire.cn/fal-ai/minimax/requests/{request_id}",  # 目前是fal todo

    "fal": "https://api.chatfire.cn/fal-ai/{model}/requests/{request_id}",

    "doubao": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",
    "jimeng": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",

    "cogvideox": "https://api.chatfire.cn/zhipuai/v1/async-result/{task_id}",

    "minimax": "https://api.chatfire.cn/minimax/v2/async/minimax-hailuo-02",

    "wan": "https://api.chatfire.cn/sf/v1/videos/generations",  # wan-ai-wan2.1-t2v-14b 可能还有其他平台

    "veo3": "https://api.chatfire.cn/veo/v1/videos/generations?id={task_id}",

}


async def get_tasks(platform: str = "flux", action: str = "", status: str = "NOT_START"):
    base_url = "https://api.chatfire.cn"
    path = "/api/task/"
    headers = {
        'authorization': f'Bearer {os.getenv("CHATFIRE_ONEAPI_TOKEN")}',
        'new-api-user': '1',
        'rix-api-user': '1',
    }

    submit_timestamp = int(time.time() - 24 * 3600)
    end_timestamp = int(time.time() - 5 * 60)

    params = {
        "p": 1,
        "page_size": 100,
        "user_id": "",
        "channel_id": "",
        "task_id": "",
        "submit_timestamp": submit_timestamp,
        "end_timestamp": end_timestamp,
        "platform": platform,
        "action": action,
        "status": status
    }
    response = await make_request_httpx(
        base_url=base_url,
        path=path,
        params=params,
        headers=headers
    )
    return response


async def polling_tasks(platform: str = "flux", action: str = "", status: str = "NOT_START"):
    response = await get_tasks(platform, action, status)
    if items := response['data']['items']:
        tasks = []
        model = ''
        for item in items[:8]:  # 批量更新
            task_id = item['task_id']
            action = item['action'].split('-', maxsplit=1)[0]  # 模糊匹配
            if 'fal-' in item['action']:
                model = item['action'].split('-')[1]

            if action not in ACTIONS:
                logger.warning(f"未知任务类型：{action}")
                continue

            url = ACTIONS[action].format(model=model, task_id=task_id, request_id=task_id)

            logger.debug(f"任务类型：{action} {task_id} {url}")

            # if action in {"veo3"}:
            #     logger.debug(task_id)
            #     payload = {"id": task_id, "task_id": task_id}

            # logger.debug(url)

            # task = await make_request_httpx(
            #             base_url=base_url,
            #             path=path
            #         )
            # logger.debug(bjson(task))
            base_url, path = url.rsplit("/", maxsplit=1)
            _ = asyncio.create_task(
                make_request_httpx(
                    base_url=base_url, path=path
                )
            )
            tasks.append(_)
        data = await asyncio.gather(*tasks)
        return data


async def refund_tasks(task_id: Optional[str] = None):  # 只补偿一次
    if task_id is None:
        response = await get_tasks(action="async-task", status="FAILURE")
        if items := response['data']['items']:
            item = items[-1]
            task_id = item['task_id']

    response = await get_logs(task_id, type=2)  # 获取消费日志
    if items := response['data']['items']:
        item = items[-1]

        user_id = item['user_id']
        quota = item['quota']  # 退款金额

        logger.debug(quota)
        logger.debug(await get_user(user_id))

        logger.debug(f"退款金额：{quota / 500000} RMB = {quota}")

        _ = await update_user_for_refund(user_id, quota=quota)  # 管理

        _['refund_quota'] = quota
        return _


if __name__ == '__main__':
    pass
    arun(polling_tasks())
    # arun(get_tasks(action="async-task", status="FAILURE"))
    # arun(refund_tasks())

"""
UPSTREAM_BASE_URL=https://api.ffire.cc
UPSTREAM_API_KEY=

API_KEY=https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=1DCblQ[:200]
BASE_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions



curl -X 'POST' 'http://0.0.0.0:8000/oneapi/channel' \
    -H "Authorization: Bearer $API_KEY" \
    -H "UPSTREAM-BASE-URL: $UPSTREAM_BASE_URL" \
    -H "UPSTREAM-API-KEY: $UPSTREAM_API_KEY" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
      -d '{
        "id": "10000:10100",
        "name": "火山企业",
        "tag": "火山企业",
        "key": "$KEY",
        "type": 8,
        "priority": 999,

        "base_url": "'$BASE_URL'",

        "models": "deepseek-r1-250120,deepseek-r1-250528,doubao-1-5-thinking-vision-pro-250428,doubao-1-5-thinking-pro,doubao-1-5-thinking-pro-250415,doubao-seed-1-6-thinking-250715,doubao-seed-1-6-flash-250715,doubao-seed-1-6-250615,doubao-1-5-pro-32k-250115,doubao-1.5-pro-32k,deepseek-r1-250528,deepseek-r1,deepseek-reasoner,deepseek-v3-250324,deepseek-v3,deepseek-chat,doubao-1-5-ui-tars-250428,doubao-1.5-vision-pro-250328,doubao-1-5-pro-256k-250115,moonshot-v1-8k,moonshot-v1-32k,moonshot-v1-128k",
        "group": "default,volc,volcengine",
        
        "status_code_mapping": "{\n  \"429\": \"500\"\n}",
        "model_mapping": {
        
        "kimi-k2-0711-preview":"kimi-k2-250711",
        "moonshotai/kimi-k2-instruct":"kimi-k2-250711",
        
        "deepseek-r1": "deepseek-r1-250120",
        "deepseek-reasoner": "deepseek-r1-250120",
        "deepseek-v3-0324": "deepseek-v3-250324",
        "deepseek-v3": "deepseek-v3-250324",
        "deepseek-chat": "deepseek-v3-250324",
        "doubao-1-5-vision-pro-32k": "doubao-1-5-vision-pro-32k-250115",
        "doubao-1.5-vision-pro-32k": "doubao-1-5-vision-pro-32k-250115",
        "doubao-pro-32k": "doubao-1-5-pro-32k-250115",
        "doubao-pro-256k": "doubao-1-5-pro-256k-250115",
        "doubao-1.5-lite-32k": "doubao-1-5-lite-32k-250115",
        "doubao-lite-4k": "doubao-1-5-lite-32k-250115",
        "doubao-lite-32k": "doubao-1-5-lite-32k-250115",
        "doubao-lite-128k": "doubao-lite-128k-240828",
        "doubao-1.5-lite": "doubao-1-5-lite-32k-250115",
        "doubao-vision-lite-32k": "doubao-vision-lite-32k-241015",
        "doubao-vision-pro-32k": "doubao-1-5-vision-pro-32k-250115",
        "doubao-1.5-pro-32k": "doubao-1-5-pro-32k-250115",
        "doubao-1.5-pro-256k": "doubao-1-5-pro-256k-250115",
        "doubao-1-5-thinking-pro": "doubao-1-5-thinking-pro-250415",
        "doubao-1-5-thinking-pro-vision": "doubao-1-5-thinking-vision-pro-250428"
        }
    }'

"""
