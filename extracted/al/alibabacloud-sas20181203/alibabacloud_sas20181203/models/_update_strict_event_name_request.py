# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class UpdateStrictEventNameRequest(DaraModel):
    def __init__(
        self,
        event_name_list: List[str] = None,
        lang: str = None,
        operator: str = None,
        resource_directory_account_id: int = None,
    ):
        # The list of strict mode alerts to be updated. This is a full list. Strict mode alerts not included in this list will be subjected to the opposite operation.
        # > You can call [DescribeStrictEventName](~~DescribeStrictEventName~~) to obtain the list of all strict mode alerts.
        # > -
        self.event_name_list = event_name_list
        # Specifies the language of the request and response. Default value: **zh**. Valid values:
        # 
        # - **zh**: Chinese.
        # - **en**: English.
        self.lang = lang
        # Specifies the action to perform on the alerts. Valid values:
        # 
        # - *on*: enables alerts.
        # - *off*: disables alerts.
        # 
        # This parameter is required.
        self.operator = operator
        self.resource_directory_account_id = resource_directory_account_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.event_name_list is not None:
            result['EventNameList'] = self.event_name_list

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.operator is not None:
            result['Operator'] = self.operator

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EventNameList') is not None:
            self.event_name_list = m.get('EventNameList')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('Operator') is not None:
            self.operator = m.get('Operator')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        return self

