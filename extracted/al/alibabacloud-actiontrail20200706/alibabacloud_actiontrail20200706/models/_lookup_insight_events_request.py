# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_actiontrail20200706 import models as main_models
from darabonba.model import DaraModel

class LookupInsightEventsRequest(DaraModel):
    def __init__(
        self,
        end_time: str = None,
        lookup_attribute: List[main_models.LookupInsightEventsRequestLookupAttribute] = None,
        max_results: str = None,
        next_token: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.lookup_attribute = lookup_attribute
        self.max_results = max_results
        self.next_token = next_token
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
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        self.lookup_attribute = []
        if m.get('LookupAttribute') is not None:
            for k1 in m.get('LookupAttribute'):
                temp_model = main_models.LookupInsightEventsRequestLookupAttribute()
                self.lookup_attribute.append(temp_model.from_map(k1))

        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')

        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        return self

class LookupInsightEventsRequestLookupAttribute(DaraModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
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

