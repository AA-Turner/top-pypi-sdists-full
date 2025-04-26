#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : spider
# @Time         : 2024/1/18 10:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: pdf/截图

from meutils.pipe import *
from meutils.playwright_utils import get_new_page

from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request

router = APIRouter()


@router.get("/playwright")  # todo: 多个url
@alru_cache(maxsize=10240, ttl=3 * 24 * 3600)
async def get_content(
        url: str,
        # page=Depends(get_new_page) # Depends get_new_page 里面的参数也会暴露出来
):
    url = url.strip()

    page = await get_new_page()
    await page.goto(url)

    if url.startswith("https://mp.weixin.qq.com"):
        content = await page.inner_text('//*[@id="page-content"]')  # 使用page.query_selector_all获取a节点列表
    else:
        # todo: xpath
        # wait
        await page.wait_for_load_state(state='load')
        await page.wait_for_load_state(state='networkidle')
        await page.wait_for_load_state(state='domcontentloaded')
        await page.wait_for_selector('body')

        content = await page.inner_text('body')

    return {"content": content}


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()
    app.include_router(router)
    app.run(port=39666)
