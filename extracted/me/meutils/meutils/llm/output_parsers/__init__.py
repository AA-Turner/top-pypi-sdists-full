#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2024/4/24 13:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/qq_56591814/article/details/134774051

from meutils.pipe import *

from langchain.schema import BaseOutputParser
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser, SimpleJsonOutputParser


if __name__ == '__main__':
    #     text = """
    #     ```json
    # {
    #   "prompt": "中文标题：酒入愁肠\n英文标题：Wine and Sorrows\n\n歌词结构：\n[Intro]\n（独奏）\n\n[Verse 1]\n月光洒在破旧的篱笆，\n李白提壶独自彷徨。\n酒香飘逸入云端，\n笔下是豪迈的想象。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Verse 2]\n江水流淌带走忧伤，\n杜甫凝眉思国家。\n文章锋利剑如霜，\n心中苦，却言者无罪当。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Bridge]\n一千年来谁能懂，\n酒与愁是最深的重。\n历史长河波澜壮，\n诗人眼中看尽繁华空。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Outro]\n（独奏）",
    #   "tags": "传统民谣",
    #   "title": "酒入愁肠/Wine and Sorrows"
    # }
    # ```
    #     """
    #
    #     # PydanticOutputParser.parse()
    #
    #     print(JsonOutputParser().parse(text=text))
    #     print(PydanticOutputParser().parse_obj(text=text))
    # this code example is complete and should run as it is


    # @llm_prompt(output_parser='auto')  # `auto` | `json` | `str` | `list`
    # def write_name_suggestions(company_business: str, count: int):
    #     """ Write me {count} good name suggestions for company that {company_business}
    #     """
    #     pass

    # print(write_name_suggestions(company_business="sells cookies", count=5))

    from langchain_decorators import llm_prompt
    from pydantic import BaseModel, Field

    #
    # class TheOutputStructureWeExpect(BaseModel):
    #     name: str = Field(description="The name of the company")
    #     headline: str = Field(description="The description of the company (for landing page)")
    #     employees: list[str] = Field(description="5-8 fake employee names with their positions")
    #
    #
    # @llm_prompt()
    # def fake_company_generator(company_business: str) -> TheOutputStructureWeExpect:
    #     """ Generate a fake company that {company_business}
    #     {FORMAT_INSTRUCTIONS}
    #     """
    #     return
    #
    #
    # company = fake_company_generator(company_business="sells cookies")
    #
    # # print the result nicely formatted
    # print("Company name: ", company.name)
    # print("company headline: ", company.headline)
    # print("company employees: ", company.employees)
    #


    @llm_prompt
    def write_me_short_post(topic:str, platform:str="twitter", audience:str = "developers")->str:
        """
        Write me a short header for my post about {topic} for {platform} platform.
        It should be for {audience} audience.
        (Max 15 words)
        """
        return

    # run it naturaly
    print(write_me_short_post(topic="starwars"))
