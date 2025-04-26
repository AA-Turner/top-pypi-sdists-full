#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/4/24 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://python.langchain.com/docs/modules/model_io/output_parsers/types/pydantic/

from meutils.pipe import *
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


# 使用Pydantic创建一个数据格式，表示材料
class Flower(BaseModel):
    name: str = Field(description="name of a Material")
    colors: List[str] = Field(description="the colors of this Material")


# 定义一个用于获取某种材料的颜色列表的查询
flower_query = "Generate the charaters for a random Material."

# 定义一个格式不正确的输出
misformatted = "{'name': '汽车漆', 'colors': ['粉红色','白色','红色','紫色','黄色']}"

# 创建一个用于解析输出的Pydantic解析器，此处希望解析为Flower格式
parser = PydanticOutputParser(pydantic_object=Flower)

# 使用Pydantic解析器解析不正确的输出
# parser.parse(misformatted) # 这行代码会出错
# OutputParserException: Failed to parse Flower from completion {'name': '汽车漆', 'colors': ['粉红色','白色','红色','紫色','黄色']}. Got: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

# 从langchain库导入所需的模块
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser

# 使用OutputFixingParser创建一个新的解析器，该解析器能够纠正格式不正确的输出
new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

# print(new_parser)
# 使用新的解析器解析不正确的输出
result = new_parser.parse(misformatted)  # 错误被自动修正
print(result)  # 打印解析后的输出结果
# name='汽车漆' colors=['粉红色', '白色', '红色', '紫色', '黄色']

if __name__ == '__main__':
    text = """
    请根据我的自定义歌词和音乐风格来创作歌曲：中文标题：酒入愁肠
    英文标题：Wine and Sorrows

    歌词结构：
    [Intro]
    （独奏）

    [Verse 1]
    月光洒在破旧的篱笆，
    李白提壶独自彷徨。
    酒香飘逸入云端，
    笔下是豪迈的想象。

    [Chorus]
    一壶浊酒喜相逢，
    千载孤愁只杜甫懂。
    古道西风瘦马间，
    人间事，两行清泪长。

    [Verse 2]
    江水流淌带走忧伤，
    杜甫凝眉思国家。
    文章锋利剑如霜，
    心中苦，却言者无罪当。

    [Chorus]
    一壶浊酒喜相逢，
    千载孤愁只杜甫懂。
    古道西风瘦马间，
    人间事，两行清泪长。

    [Bridge]
    一千年来谁能懂，
    酒与愁是最深的重。
    历史长河波澜壮，
    诗人眼中看尽繁华空。

    [Chorus]
    一壶浊酒喜相逢，
    千载孤愁只杜甫懂。
    古道西风瘦马间，
    人间事，两行清泪长。

    [Outro]
    （独奏）

    音乐风格：
    传统民谣
    主要乐器：古筝、琵琶、笛子
    节奏：缓慢而深情
    氛围：沉郁、古典、充满历史感
    """


    class Song(BaseModel):
        title: str = Field(description="song title")
        lyrics: str = Field(description="Enter your own lyrics", examples=['[Intro]...[Verse]...[Chorus]...'])
        music_style: str = Field(description="Style of Music, Maximum 10 words", examples=['syncopated country ...'])


    song_parser = OutputFixingParser.from_llm(parser=PydanticOutputParser(pydantic_object=Song), llm=ChatOpenAI(model="kimi"))

    result = song_parser.parse(text)  # 错误被自动修正
    print(result)  # 打印解析后的输出结果
