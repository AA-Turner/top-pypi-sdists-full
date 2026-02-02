#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : haimian_types
# @Time         : 2024/8/2 15:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : model=灵感创作 model=自定义创作

from meutils.pipe import *


# https://www.haimian.com/jd/api/v1/generate/text2bgm 纯音乐


class HaimianRequest(BaseModel):
    prompt: str
    batch_size: int = 1

    generate_cover: bool = True
    generate_title: bool = True
    is_original_prompt: bool = False


class HaimianCustomRequest(HaimianRequest):
    # 自定义模式
    title: Optional[str] = None
    lyrics: str

    genre: Optional[Union[str, Literal[
        "Folk", "Pop", "Rock", "Romantic", "GuFeng Music", "Hip Hop/Rap", "R&B/Soul", "Jazz", "Reggae",
        "Chinoiserie Electronic", "Trap Rap""Contemporary R&B", "Bossa Nova",
    ]]] = None

    mood: Optional[Union[str, Literal[
        "Happy",
        "Sentimental/Melancholic/Lonely",  # emo
        "Dynamic/Energetic",  # 活力
        "Nostalgic/Memory",  # 怀旧
        "Groovy/Funky",  # 律动
        "Sorrow/Sad",  # 伤感
        "Chill",  # 放松
        "Romantic",  # 浪漫
    ]]] = None

    gender: Optional[Literal["Male", "Female"]] = None

    is_original_tag: bool = False

    source_lyric_id: Optional[str] = None
