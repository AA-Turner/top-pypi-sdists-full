# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GetAegisContainerPluginRuleRequest(DaraModel):
    def __init__(
        self,
        id: str = None,
        lang: str = None,
        rule_type: int = None,
    ):
        # The ID of the container escape prevention rule. You can call the [ListAegisContainerPluginRule](~~ListAegisContainerPluginRule~~) operation to obtain the ID. This parameter is required. If this parameter is not specified, the API returns HTTP 400 and the error code -101.
        self.id = id
        # Specifies the language of the request and response. Default value: **zh**. Valid values:
        # 
        # 
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # The rule type. Valid values:
        # - **0**: Custom
        # - **1**: Built-in
        self.rule_type = rule_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.id is not None:
            result['Id'] = self.id

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        return self

