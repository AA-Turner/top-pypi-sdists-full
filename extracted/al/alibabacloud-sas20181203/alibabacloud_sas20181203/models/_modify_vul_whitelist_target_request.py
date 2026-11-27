# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyVulWhitelistTargetRequest(DaraModel):
    def __init__(
        self,
        id: int = None,
        reason: str = None,
        source_ip: str = None,
        target_info: str = None,
    ):
        # The ID of the vulnerability whitelist.
        # > You can call the [DescribeVulWhitelist](~~DescribeVulWhitelist~~) operation to obtain the ID of the vulnerability whitelist.
        # 
        # This parameter is required.
        self.id = id
        # The reason for adding the whitelist.
        self.reason = reason
        # The source IP address.
        self.source_ip = source_ip
        # Specifies the scope where the whitelist takes effect. This field is in JSON format and contains the following fields:
        # - **type**: the scope type. Valid values:
        #     - **GroupId**: group
        #     - **Uuid**: server asset
        # - **uuids**: the collection of server asset UUIDs.
        # - **groupIds**: the collection of group IDs.
        # > If this value is empty, the whitelist applies to all servers. If **type** is set to **GroupId**, **groupIds** cannot be empty. If **type** is set to **Uuid**, **uuids** cannot be empty.
        self.target_info = target_info

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.id is not None:
            result['Id'] = self.id

        if self.reason is not None:
            result['Reason'] = self.reason

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.target_info is not None:
            result['TargetInfo'] = self.target_info

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')

        if m.get('Reason') is not None:
            self.reason = m.get('Reason')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('TargetInfo') is not None:
            self.target_info = m.get('TargetInfo')

        return self

