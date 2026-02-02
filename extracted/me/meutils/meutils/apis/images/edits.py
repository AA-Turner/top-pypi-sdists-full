#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_tools
# @Time         : 2024/8/28 13:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.apis.proxy.kdlapi import get_one_proxy

from meutils.decorators.retry import retrying, IgnoredRetryException

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.image_types import ImageRequest, ImagesResponse, HunyuanImageProcessRequest
from meutils.schemas.image_types import ImageProcess
from meutils.schemas.yuanbao_types import YUANBAO_BASE_URL, FEISHU_URL as YUANBAO_FEISHU_URL

from meutils.io.files_utils import to_bytes, to_base64, to_url_fal, to_url
from meutils.notice.feishu import send_message as _send_message

from fake_useragent import UserAgent

ua = UserAgent()

BASE_URL = "https://image.baidu.com"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=jrWhAS"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(min=3, ignored_exception_types=(IgnoredRetryException,))
async def make_request_for_hunyuan(payload, token: Optional[str] = None, response_format: str = "url"):
    s = time.time()

    token = token or await get_next_token_for_polling(YUANBAO_FEISHU_URL)

    model = payload.pop("model", "removewatermark")

    logger.debug(payload)

    headers = {
        'cookie': token,
        'User-Agent': ua.random,
    }
    async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post(f"/api/image/{model}", json=payload)
        response.raise_for_status()
        logger.debug(response.text)

        skip_strings = ['DONE', 'TRACEID']
        data = response.text.replace(r'\u0026', '&').splitlines() | xsse_parser(skip_strings=skip_strings)
        data = data and data[-1]
        logger.debug(data)

        # todo: 错误处理
        if isinstance(data, dict) and any(data["code"] == code for code in {"429"}):
            Exception(f"重试: {response.text}")

        elif isinstance(data, list) or any(i in response.text for i in {"当前图片没有检测到水印"}):  # 跳过重试并返回原始错误
            raise IgnoredRetryException(f"忽略重试: \n{response.text}")

        data = [
            {
                "url": data["imageUrl"],
                "imageUrl": data["imageUrl"],
                "thumbnailUrl": data["thumbnailUrl"],
            }
        ]
        if response_format == "url":
            return ImagesResponse(data=data, timings={"inference": time.time() - s})
        else:
            data[0]["b64_json"] = await to_base64(data[0]['url'])
            return ImagesResponse(data=data, timings={"inference": time.time() - s})


@retrying(min=3, ignored_exception_types=(IgnoredRetryException,))
async def make_request_for_gitee(payload, token: Optional[str] = None, response_format: str = "url"):
    s = time.time()
    feishu_url = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=gg5DNy"
    token = token or await get_next_token_for_polling(feishu_url)

    logger.debug(token)

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Failover-Enabled": "true",
        "X-Package": "1910"
    }

    files = {
        "image": ("_.png", payload.pop('image'))
    }
    base_url = "https://ai.gitee.com/v1"
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=60) as client:
        response = await client.post("/images/mattings", data=payload, files=files)
        response.raise_for_status()
        response = ImagesResponse(**response.json())
        if response_format == "url":
            url = await to_url_fal(response.data[0].b64_json, content_type="image/png")
            response.data[0].url = url
            response.data[0].b64_json = None
            response.timings = {"inference": time.time() - s}

        return response


async def make_request_for_baidu(payload, token: Optional[str] = None, response_format: str = "url"):
    s = time.time()
    # token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)
    headers = {
        # 'Cookie': token,
        'User-Agent': ua.random,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    request_kwargs = {
        "proxy": await get_one_proxy(),
    }

    # logger.debug(request_kwargs)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=120, **request_kwargs) as client:
        response = await client.post("/aigc/pccreate", data=payload)  # pcEditTaskid
        response.raise_for_status()
        data = response.json()

        logger.debug(data)

        image_base64 = None
        if task_id := data.get("pcEditTaskid"):
            for i in range(30):
                await asyncio.sleep(3)
                try:
                    response = await client.get(f'/aigc/pcquery?taskId={task_id}&', )  # todo: get任务未加代理
                    # logger.debug(response.json())
                    if data := response.json().get("picArr", []):
                        image_base64 = data[0].get("src")
                        break
                except Exception as e:
                    logger.error(e)
                    # request_kwargs["proxy"] = await get_one_proxy()

                    if i > 3:
                        raise IgnoredRetryException(f"忽略重试: \n{response.text}")

        if not image_base64:
            raise Exception(f"NO WATERMARK FOUND: {data}")  #############

        if response_format == "url":
            url = await to_url(image_base64, filename=f"{shortuuid.random()}_hd.png", content_type="image/png")

            return ImagesResponse(data=[{"url": url}], timings={"inference": time.time() - s})
        else:
            return ImagesResponse(data=[{"b64_json": image_base64}], timings={"inference": time.time() - s})


async def edit_image(request: Union[ImageProcess, ImageRequest]):
    if isinstance(request, ImageRequest):
        image = mask = None
        if len(request.image_urls) > 1:
            image = request.image_urls[0]
            mask = request.image_urls[1]

        request = ImageProcess(
            model=request.model,
            image=image,
            mask=mask,
            aspect_ratio=request.aspect_ratio,
            response_format=request.response_format,
        )

    image, mask = await asyncio.gather(to_base64(request.image, content_type="image/png"), to_base64(request.mask))

    # baidu_url = "https://chatfire.hkg.bcebos.com/zjz.jpg"
    # baidu_url = "https://cfcdn.bj.bcebos.com/zjz.jpg"
    # baidu_url =  "https://edit-upload-pic.cdn.bcebos.com/e9f47f610f22b5be48bd7dd45e1e5acd.jpeg?authorization=bce-auth-v1%2FALTAKh1mxHnNIyeO93hiasKJqq%2F2025-07-04T06%3A06%3A56Z%2F3600%2Fhost%2F7f46f4a362f50b39ec5cc2ff552a26a04b898cf66b71bdf8281150c0f7669c8e"

    payload = {
        "type": "1",  # 去水印

        "picInfo": image,
        # "picInfo2": mask,

        # # 百度云盘 才会更快
        # "image_source": "1",
        # "original_url": baidu_url,
        # # # 更快但是会有错误
        # "thumb_url": baidu_url,
        # 更快但是会有错误

    }

    if request.model == "clarity":
        payload['type'] = "3"

        return await make_request_for_baidu(payload, response_format=request.response_format)
        # 临时替换
        # from meutils.apis.baidu.image_enhance import image_enhance
        # data = await image_enhance(request.image)
        # return ImagesResponse(data=[{"url": data.get("image")}])

    elif request.model == "remove-watermark":
        if mask:  ####### todo: mask 抠图
            payload['type'] = "2"
        return await make_request_for_baidu(payload, response_format=request.response_format)

    elif request.model == "clarity":
        payload['type'] = "3"

        return await make_request_for_baidu(payload, response_format=request.response_format)


    elif request.model == "expand":
        payload['type'] = "4"
        payload['ext_ratio'] = request.aspect_ratio
        return await make_request_for_baidu(payload, response_format=request.response_format)
    ################################################################################################

    elif request.model == "rmbg-2.0":
        payload = {
            "model": request.model,
            "image": await to_bytes(image),
        }
        return await make_request_for_gitee(payload, response_format=request.response_format)

    elif request.model.startswith("hunyuan-"):
        payload = {
            "imageUrl": request.image if request.image.startswith("http") else await to_url_fal(request.image),
        }
        # "remove-watermark" "clarity"
        if "remove-watermark" in request.model:
            payload["model"] = "removewatermark"
        elif "clarity" in request.model:
            payload["model"] = "clarity"

        return await make_request_for_hunyuan(payload, response_format=request.response_format)


if __name__ == '__main__':
    token = "BAIDUID=FF8BB4BF861992E2BF4A585A37366236:FG=1; BAIDUID_BFESS=FF8BB4BF861992E2BF4A585A37366236:FG=1; BIDUPSID=FF8BB4BF861992E2BF4A585A37366236; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; ab_sr=1.0.1_NjY5OWZiZDg5YTJmYTQzNWUyNzU1YjBmN2FlMDFiNjMyOTVhMDE3ZWVlYWY5N2Y2MTg4NGI1MzRmMmVjMjQyZjlhZTU2MmM1NDRlMmU4YzgwMzRiMjUyYTc4ZjY1OTcxZTE4OTA4YTlmMWIwZWUzNTdiMzlhZTRiM2IzYTQ0MjgyMzc2MjQwMGRlYzZlZDhjOTg5Yzg4NWVjMTNiZmVmZQ==; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; H_WISE_SIDS=60273_60360_60623_60664_60678_60684_60700"
    # hunyuan
    token = "web_uid=ac283ec7-4bf6-40c9-a0ce-5a2e0cd7db06; hy_source=web; hy_user=I09MgMfFcUUyVSIg; hy_token=hevVCi/QuVjQcre5NDRMO7FuiWCZoDMIq3Zp8IwNxrPUofl4zWYazHEdeZ2S5o7q; _qimei_q36=; _qimei_h38=f2d27f50f0f23e085296d28303000006a17a09; _qimei_fingerprint=efbb885a22f7d4e5589008c28bc8e7ba; _qimei_uuid42=18c0310102d1002a082420cd40bb9717523c3c7e12; _gcl_au=1.1.915258067.1733278380; _ga_RPMZTEBERQ=GS1.1.1733722091.3.1.1733722108.0.0.0; _ga=GA1.2.981511920.1725261466; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100000458739%22%2C%22first_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE5OGM3YjJkNTItMGZjY2E4ZDczMWNiOWI4LTE4NTI1NjM3LTIwNzM2MDAtMTkxYjE5OGM3YjMxZmQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTAwMDAwNDU4NzM5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22100000458739%22%7D%2C%22%24device_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%7D"

    # url = "https://api.chatfire.cn/beta/https://s3.ffire.cc/files/jimeng.jpg"
    # url = "https://juzhen-1318772386.cos.ap-guangzhou.myqcloud.com/mj/2025/06/07/7b347a36-8146-4d3d-a5dc-0b8dc365817d.png"
    url = "https://oss.ffire.cc/files/shuiyin.jpg"
    url = "https://cdn.qwenlm.ai/output/675ef500-064c-4ed0-9822-a03db065f773/t2i/6ffdc470-af73-4fa1-bb37-b13b096af4ac/1755737594.png?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV91c2VyX2lkIjoiNjc1ZWY1MDAtMDY0Yy00ZWQwLTk4MjItYTAzZGIwNjVmNzczIiwicmVzb3VyY2VfaWQiOiIxNzU1NzM3NTk0IiwicmVzb3VyY2VfY2hhdF9pZCI6IjQ3OGM4ODE0LTI1NWQtNGFmMC04OWY1LTczYmM2OTRjZmFjNiJ9.PBoOGxrEhYrgkwK3D28TExVK5JGPgMKLM5Xlw4fkq6U"
    # url = "https://oss.ffire.cc/files/shuiyin3.jpg"

    # url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_mmu_txt2img_aiweb/9c520b80-efc2-4321-8f0e-f1d34d483ddd/1.png"

    request = ImageProcess(
        # model="hunyuan-remove-watermark",

        model="remove-watermark",
        # model="clarity",
        # model="expand",
        # model="rmbg-2.0",

        image=url,
        # mask=url,

        # response_format="b64_json"
    )
    arun(edit_image(request))

    # arun(image_edit(request))
    #
    # from urllib.parse import parse_qs, parse_qsl
    #
    # s = "query=bdaitpzs%E7%99%BE%E5%BA%A6AI%E5%9B%BE%E7%89%87%E5%8A%A9%E6%89%8Bbdaitpzs&picInfo=&picInfo2=&type=3&text=&ext_ratio=&expand_zoom=&original_url=https%3A%2F%2Fedit-upload-pic.cdn.bcebos.com%2F5a7311e6fc3425b307ac4359e4304431.jpeg%3Fauthorization%3Dbce-auth-v1%252FALTAKh1mxHnNIyeO93hiasKJqq%252F2025-07-02T10%253A42%253A07Z%252F3600%252Fhost%252Ff14fa759bffee374474540d0705a04c25068b40f432a720b4579056bac813a5f&thumb_url=https%3A%2F%2Fedit-upload-pic.cdn.bcebos.com%2F5a7311e6fc3425b307ac4359e4304431.jpeg%3Fauthorization%3Dbce-auth-v1%252FALTAKh1mxHnNIyeO93hiasKJqq%252F2025-07-02T10%253A42%253A07Z%252F3600%252Fhost%252Ff14fa759bffee374474540d0705a04c25068b40f432a720b4579056bac813a5f&front_display=0&create_level=0&image_source=1&style=&queryFeature=&imageFeature="
    # print(parse_qsl(s))
