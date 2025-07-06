#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : runwayml_types
# @Time         : 2024/7/16 10:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://api.runwayml.com/v1"

EXAMPLES = [
    {
        "taskType": "europa",
        "internal": False,
        "options": {
            "name": "Gen-3 Alpha 文生视频",
            "seconds": 10,
            "text_prompt": "童话里的世界，如同一个缤纷的调色盘，各种色彩交织在一起，组成了一幅美丽的画卷。那里有翠绿如茵的森林、湛蓝如海的天空、缤纷如梦的城堡，还有各种各样让人惊奇的生物。",
            "seed": 2319398808,
            "exploreMode": True,
            "watermark": False,
            "enhance_prompt": True,
            "width": 1280,
            "height": 768,
            "assetGroupName": "Generative Video"
        }
    },
    {
        "taskType": "gen2",
        "internal": False,
        "options": {
            "name": "Gen-2 文生视频",
            "seconds": 4,
            "gen2Options": {
                "mode": "gen2",
                "seed": 2919970896,
                "interpolate": False,
                "upscale": False,
                "watermark": False,
                "width": 1366,
                "height": 768,
                "motion_score": 22,
                "use_motion_score": True,
                "use_motion_vectors": False,
                "text_prompt": "童话里的世界，如同一个缤纷的调色盘，各种色彩交织在一起，组成了一幅美丽的画卷。那里有翠绿如茵的森林、湛蓝如海的天空、缤纷如梦的城堡，还有各种各样让人惊奇的生物。",
                "style": "cinematic"
            },
            "exploreMode": True,
            "assetGroupName": "Generative Video"
        },
        # "asTeamId": 17249553
    },
    {
        "taskType": "gen2",
        "internal": False,
        "options": {
            "name": "Gen-2 图生视频",
            "seconds": 4,
            "gen2Options": {
                "mode": "gen2",
                "seed": 1235659561,
                "interpolate": True,
                "upscale": True,
                "watermark": False,
                "motion_vector": {
                    "x": -0.5,
                    "y": 0,
                    "z": 0,
                    "r": 0,
                    "bg_x_pan": 0,
                    "bg_y_pan": 0
                },
                "use_motion_score": False,
                "use_motion_vectors": True,
                "text_prompt": "童话里的世界，如同一个缤纷的调色盘，各种色彩交织在一起，组成了一幅美丽的画卷。那里有翠绿如茵的森林、湛蓝如海的天空、缤纷如梦的城堡，还有各种各样让人惊奇的生物。",
                "image_prompt": "https://d2jqrm6oza8nb6.cloudfront.net/datasets/7df0aa53-334b-42d7-95c1-a054732c2166.jpg?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiODhmYTFhN2NjNjVkNjQ5ZiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTcyMTI2MDgwMH0.DLzXSWLnXAiL2Npm3KE9NnG1IpOzjZCksYC77_DWvlY",
                "init_image": "https://d2jqrm6oza8nb6.cloudfront.net/datasets/7df0aa53-334b-42d7-95c1-a054732c2166.jpg?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiODhmYTFhN2NjNjVkNjQ5ZiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTcyMTI2MDgwMH0.DLzXSWLnXAiL2Npm3KE9NnG1IpOzjZCksYC77_DWvlY"
            },
            "exploreMode": True,
            "assetGroupName": "Generative Video"
        },
        # "asTeamId": 17249553
    }
]

ASPECT_RATIOS = {
    "1:1": "1024x1024",

    "16:9": "1366x768",
    "9:16": "768x1366",

    "4:3": "1280x960",
    "3:4": "960x1280",

    "21:9": "1344x576",

}

STYLES = {
    "Cinematic",
    "Abandoned",
    "Abstract Sculpture",
    "Advertising",
    "Anime"
}


class MotionVector(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0.5
    r: float = 0
    bg_x_pan: float = 0
    bg_y_pan: float = 0


class Gen2Options(BaseModel):
    mode: str = "gen2"

    image_prompt: Optional[str] = None
    init_image: Optional[str] = None
    text_prompt: Optional[str] = None

    style: Union[str, Literal[(i for i in STYLES)]] = 'none'

    motion_score: Optional[int] = None
    motion_vector: Optional[MotionVector] = None

    interpolate: bool = False  # Smooth out your frames.
    upscale: bool = False
    use_motion_score: bool = False
    use_motion_vectors: bool = True

    watermark: bool = False
    seed: Optional[int] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.use_motion_score = True if self.motion_score else False
        self.use_motion_vectors = True if self.motion_vector else False


class Options(BaseModel):
    name: str = f'Gen-3 Alpha {np.random.randint(10e9)}'
    assetGroupName: str = 'Generative Video'

    text_prompt: Optional[str] = None  # 文生视频

    gen2Options: Optional[Union[Gen2Options]] = None  # 图生视频 todo gen3

    seconds: int = 5

    watermark: bool = False
    exploreMode: bool = True  # 探索模式 不扣积分（看是否有积分）
    enhance_prompt: bool = True
    width: int = 1280
    height: int = 768

    seed: Optional[int] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)


class RunwayRequest(BaseModel):
    taskType: Literal["europa", "gen2", "gen3"] = 'gen3'

    options: Options

    internal: bool = False
    asTeamId: Optional[int] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.taskType = "europa" if self.taskType == 'gen3' else self.taskType

    class Config:
        json_schema_extra = {
            "examples": EXAMPLES
        }


if __name__ == '__main__':
    # print(RunwayRequest(**EXAMPLES[2]).model_dump_json(indent=4))
    # print(RunwayRequest.Config.json_schema_extra)
    print(RunwayRequest.model_config)
