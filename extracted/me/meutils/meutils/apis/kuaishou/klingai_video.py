#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : klingai
# @Time         : 2024/7/9 13:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import jsonpath

from meutils.pipe import *
from meutils.schemas import kling_types
from meutils.schemas.task_types import TaskType, Task
from meutils.schemas.kuaishou_types import BASE_URL, KlingaiVideoRequest, FEISHU_URL, FEISHU_URL_VIP

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.apis.kuaishou.klingai import get_reward, get_point, check_token, download, get_task_plus

from meutils.apis.proxy.kdlapi import get_one_proxy

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


# BASE_URL = GUOJI_BASE_URL


# 自动延长
# {"type":"m2v_extend_video","inputs":[{"name":"input","inputType":"URL","url":"https://h1.inkwai.com/bs2/upload-ylab-stunt/special-effect/output/HB1_PROD_ai_web_29545092/8992112608804666920/output_ffmpeg.mp4","fromWorkId":29545092}],"arguments":[{"name":"prompt","value":""},{"name":"biz","value":"klingai"},{"name":"__initialType","value":"m2v_img2video"},{"name":"__initialPrompt","value":"母亲对着镜头挥手"}]}
# 自定义创意延长
# {"type":"m2v_extend_video","inputs":[{"name":"input","inputType":"URL","url":"https://h2.inkwai.com/bs2/upload-ylab-stunt/special-effect/output/HB1_PROD_ai_web_29542959/396308539942414182/output_ffmpeg.mp4","fromWorkId":29542959}],"arguments":[{"name":"prompt","value":"加点字"},{"name":"biz","value":"klingai"},{"name":"__initialType","value":"m2v_txt2video"},{"name":"__initialPrompt","value":"让佛祖说话，嘴巴要动，像真人一样"}]}
@retrying(max_retries=8, max=8, predicate=lambda r: not r)
async def create_task(request: KlingaiVideoRequest, cookie: Optional[str] = None, vip: bool = False):
    cookie = cookie or await get_next_token_for_polling(FEISHU_URL_VIP if vip else FEISHU_URL, check_token=check_token,
                                                        from_redis=True)

    task_type = TaskType.kling_vip if vip else TaskType.kling

    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    request_kwargs = {}
    for i in range(3):
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, **request_kwargs) as client:
            response = await client.post("/api/task/submit", json=request.payload)
            if response.is_success:
                data = response.json()  # metadata
                send_message(bjson(data))

                # 触发重试 404 429 520
                if any(i in str(data) for i in {"页面未找到", "请求超限", "配额耗尽", "积分消费失败"}):
                    send_message(f"{data}\n\n{cookie}")

                    # 走代理
                    request_kwargs = {
                        "proxy": await get_one_proxy(from_redis=True),
                        # "proxies": proxies,
                    }

                    return

                try:
                    task_ids = jsonpath.jsonpath(data, "$..task.id")  # $..task..[id,arguments]
                    if task_ids:
                        task_id = f"{task_type}-{task_ids[0]}"
                        return Task(id=task_id, data=data, system_fingerprint=cookie)
                    else:
                        return Task(status=0, data=data)

                except Exception as e:
                    logger.error(e)
                    send_message(f"未知错误：{e}")


@retrying(max_retries=3, predicate=lambda r: not r)
async def create_task_plus(request: KlingaiVideoRequest, token: Optional[str] = None, vip: bool = False):
    token = token or await get_next_token_for_polling(FEISHU_URL_VIP if vip else FEISHU_URL, check_token=check_token,
                                                      from_redis=True)

    if not vip: request.mode = "mini"  # 针对普号

    headers = {
        'Cookie': token,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    request_kwargs = {}
    for i in range(3):
        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100, **request_kwargs) as client:
            response = await client.post("/api/task/submit", json=request.payload)
            if response.is_success:
                data = response.json()
                kling_types.send_message(data)

                # 触发重试 404 429 520
                if any(i in str(data) for i in {"页面未找到", "请求超限", "配额耗尽", "积分消费失败"}):
                    kling_types.send_message(f"{data}\n\n{token}")

                    # 走代理
                    request_kwargs = {
                        "proxy": await get_one_proxy(from_redis=True),
                        # "proxies": proxies,
                    }

                    return

                task_id = message = task_status_msg = ''
                code = data.get("status")
                if data.get("data"):
                    data = data.get("data")
                    if task := data.get("task"):
                        code = 0
                        task_id = f"""kling-video-{request.mode}-{task.get("id")}"""
                        task_status = "processing"
                        task_status_msg = data.get("message")
                    else:
                        task_status = "failed"
                        task_status_msg = data.get("message")

                else:
                    message = data.get("message")
                    task_status = "failed"

                return kling_types.TaskResponse(
                    code=code,
                    message=message,
                    data=kling_types.Task(task_id=task_id, task_status=task_status, task_status_msg=task_status_msg),
                    system_fingerprint=token,
                )


if __name__ == '__main__':
    # https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=v8vcZY

    # cookie = "_did=web_474598569404BC09;did=web_43cec8fac6fa32077f3b12bf131b77a7310f;kuaishou.ai.portal_ph=0e15bfbb51aa3d52d065602d7e566d622ba4;kuaishou.ai.portal_st=ChVrdWFpc2hvdS5haS5wb3J0YWwuc3QSsAHW9jii6pSdK5oTimSzQslDxQ5mLAW8m2j8dKFP4uptOr8aycVOX72ydltRPJhO6QbD4fGYD2pFXD_c4gqsAZPLZluo4DeIxFAWhEplxrmSA61cb-VBtCEB2bxyM1gC-sooTaSESNkekMI5WBEq1_NL5E2x-wigAGi6jm1Chpq-bJ3oTAXe9yMLV3oY4qilfoV9M77nn3cY-r76Z2Z9G-3JICGNjTmN2OAQSf_q3EXtMRoSITGi7VYyBd022GVFnVcqtiPoIiDjv6HmF2lhkn6FgvYhjgLMGinYaZxZj84kbjL8GfxuiygFMAE;userId=415950813"
    # token = "weblogger_did=web_9665177505014D12; _gcl_au=1.1.961392860.1725442018; did=web_d77db05423a7f37445a28355351bf2736bf0; anonymous-message-release-notice-1=true; userId=5138238; ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqABA02dJVaF0Q5XvWFZVNWLa-7fNeGjTJZ_BP3zPN4JN1Ct8LRrLlT8ZAtqXZa0X_fOBXuQFiOqfoIuTziI8bNUaIKPNjhfcCT2CUcLv9bIVdYkwlJGlzMai8-2o2MoF9yopDzeYfwphWxBh575DrMjMjnPoNp0MqSq3iDIIA9glYGxEOYRcotovl63JPPI1Vy4mSX46S1Omh1X0suF2oWKCBoSPFqCkp3UokbKTh0UPCIW9AgsIiBZRgCwD_UpSF1elCUq5jwFhe-Wr2hErFmS73Zc4GyXOSgFMAE; ksi18n.ai.portal_ph=c52b0d2188bc0e0d209a401f9cb4c4889227"
    request = KlingaiVideoRequest(prompt="一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头",
                                  duration=5)  # 27638649
    # e = KlingaiVideoRequest.Config.json_schema_extra.get('examples')[-1]  # 尾帧
    # request = KlingaiVideoRequest(**e)
    #
    print(arun(create_task(request, vip=True)))
    # arun(get_task("31298981", cookie))
    # arun(get_task("vip-47426519", token))

    # pprint(arun(create_image(rquest)))

    # request
    # request = KlingaiVideoRequest(
    #     prompt="一条可爱的小狗",
    #     url="https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/special-effect/output/HB1_PROD_ai_web_30135907/1706269798026373672/output_ffmpeg.mp4"
    # )
    # pprint(arun(create_task(request, cookie)))
    # pprint(arun(get_task(28106800, cookie)))  # 拓展的id 28106800  可能依赖账号 跨账号失败: 单账号测试成功

    # url = "http://p2.a.kwimgs.com/bs2/upload-ylab-stunt/ai_portal/1720681052/LZcEugmjm4/whqrbrlhpjcfofjfywqqp9.png"
    # request = KlingaiVideoRequest(prompt="狗狗跳起来", url=url)  # 28110824
    # pprint(arun(create_task(request, cookie, feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=EXxwtQ")))

    # pprint(arun(get_task(28110824, cookie)))

    # url = "http://p2.a.kwimgs.com/bs2/upload-ylab-stunt/ai_portal/1720681052/LZcEugmjm4/whqrbrlhpjcfofjfywqqp9.png"

    # request = KlingaiVideoRequest(prompt="狗狗跳起来", url=url)  # 28110824
    # pprint(arun(create_task(request, vip=True)))

    # pprint(arun(get_task(30974235, cookie)))
    # pprint(arun(get_task(28377631, cookie)))
    # pprint(arun(get_task(28383134, cookie)))

    # pprint(arun(beautify_prompt()))

    # 国际
    # cookie = "did=web_b11919c67a1966b83eaef4a19fb2de266cba;ksi18n.ai.portal_ph=644033a151612d07cbdedc21513f5d2191b6;ksi18n.ai.portal_st=ChNrc2kxOG4uYWkucG9ydGFsLnN0EqABChr9Is3s_8NQtSRM3A10k93e-Yg2PRAw5SR8BswQAdCW33dIk_7cWf5EQohyx45HoVG4nYAdpPZRg02_y4vsA5AA2TCzde2-cxAMecVk_Rg_oOnQBGWqMjVachSC82Qf4xA-vpOj1KYRGv4XwQ6ZvpqLRysjpt0543UjaasSUa8sHlD6XT_nwPnOc2LGaIDdhXExgvh85OqK7-FpcvniWRoSSiD-9Kd-wI-i_qkoWz9SxkEvIiDCLGRyg7lgXBHZcPxIy0hnLZfkuyO9AMaVYFzUapkQmCgFMAE;userId=3412057;weblogger_did=web_8897873009A74F8"
    # arun(create_task(request, cookie))

    # cookie = arun(get_next_token_for_polling(feishu_url=FEISHU_URL_VIP, check_token=check_token))
    # arun(get_task("kling@vip-41009887", cookie))

    # with timer():
    #     arun(check_token(cookie))
    #
    #
    #
    #
    # arun(get_reward(token))  # 签到
    # arun(get_point(token))  # 签到

    # arun(get_task_plus('60909700', token=token))
