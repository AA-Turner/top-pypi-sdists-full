#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/12/27 17:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/OldGmXfoJZ9cObKU5f-q2Q

from meutils.pipe import *
from playwright.async_api import Playwright, async_playwright, expect, Request, Response


@alru_cache(ttl=3600)
async def get_new_browser(headless: bool = True):
    logger.info("初始化浏览器")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)

    return browser


@alru_cache(ttl=3600)
async def get_new_page(headless: bool = True, iphone: Optional[str] = None, browser_type: str = "webkit"):
    """

    :param headless:
    :param iphone: 'iPhone 13'
    :return: WebKit
    """

    playwright = await async_playwright().start()  # 打开未关闭
    if browser_type == "webkit":
        browser = await playwright.webkit.launch(headless=headless)
    else:
        browser = await playwright.chromium.launch(headless=headless)  # todo: close

    logger.info("初始化浏览器-页面")

    iphone = iphone and playwright.devices[iphone] or {}

    context = await browser.new_context(**iphone)
    page = await context.new_page()
    return page


# 监听所有的请求和响应
async def open(headless):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, args=["--start-maximized"])
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        page.on("response", filter_response)
        ''''''


async def filter_response(response):
    if 'souhu......' in response.url:
        response_data = await Response.body(response)
        if isinstance(response_data, bytes):
            response_data = response_data.decode()  # 请求返回数据


async def my_request(request):
    """https://blog.csdn.net/B11050729/article/details/131293769
    """
    print(await request.all_headers())


async def _monitor_requests(request: Request, method):
    if request.method == method:
        # _ = await request.post_data()

        _ = request.post_data_json

        logger.debug(f"{method}: \n {request.url}")
        return _


async def monitor_requests_get(request: Request, method='GET'):
    return _monitor_requests(request, method)


async def monitor_requests_put(request: Request, method='PUT'):
    return _monitor_requests(request, method)


async def monitor_requests_post(request: Request, method='POST'):
    return _monitor_requests(request, method)
