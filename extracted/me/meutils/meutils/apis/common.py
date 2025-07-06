#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/12/4 16:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying
from urllib.parse import quote


@retrying
@lru_cache(maxsize=1024)
def shorten_url(url, shortener='dagd'):
    """
        https://w3.do/k0xi_szO
        https://da.gd/haFET # 耗时更短
        https://tinyurl.com/ym8xkpyl
        https://clck.ru/36vUv9 # 微信没法直接跳转

    :param url:
    :param shortener:
    :return:
    """
    if shortener.startswith('w3'):
        url = f"https://w3.do/get?url={url}"
        url = f"""https://{requests.get(url).json().get("url")}"""

    elif shortener.startswith('ft'):  # https://www.ft12.com/
        API_KEY = "18550288233@81fbd6ad8469aba2b45e26929d4ff6a8"

        url = f"http://two.ft12.com/api.php?format=json&url={quote(url)}&apikey={API_KEY}"
        url = f"""{requests.get(url).json().get("url")}"""


    else:
        from pyshorteners import Shortener

        url = Shortener().__getattr__(shortener).short(url)
    return url


@retrying
@lru_cache(maxsize=1024)
def data2qrcodeurl(data, qrcode_api: str = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}", shortened: bool = False):
    """
        apis = [
            "https://api.isoyu.com/qr/?m=1&e=L&p=8&url={}",
            "https://api.qrserver.com/v1/create-qr-code/?data={}",
            # "https://api.qrserver.com/v1/create-qr-code/?size=500×500&data={}",
            "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}"
        ]

        for api in apis:
            print(to_qrcode(url, api))

    :param url:
    :param qrcode_api:
    :return: https://api.isoyu.com/qr/?m=1&e=L&p=20&url=https://vip.chatllm.vip/
    """
    url = qrcode_api.format(data)

    # url = qrcode_api.format(quote(data))

    return shorten_url(url, 'w3') if shortened else url


@retrying
@lru_cache
def qrcodeurl2data(qrcodeurl):
    """

    :param qrcodeurl: https://api.isoyu.com/qr/?m=1&e=L&p=8&url=123
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE '
    }
    return requests.get(qrcodeurl, headers=headers).content


if __name__ == '__main__':
    # url = "https://vip.chatllm.vip/"
    # url = "http://www.zhihechat.com/#home"

    "https://nextchat.chatfire.cn/#/?settings={\"key\":\"{key}\"}"
    url = """https://ichat.chatllm.vip/#/?settings={"key":"sk-"}"""
    # url = "http://111.173.117.175:40000/rag/"
    url = "http://oss.cloudbellai.com/file/%E5%8A%9F%E8%83%BD%E7%82%B9%E5%9B%BE%E7%89%87/MES%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88/%E3%80%90%E6%8E%A8%E8%8D%90%E3%80%91MES%E7%B3%BB%E7%BB%9F%E8%A7%84%E5%88%92%E4%B8%8E%E5%AE%9E%E6%96%BD/MES%E7%B3%BB%E7%BB%9F%E8%BE%B9%E7%95%8C%E4%B8%8E%E9%9B%86%E6%88%90.png"
    # print(shorten_url(url, 'w3'))
    # print(shorten_url(url, 'dagd'))
    # print(shorten_url(url, 'clckru'))
    # print(shorten_url(url, 'tinyurl'))
    # print(shorten_url(url, 'ft'))
    print(shorten_url(url))

    from meutils.io.image import image_to_base64

    # apis = [
    #     # "https://api.isoyu.com/qr/?m=1&e=L&p=8&url={}",
    #     # "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}",
    #     # "https://api.qrserver.com/v1/create-qr-code/?data={}",
    #     "https://api.qrserver.com/v1/create-qr-code/?size=500×500&data={}",
    # ]
    #
    # for api in apis:
        # print(data2qrcodeurl('知盒欢迎你', api, shortened=True))
        # print(data2qrcodeurl("http://www.zhihechat.com/#home", api, shortened=True))
        # print(data2qrcodeurl("https://www.baidu.com", api, shortened=True))

        # print(data2qrcodeurl(image_to_base64('qr.png'), api, shortened=True))

        # break

    # print(qrcodeurl2data('https://api.isoyu.com/qr/?m=1&e=L&p=8&url=123'))


