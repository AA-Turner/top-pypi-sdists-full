#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : llm_qa
# @Time         : 2024/4/24 18:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser
from langchain.output_parsers import PydanticOutputParser


class ExpressRequest(BaseModel):
    express_no: str = Field(description="快递单号")
    phone_number: str = Field(description="手机号")

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)
        self.express_no = f"{self.express_no}:{self.phone_number[-4:]}"


parser = PydanticOutputParser(pydantic_object=ExpressRequest)

print(parser.get_format_instructions())


# parser = OutputFixingParser.from_llm(
#     parser=parser,
#     # llm=ChatOpenAI(temperature=0),
#     llm=ChatOpenAI(model="kimi"),
# )
#
text = """
快递号
SF1442153365663
手机号是
121215651
"""
#
# result = parser.parse(text)  # 错误被自动修正
# print(text)
# print(result)


print(parser.parse("""{'快递号': SF1442153365663}"""))


import openai

openai.OpenAI