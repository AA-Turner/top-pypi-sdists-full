#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vidu_types
# @Time         : 2024/7/31 08:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# BASE_URL = "https://api.vidu.studio/vidu/v1"
BASE_URL = "https://service.vidu.com/vidu/v1"
UPLOAD_BASE_URL = "https://api.vidu.studio/tools/v1"  # /files/uploads

EXAMPLES = [
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "两个人举起茶杯小口抿了一口。左边的人轻抿双唇后微笑，右边的人专注于他们的茶，形成一种静雅和微妙互动的场景。布景精致，淡雅的颜色、花卉布置和古典家具增强了优雅氛围。",
                }
            ],
            "enhance": True,
        },
        "type": "text2video",
        "settings": {
            "style": "general",
            "duration": 4,
            "model": "vidu-1",
            "aspect_ratio": "16:9",

        }
    },
    {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": "开花吧",
                    "enhance": True
                },
                {
                    "type": "image",
                    "content": "ssupload:?id=2368323193735387",
                    "enhance": True
                }
            ]
        },
        "type": "img2video",
        "settings": {
            "style": "general",
            "aspect_ratio": "16:9",
            "duration": 4,
            "model": "vidu-1"
        }
    }
]


# {
#     "input": {
#         "prompts": [
#             {
#                 "type": "text",
#                 "content": "跳起来"
#             },
#             {
#                 "type": "image",
#                 "content": "https://oss.ffire.cc/files/kling_watermark.png",
#                 "src_imgs": [
#                     "https://oss.ffire.cc/files/kling_watermark.png"
#                 ]
#             }
#         ],
#         "enhance": true
#     },
#     "type": "img2video",
#     "settings": {
#         "style": "general",
#         "duration": 4,
#         "model": "vidu-high-performance",
#         "model_version": "1.0"
#     }
# }

class VideoRequest(BaseModel):
    pass


class ViduRequest(BaseModel):
    """quality 倍率2"""
    model: Union[
        str, Literal['vidu-2.0', 'vidu-1.5', 'vidu-high-performance', 'vidu-high-quality']] = "vidu-high-performance"

    prompt: Optional[str] = None

    url: Optional[str] = None  # ssupload:?id=
    tail_image_url: Optional[str] = None

    style: str = "general"  # anime
    aspect_ratio: str = "16:9"
    duration: int = 4

    type: Optional[str] = None  # text2video img2video character2video headtailimg2video

    """vidu-1.5"""
    resolution: Union[str, Literal['512', '720p', '1080p']] = "512"
    movement_amplitude: Optional[str] = "auto"  # small medium high

    sample_count: int = 1
    schedule_mode: Literal["normal", "nopeak"] = "normal"

    payload: dict = {}

    def __init__(self, **data):
        super().__init__(**data)

        if self.duration > 4:
            self.duration = 8
        else:
            self.duration = 4

        input = {
            "prompts": [],
            "enhance": True
        }

        if self.prompt:
            input['prompts'].append(
                {
                    "type": "text",
                    "content": self.prompt,
                }
            )
        type = "text2video"
        if self.url:
            type = "img2video"  # character2video

            input['prompts'].append(
                {
                    "type": "image",
                    "content": self.url,
                    "src_imgs": [self.url, ]
                }
            )

        if self.tail_image_url:
            type = "headtailimg2video"
            input['prompts'].append(
                {
                    "type": "image",
                    "content": self.tail_image_url,
                    "src_imgs": [self.tail_image_url, ]
                }
            )

        if self.model in ("vidu-2.0",):
            self.payload = {
                "input": input,
                "type": self.type or type,
                "settings": {
                    "model_version": "2.0",  #######
                    "style": "general",
                    "duration": self.duration,

                    "resolution": self.resolution,
                    "aspect_ratio": self.aspect_ratio,

                    "movement_amplitude": self.movement_amplitude,
                    "sample_count": self.sample_count,
                    "schedule_mode": self.schedule_mode,

                }
            }

        else:

            self.payload = {
                "input": input,
                "type": self.type or type,
                "settings": {
                    "model": self.model,
                    "model_version": "1.0",

                    "style": self.style,

                    "aspect_ratio": self.aspect_ratio,

                    "duration": self.duration,

                }
            }

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "prompt": "一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头。",
                }
            ]
        }


class ViduUpscaleRequest(BaseModel):
    task_id: str  # vip
    creation_id: str


# todo: 兼容官方api https://kimi.moonshot.cn/chat/cs33f8j1ch3mt3umbsp0
text2video = {
    "type": "text2video",  # type (string, enum: text2video, img2video, character2video, upscale):
    "model": "vidu-1",
    "style": "general",

    "input": {
        "seed": 123,
        "enhance": True,
        "prompts": [
            {
                "type": "text",
                "content": "小白兔白又白"
            }
        ]
    },

    "output_params": {
        "sample_count": 1,
        "duration": 4
    },
    "moderation": False
}

img2video = {
    "type": "img2video",
    "model": "vidu-1",
    "style": "general",

    "input": {
        "enhance": True,
        "prompts": [
            {
                "type": "text",
                "content": "小白兔白又白"
            },
            {
                "type": "image",
                "content": "https://pic.netbian.com/uploads/allimg/170624/1722311498296151ea67.jpg"
            }
        ]
    },

    "output_params": {
        "sample_count": 1,
        "duration": 4
    },
    "moderation": False
}

i2v_15 = {
    "input": {
        "prompts": [
            {
                "type": "image",
                "content": "ssupload:?id=2608006135309944",
                "src_imgs": [
                    "ssupload:?id=2608006135309944"
                ]
            }
        ],
        "enhance": True
    },
    "type": "img2video",
    "settings": {
        "style": "general",
        "duration": 4,
        "resolution": "512",
        "movement_amplitude": "auto",
        "aspect_ratio": "16:9",
        "sample_count": 1,
        "schedule_mode": "nopeak",
        "model_version": "1.5"
    }
}

i2v = {
    "input": {
        "prompts": [
            {
                "type": "image",
                "content": "ssupload:?id=2608006135309944",
                "src_imgs": [
                    "ssupload:?id=2608006135309944"
                ]
            }
        ],
        "enhance": True
    },
    "type": "img2video",
    "settings": {
        "style": "general",
        "duration": 4,
        "resolution": "512",
        "movement_amplitude": "auto",
        "aspect_ratio": "16:9",
        "sample_count": 1,
        "schedule_mode": "nopeak",
        "model_version": "2.0"
    }
}

headtailimg2video = {
    "input": {
        "prompts": [
            {
                "type": "image",
                "content": "ssupload:?id=2608004743287446",
                "src_imgs": [
                    "ssupload:?id=2607999433445006"
                ],
                "selected_region": {
                    "top_left": {
                        "x": 0,
                        "y": 0
                    },
                    "bottom_right": {
                        "x": 1280,
                        "y": 848
                    }
                }
            },
            {
                "type": "image",
                "content": "ssupload:?id=2608004785735138",
                "src_imgs": [
                    "ssupload:?id=2608004785791540"
                ],
                "selected_region": {
                    "top_left": {
                        "x": 0,
                        "y": 0
                    },
                    "bottom_right": {
                        "x": 1280,
                        "y": 848
                    }
                }
            }
        ],
        "enhance": True
    },
    "type": "headtailimg2video",
    "settings": {
        "style": "general",
        "duration": 4,
        "resolution": "512",
        "movement_amplitude": "auto",
        "aspect_ratio": "16:9",
        "sample_count": 1,
        "schedule_mode": "nopeak",
        "model_version": "2.0"
    }
}
