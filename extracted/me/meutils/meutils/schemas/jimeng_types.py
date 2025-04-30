#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : jimeng_types
# @Time         : 2024/12/16 18:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import uuid

from meutils.pipe import *

BASE_URL = "https://jimeng.jianying.com"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=zkPAHw"

FEISHU_URL_MAPPER = {
    "758": "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=6JWRxt"  # 柏拉图
}

MODELS_MAP = {
    "jimeng-2.1": "high_aes_general_v21_L:general_v2.1_L",

    "jimeng-2.0-pro": "high_aes_general_v20_L:general_v2.0_L",
    "high_aes_general_v20_L:general_v2.0_L": "high_aes_general_v20_L:general_v2.0_L",

    "jimeng-2.0": "high_aes_general_v20:general_v2.0",
    "jimeng-1.4": "high_aes_general_v14:general_v1.4",
    "jimeng-xl-pro": "text2img_xl_sft",

    "default": "high_aes_general_v30l:general_v3.0_18b"
}


class LogoInfo(BaseModel):
    add_logo: bool = False
    position: int = 0
    language: int = 0
    opacity: float = 0.3
    logo_text_content: str = "这里是明水印内容"


class ImageRequest(BaseModel):
    req_key: Union[
        str, Literal["jimeng_high_aes_general_v21_L", "byteedit_v2.0", " high_aes_general_v30l_zt2i"]
    ] = "jimeng_high_aes_general_v21_L"
    prompt: str = "魅力姐姐"
    seed: int = -1
    width: int = 512
    height: int = 512
    use_pre_llm: bool = True

    use_sr: bool = False
    return_url: bool = True
    logo_info: Optional[LogoInfo] = None


class VideoRequest(BaseModel):
    req_key: Union[str, Literal["jimeng_vgfm_t2v_l20", "jimeng_vgfm_i2v_l20"]] = "jimeng_vgfm_t2v_l20"
    prompt: str = "魅力姐姐"
    seed: int = -1

    aspect_ratio: Literal['16:9', '4:3', '1:1', '3:4', '9:16', '21:9', '9:21'] = "16:9"

    image_urls: Optional[List[str]] = None
    binary_data_base64: Optional[List[str]] = None
