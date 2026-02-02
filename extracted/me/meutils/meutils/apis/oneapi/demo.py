#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2025/4/24 19:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

data = {
    "id": 1230,
    "type": 1,
    "key": "",
    "openai_organization": "",
    "test_model": "",
    "status": 1,
    "name": "x",
    "weight": 11,
    "created_time": 1745495162,
    "test_time": 0,
    "response_time": 0,
    "base_url": "https://huggingface.co/Qwen/Qwen2.5-Omni-7B",
    "other": "",
    "balance": 0,
    "balance_updated_time": 0,
    "models": "m1,m2",
    "group": "default",
    "used_quota": 0,
    "model_mapping": "{\n  \"gpt-3.5-turbo\": \"gpt-3.5-turbo-0125\"\n}",
    "status_code_mapping": "",
    "priority": 1,
    "auto_ban": 1,
    "other_info": "",
    "settings": "",
    "tag": "test",
    "setting": "",
    "param_override": "{\"temperature\": 0\n}"
}
print(dict_to_model(data))


class Channel(BaseModel):
    id: Optional[int] = None
    name: str = 'name'
    type: int = '1'  # 8 自定义
    key: str = ''
    openai_organization: str = ''
    test_model: str = ''
    status: int = 1  # 0 禁用 1 启用

    priority: int = 0
    weight: int = 0

    test_time: int = 0
    response_time: int = '0'
    base_url: str = 'https://huggingface.co/Qwen/Qwen2.5-Omni-7B'
    other: str = ''
    balance: int = '0'
    balance_updated_time: int = '0'
    models: str = 'm1,m2'
    group: str = 'default'
    used_quota: int = '0'
    model_mapping: str = '{"gpt-3.5-turbo": "gpt-3.5-turbo-0125"}'
    status_code_mapping: str = ''
    auto_ban: int = '1'
    other_info: str = ''
    settings: str = ''
    tag: str = 'tag'
    setting: str = ''
    param_override: str = '{"temperature": 0}'

    created_time: int = '1745495162'
