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

    "volc": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",
    "doubao": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",
    "jimeng": "https://api.chatfire.cn/volc/v1/contents/generations/tasks/{task_id}",

    "cogvideox": "https://api.chatfire.cn/zhipuai/v1/async-result/{task_id}",

    "minimax": "https://api.chatfire.cn/minimax/v2/async/minimax-hailuo-02",
    # :"https://api.chatfire.cn/minimax/v1/query/video_generation",

    "wan": "https://api.chatfire.cn/sf/v1/videos/generations",  # wan-ai-wan2.1-t2v-14b 可能还有其他平台

    "veo3": "https://api.chatfire.cn/veo/v1/videos/generations?id={task_id}",
    "sora": "https://api.chatfire.cn/sora/v1/videos/generations?id={task_id}",

}


async def get_tasks(platform: str = "flux", action: str = "", status: str = "NOT_START", return_ids: bool = False):
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
    if return_ids:
        # from meutils.str_utils.json_utils import json_path

        return [item['task_id'] for item in response['data']['items']] | xUnique

    return response


async def polling_tasks(platform: str = "flux", action: str = "", status: str = "NOT_START"):
    response = await get_tasks(platform, action, status)
    if items := response['data']['items']:
        tasks = []
        model = ''
        for item in items[:64]:  # 批量更新
            task_id = item['task_id']
            action = item['action'].split('-', maxsplit=1)[0]  # 模糊匹配
            if 'fal-' in item['action']:
                model = item['action'].split('-')[1]

            if task_id.startswith("cgt-"):
                action = "volc"

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
            logger.debug(f"base_url: {base_url}, path: {path}")
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
    # arun(get_tasks(action="jimeng-video-3.0", status="FAILURE"))
    # arun(get_tasks(action="jimeng-video-3.0", return_ids=True))

    # arun(get_tasks(action="jimeng-video-3.0", return_ids=True))

    # arun(refund_tasks())

    # arun(get_tasks(return_ids=True))