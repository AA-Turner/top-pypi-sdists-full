# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class UpdateClientAlertModeRequest(DaraModel):
    def __init__(
        self,
        mode: str = None,
        resource_directory_account_id: int = None,
        uuids: List[str] = None,
    ):
        # Specifies the protection mode. Valid values:
        # - **strict**: Strict mode. Defense mode has a certain risk of false positives and is recommended during critical event protection.
        # - **balance**: Balanced mode. Defense mode detects more suspicious risks while reducing false positives.
        self.mode = mode
        self.resource_directory_account_id = resource_directory_account_id
        # The list of server UUIDs.
        self.uuids = uuids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.mode is not None:
            result['Mode'] = self.mode

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.uuids is not None:
            result['Uuids'] = self.uuids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Uuids') is not None:
            self.uuids = m.get('Uuids')

        return self

