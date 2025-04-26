#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : textin_types
# @Time         : 2025/3/23 11:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# BASE_URL = "https://api.textin.com"
BASE_URL = "https://api.textin.com/ai/service/v1"


# dict_to_model(d)

class DynamicModel(BaseModel):
    pdf_pwd: Optional[str] = 'None'
    dpi: int = '144'
    page_start: int = '0'
    page_count: int = '1000'
    apply_document_tree: int = '0'
    markdown_details: int = '1'
    page_details: int = '0'
    table_flavor: str = 'md'
    get_image: str = 'none'
    parse_mode: str = 'scan'


class WatermarkRemove(BaseModel):
    image: str  # path url base64 # from pydantic import HttpUrl
    response_format: Literal["url", "b64_json"] = 'b64_json'

    class Config:
        extra = "allow"

        json_schema_extra = {
            "examples": [
                {
                    "image": "https://oss.ffire.cc/files/sese1.jpg",
                    "response_format": "url"

                },
            ]
        }


class WatermarkRemoveResponse(BaseModel):
    """{'code': 200,
     'duration': 375,
     'has_watermark': 1,
     'message': 'success',
     'result': {'image': },'version': '0.2.1'}
    """
    pass

    class Config:
        extra = "allow"


if __name__ == '__main__':
    pass
