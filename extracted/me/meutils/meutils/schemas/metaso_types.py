#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : metaso_types
# @Time         : 2024/11/11 17:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://metaso.cn"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=cyKbvv"


class MetasoRequest(BaseModel):
    model: Optional[Literal["ds-r1",]] = None

    """search-mini search search-pro"""
    mode: Union[str, Literal["concise", "detail", "research", "strong-research"]] = "detail"  # concise detail research

    question: str = "Chatfire"

    """全网 文库 学术 图片 播客"""
    scholarSearchDomain: str = "all"

    url: str = "https://metaso.cn/"
    lang: str = "zh"

    searchTopicId: Optional[str] = None
    searchTopicName: Optional[str] = None

    enableMix: str = 'true'
    newEngine: str = 'true'
    enableImage: str = 'true'


# question: hi
# mode: detail
# scholarSearchDomain: all
# model: ds-r1
# url: https://metaso.cn/
# lang: zh
# enableMix: true
# newEngine: true
# enableImage: true
# metaso-pc: pc
class MetasoResponse(BaseModel):  # sse

    type: Optional[str] = None  # query set-reference heartbeat append-text
    content: str = ""

    data: Optional[dict] = None
    references: list = []

    # 原生内容
    chunk: str

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        chunk = self.chunk.lstrip("data:")
        self.data = json.loads(chunk)

        self.type = self.data.get("type")
        self.content = self.data.get("text", "")

        # {'realQuestion': '你是谁', 'data': [], 'label': '', 'id': '8544588308750417920', 'type': 'query'}
        if self.type == "query":
            self.data.pop("id", None)
            self.data.pop("debugId", None)
            self.content = f"""> 🚀AISearch\n```json\n{self.data}\n```\n\n"""

        if self.type in {"set-reference", "update-reference"}:
            self.references = self.data.get("list", [])


if __name__ == '__main__':
    chunk = """data:{"type":"heartbeat"}"""

    print(MetasoResponse(chunk=chunk))
