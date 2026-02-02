#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2025/12/29 16:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def getali231():
    file = get_resolve_path('../../data/apis/fireyejs.js', __file__)
    # node执行231.js
    res = subprocess.run(['node', file], capture_output=True, text=True)
    # logger.debug(res)

    ali231 = re.search(r'###(.*?)###', res.stdout).group(1)
    # print(ali231)
    return ali231


if __name__ == '__main__':
    print(getali231())

    # import execjs
    # import pathlib
    #
    # # 1. 读取 JS 源码（包含 code.js 和 fireyejs.js 合并后的完整代码）
    # js_code = pathlib.Path("fireyejs.js").read_text(encoding="utf-8")
    #
    #
    #
    # # 2. 初始化运行环境
    # ctx = execjs.compile(js_code)
    #
    # # 3. 调用函数
    # ali231 = ctx.call("getToken")
    # print("ali231 =", ali231)
