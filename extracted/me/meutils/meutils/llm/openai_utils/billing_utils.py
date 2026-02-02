#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : usage_utils
# @Time         : 2025/6/24 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
1. 同步任务（流 非流）
    - 按次
    - 按量
2. 异步任务
    - 按次
    - 按量
"""

from contextlib import asynccontextmanager

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.apis.utils import make_request
from meutils.apis.oneapi.user import get_user_money
from fastapi import status, HTTPException

base_url = "https://api.chatfire.cn/flux/v1"
# base_url = "http://110.42.51.201:38886/flux/v1"


# base_url="http://110.42.51.201:38888/flux/v1"
# base_url = "http://0.0.0.0:8000/v1/async/flux/v1"
# base_url = "https://openai-dev.chatfire.cn/usage/async/flux/v1"

async def billing_for_async_task(
        model: str = "async-task",
        task_id: str = "sync",
        n: float = 1,
        api_key: Optional[str] = None  ########## 注意
):
    model = model.lower().replace('/', '-')  # 统一小写 # wan-ai-wan2.1-t2v-14b
    if n := int(np.round(n)):
        tasks = [
            make_request(
                base_url=base_url,
                api_key=api_key,
                path=f"/{model}",
                payload={
                    "id": task_id,
                    "seed": task_id,
                    "webhook_secret": task_id,  # 平替 task_id
                    # "prompt": "ChatfireAPI",
                    # 'polling_url': f'{base_url}/get_result?id={task_id}',
                }
            )
            for i in range(n)
        ]

        _ = await asyncio.gather(*tasks)
        if _ and isinstance(_[0], str):
            raise Exception("未知模型错误，请联系管理员")

        return _


async def get_async_task(id: str = "123456"):
    # 计费
    _ = await make_request(
        base_url=base_url,
        path=f"/get_result?id={id}",

        method="GET"
    )

    return _


async def billing_for_tokens(
        model: str = "usage-chat",

        usage: Optional[dict] = None,

        api_key: Optional[str] = None,

        n: Optional[float] = None,  # 按次走以前逻辑也行

        task_id: Optional[str] = None,
):
    """

    image_usage = {
            "input_tokens": input_tokens,
            "input_tokens_details": {
                "text_tokens": input_tokens,
                "image_tokens": 0,
            },
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        }

    usage = {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens
        }
    """
    usage = usage or {}
    n = n and int(np.round(n))

    client = AsyncOpenAI(api_key=api_key, timeout=30)
    if n:
        _ = await client.images.generate(
            model=model,
            prompt="ChatfireAPI",
            n=n,
            user=task_id
        )

    elif "input_tokens" in usage:
        _ = await client.images.generate(
            model=model,
            prompt="ChatfireAPI",
            n=n,
            extra_body={"extra_fields": usage},

            user=task_id
        )
    else:
        # todo 设计 id chatcmpl-NEdenEpvzGiKR2FfK2GmzK => 表达某些含义
        _ = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ChatfireAPI"}],
            extra_body={"extra_body": usage},
            user=task_id
        )
    return _


def get_billing_n(request: Union[BaseModel, dict], duration: float = 6, resolution: Optional[str] = None):
    """继续拓展其兼容性
         MINIMAX_HAILUO_02_10S_768P
    :param request:
    :param duration:
    :return:
    """
    resolution = (resolution or "500").lower().removesuffix('p')

    if isinstance(request, BaseModel):
        request = request.model_dump()

    # 数量
    num = request.get("n") or request.get("num_images") or 1

    # 时长
    dur = np.ceil(int(request.get("duration", duration)) / duration)  # 默认 6s
    durs = {"--duration 10", "--dur 10"}
    if any(i in str(request) for i in durs):
        dur = max(dur, 2)

    # 分辨率 resolution 480p 720p 1080p
    rs = request.get("resolution", resolution).lower().removesuffix('p')  # 默认 720p
    rs = np.round((int(rs) / int(resolution)) ** 2)

    # rss = {"--resolution 1080p", "--rs 1080p"}

    return num * dur * rs or 1


def get_billing_model(
        request: Union[BaseModel, dict],

        default_model: Optional[str] = None,
        default_duration: Optional[int] = None,
        default_resolution: Optional[str] = None
):
    """继续拓展其兼容性
    什么时候走这个逻辑？
    """
    if isinstance(request, BaseModel):
        request = request.model_dump()

    model = (request.get("model") or request.get("model_name") or default_model or "undefined model").lower()
    if model.startswith("doubao-seedance"):
        model = model.rsplit('-', maxsplit=1)[0].strip("-i2v").strip("-t2v")

    # 某些模型不需要匹配，单模型计费
    if model.startswith(("veo", "jimeng", "cogvideo")):  # todo 后续再拓展
        return model

    duration = request.get("duration", default_duration or "5")
    resolution = request.get("resolution", default_resolution or "720p")

    # 火山
    if any(i in str(request).lower() for i in {"--duration 10", "--dur 10"}):
        duration = 10

    for rs in {"480p", "720p", "1080p"}:
        if any(i in str(request).lower() for i in {f"--resolution {rs}", f"--rs {rs}"}):
            resolution = rs

    return f"{model}_{duration}s_{resolution}"


@asynccontextmanager
async def billing_flow_for_async_task(
        model: str = "usage-async",
        task_id: str = "123456",
        n: float = 1,
        api_key: Optional[str] = None
):
    if n and (user_money := await get_user_money(api_key)):  # 计费

        # 判断
        if user_money < 1:
            raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="余额不足或API-KEY限额")

        # 执行
        yield

        # 计费
        await billing_for_async_task(model, task_id=task_id, n=n, api_key=api_key)

    else:  # 不计费
        a = yield
        logger.debug(a)


# # 检查余额
# if user_money := await get_user_money(api_key):
#     if user_money < 1:
#         raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="余额不足或API-KEY限额")
@asynccontextmanager
async def billing_flow_for_tokens(
        model: str = "usage-chat",

        usage: Optional[dict] = None,  # None就是按次

        api_key: Optional[str] = None,
):
    await billing_for_tokens(model, usage=usage, api_key=api_key)

    yield


if __name__ == '__main__':
    # arun(create_usage_for_tokens())
    # usage = {
    #     "input_tokens": 1,
    #     "input_tokens_details": {
    #         "text_tokens": 1,
    #         "image_tokens": 0,
    #     },
    #     "output_tokens": 100,
    #     "total_tokens": 101
    # }
    # n = 1
    usage = {
        "prompt_tokens": 1000, "completion_tokens": 100,  # "total_tokens": 2000,
    }
    # arun(billing_for_tokens(model="tokens", usage=usage, task_id='xx'))
    # arun(billing_for_tokens(model="fal", usage=usage, task_id='xx'))

    # arun(create_usage_for_async_task(task_id="task_id", n=1))

    model = "async"
    # model = "fal-ai/model1"
    task_id = f"{model}-{int(time.time())}"
    # model = "doubao-seedance-1-0-pro-250528"
    model = "Wan-AI/Wan2.1-T2V-14B"

    # arun(billing_for_async_task(model, task_id=task_id, n=3))
    # arun(billing_for_async_task(task_id='fal-ai-sync'))
    # model = "doubao-seedance-1-0-lite-i2v-250428_5s_10"
    # model="doubao-seedance-1-0-lite-i2v-250428"
    # model = "doubao-seedance-1-0-pro-250528_10s_1080p"
    model = "minimax-hailuo-02_6s_1080p"
    # model = "flux-kontext-pro"
    arun(billing_for_async_task(model, task_id=model))

    data = {
        "video_url": "https://storage.googleapis.com/falserverless/example_inputs/wan_animate_input_video.mp4",
        "image_url": "https://storage.googleapis.com/falserverless/example_inputs/wan_animate_input_image.jpeg",
        "resolution": "580p",
        "num_inference_steps": 20,
        "enable_safety_checker": True,
        "shift": 5,
        "video_quality": "high",
        "video_write_mode": "balanced"
    }

    data = {
        "model": "doubao-seedance-1-0-pro-250528",
        "content": [
            {
                "type": "text",
                "text": "--resolution 1080p  --duration 10  --camerafixed true多个镜头。一名侦探进入一间光线昏暗的房间。他检查桌上的线索，手里拿起桌上的某个物品。镜头转向他正在思索。 --ratio 16:9，主体:男人转动头部打量四周\n景别:全景\n运镜:转动镜头\n视角:平视\n构图:居中构图\n风格统一:动漫风格"
            }
        ]
    }

    data = {
        "model": "doubao-seedance-1-0-lite-i2v-250428",
        "content": [
            {
                "text": "一本古老的魔法书，镜头弧形环绕至的正面俯视特写 --dur 10 --resolution 720p",
                "type": "text"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://mjimg.zhanjuzhe.cn/raw/media/202510/28/20251028134055523409.png"
                }
            }
        ]
        ,
        "duration": 5,
        "created_at": 1761630940,
        "resolution": "720p",
        "updated_at": 1761630982,
        "framespersecond": 24
    }

    data = {
        "model": "doubao-seedance-1-0-pro-250528",
        "content": [
            {
                "text": "推镜到女人脸，女人表情气鼓鼓的，微微皱眉，看着男人，右手摸着脑袋 ，然后放下手  --resolution 1080p  --duration 5  --camerafixed false",
                "type": "text"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://cdn.jeff1992.com/ai-video/2025/10/28/mpyzyn_1761629867192.jpg"
                }
            }
        ]
        ,
        "duration": 5,
        "created_at": 1761630465,
        "resolution": "1080p",
        "updated_at": 1761630529,
        "framespersecond": 24
    }

    # "model": "doubao-seedance-1-0-lite-i2v-250428",

    data = {
        "model": "doubao-seedance-1-5-pro-251215",

        "content": [
            {
                "text": "男人背过身，抬头看到红布条 --rs 1080p --dur 5 --cf false --seed -1 --wm false --rt 9:16",
                "type": "text"
            },
            {
                "role": "first_frame",
                "type": "image_url",
                "image_url": {
                    "url": "https://renren-animation.xyzpgc.com/resources/png/2025/10/28/byteFile-1761620822538-4760.png"
                }
            }
        ]
        ,
        "duration": 5,
        "created_at": 1761633057,
        "resolution": "1080p",
        "updated_at": 1761633094,
        "framespersecond": 24
    }


    #
    print(get_billing_model(data))  # doubao-seedance-1-0-lite-i2v-250428_10s_720p

    # doubao-seedance-1-0-pro-250528_5s_1080p
    #
    # arun(get_async_task(task_id))
    #
    # arun(get_async_task(f"{task_id}-Ready", status="Ready"))

    # arun(get_async_task('chatfire-123456-Ready-1'))

    # {
    #   "id": "chatfire-1750769977.856766",
    #   "result": {},
    #   "status": "Error",
    #   "details": {
    #     "xx": [
    #       "xxxx"
    #     ]
    #   },
    #   "progress": 99
    # }

    # data = {
    #     "model": "veo3",
    #     "prompt": "女人飞上天了",
    #     "images": [
    #         "https://oss.ffire.cc/files/kling_watermark.png"
    #     ],
    #     "enhance_prompt": True
    # }
    # print(get_billing_model(data, default_resolution=""))
