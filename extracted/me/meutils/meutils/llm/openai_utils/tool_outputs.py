#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tool_outputs
# @Time         : 2024/7/25 18:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
import mimetypes

import pandas as pd

from meutils.pipe import *


def web_browser_outputs_to_markdown(outputs):  # json_format
    yield pd.DataFrame(outputs).to_markdown()


def code_interpreter_outputs_to_markdown(outputs):
    pass


def drawing_tool_outputs_to_markdown(outputs):
    """
    :param outputs: [{'image': 'https://sfile.chatglm.cn/testpath/b49a5472-59d2-5dad-8949-e53dea03b326_0.png'}]
    :return:
    """
    for output in outputs:
        yield f"![]({output['image']})"


def outputs_to_markdown(*outputs):
    for output in outputs:
        if isinstance(output, dict):
            yield f"""```json\n{json.dumps(output, indent=4)}\n```"""

        elif isinstance(output, str) and output.startswith("http"):  # 链接
            mimetype, _ = mimetypes.guess_type(output)
            if mimetype:
                if mimetype.startswith("image"):
                    yield f"![]({output})"
                else:
                    yield f"[]({output})"
