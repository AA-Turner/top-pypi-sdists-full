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

# headers
ACTIONS = {
    "doubao": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",
    "jimeng": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",

    "cogvideox": "https://api.chatfire.cn/zhipuai/v1/async-result/{task_id}",

    "minimax": "https://api.chatfire.cn/minimax/v2/async/minimax-hailuo-02",
    "fal": "https://api.chatfire.cn/fal-ai/{model}/requests/{request_id}",

    "wan": "https://api.chatfire.cn/sf/v1/videos/generations",  # wan-ai-wan2.1-t2v-14b 可能还有其他平台
}


async def polling_tasks(platform: str = "flux", action: str = "", status: str = "NOT_START"):
    base_url = "https://api.chatfire.cn"
    path = "/api/task/"
    headers = {
        'authorization': f'Bearer {os.getenv("CHATFIRE_ONEAPI_TOKEN")}',
        'new-api-user': '1',
        'rix-api-user': '1',
    }

    params = {
        "p": 1,
        "page_size": 100,
        "user_id": "",
        "channel_id": "",
        "task_id": "",
        "submit_timestamp": int(time.time() - 24 * 3600),
        "end_timestamp": int(time.time() - 0.5 * 3600),
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

            url = ACTIONS[action].format(model=model, task_id=task_id)
            # logger.debug(url)

            # task = await make_request_httpx(
            #             base_url=base_url,
            #             path=path
            #         )
            # logger.debug(bjson(task))
            base_url, path = url.rsplit("/", maxsplit=1)
            _ = asyncio.create_task(
                make_request_httpx(
                    base_url=base_url, path=path,
                )
            )
            tasks.append(_)
        data = await asyncio.gather(*tasks)
        return data


if __name__ == '__main__':
    arun(polling_tasks())
