#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : reload
# @Time         : 2023/12/27 11:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 保持常驻状态并刷新

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.playwright_utils import get_new_browser

from playwright.async_api import Playwright, async_playwright


# @retrying
# async def _refresh_cookies(url, headless=True, storage_state: Optional[Path] = '', timeout: int = 0, delay: int = 1):
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch(headless=headless)
#         while delay:
#             context = await browser.new_context(storage_state=storage_state if Path(storage_state).exists() else None)
#
#             page = await context.new_page()
#
#             await page.goto(url)
#             await page.wait_for_load_state(state='load')
#             await page.wait_for_load_state(state='networkidle')
#             await page.wait_for_load_state(state='domcontentloaded')
#             await page.wait_for_timeout(timeout=timeout * 1000)
#
#             await asyncio.sleep(delay)
#             await page.reload()
#             await context.storage_state(path=storage_state)  # 保存状态文件，覆盖更新
#             logger.success(f"刷新cookies成功: {storage_state}")


@retrying
async def _refresh_cookies(
        url: str,
        headless=True,
        storage_state: Optional[Path] = '',
        timeout: int = 1,
        delay: int = 5,
        only_once: bool = True
):
    browser = await get_new_browser(headless=headless)

    while True:
        context = await browser.new_context(storage_state=storage_state if Path(storage_state).exists() else None)
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_load_state(state='load')
        await page.wait_for_load_state(state='networkidle')
        await page.wait_for_load_state(state='domcontentloaded')
        await page.wait_for_timeout(timeout=timeout * 1000)

        await page.reload()
        await asyncio.sleep(delay)

        await context.storage_state(path=storage_state)  # 保存状态文件，覆盖更新
        logger.success(f"刷新cookies成功: {storage_state}")

        await context.close()
        await page.close()

        if only_once: break  # 默认一次


def refresh_cookies(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = True,
        storage_state: str = 'kimi*.json',
        timeout: int = 3,
        delay: int = 5,
        only_once: bool = True
):
    """刷新cookies 后台常驻"""

    ps = Path(Path(storage_state).parent).glob(Path(storage_state).name)

    fn = partial(_refresh_cookies, url=url, headless=headless, timeout=timeout, delay=delay, only_once=only_once)

    tasks = [fn(storage_state=storage_state) for storage_state in ps]
    tasks | xAsyncio()


if __name__ == '__main__':
    refresh_cookies(storage_state='kimi_cookies.json', headless=False, only_once=False)
