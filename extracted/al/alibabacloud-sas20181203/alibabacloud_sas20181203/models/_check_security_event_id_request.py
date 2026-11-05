# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class CheckSecurityEventIdRequest(DaraModel):
    def __init__(
        self,
        security_event_ids: List[str] = None,
        uuid: str = None,
    ):
        # The IDs of the alert events to be verified. You can specify up to 100 alert event IDs. If this parameter is left empty, the verification result **Data** defaults to **false**, indicating that the events do not belong to the specified server.
        # > Call the [DescribeSuspEvents](~~DescribeSuspEvents~~) operation to retrieve this parameter.
        self.security_event_ids = security_event_ids
        # The UUID of the server to be verified.
        # > Call the [DescribeCloudCenterInstances](~~DescribeCloudCenterInstances~~) operation to retrieve this parameter.
        # 
        # This parameter is required.
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.security_event_ids is not None:
            result['SecurityEventIds'] = self.security_event_ids

        if self.uuid is not None:
            result['Uuid'] = self.uuid

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SecurityEventIds') is not None:
            self.security_event_ids = m.get('SecurityEventIds')

        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')

        return self

