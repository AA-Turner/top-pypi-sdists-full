# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class UpdateWhiteListStrategyStatusRequest(DaraModel):
    def __init__(
        self,
        lang: str = None,
        source_ip: str = None,
        status: int = None,
        strategy_ids: str = None,
    ):
        # The language of the request and response. Default value: **zh**. Valid values:
        # 
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # The source IP address of the request. You do not need to specify this parameter. The system automatically retrieves the value.
        self.source_ip = source_ip
        # The status of the policy. Valid values:
        # - **0**: deleted
        # - **1**: learning
        # - **2**: paused
        # - **3**: learning completed
        # - **4**: effective
        # 
        # > - You can change the status from **Learning** only to **Paused**.
        # > - You can change the status from **Paused** only to **Learning**.
        # > - You can change the status from **Learning completed** only to **Effective**.
        # 
        # This parameter is required.
        self.status = status
        # The policy ID.
        # > You can call the [DescribeWhiteListStrategyList](~~DescribeWhiteListStrategyList~~) operation to obtain the value of this parameter.
        # 
        # This parameter is required.
        self.strategy_ids = strategy_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.lang is not None:
            result['Lang'] = self.lang

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.status is not None:
            result['Status'] = self.status

        if self.strategy_ids is not None:
            result['StrategyIds'] = self.strategy_ids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('StrategyIds') is not None:
            self.strategy_ids = m.get('StrategyIds')

        return self

