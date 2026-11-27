# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeSuspiciousOverallConfigRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        type: str = None,
    ):
        # The ID of the member accounts in the resource folder (Alibaba Cloud account).
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The source IP address.
        self.source_ip = source_ip
        # The switch type. Valid values:
        # 
        # - **auto_breaking**: Anti-virus.
        # - **ransomware_breaking**: Anti-ransomware (decoy capture).
        # - **webshell_cloud_breaking**: Web shell connection defense.
        # - **alinet**: Malicious network behavior defense.
        # - **k8s_log_analysis**: Container K8s threat detection.
        # - **alisecguard**: Client self-protection defense mode.
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

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

