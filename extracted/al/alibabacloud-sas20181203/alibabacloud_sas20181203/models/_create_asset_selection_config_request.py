# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateAssetSelectionConfigRequest(DaraModel):
    def __init__(
        self,
        business_type: str = None,
        client_token: str = None,
        dry_run: bool = None,
        platform: str = None,
        target_type: str = None,
    ):
        # The business type of the asset selection. Valid values:
        # 
        # - **VIRUS_SCAN_CYCLE_CONFIG**: Virus scan configuration.
        # - **VIRUS_SCAN_ONCE_TASK**: One-time virus scan.
        # - **AGENTLESS_MALICIOUS_WHITE_LIST_[ID]**: Whitelist rule for agentless detection alerts.
        # - **AGENTLESS_VUL_WHITE_LIST_[ID]**: Whitelist rule for agentless detection vulnerabilities.
        # - **FILE_PROTECT_RULE_SWITCH_TYPE_[ID]**: Core file protection.
        # 
        # This parameter is required.
        self.business_type = business_type
        # The client token that is used to ensure the idempotence of the request. You can use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to only precheck the request. Valid values:
        # - true: Prechecks the request without performing the actual operation.
        # - false: Performs the request.
        # Default value: false.
        self.dry_run = dry_run
        # The operating system of the target asset. Valid values:
        # 
        # - **all**: All operating systems.
        # - **windows**: Windows operating system.
        # - **linux**: Linux operating system.
        # > If this parameter is left empty, the default value is matched based on the **BusinessType** value.
        # > - **VIRUS_SCAN_CYCLE_CONFIG**: The value is **all**.
        # > - **VIRUS_SCAN_ONCE_TASK**: The value is **all**.
        # > - **AGENTLESS_MALICIOUS_WHITE_LIST_[ID]**: The value is **all**.
        # > - **AGENTLESS_VUL_WHITE_LIST_[ID]**: The value is **all**.
        # > - **FILE_PROTECT_RULE_SWITCH_TYPE_[ID]**: The value is **linux**.
        self.platform = platform
        # The target Asset Type. Valid values:
        # 
        # - **all_instance**: All servers.
        # - **instance**: By server.
        # - **group**: By group.
        # - **vpc**: By VPC.
        # 
        # This parameter is required.
        self.target_type = target_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.business_type is not None:
            result['BusinessType'] = self.business_type

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.platform is not None:
            result['Platform'] = self.platform

        if self.target_type is not None:
            result['TargetType'] = self.target_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BusinessType') is not None:
            self.business_type = m.get('BusinessType')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('Platform') is not None:
            self.platform = m.get('Platform')

        if m.get('TargetType') is not None:
            self.target_type = m.get('TargetType')

        return self

