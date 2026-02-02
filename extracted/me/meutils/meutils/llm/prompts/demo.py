#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/9/11 15:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.files_utils import to_url

# import imgkit
#
# # HTML代码
# html_content = """
# <html>
# <body>
# <h1>Hello, World!</h1>
# <p>This is a test.</p>
# </body>
# </html>
# """
#
# # 配置
# config = imgkit.config(wkhtmltoimage='path/to/wkhtmltoimage')
#
# # 转换HTML为图片
# imgkit.from_string(html_content, 'output.jpg', config=config)
#
# print("Image saved as output.jpg")

# from html2image import Html2Image
#
# hti = Html2Image()
#
# html_content = """
# <html>
# <head>
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <style>
#         body { font-family: Arial, sans-serif; }
#         @media (max-width: 600px) {
#             body { font-size: 14px; }
#         }
#         @media (min-width: 601px) {
#             body { font-size: 16px; }
#         }
#     </style>
# </head>
# <body>
#     <h1>Responsive Test</h1>
#     <p>This content should adapt to different screen sizes.</p>
# </body>
# </html>
# """
#
# hti.screenshot(html_str=html_content, save_as='output_desktop.png', size=(1920, 1080))
# hti.screenshot(html_str=html_content, save_as='output_mobile.png', size=(375, 812))

# from playwright.sync_api import sync_playwright
#
# # HTML代码
# html_content = """
# <html>
# <body>
# <h1>Hello, World!</h1>
# <p>This is a test.</p>
# </body>
# </html>
# """
#
# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.set_content(html_content)
#     page.screenshot(path="output.png")
#     browser.close()
#
# print("Image saved as output.png")
#
#

# HTML 内容，包含响应式 CSS
html_content = """
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
        }
        p {
            font-size: 16px;
        }
        @media (max-width: 600px) {
            h1 {
                font-size: 20px;
            }
            p {
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a test with responsive design.</p>
</body>
</html>
"""

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

html_content = Path('x.html').read_text()


async def capture_screenshot(page, width, height, filename):
    await page.set_viewport_size({"width": width, "height": height})
    await page.screenshot(path=filename)
    print(f"Screenshot saved as {filename}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)

        with tempfile.NamedTemporaryFile(suffix='.png') as file:
            logger.debug(file.name)

            # # 捕获桌面版截图
            # await capture_screenshot(page, 1280, 800, "output_desktop.png")
            #
            # # 捕获平板版截图
            # await capture_screenshot(page, 768, 1024, "output_tablet.png")

            # 捕获移动版截图
            await capture_screenshot(page, 375, 812, file.name)
            url = await to_url(file.name)
            logger.debug(url)

        await browser.close()


if __name__ == '__main__':
    arun(main())
