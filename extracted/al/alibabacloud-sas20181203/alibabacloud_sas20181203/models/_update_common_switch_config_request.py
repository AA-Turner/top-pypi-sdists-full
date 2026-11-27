# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class UpdateCommonSwitchConfigRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        target_default: str = None,
        type: str = None,
    ):
        self.resource_directory_account_id = resource_directory_account_id
        # Specifies whether the switch takes effect by default. Valid values:
        # 
        # - **add**: Takes effect by default for newly added servers.
        # - **del**: Does not take effect by default for newly added servers.
        self.target_default = target_default
        # The general switch type.
        # >You can obtain this parameter from the SwitchId response parameter of the [ListClientUserDefineRules](~~ListClientUserDefineRules~~) and [ListSystemClientRules](~~ListSystemClientRules~~) operations.
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

        if self.target_default is not None:
            result['TargetDefault'] = self.target_default

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('TargetDefault') is not None:
            self.target_default = m.get('TargetDefault')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

