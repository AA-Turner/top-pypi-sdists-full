#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hivisionidphotos
# @Time         : 2024/9/2 16:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# {
#     '一寸': '一寸',
#     '二寸': '二寸',
#     '小一寸': '小一寸',
#     '小二寸': '小二寸',
#     '大一寸': '大一寸',
#     '大二寸': '大二寸',
#     '五寸': '五寸',
#     '教师资格证': '教师资格证',
#     '国家公务员考试': '国家公务员考试',
#     '初级会计考试': '初级会计考试',
#     '英语四六级考试': '英语四六级考试',
#     '计算机等级考试': '计算机等级考试',
#     '研究生考试': '研究生考试',
#     '社保卡': '社保卡',
#     '电子驾驶证': '电子驾驶证'
# }


class DetailedPhotoSpec(BaseModel):
    url: str

    size: Literal['一寸', '二寸', '小一寸', '小二寸', '大一寸', '大二寸', '五寸', '教师资格证', '国家公务员考试', '初级会计考试', '英语四六级考试', '计算机等级考试', '研究生考试', '社保卡', '电子驾驶证'] = "证件照规格"

    color: Literal['蓝色', '白色', '红色', '自定义底色'] = '蓝色'

    style: Literal['纯色', '上下渐变(白)', '中心渐变(白)'] = '纯色'

    dpi: int = 50  # 10-1000,	# int | float (numeric value between 10 and 1000) in 'KB大小' Slider component

    id_photo_params: list = []

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        self.id_photo_params = [self.url, "尺寸列表", "英语四六级考试", "蓝色", "纯色", "不设置", 0, 0, 0, 413, 295, 10]

        if self.size == '尺寸列表':
            pass

        if self.id_photo_params[5] == '不设置':
            pass


async def create_request(
        url,
        request,
        token: str = None,
        headers: Optional[dict] = None,
        post_kv: Optional[dict] = None
):
    token = token or 'This is a token'
    payload = request if isinstance(request, dict) else request.model_dump(exclude_none=True)

    headers = {
        'Authorization': f'Bearer {token}',
        'Cookie': token,
        **(headers or {})
    }
    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        response = await client.post(url=url, json=payload, **(post_kv or {}))
        if response.is_success:
            return response.json()
        response.raise_for_status()


if __name__ == '__main__':
    DetailedPhotoSpec(type='一寸')
