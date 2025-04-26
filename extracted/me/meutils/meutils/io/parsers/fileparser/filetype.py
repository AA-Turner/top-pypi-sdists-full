#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : filetype
# @Time         : 2023/7/15 15:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 文件或扩展名被更改

from meutils.pipe import *

import filetype
import magic
import mimetypes

import mimetypes

# mimetype, _ = mimetypes.guess_type('example.txt')
# print(mimetype)
#
# import magic
#
# file_type = magic.from_file('example.pdf', mime=True)
# print(file_type)
#
# import filetype
#
# kind = filetype.guess('example.jpg')
# if kind is None:
#     print('Cannot guess file type!')
# else:
#     print('File extension: %s' % kind.extension)
#     print('File MIME type: %s' % kind.mime)

if __name__ == '__main__':
    # mimetype, _ = mimetypes.guess_type('example.mp3')
    mimetype, _ = mimetypes.guess_type('https://www.baidu.com/img/flexible/logo/pc/result@2.png')

    print(mimetype)
    print(_)
