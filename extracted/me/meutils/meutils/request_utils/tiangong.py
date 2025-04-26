from meutils.pipe import *
from meutils.decorators.retry import retrying

from playwright.sync_api import Playwright, sync_playwright


def my_request(request):
    """https://blog.csdn.net/B11050729/article/details/131293769
    """
    print(request.all_headers())


@retrying(predicate=lambda r: r and len(r['data']['chatDetailList'][0]['data']) < 5)
def response_parser(url):
    r = requests.get(url).json()
    # logger.debug(len(r['data']['chatDetailList'][0]['data']))
    return r


def run(playwright: Playwright) -> None:
    iphone = {}
    # iphone = playwright.devices['iPhone 15']

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(**iphone)
    page = context.new_page()

    page.on("request", my_request)
    page.goto("https://search.tiangong.cn/")
    logger.debug(page.url)

    page.get_by_placeholder("试试输入任何想了解的问题").fill("林俊杰")
    page.wait_for_load_state(state='networkidle')

    page.get_by_placeholder("试试输入任何想了解的问题").press("Enter")

    page.wait_for_load_state(state='networkidle')
    page.wait_for_url(page.url, wait_until='networkidle')

    page.wait_for_timeout(30 * 1000)
    logger.debug(page.url)

    page.screenshot(full_page=True, path='screenshot.png')
    page.pdf(path='p.pdf')
    conversationId = page.url.split('/')[-1]
    url = f"https://api-search.tiangong.cn/chat-user/api/chat/conversation/detail?conversationId={conversationId}"

    logger.debug(url)

    response = response_parser(url)
    response['data']['url'] = url

    #
    # new_page = new_page_info.value
    # new_page.wait_for_load_state()
    # print(new_page)
    #
    # page.screenshot(full_page=True, path='screenshot.png')
    # # print(page)
    # page.wait_for_load_state('networkidle')
    # page.wait_for_timeout(5000)
    #
    # page.pdf(path='p.pdf')

    # "//*[@id="app"]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div[2]"
    # "//*[@id="app"]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div[3]"

    #
    # page.locator("div").filter(has_text=re.compile(r"^参考$")).click()
    # with page.expect_popup() as page1_info:
    #     page.get_by_text("参考郭富城赛车时发生车祸：车辆故障被迫退赛 - 快科技mydrivers · 1郭富城赛车时发生车祸！回应来了 - 每日经济新闻nbd · 2郭富城赛车时发生车").click()
    # page1 = page1_info.value
    # page1.close()
    # page.locator(".el-scrollbar__view > div").click()
    #
    # with page.expect_popup() as page4_info:
    #     page.locator("#md-editor-v3-preview-wrapper").click()
    # page4 = page4_info.value
    # page4.close()
    # page.locator(".el-scrollbar__view > div").click()
    # with page.expect_popup() as page5_info:
    #     page.locator("#md-editor-v3-preview-wrapper").click()
    # page5 = page5_info.value
    # page5.locator("html").click(modifiers=["Meta"])
    # page5.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
