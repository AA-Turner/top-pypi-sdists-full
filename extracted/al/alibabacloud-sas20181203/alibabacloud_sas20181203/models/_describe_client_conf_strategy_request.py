# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeClientConfStrategyRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        tag: str = None,
        tag_value: str = None,
    ):
        # The ID of the member accounts in the resource folder (Alibaba Cloud account).
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # Specifies the client resource tag to query.
        # 
        # This parameter is required.
        self.tag = tag
        # The tag value of the asset. Valid values:
        # - major
        # - advanced
        # - basic
        # 
        # This parameter is required.
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.tag is not None:
            result['Tag'] = self.tag

        if self.tag_value is not None:
            result['TagValue'] = self.tag_value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Tag') is not None:
            self.tag = m.get('Tag')

        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')

        return self

