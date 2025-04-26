#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kuaishou_types
# @Time         : 2024/7/9 13:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# oss
"https://s2-111386.kwimgs.com/bs2/mmu-kolors-public/5f9c7b42688fe95c4b8d9ebd1dba3431.png?x-oss-process=image/resize,m_mfit,w_305"

# BASE_URL = "https://klingai.kuaishou.com"
# UPLOAD_BASE_URL = "https://upload.kuaishouzt.com"
# DOWNLOAD_URL= "https://klingai.kuaishou.com/api/works/batch_download_v2"

BASE_URL = "https://klingai.com"
UPLOAD_BASE_URL = "https://upload.uvfuns.com"
DOWNLOAD_URL = "https://klingai.com/api/works/batch_download_v2"  # /api/works/batch_download_v2?workIds=100331495&fwm=false

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=XuxPYK"
FEISHU_URL_VIP = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=hw8MXS"

ASPECT_RATIOS = {
    "1:1": "1024x1024",

    "16:9": "1344x768",
    "9:16": "768x1344",

    "4:3": "1152x896",
    "3:4": "896x1152",

    "3:2": "1216x832",
    "2:3": "832x1216",

}

STYLES = {
    "默认", "皮克斯", "卡通盲盒", "新海诚", "动漫3D", "怀旧动漫", "电子游戏", "水彩插画", "莫奈油画", "高清写实"
}

STATES = {
    5: "queue",
    10: "processing",
    99: "completed",
    50: "failed",
}


class KolorsRequest(BaseModel):
    prompt: str = '多肉植物，带着水珠，潮玩盲盒风格，皮克斯，3D质感，温馨的环境，丰富的场景，最佳画质，超精细，Octane渲染'
    negativePrompt: str = ''  # 不希望出现的内容

    style: str = "默认"
    imageCount: int = 1
    resolution: str = "1024x1024"

    #
    aspect_ratio: Literal["1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"] = "1:1"

    # 垫图
    referImage: str = ''
    fidelity: float = 0.5  # 参考度

    cfgScale: float = 7
    strength: float = 0.8

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.style not in STYLES:
            self.style = "默认"

        if self.resolution not in set(ASPECT_RATIOS.values()):
            self.resolution = ASPECT_RATIOS.get(self.aspect_ratio, "1024x1024")

        if self.referImage and self.referImage.startswith("http"):
            self.imageCount = 4
            self.referImage = self.referImage.split("/")[-2].split('?')[0]


class KlingaiImageRequest(BaseModel):
    mode: str = "pro"

    prompt: str = '清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K'
    style: str = "默认"
    aspect_ratio: Optional[Literal["1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"]] = "1:1"

    n: int = 1

    url: Optional[str] = None

    image_fidelity: Optional[float] = None

    #
    payload: dict = {}

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        inputs = []
        task_type = "mmu_txt2img_aiweb"
        if self.url:
            task_type = "mmu_img2img_aiweb"
            inputs.append({'name': 'input', 'inputType': 'URL', 'url': self.url})
            # inputs[-1]["fromWorkId"] = self.url.split('/')[-3].split('_')[-1]

        arguments = [
            {'name': 'prompt', 'value': self.prompt},
            {'name': 'style', 'value': self.style},
            {'name': 'aspect_ratio', 'value': self.aspect_ratio or "1:1"},
            {'name': 'imageCount', 'value': self.n},
            {"name": "fidelity", "value": self.image_fidelity or 0.5},
            {'name': 'biz', 'value': 'klingai'},
            {"name": "kolors_version", "value": "1.5"} ####### 1.5
        ]
        self.payload = {
            'arguments': arguments,
            'type': task_type,
            'inputs': inputs
        }


class Camera(BaseModel):
    type: Literal[
        "empty", "horizontal", "vertical", "zoom", "tilt", "pan", "roll", "down_back",
        "simple", "down_back", "forward_up", "left_turn_forward", "right_turn_forward",
    ] = "empty"
    horizontal: Optional[int] = 0
    vertical: Optional[int] = 0
    zoom: Optional[int] = 0
    tilt: Optional[int] = 0
    pan: Optional[int] = 0
    roll: Optional[int] = 0
    # """水平运镜，可选，取值范围：[-10, 10]"""
    # horizontal: Optional[int] = None
    # """水平摇镜，可选，取值范围：[-10, 10]"""
    # pan: Optional[int] = None
    # """旋转运镜，可选，取值范围：[-10, 10]"""
    # roll: Optional[int] = None
    # """垂直摇镜，可选，取值范围：[-10, 10]"""
    # tilt: Optional[int] = None
    # """垂直运镜，可选，取值范围：[-10, 10]"""
    # vertical: Optional[int] = None
    # """变焦，可选，取值范围：[-10, 10]"""
    # zoom: Optional[int] = None

    camera_json: str = ""  # 运镜

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.type == "down_back":
            self.vertical = self.vertical or -10
            self.zoom = self.zoom or -10

        if self.type == "SIMPLE":
            self.type = "empty"
        # elif hasattr(self, self.type):
        #     self.__setattr__(self.type, self.__getattr__(self.type))

        self.camera_json = json.dumps(self.dict(exclude={'camera_json'}))


class KlingaiVideoRequest(BaseModel):
    """增加计费模式，支持高质量模式
    kling-v1.0-std-5s

    kling-v1.5-std-5s 20积分
    kling-v1.5-std-10s

    kling-v1.5-pro-5s 35积分
    kling-v1.5-pro-10s

    kling-v1.6-std-5s 20积分
    kling-v1.6-std-10s

    kling-v1.6-pro-5s 35积分
    kling-v1.6-pro-10s

    """
    model: str = 'kling-v1.6'
    mode: Literal["mini", "std", "pro"] = "std"

    prompt: str = ''
    negative_prompt: Optional[str] = ''  # 不希望出现的内容

    n: Literal[1, 2, 3, 4] = 1

    duration: Optional[int] = 5
    aspect_ratio: Literal["1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"] = "16:9"
    cfg_scale: Optional[float] = 0.5  # 创意程度
    camera: Camera = Camera()  # 运镜

    url: Optional[str] = ''
    # 图生视频
    tail_image_url: Optional[str] = ''

    #
    payload: dict = {}

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        if self.duration > 5:
            self.duration = 10
        else:
            self.duration = 5

        if self.tail_image_url or self.mode == 'mini':
            self.duration = 5  # 尾帧仅支持 5s

        arguments = [
            {'name': 'prompt', 'value': self.prompt},
            {'name': 'negative_prompt', 'value': self.negative_prompt},
            {'name': 'duration', 'value': self.duration},
            {'name': 'aspect_ratio', 'value': self.aspect_ratio},
            {"name": "imageCount", "value": self.n},
            {'name': 'cfg', 'value': self.cfg_scale},
            {'name': 'camera_json', 'value': self.camera.camera_json},

            {'name': 'biz', 'value': 'klingai'},
        ]

        kling_version = '1.5'
        if self.model == 'kling-v1.6':
            kling_version = "1.6"
            arguments.append({"name": "camera_control_enabled", "value": "false"})  # 暂不支持
        else:
            arguments.append({"name": "camera_control_enabled", "value": "true"})

        arguments.append({"name": "kling_version", "value": kling_version})

        inputs = []
        task_type = "m2v_txt2video"
        if self.url:
            task_type = "m2v_img2video"
            inputs.append({'name': 'input', 'inputType': 'URL', 'url': self.url})
            if self.url.endswith(".mp4"):  # 待测试
                inputs[-1]["fromWorkId"] = self.url.split('/')[-3].split('_')[-1]
                task_type = "m2v_extend_video"

        if self.tail_image_url:
            task_type = "m2v_img2video"  # 尾帧 高质量模式

            arguments.append({"name": "tail_image_enabled", "value": "true"})
            inputs.append({'name': 'tail_image', 'inputType': 'URL', 'url': self.tail_image_url})

        self.payload = {
            'arguments': arguments,
            'type': f"""{task_type}{'_hq' if self.mode == 'pro' else ''}""",
            'inputs': inputs
        }

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "prompt": "一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头",

                    "url": "",
                    "tail_image_url": "",

                    "negative_prompt": "",
                    "duration": 5,
                    "aspect_ratio": "16:9",
                    "cfg": 0.5,
                    "camera": {
                        "type": "empty",
                        "horizontal": 0,
                        "vertical": 0,
                        "zoom": 0,
                        "tilt": 0,
                        "pan": 0,
                        "roll": 0
                    }
                },

                {
                    "prompt": "一只可爱的黑白边境牧羊犬，头伸出车窗，毛发被风吹动，微笑着伸出舌头",

                    "url": "https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/ai_portal/1720681052/LZcEugmjm4/whqrbrlhpjcfofjfywqqp9.png",
                    "tail_image_url": "",

                    "negative_prompt": "",
                    "duration": 5,
                    "aspect_ratio": "16:9",
                    "cfg": 0.5,
                    "camera": {
                        "type": "empty",
                        "horizontal": 0,
                        "vertical": 0,
                        "zoom": 0,
                        "tilt": 0,
                        "pan": 0,
                        "roll": 0
                    }
                },

                {
                    "prompt": "开花过程",

                    "url": "https://h2.inkwai.com/bs2/upload-ylab-stunt/ai_portal/1721561429/3z7bHmSC1Y/3yrmpqh7typspfcchmepar.png",
                    "tail_image_url": "https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/ai_portal/1721561524/GPoJWxBS8s/y9wlbuku3exeo7ra85s4su.png",

                    "negative_prompt": "",
                    "duration": 5,
                    "aspect_ratio": "16:9",
                    "cfg": 0.5,
                    "camera": {
                        "type": "empty",
                        "horizontal": 0,
                        "vertical": 0,
                        "zoom": 0,
                        "tilt": 0,
                        "pan": 0,
                        "roll": 0
                    }
                }

            ]
        }


"https://p2.a.kwimgs.com/bs2/upload-ylab-stunt/special-effect/output/HB1_PROD_ai_web_30121850/8784600431869866912/out.mp4"
if __name__ == '__main__':
    # print(Camera().camera_json)
    print(KlingaiVideoRequest.Config.json_schema_extra.get('examples')[-1])
