#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm_types
# @Time         : 2024/3/11 20:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
# 💡：用于表示新的想法或者重要的信息。
# ✔️：用于表示成功的执行或者完成的任务。
# > ✔️ The code executed successfully!
# 📊：用于表示数据或者统计结果。
# 📈：用于表示增长或者进步。
# 🎯：用于表示达到的目标或者预期的结果。
# 🚀：用于表示速度、效率或者进步。

from meutils.pipe import *

BASE_URL = "https://chatglm.cn/chatglm/backend-api/v1"
VIDEO_BASE_URL = "https://chatglm.cn/chatglm/video-api/v1"


class Part(BaseModel):
    """

    meta_data
        "metadata_list": [{
            "type": "webpage",
            "title": "南京天气预报,南京7天天气预报,南京15天天气预报,南京天气查询",
            "url": "http://www.weather.com.cn/weather/101190101.shtml",
            "text": "Web 结果1 天前 · 南京天气预报,南京7天天气预报,南京15天天气预报,南京天气查询. 预报. 全国 > 江苏 > 南京 > 城区. 18:00更新 | 数据来源 中央气象台. 今天. 7天. 8-15天. 40天. 雷达图. 2日（今天） 晴. 0℃. 3-4级. 3日（明天） 多云. 14℃ / 3℃. <3级转3-4级. 4日（后天） 阵雨转中雨. 13℃ / 7℃. <3级. 5日（周二） 阵雨转阴. 13℃ / 5℃. 4-5级. 6日（周 …   ",
            "pub_date": "1970-01-01T00:00:00.0000000"
        }]
    """
    id: str
    logic_id: str = ''
    role: str
    content: List[Dict[str, Any]]
    model: str
    recipient: str = ''
    created_at: str
    meta_data: dict = {}

    status: str

    # 预处理
    event: str = ''  # 类型
    markdown_data: str = ''

    def __init__(self, **data):
        super().__init__(**data)

        # self.event =
        # logger.debug(f"{self.status}: {self.content}")
        # logger.debug(
        #     f"""{self.status}: {self.content}\n{self.content and self.content[0].get("type")} \n {self.meta_data}""")
        # tool_calls image browser_result quote_result system_error
        if self.status == "finish" and self.content:
            content_type = self.content[0].get("type")

            # tool_calls
            if content_type == "tool_calls":
                _ = self.content[0].get("tool_calls", {})
                if "mclick" not in str(_):
                    self.markdown_data = f"""\n```{_.get("name")}\n{_}\n```\n"""

            if content_type == "quote_result" and self.meta_data:
                # logger.debug(self.meta_data)
                for metadata in self.meta_data.get("metadata_list", []):
                    if metadata.get("type") == "webpage":
                        self.markdown_data += f"[🔗{metadata.get('title')}]({metadata.get('url')})\n\n"

            # code
            if content_type == "code":
                code = self.content[0].get("code", "")
                self.markdown_data += f"""\n```{self.meta_data.get("toolCallRecipient", "python")}\n{code}\n```\n"""

            if content_type == "execution_output":  # todo: 展示块
                _ = self.content[0]
                self.markdown_data = f"\n```{content_type}\n{_}\n```\n{self.content[0].get('content')}\n"

            # image
            if content_type == "image" and self.status == "finish":

                images = self.content[0].get("image", [])
                for image in images:
                    self.markdown_data += f"![image]({image['image_url']})\n\n"

        # text
        if self.content and self.content[0].get("type") == "text":
            # self.markdown_data = f"""<text>{self.content[0].get("text", "")}"""
            self.markdown_data = f"""{self.content[0].get("text", "")}"""


class Data(BaseModel):
    """
    {
        "id": "65eef45f3901fe6e0bb7153b",
        "conversation_id": "65eef45e3901fe6e0bb7153a",
        "assistant_id": "65940acff94777010aa6b796",
        "parts": [
            {
                "id": "65eef45f3901fe6e0bb7153b",
                "logic_id": "62a2d941-43ba-4a00-9933-4f2a18979201",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "这是我为您创作的可爱猫咪图画，希望您喜欢。",
                        "status": "finish"
                    }
                ],
                "model": "chatglm-all-tools",
                "recipient": "all",
                "created_at": "2024-03-11 20:09:03",
                "meta_data": {
                    "toolCallRecipient": null
                },
                "status": "finish"  #
            }
        ],
        "created_at": "2024-03-11 20:09:03",
        "meta_data": {},
        "status": "finish",
        "last_error": {}
    }

    """
    id: str = "65940acff94777010aa6b796"  # chatglm4
    conversation_id: str
    assistant_id: str
    parts: List[Part]
    created_at: str
    status: str
    last_error: dict


"https://chatglm.cn/chatglm/video-api/v1/chat"

EXAMPLES = [
    {
        "prompt": "一艘巨大的古典帆船在巨浪的海面上行驶，灰蒙蒙的夜晚，月光照出蓝色的光影，风浪显得气氛很紧张",
        "conversation_id": "",
        "advanced_parameter_extra": {
            "video_style": "电影感",
            "emotional_atmosphere": "凄凉寂寞",
            "mirror_mode": "推近"
        }
    },

    {
        "prompt": "跳动起来",
        "conversation_id": "",
        "source_list": ["66a3379d3497367b9914de49"]  # 66a3379d3497367b9914de49 66a76a300603e53bccba4a1b
    }
]

"""
卡通3D
黑白老照片
油画
电影感

温馨和谐
生动活泼
紧张刺激
凄凉寂寞

水平
垂直
推近
拉远

"""


class Parameter(BaseModel):
    video_style: str = ''
    emotional_atmosphere: str = ''
    mirror_mode: str = ''


class VideoRequest(BaseModel):
    prompt: str
    conversation_id: str = ''
    advanced_parameter_extra: Parameter = {}
    source_list: Optional[list] = None  # 视频 "66a3373d57c37b00f049f7e5"

    class Config:
        json_schema_extra = {
            "examples": EXAMPLES
        }

# "https://chatglm.cn/chatglm/video-api/v1/static/composite_video" 加配音

# 66a6f2890603e53bccb9aa98
