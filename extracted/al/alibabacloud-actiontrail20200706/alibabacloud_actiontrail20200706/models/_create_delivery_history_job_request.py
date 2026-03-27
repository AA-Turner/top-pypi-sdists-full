# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateDeliveryHistoryJobRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        trail_name: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You can use the client to generate the value, but you must make sure that it is unique among different requests.
        # 
        # The token can contain only ASCII characters and can be up to 64 characters in length.
        # 
        # For more information, see [How to ensure idempotence](https://help.aliyun.com/document_detail/25693.html).
        self.client_token = client_token
        # The name of the trail for which you want to create a historical event delivery task.
        # 
        # This parameter is required.
        self.trail_name = trail_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.trail_name is not None:
            result['TrailName'] = self.trail_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('TrailName') is not None:
            self.trail_name = m.get('TrailName')

        return self

