#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/7/21 10:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 爬虫学习playwright  https://blog.csdn.net/wx17343624830/article/details/130622056
#
# https://news.sohu.com/a/685709792_121368355
# 公众号爬虫

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://mp.weixin.qq.com/s?__biz=Mzg2MjIwODc3Mw==&amp;mid=2247493349&amp;idx=1&amp;sn=e21830aa26c956be38a5b47a33cfa2e7&amp;chksm=ce09f08ff97e7999caf268e06510e4ab00bca6d0e89a6e96f2ff1207cc57cea698aa3b973d36&amp;mpshare=1&amp;scene=1&amp;srcid=1101LIjE8Yh1t8wfX7gu3JQQ&amp;sharer_shareinfo=a31a8170ed734f0c59b1713c3f20ec57&amp;sharer_shareinfo_first=a31a8170ed734f0c59b1713c3f20ec57#wechat_redirect")
    # page.wait_for_load_state('networkidle')
    # page.pdf(path='p.pdf')

    # print(page.title())
    # html = page.content()
    # page.wait_for_timeout(5000)
    # print(page.query_selector_all("""//text()"""))

    # page.screenshot(full_page=True, path='screenshot.png')
    # page.locator('//*[@id="img-content"]').screenshot(path='screenshot11.png')  # 带标题
    # page.locator("#js_content").screenshot(path='screenshot22.png')  # 不带标题

    blog = page.locator("#js_content")
    print(page.locator('//*[@id="img-content"]').inner_text())

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
