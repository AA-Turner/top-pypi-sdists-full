#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/10/18 13:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *


class A(BaseModel):
    a: Literal['a', 'b']


import streamlit as st
from streamlit_extras.streaming_write import write

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""


def stream_example():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.1)

    # # Also supports any other object supported by `st.write`
    # yield pd.DataFrame(
    #     np.random.randn(5, 10),
    #     columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    # )
    #
    # for word in _LOREM_IPSUM.split():
    #     yield word + " "
    #     time.sleep(0.05)


def f():
    with st.chat_message('assistant'):

        write('😘😘😘 嗨，我是你的解题小能手！\n\n **参考示例**：')



