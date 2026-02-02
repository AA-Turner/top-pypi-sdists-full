#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : icons
# @Time         : 2024/12/3 16:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://app.napkin.ai/api/v1/auth/sessions
import json

from meutils.pipe import *
from meutils.schemas.napkin_types import BASE_URL, ASSETS_BASE_URL, IconsSimilarRequest, Icon, IconsSimilarResponse


async def icons_similar(request: IconsSimilarRequest):
    headers = {

        "cookie": "napkin.identity.visitor=visitor%409e2a59af-19ad-4dc3-96c8-9efbca71c547; napkin.analytics.device_id=d_950e4683-ae41-4941-b9a7-7e8deba8e669_1733214660768; _ga=GA1.1.511154647.1733214661; _fbp=fb.1.1733214661606.54464059277067597; _tt_enable_cookie=1; _ttp=SFxRhdE5PO5Rslohwet46IwiaB3.tt.1; _clck=16odoyg%7C2%7Cfre%7C0%7C1798; intercom-id-zrfc296i=6eb3740a-9c79-4681-87ec-532e4334816f; intercom-device-id-zrfc296i=f282621f-dcec-429b-90c0-fc98bd9dbb71; _ga_NM0S4FZ9JH=GS1.1.1733214661.1.0.1733214667.0.0.0; napkin.app.identity.session=NGJlMjdiZGEtZGEwNi00ZWE5LTkwMjEtN2U4ODAyNjE5NGJm.5092981dc495fe0041ed99fc68dcefa4ba26a0f6; intercom-session-zrfc296i=MGpOUDEvRlE3ZlRyUkhmaUdsVmZjYXNQT2lJYSsxYitaWDhTT0tMWlJFVkVuVjBwTno5emJydVd3VUhvKzlvRC0tLys4ZEp5a0F5M1YzNkFOazJUV2Nudz09--d6be7442da979794afe682b2e044bf51bd19ac88; _clsk=yficge%7C1733214772932%7C9%7C1%7Cr.clarity.ms%2Fcollect; _ga_L149GZ61DV=GS1.1.1733214675.1.1.1733215282.58.0.0",
        "origin": "https://app.napkin.ai",

        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    payload = request.model_dump()

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post(
            "/features/text/icons_similar",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(data)
        response = IconsSimilarResponse(**data)

        return response.model_dump()


if __name__ == '__main__':
    request = IconsSimilarRequest(caption="一杯咖啡与灵感的邂逅")
    arun(icons_similar(request))
