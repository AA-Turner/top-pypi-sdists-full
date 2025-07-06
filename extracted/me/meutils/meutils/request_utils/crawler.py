#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : crawler
# @Time         : 2021/9/2 下午2:47
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : httpx异步优化
# @Description  : https://blog.csdn.net/u013332124/article/details/80621638
# pd: https://blog.csdn.net/zhang862520682/article/details/86701078

from lxml.etree import HTML
from meutils.request_utils import request, request4retry


class Crawler(object):

    def __init__(self, url, encoding=None, *args, **kwargs):
        self.url = url
        self.html = self.get_html(url, encoding)

    def xpath(self, _path="//text()", **_variables):
        return self.html.xpath(_path, **_variables)

    @staticmethod
    def get_html(url, encoding='utf-8'):
        r = request4retry(url, return_json=False, encoding=encoding)
        return HTML(r.text)


if __name__ == '__main__':
    from meutils.pipe import *
    url = "https://top.baidu.com/board?tab=realtime"

    #
    #
    # _ = Crawler(url).xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[*]/div[2]/a/div[1]//text()')
    # print("\n".join(_))



    # from meutils.request_utils.crawler import Crawler
    #
    # url = 'http://10.2.41.63:8004/bert_models/bert-base-uncased/'
    # Crawler(url).xpath('//@href')

    # c = Crawler('https://www.maoyan.com/board?offset=0') # 猫眼top10
    # _ = c.xpath('//*[@id="app"]/div/div/div/dl/dd[*]/div/div/div[1]//text()') | xgroup(7)
    # top10 = pd.DataFrame(_)

    # from meutils.request_utils.crawler import Crawler
    # w = "宝能公馆1288"
    # url = f"https://m.fang.com/fangjia/sh_list_pinggu/?keyword={w}&city=sh&r=0.9648271001521231"
    #
    # print(Crawler(url).xpath('//*[@id="houselist"]/li/a//text()'))

    url  = "https://chat.tune.app/?id=7f268d94-d2d4-4bd4-a732-f196aa20dceb"
    url = "https://app.yinxiang.com/fx/8b8bba1e-b254-40ff-81e1-fa3427429efe"

    print(Crawler(url).xpath('//script//text()'))

    # html_content = httpx.get(url).text


    # # 正则表达式匹配以 "/_next/static/chunks/7116-" 开头的 JS 文件
    # pattern = r'(/_next/static/chunks/7116-[^"]+\.js)'
    #
    # # 使用 re.findall() 找到所有匹配项
    # matches = re.findall(pattern, html_content)
    #
    # "/_next/static/chunks/7116-aed224a0caaab94c.js"
    #
    # # 打印结果
    # for match in matches:
    #     print(match)
