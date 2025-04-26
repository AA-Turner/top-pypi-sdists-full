#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ips
# @Time         : 2024/9/27 12:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 增加代理检测
# https://github.com/Sndeok/HarbourJ/blob/5bbbc4b6118df779929d1521270864753731b78a/jd_inviteDraw.py#L117

from meutils.pipe import *
from meutils.caches import rcache
from meutils.decorators.retry import retrying
from meutils.hash_utils import murmurhash
from meutils.config_utils.lark_utils import get_next_token_for_polling, get_series

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/XfjqszII3hZAEvtTOgecOgv2nye?sheet=c14b34"
FEISHU_URL_METASO = "https://xchatllm.feishu.cn/sheets/XfjqszII3hZAEvtTOgecOgv2nye?sheet=MXvEIN"

BASE_URL = "http://ip.chatfire.cn"
# BASE_URL = "http://api.xiequ.cn"

IPS = "58.240.255.226,110.42.51.201,154.37.214.121,154.40.54.76"


@rcache(ttl=60)
async def get_one_proxy(token: Optional[str] = None, feishu_url: str = "", from_redis: bool = True):
    feishu_url = feishu_url or FEISHU_URL
    if token:  # 按token分配固定的ip
        ips = await get_series(feishu_url=feishu_url, duplicated=True)

        idx = murmurhash(token, bins=len(ips))
        logger.debug(f"{idx}: {ips}")
        ip = ips[idx]

    else:
        # 随机获取ip: 如果从redis就是循环队列 check_proxy
        ip = await get_next_token_for_polling(feishu_url, from_redis=from_redis)
    # https://github.com/encode/httpx/pull/2879
    # proxies = {
    #     "http://": f"http://{ip}",  # 自建 38443
    #     "https://": f"http://{ip}",
    # }

    proxy = f"http://{ip}"

    logger.debug(f"proxy: {proxy}")

    return proxy


def checkip():  # 获取本地ip
    url = 'http://api.xiequ.cn/VAD/OnlyIp.aspx?yyy=123'
    response = requests.get(url).text
    return response


# ukey=7C4B6F4BF696311B9AB961F253184A20
# key=1ea276146ccb4149bf96f1cfcee1973a
async def add_ips(ips: Optional[str] = None):
    ips = (ips or IPS).split(',')
    params = {
        "uid": "134597",
        "ukey": "42EB7F0B846C187F1FDAF28873AE759E",
        "act": "del",
        "ip": "all"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=100) as client:
        resp = await client.get("/IpWhiteList.aspx", params=params)
        logger.debug(f"删除：{resp.text}")

        for ip in ips:
            params['ip'] = ip
            params['act'] = "add"
            resp = await client.get("/", params=params)

            logger.debug(f"添加：{resp.text}")
            await asyncio.sleep(5)


@rcache(ttl=25)
@retrying()
async def get_proxies(request_type: str = "httpx", **kwargs):
    params = {
        'num': '1',

        'act': 'get',
        'uid': '134597',
        'vkey': '07A1D82FDDE1E96DB5CEF4EF12C8125F',
        'time': '30',
        'plat': '1',
        're': '1',
        'type': '0',
        'so': '1',
        'ow': '1',
        'spl': '1',
        'db': '1'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=100) as client:
        resp = await client.get("/VAD/GetIp.aspx", params=params)
        ip = resp.text
        if request_type == "httpx":
            return f"http://{ip}"
        else:

            proxies = {
                # "http://": f"socks5://{ip}",
                # "https://": f"socks5://{ip}",

                "http": f"http://{ip}",
                "https": f"http://{ip}",

            }
        logger.debug(proxies)
        return proxies


async def check_proxy(proxy):
    try:
        async with httpx.AsyncClient(proxy=proxy) as client:
            response = await client.get("http://icanhazip.com", timeout=5)  # http://httpbin.org/ip
            logger.debug(response.status_code)
            logger.debug(response.text)

            return response.is_success
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    proxies = arun(get_proxies())
    # url = "http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=134597&vkey=07A1D82FDDE1E96DB5CEF4EF12C8125F&num=1&time=30&plat=1&re=1&type=0&so=1&ow=1&spl=1&addr=&db=1"
    # url = f"{BASE_URL}/VAD/GetIp.aspx?act=get&uid=134597&vkey=07A1D82FDDE1E96DB5CEF4EF12C8125F&num=1&time=30&plat=1&re=1&type=0&so=1&ow=1&spl=1&addr=&db=1"
    #
    # resp = httpx.Client(
    #     proxies=proxies,
    #     timeout=100
    # ).get(url)
    #
    # logger.debug(resp.text)
    ip = "http://proxy.chatfire.cn"
    ip = "http://chatfire:chatfire@110.42.51.201:38443"
    ip = "http://154.9.253.9:38443"
    ip = "http://154.9.252.28:38443"
    ip = "http://110.42.51.223:38443"
    ip = "http://154.40.54.76:38443"
    proxy = "http://120.26.134.112:22443"

    # arun(check_proxy(proxy))

    arun(get_one_proxy())

    # arun(add_ips())
    # arun(get_one_proxy(from_redis=True))
    # arun(get_one_proxy("FEISHU_URL", exclude_ips="154.40.54.76"))
    # arun(get_one_proxy("FEISHU_URL", exclude_ips="154.40.54.76", from_redis=True))
    # arun(get_one_proxy(from_redis=True))
