# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class UninstallBackupClientRequest(DaraModel):
    def __init__(
        self,
        policy_version: str = None,
        uuid: str = None,
        uuid_list: List[str] = None,
    ):
        # The version of the protection policy. You can call the [DescribeBackupPolicies](~~DescribeBackupPolicies~~) operation to query the version. Valid values:
        # 
        # - **1.0.0**: The version of the protection policy is 1.0.0.
        # - **2.0.0**: The version of the protection policy is 2.0.0.
        # 
        # This parameter is required.
        self.policy_version = policy_version
        # The UUID of the server from which you want to uninstall the anti-ransomware client.
        # 
        # > UuidList.N and UUID cannot both be empty.
        self.uuid = uuid
        # The list of UUIDs of the servers from which you want to uninstall the anti-ransomware client.
        # 
        # > UuidList and UUID cannot both be empty.
        self.uuid_list = uuid_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.policy_version is not None:
            result['PolicyVersion'] = self.policy_version

        if self.uuid is not None:
            result['Uuid'] = self.uuid

        if self.uuid_list is not None:
            result['UuidList'] = self.uuid_list

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PolicyVersion') is not None:
            self.policy_version = m.get('PolicyVersion')

        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')

        if m.get('UuidList') is not None:
            self.uuid_list = m.get('UuidList')

        return self

