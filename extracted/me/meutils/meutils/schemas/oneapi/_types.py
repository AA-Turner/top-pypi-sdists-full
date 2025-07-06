#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : oneapi_types
# @Time         : 2024/6/28 10:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.data.oneapi import NOTICE, FOOTER

BASE_URL = "https://api.chatfire.cn"


class ModelGroupInfo(BaseModel):
    """注：信息JSON共有以下键值，均全为string类型：name（厂商名称）、desc（厂商介绍，支持MD）、icon（厂商图标链接，不定义则会自动匹配默认图标库）、notice（厂商使用公告说明，支持MD）"""
    name: str

    desc: Optional[str] = None

    icon: Optional[str] = None

    notice: Optional[str] = None


class ModelInfo(BaseModel):
    """note（模型说明，支持MD）、icon（模型图标链接，不定义则会自动匹配默认图标库）、tags（模型标签，多个｜分割）、group（模型归属分组，例如OpenAI，或与下方【模型厂商信息中的Key相对应】）"""
    note: Optional[str] = None

    icon: Optional[str] = None

    tags: Optional[str] = None

    """ModelGroupInfo.name"""
    group: Optional[str] = None


class ChannelInfo(BaseModel):
    id: Optional[Union[int, str]] = None  # 不存在就新建
    type: int = 1  # 枚举值 openai

    name: str = ''
    tag: str = ''
    group: str = 'default'

    base_url: str = ''
    key: str  # 与id相对应
    models: str = 'MODEL'

    access_token: str = ''
    openai_organization: str = ''
    test_model: str = ''
    status: int = 1
    weight: int = 0
    created_time: int = Field(default_factory=lambda: int(time.time()))
    test_time: int = 0
    response_time: int = 0
    other: str = ''

    balance: int = 0
    balance_updated_time: int = 0

    used_quota: float = 0.001
    upstream_user_quota: int = 0

    model_mapping: Union[str, dict] = ""  # json

    headers: str = ''  # json
    status_code_mapping: str = ''
    priority: int = 0
    auto_ban: int = 1
    empty_response_retry: int = 0
    not_use_key: int = 0
    remark: str = ''
    mj_relax_limit: int = 99
    mj_fast_limit: int = 99
    mj_turbo_limit: int = 99
    other_info: str = ''
    channel_ratio: int = 1
    error_return_429: int = 0
    setting: str = ''

    """参数覆盖"""
    param_override: str = ''  # json
    is_tools: bool = False

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        self.id = self.id or None

        self.name = f"""{str(datetime.datetime.now())[:10]} {self.name or self.base_url or "NAME"}"""
        self.tag = f"""{str(datetime.datetime.now())[:10]} {self.tag or self.base_url or "TAG"}"""
        self.group = self.group or self.base_url or "GROUP"

        self.setting = self.setting or ""
        self.param_override = self.param_override or ""
        if isinstance(self.model_mapping, dict):
            self.model_mapping = json.dumps(self.model_mapping)

        if self.used_quota < 10000:
            self.used_quota = int(self.used_quota * 500000)


# https://oss.ffire.cc/images/qw.jpeg?x-oss-process=image/format,jpg/resize,w_512
if __name__ == '__main__':
    # print(','.join(REDIRECT_MODEL.keys()))

    from meutils.apis.oneapi import option, channel

    # option()
    #
    # arun(channel.edit_channel(MODEL_PRICE))
