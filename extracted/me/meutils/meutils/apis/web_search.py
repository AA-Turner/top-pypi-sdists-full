#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : web_search
# @Time         : 2024/5/10 11:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import langchain
from meutils.pipe import *
import urllib, json

def results(original_query):
    search_specs = [
         ["Google", "~googlequery", "https://www.google.com/search?q="],
         ["Duck Duck Go", "~duckduckgoquery", "https://duckduckgo.com/?q="],
         ["Google Images", "~googleimagequery", "https://www.google.com/search?tbm=isch&q="],
         ["Baidu", "~baiduquery", "http://www.baidu.com/s?wd="],
         ["Bing", "~bingquery", "http://www.bing.com/search?q="],
         ["Yahoo", "~yahooquery", "https://sg.search.yahoo.com/search?p="],
         ["Twitter", "~twitterquery", "https://mobile.twitter.com/search?q="],
         ["Reddit", "~redditquery", "https://www.reddit.com/search?q="]
    ]





if __name__ == '__main__':
    results(original_query="周杰伦")