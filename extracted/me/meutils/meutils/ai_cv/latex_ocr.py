#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr_latex
# @Time         : 2023/10/27 11:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

@retrying
@lru_cache
def latex_ocr(file: Optional[Union[str, bytes]], token: Optional[str] = None):
    api_url = "https://server.simpletex.cn/api/latex_ocr"  # 接口地址
    header = {"token": token or os.getenv('LATEX_OCR_TOKEN')}  # 鉴权信息，此处使用UAT方式

    file_bytes = file
    filename = 'x.png'
    if isinstance(file, str):
        file_bytes = Path(file).read_bytes()
        filename = Path(file).name

    file = [("file", (filename, file_bytes))]  # 请求文件,字段名一般为file

    res = requests.post(api_url, files=file, headers=header)  # 使用requests库上传文件
    logger.debug(res.json())
    return res.json().get('res', {}).get('latex')


if __name__ == '__main__':
    rprint(latex_ocr(open('test.png', 'rb').read()))  # \text{求极限}\lim_{x\to0}\frac{e^x-e^{-x}-2x}{x-\sin x}
