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
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.schemas.image_types import BAIDU_TASKS, BaiduImageProcessRequest

from meutils.decorators.retry import retrying
from meutils.schemas.image_types import ASPECT_RATIOS
from meutils.oss.minio_oss import Minio
from meutils.decorators.contextmanagers import try_catcher
from meutils.schemas.baidu_types import BDAITPZSRequest
from meutils.schemas.task_types import Task, TaskType
from meutils.io.image import image_to_base64, crop_polygon
from meutils.io.files_utils import to_bytes, to_base64, to_url
from meutils.apis.proxy.kdlapi import get_one_proxy
from fake_useragent import UserAgent

ua = UserAgent()
from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://image.baidu.com"

url = "https://image.baidu.com/aigc/pccreate"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=jrWhAS"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


@retrying(max_retries=3, title=__name__)
async def create_task(
        request: BDAITPZSRequest,
        token: Optional[str] = None,
        is_async: bool = True,
        response_format: Optional[Literal["url", "b64_json"]] = None
):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

    request.picInfo = await to_base64(request.original_url)

    payload = request.model_dump()

    headers = {
        # 'X-Requested-With': 'XMLHttpRequest',
        'Cookie': token,
        'User-Agent': ua.random,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    request_kwargs = {
        "proxy": await get_one_proxy()
    }

    logger.debug(request_kwargs)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100, **request_kwargs) as client:

        response = await client.post('/aigc/pccreate', data=payload)

        logger.debug(response.status_code)
        # logger.debug(response.text)
        # {"status":5,"message":"网络异常，请稍候再试~","isGenerate":true} 服务端url访问不了
        # {'status': 0, 'resType': 2, 'timestamp': '1727233935', 'token': '5a5fc23b052b31d2120abab9c1d02178'} 没有水印

        if response.is_success:
            data = response.json()

            if "pcEditTaskid" not in data:  # data.get('status') == 0
                send_message(f"照片失败\n{request.original_url}\n{request.model_dump_json(indent=4)}")
                raise Exception(f"无法处理该照片，可联系管理员\n{data}")

            if is_async:
                # {
                #     "status": 0,
                #     "pcEditTaskid": "cr7sbuue1pnfd61bjgu0",
                #     "resType": 0,
                #     "timestamp": "1724892667",
                #     "token": "e668cb4457494351f65300d9f388bb2b"
                # }

                task_id = f"{TaskType.pcedit}-{data['pcEditTaskid']}"
                return Task(id=task_id, data=data, system_fingerprint=token)

            else:  # {'algoprocess': 0, 'isGenerate': False, 'progress': 4}
                logger.debug(data)
                task_id = data['pcEditTaskid']

                for i in range(1, 30):
                    await asyncio.sleep(2 / i)
                    with try_catcher():
                        data = await get_task(task_id, response_format=response_format)
                        logger.debug(f"progress: {data['progress']}")
                        if data['isGenerate']:
                            return data

        response.raise_for_status()


@retrying(max_retries=3, title=__name__)
async def get_task(
        task_id,
        token: Optional[str] = None,
        response_format: Optional[Literal["url", "b64_json"]] = None
):
    task_id = task_id.split("-", 1)[-1]

    params = {
        "taskId": task_id
    }
    request_kwargs = {
        "proxy": await get_one_proxy()
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30, **request_kwargs) as client:
        response = await client.get('/aigc/pcquery', params=params)
        data = response.json()

        if response_format == "url":
            for arr in data.get('picArr', []):
                if base64_string := arr.pop('src', None):
                    data['url'] = await to_url(base64_string, filename=f"{task_id}.png")

        return data


TASKS = {
    "matting": '9',
    "removewatermark": '1'
}


async def image_process(request: BaiduImageProcessRequest):
    _request = BDAITPZSRequest(type=TASKS.get(request.task), original_url=request.image, thumb_url=request.image)
    data = await create_task(_request, is_async=False, response_format="url")

    if request.task == "matting":
        outline_points = []
        inline_points = []

        if "foreground" not in data:  # 未识别到主体： todo: mask
            return {"data": [{"url": data['url']}]}

        for outlines in data['foreground'][0].get('outlines', []):
            _ = list(map(lambda point: (point['x'], point['y']), outlines['line']))
            outline_points.append(_)

        for inlines in data['foreground'][0].get('inlines', []):
            _ = list(map(lambda point: (point['x'], point['y']), inlines['line']))
            inline_points.append(_)

        image = await to_bytes(request.image)
        result = crop_polygon(image, outline_points, inline_points)

        # 将 PIL Image 转换为字节
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        byte_data = buffer.getvalue()
        url = await to_url(byte_data)

        return {"data": [{"url": url}]}
    return {"data": [{"url": data['url']}]}


if __name__ == '__main__':
    url = "https://oss.ffire.cc/files/kling_watermark.png"
    # url = "https://env-00jxgna201cb.normal.cloudstatic.cn/ori/tmp_dc12fc648ab10c4b8d310f3e8645781278e556a0264836d7fdb806c6bb83c493.jpeg"

    # 涂抹消除
    # url = "https://env-00jxgna201cb.normal.cloudstatic.cn/ori/tmp_dc12fc648ab10c4b8d310f3e8645781278e556a0264836d7fdb806c6bb83c493.jpeg"
    # url_ = "https://env-00jxgna201cb.normal.cloudstatic.cn/water/tmp_2954a8d96011173a7f2b6baad8cc28317278e368d1393ca6.jpg"
    # picInfo2 = image_to_base64(url_)
    #
    url = "https://cdn.meimeiqushuiyin.cn/imgImprove/tmp_f5648a3c7cc8973b483ee3bb54d23aea.jpg"  # 网络异常
    url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_mmu_txt2img_aiweb/d08b9526-d641-4e04-83d2-27d48e29fa8c/1.png"
    url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_mmu_txt2img_aiweb/9c520b80-efc2-4321-8f0e-f1d34d483ddd/1.png"
    request = BDAITPZSRequest(
        # picInfo=image_to_base64(url),
        original_url=url,
        thumb_url=url
    )

    # from meutils.io.image import image2nowatermark_image
    #
    # api_keys = get_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True)[0]
    # for token in api_keys:
    #     if token:
    #         # request = BDAITPZSRequest(original_url=url, thumb_url=url)
    #         # task = arun(create_task(request, token=token, is_async=False))
    #         # print(task)
    #         arun(image2nowatermark_image(url))
    #         # arun(image2nowatermark_image(url, token=token))

    #
    token = "BAIDUID=FF8BB4BF861992E2BF4A585A37366236:FG=1; BAIDUID_BFESS=FF8BB4BF861992E2BF4A585A37366236:FG=1; BIDUPSID=FF8BB4BF861992E2BF4A585A37366236; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; ab_sr=1.0.1_NjY5OWZiZDg5YTJmYTQzNWUyNzU1YjBmN2FlMDFiNjMyOTVhMDE3ZWVlYWY5N2Y2MTg4NGI1MzRmMmVjMjQyZjlhZTU2MmM1NDRlMmU4YzgwMzRiMjUyYTc4ZjY1OTcxZTE4OTA4YTlmMWIwZWUzNTdiMzlhZTRiM2IzYTQ0MjgyMzc2MjQwMGRlYzZlZDhjOTg5Yzg4NWVjMTNiZmVmZQ==; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; H_WISE_SIDS=60273_60360_60623_60664_60678_60684_60700"
    # # token='BAIDUID=F2185337B2F3F85DAB5D2E661BC00C8D:FG=1; BDUSS=hNQkdpbjBOT05EVjRCSFp3TUF-TXFKWHktcFppUGNyd0xZZGp3Mkp6TmVnbFptSVFBQUFBJCQAAAAAAAAAAAEAAACsbZVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF71LmZe9S5mOX; BDUSS_BFESS=hNQkdpbjBOT05EVjRCSFp3TUF-TXFKWHktcFppUGNyd0xZZGp3Mkp6TmVnbFptSVFBQUFBJCQAAAAAAAAAAAEAAACsbZVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF71LmZe9S5mOX; MAWEBCUID=web_axHhqlIWargVQsXuskqOnMzVXDWQHqQXOpFPkPVSvXFIwTNYaC; PSTM=1716434076; BIDUPSID=5FEB509ECAE0F7843030FD4ECC0800F8; newlogin=1; MCITY=-315%3A; H_WISE_SIDS_BFESS=60360_60674; indexPageSugList=%5B%22%E8%AF%81%E4%BB%B6%E7%85%A7%20%E7%94%B7%22%2C%22%E6%85%88%E7%A6%A7%E5%92%8C%E6%9D%8E%E8%8E%B2%E8%8B%B1%22%2C%22%E7%AE%80%E9%A1%BF%E7%81%AF%E5%85%B7%20%E9%81%A5%E6%8E%A7%E5%99%A8%22%2C%22%E5%88%B0%E5%BD%93%E9%81%93%E5%A3%AB%E9%82%A3%E4%BA%9B%E5%B9%B4%20%E8%B1%86%E7%93%A3%22%2C%22%E9%81%93%E5%A3%AB%20%E5%8D%A1%E9%80%9A%22%2C%22%E9%81%93%E5%A3%AB%22%2C%22%E6%88%91%E5%BD%93%E9%81%93%E5%A3%AB%E9%82%A3%E4%BA%9B%E5%B9%B4%22%2C%22%E8%AF%BB%E6%9E%B6%22%2C%22%E6%9D%B0%E8%AF%BA%E6%AF%94%E5%88%A9%20%E5%AF%B9%E6%AF%94%E7%85%A7%20%E5%8D%95%E8%86%9D%E8%B7%AA%E5%9C%B0%22%5D; BAIDUID_BFESS=F2185337B2F3F85DAB5D2E661BC00C8D:FG=1; BDRCVFR[C0p6oIjvx-c]=I67x6TjHwwYf0; delPer=0; PSINO=5; BDRCVFR[C0sZzZJZb70]=mk3SLVN4HKm; BA_HECTOR=alal0125ah0h0h0l8k8l0l01blu4191jd049m1u; ZFY=C8vEYu7ZbY0zTEITG3A0aWCevri4:BT:B0H1NpNZdQWKM:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=60360_60674_60683_60694_60572; BCLID=11757829139010941756; BCLID_BFESS=11757829139010941756; BDSFRCVID=pZCOJexroG3bGRntFj9auQWaJgKKv3JTDYLE8yu9T4VNR5DVYtg8EG0Pt_ZYMak-XolpogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=pZCOJexroG3bGRntFj9auQWaJgKKv3JTDYLE8yu9T4VNR5DVYtg8EG0Pt_ZYMak-XolpogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJkH_KthJIP3e4515Pr_q4tJbq58etJXfaO4Vp7F54nKDp0R0JbI0J0h5p6vaP3m066MaM-ELDOxsMT4QfJJhxuH-qoKel5tQH5MXprN3KJmf-Op2hO0ytDNbHOE2-biW2tH2Mbdax7P_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6KbD6bQDH8Oq-jeHDrKBRbaHJOoDDv8QxRcy4LbKxnxJhoe0H6JXt3LBJnfEpjlbURxqqjy3-OkbfQ9babTQ-tbBp3k8MQXbn7FQfbQ0hOe5RvnMe5a2JK2MJ7JOpvsDxnxy-umQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IHJbufoID2fIvDqTrP-trf5DCShUFs5J3dB2Q-XPoO3KOGqpoh5b6b2xKJb-bCb4biQPjNoMbgy4op8P3y0bb2DUA1y4vpX4bOBeTxoUJ2-bjWS-cV-xTqjbIebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0MD8xDT8Bj6Pq5fcj2nQXK4_tVTrJabC3qMcJXU6q2bDeQNba0hjXbgcBVRjaLx3HOR3oynD5yl0vWtv4qnctfGPJ-qr4Jlb4otbTeMonDh83Bn6kW4oWHGbyWPJO5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRAHoK-h3j; H_BDCLCKID_SF_BFESS=tJkH_KthJIP3e4515Pr_q4tJbq58etJXfaO4Vp7F54nKDp0R0JbI0J0h5p6vaP3m066MaM-ELDOxsMT4QfJJhxuH-qoKel5tQH5MXprN3KJmf-Op2hO0ytDNbHOE2-biW2tH2Mbdax7P_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6KbD6bQDH8Oq-jeHDrKBRbaHJOoDDv8QxRcy4LbKxnxJhoe0H6JXt3LBJnfEpjlbURxqqjy3-OkbfQ9babTQ-tbBp3k8MQXbn7FQfbQ0hOe5RvnMe5a2JK2MJ7JOpvsDxnxy-umQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IHJbufoID2fIvDqTrP-trf5DCShUFs5J3dB2Q-XPoO3KOGqpoh5b6b2xKJb-bCb4biQPjNoMbgy4op8P3y0bb2DUA1y4vpX4bOBeTxoUJ2-bjWS-cV-xTqjbIebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0MD8xDT8Bj6Pq5fcj2nQXK4_tVTrJabC3qMcJXU6q2bDeQNba0hjXbgcBVRjaLx3HOR3oynD5yl0vWtv4qnctfGPJ-qr4Jlb4otbTeMonDh83Bn6kW4oWHGbyWPJO5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRAHoK-h3j; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; ab_sr=1.0.1_NTY4Y2RjNTU5MWYzM2IyZjY4M2EzMWNjYWM1MWRhYjdlZDhmZTdkZGQ1NGE0MGFkZDU0NWQzNTU1OWJiZDllZmU4YjcyZDIyNTJiNzYxOWQ4OGM1MjQ2ODQzYTM2OGQ3YjdkMzQxZWI4Y2U5ZjQ3ZWZkYTQ2M2I3Yzc2MDkxMjBhZjczODNjMDNmNTAxMzhiZDg2ZmU0MTIwZTUxYWMxNQ==; H_WISE_SIDS=60360_60674_60683_60694_60572'
    # request = BDAITPZSRequest(original_url=url, thumb_url=url)

    url = "https://oss.ffire.cc/files/shuiyin.jpg"
    url = "https://oss.ffire.cc/files/nsfw.jpg"

    request = BDAITPZSRequest(
        type="1",
        # picInfo=image_to_base64(url),
        original_url=url,
        thumb_url=url
    )
    arun(create_task(request, is_async=False, response_format='url'))

    # arun(get_task('cr84hhue1pn8m151of3g', response_format='url'))

    # url = "https://oss.ffire.cc/files/kling_watermark.png"
    # url = "https://cdn.meimeiqushuiyin.cn/2024-10-20/removeBg/tmp_037244e2d6e1ebb8aa6ae3e98584f7b0482fed4ec5ecae98.jpg"
    #
    # request = BaiduImageProcessRequest(
    #     task="matting",
    #     image=url,
    # )
    #
    # arun(image_process(request))
