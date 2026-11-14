# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DeleteModelOperatorApiKeyResponseBody(DaraModel):
    def __init__(
        self,
        api_key_id: int = None,
        request_id: str = None,
    ):
        # The ID of the API key for which the deletion is accepted. The return of this field does not indicate that the underlying cleanup is complete.
        self.api_key_id = api_key_id
        # The ID of the request. You can use the ID to locate and troubleshoot the request.
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.api_key_id is not None:
            result['ApiKeyId'] = self.api_key_id

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApiKeyId') is not None:
            self.api_key_id = m.get('ApiKeyId')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        return self

