# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DeleteModelOperatorApiKeyRequest(DaraModel):
    def __init__(
        self,
        api_key_id: int = None,
    ):
        # The ID of the API key to delete. The value must be an integer greater than 0. You can obtain the ID by calling ListModelOperatorApiKeys.
        # 
        # This parameter is required.
        self.api_key_id = api_key_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.api_key_id is not None:
            result['ApiKeyId'] = self.api_key_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApiKeyId') is not None:
            self.api_key_id = m.get('ApiKeyId')

        return self

