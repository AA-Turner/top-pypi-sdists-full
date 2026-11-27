# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class OperateSuspiciousOverallConfigRequest(DaraModel):
    def __init__(
        self,
        config: str = None,
        lang: str = None,
        no_target_as_on: bool = None,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        type: str = None,
    ):
        # The switch status. Valid values:
        # 
        # - **on**: Enabled
        # - **off**: Disabled
        # 
        # This parameter is required.
        self.config = config
        # Specifies the language type for requests and response messages. Default value: **zh**. Valid values:
        # 
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # Specifies whether to configure assets. Default value: **false**. Valid values:
        # - **true**: Yes
        # - **false**: No
        # > This value is valid only when **config** is set to **on**.
        self.no_target_as_on = no_target_as_on
        self.resource_directory_account_id = resource_directory_account_id
        # The source IP address.
        self.source_ip = source_ip
        # The switch type. Valid values:
        # 
        # - **auto_breaking**: Anti-virus
        # - **ransomware_breaking**: Anti-ransomware (bait capture)
        # - **webshell_cloud_breaking**: Web shell connection defense
        # - **alinet**: Malicious network behavior defense
        # - **k8s_log_analysis**: Container Kubernetes threat detection
        # - **alisecguard**: Client self-protection defense mode
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
        if self.config is not None:
            result['Config'] = self.config

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.no_target_as_on is not None:
            result['NoTargetAsOn'] = self.no_target_as_on

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Config') is not None:
            self.config = m.get('Config')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('NoTargetAsOn') is not None:
            self.no_target_as_on = m.get('NoTargetAsOn')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

