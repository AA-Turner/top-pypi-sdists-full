#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : screenshot
# @Time         : 2024/9/18 16:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_url
from meutils.playwright_utils import get_new_page
from meutils.schemas.playwright_types import ScreenshotRequest

from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request

router = APIRouter()

HTML_PARSER = re.compile(r'```html(.*?)```', re.DOTALL)


@router.post("/screenshot")  # todo: 多个url
async def capture_screenshot(
        request: ScreenshotRequest,
):
    htmls = HTML_PARSER.findall(request.html)
    if htmls:
        request.html = htmls[0]

    page = await get_new_page()
    await page.set_content(request.html)
    await page.set_viewport_size({"width": request.width, "height": request.height})

    with tempfile.NamedTemporaryFile(suffix='.png') as file:
        await page.screenshot(path=file.name)
        url = await to_url(file.name)
        page.close()
        return {"url": url}


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()
    app.include_router(router)
    app.run(port=39666)
