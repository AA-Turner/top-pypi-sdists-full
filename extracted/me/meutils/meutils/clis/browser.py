#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : browser
# @Time         : 2023/11/29 15:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 持续刷新不掉线

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.playwright_utils.reload import refresh_cookies

from playwright.async_api import Playwright, async_playwright

cli = typer.Typer(name="模拟浏览器")


@retrying
async def deepseek_sign_in(  # todo
        user_file: str = '',
        headless: bool = False,
        timeout: int = 1000,
        **kwargs
):
    url = "https://chat.deepseek.com/sign_in"
    storages = []
    df = pd.read_csv(user_file, sep=' ', names=['user', 'password'])
    for _, user, password in df.itertuples():
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context()

            page = await context.new_page()

            ####################################################################################todo：linux模拟登录有问题

            await page.goto(url)
            await page.wait_for_load_state(state='load')
            await page.wait_for_load_state(state='networkidle')
            await page.wait_for_load_state(state='domcontentloaded')
            await page.wait_for_timeout(timeout=timeout)

            await page.get_by_placeholder("请输入手机号/邮箱地址").click()
            await page.get_by_placeholder("请输入手机号/邮箱地址").fill(user)
            await page.get_by_placeholder("请输入手机号/邮箱地址").press("Tab")
            await page.get_by_placeholder("请输入密码").fill(password)
            await page.get_by_role("img").nth(3).click()
            await page.get_by_role("button", name="登录").click()

            await page.wait_for_load_state(state='load')
            await page.wait_for_load_state(state='networkidle')
            await page.wait_for_load_state(state='domcontentloaded')
            await page.wait_for_timeout(timeout=timeout)

            # # 聊天
            await page.get_by_placeholder("请输入问题。Enter 发送，Ctrl + Enter 换行").fill("你是谁")
            await page.get_by_role("button", name="发送").click()

            ####################################################################################

            # ---------------------
            # 保存状态文件
            storage_state = f'{Path(user_file).parent}/deepseek_{user}.json'
            storage = await context.storage_state(path=storage_state)  # 覆盖更新
            storages.append(storage)
            await context.close()
            await browser.close()

    return storages


@cli.command()
def prun(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = True,
        storage_state: str = 'kimi_state.json',
        kwargs: str = typer.Option(None, help="The kwargs to parse.")
):
    """
    # 刷新cookies
    mecli-browser --no-headless --url  https://kimi.moonshot.cn/
    # 模拟登录
    mecli-browser --no-headless --kwargs '{"task": "deepseek", "user_file":"deepseek.txt"}'
    python browser.py --kwargs '{"task": "deepseek", "user_file":"deepseek.txt"}' --no-headless

    ps -ef | grep "meutils.clis.browser*" | awk '{print $2}' | xargs kill -9

    """
    kwargs = kwargs and json.loads(kwargs) or {}
    logger.debug(kwargs)
    if kwargs.get('task') == 'deepseek':  # TASK
        task = deepseek_sign_in(headless=headless, **kwargs)

    else:
        task = refresh_cookies(url, headless, storage_state)

    logger.info(asyncio.run(task))


@cli.command()
def refresh(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = True,
        storage_state: str = 'kimi_*.json',
        timeout: int = 3,
        delay: int = 30,
        only_once: bool = True

):
    """todo：优化内存占用【部署个服务，定时拉取呢？】
    mecli-browser refresh --delay 10 --storage-state "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/playwright_utils/kimi*.json"
    """
    refresh_cookies(url, headless, storage_state, timeout, delay, only_once)


if __name__ == '__main__':
    cli()
    # storage_state = '/Users/betterme/PycharmProjects/AI/MeUtils/meutils/clis/kimi_*.json'
    # print(Path(Path(storage_state).parent).glob(Path(storage_state).name) | xlist)
