# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeSuspiciousUUIDConfigRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        type: str = None,
    ):
        # The ID of the member accounts in the resource folder (Alibaba Cloud account). You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The type of proactive defense to query. Valid values:
        # 
        # - **auto_breaking**: anti-virus
        # - **ransomware_breaking**: anti-ransomware (bait capture)
        # - **webshell_cloud_breaking**: web shell connection defense
        # - **alinet**: malicious network behavior defense
        # - **alisecguard**: client self-protection
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

