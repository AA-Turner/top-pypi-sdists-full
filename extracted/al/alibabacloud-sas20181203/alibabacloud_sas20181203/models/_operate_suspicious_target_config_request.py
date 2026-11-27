# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class OperateSuspiciousTargetConfigRequest(DaraModel):
    def __init__(
        self,
        lang: str = None,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        target_operations: str = None,
        target_type: str = None,
        type: str = None,
    ):
        # Specifies the language of the request and response. Default value: **zh**. Valid values:
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        self.resource_directory_account_id = resource_directory_account_id
        # The source IP address.
        self.source_ip = source_ip
        # Specifies the proactive defense parameters for servers. The following parameters are included:
        # 
        # - **targetType**: the dimension of the defense configuration. Currently, only the UUID dimension is supported. Fixed value: **uuid**.
        # - **target**: the UUID of the server for which you want to configure defense settings.
        # - **flag**: specifies whether to enable or disable proactive defense for the server. Valid values: **add** (enable) and **del** (disable).
        # 
        # This parameter is required.
        self.target_operations = target_operations
        # Specifies the dimension for managing proactive defense. Currently, only the server UUID dimension is supported.
        # 
        # Valid value: **uuid**.
        # 
        # This parameter is required.
        self.target_type = target_type
        # Specifies the type of proactive defense. Valid values:
        # - **auto_breaking**: automatic interception
        # - **webshell_cloud_breaking**: web shell connection defense
        # - **alinet**: malicious network behavior defense
        # - **ransomware_breaking**: anti-ransomware (bait capture)
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
        if self.lang is not None:
            result['Lang'] = self.lang

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.target_operations is not None:
            result['TargetOperations'] = self.target_operations

        if self.target_type is not None:
            result['TargetType'] = self.target_type

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('TargetOperations') is not None:
            self.target_operations = m.get('TargetOperations')

        if m.get('TargetType') is not None:
            self.target_type = m.get('TargetType')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

