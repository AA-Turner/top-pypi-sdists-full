# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_actiontrail20200706 import models as main_models
from darabonba.model import DaraModel

class LookupEventsRequest(DaraModel):
    def __init__(
        self,
        direction: str = None,
        end_time: str = None,
        lookup_attribute: List[main_models.LookupEventsRequestLookupAttribute] = None,
        max_results: str = None,
        next_token: str = None,
        start_time: str = None,
    ):
        # The order in which details of events are to be retrieved. Valid values:
        # 
        # *   FORWARD: ascending order.
        # *   BACKWARD: descending order. This is the default value.
        self.direction = direction
        # The end of the time range to query. The default time is the current time. Specify the time in the ISO 8601 standard in the `YYYY-MM-DDThh:mm:ssZ` format. The time must be in UTC.
        self.end_time = end_time
        # Query conditions.
        self.lookup_attribute = lookup_attribute
        # The maximum number of entries to be returned.
        # 
        # Valid values: 0 to 50.
        self.max_results = max_results
        # The token used to request the next page of query results.
        # 
        # > The request parameters must be the same as those of the last request.
        self.next_token = next_token
        # The beginning of the time range to query. The default time is seven days prior to the current time. Specify the time in the ISO 8601 standard in the `YYYY-MM-DDThh:mm:ssZ` format. The time must be in UTC.
        self.start_time = start_time

    def validate(self):
        if self.lookup_attribute:
            for v1 in self.lookup_attribute:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.direction is not None:
            result['Direction'] = self.direction

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        result['LookupAttribute'] = []
        if self.lookup_attribute is not None:
            for k1 in self.lookup_attribute:
                result['LookupAttribute'].append(k1.to_map() if k1 else None)

        if self.max_results is not None:
            result['MaxResults'] = self.max_results

        if self.next_token is not None:
            result['NextToken'] = self.next_token

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        self.lookup_attribute = []
        if m.get('LookupAttribute') is not None:
            for k1 in m.get('LookupAttribute'):
                temp_model = main_models.LookupEventsRequestLookupAttribute()
                self.lookup_attribute.append(temp_model.from_map(k1))

        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')

        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        return self

class LookupEventsRequestLookupAttribute(DaraModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        # The key of the query condition. Valid values:
        # 
        # *  ServiceName: the name of a specific Alibaba Cloud service.
        # *  EventName: the name of a specific event.
        # *  User: the name of the RAM user who calls a specific operation.
        # *  EventId: the ID of a specific event.
        # *  ResourceType: the type of resources.
        # *   ResourceName: the name of a specific resource.
        # *   EventRW: the read/write type of events.
        # *  EventAccessKeyId: the AccessKey ID used in events.
        # 
        # > You can use only one query condition for each query.
        self.key = key
        # The value of the query condition. Valid values:
        # 
        # *   When the LookupAttribute.N.Key parameter is set to ServiceName, you can set this parameter to a value such as `Ecs`.
        # *   When the LookupAttribute.N.Key parameter is set to EventName, you can set this parameter to a value such as `ConsoleSignin`.
        # *   When the LookupAttribute.N.Key parameter is set to User, you can set this parameter to a value such as `Alice`.
        # *   When the LookupAttribute.N.Key parameter is set to EventId, you can set this parameter to a value such as `B702AFA3-FD4B-40E3-88E4-C0752FAA****`.
        # *   When the LookupAttribute.N.Key parameter is set to ResourceType, you can set this parameter to a value such as `ACS::ECS::Instance`.
        # *   When the LookupAttribute.N.Key parameter is set to ResourceName, you can set this parameter to a value such as `i-bp14664y88udkt45****`.
        # *   When the LookupAttribute.N.Key parameter is set to EventRW, you can set this parameter to `Read` or `Write`.
        # *   When the LookupAttribute.N.Key parameter is set to EventAccessKeyId, you can set this parameter to a value such as `LTAI****************`.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.key is not None:
            result['Key'] = self.key

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

