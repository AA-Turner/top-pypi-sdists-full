#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : napkin_types
# @Time         : 2024/12/3 17:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://nlp-california-api.napkin.ai/api/v1"

ASSETS_BASE_URL = "https://assets.napkin.ai/assets/db"
# https://assets.napkin.ai/assets/db/24px/coffee-mug--food-drinks--24x24.svg

"https://assets.napkin.ai/assets/db/families/lens-circles-v7--family--3.svg"

class IconsSimilarRequest(BaseModel):
    caption: str


class Icon(BaseModel):
    file: str
    list: str
    name: str
    score: float


class IconsSimilarResponse(BaseModel):
    data: List[Icon]
    metadata: Dict = {}

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        for icon in self.data:
            icon.file = f"{ASSETS_BASE_URL}/{icon.list}/{icon.file}.svg"

    class Config:
        extra = "allow"

#
# {'data': [{'file': 'coffee-read--food-drinks--24x24',
#            'list': '24px',
#            'name': 'coffee-read',
#            'score': 0.48007068037986755},
#           {'file': 'coffee-mug--food-drinks--24x24',
#            'list': '24px',
#            'name': 'coffee-mug',
#            'score': 0.4368043541908264},
#           {'file': 'coffee-cup--food-drinks--24x24',
#            'list': '24px',
#            'name': 'coffee',
#            'score': 0.4181402325630188},
#           {'file': 'time-coffee-time-2--interface-essential--24x24',
#            'list': '24px',
#            'name': 'coffee-time-2',
#            'score': 0.408485472202301},
#           {'file': 'coffee-jar--food-drinks--24x24',
#            'list': '24px',
#            'name': 'coffee-jar',
#            'score': 0.4083172082901001},
#           {'file': 'time-coffee-time-3--interface-essential--24x24',
#            'list': '24px',
#            'name': 'coffee-time-3',
#            'score': 0.40657299757003784},
#           {'file': 'coffee-coldbrew-1--food-drinks--24x24',
#            'list': '24px',
#            'name': 'coldbrew',
#            'score': 0.40559959411621094},
#           {'file': 'coffee-straw--food-drinks--24x24',
#            'list': '24px',
#            'name': 'straw',
#            'score': 0.4047240614891052},
#           {'file': 'coffee-to-go--food-drinks--24x24',
#            'list': '24px',
#            'name': 'go',
#            'score': 0.39064520597457886},
#           {'file': 'dating-cup--romance--24x24',
#            'list': '24px',
#            'name': 'dating-cup',
#            'score': 0.38993847370147705}],
#  'metadata': {}}
