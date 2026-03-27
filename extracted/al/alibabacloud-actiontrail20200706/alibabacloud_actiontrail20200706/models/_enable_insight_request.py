# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class EnableInsightRequest(DaraModel):
    def __init__(
        self,
        insight_type: str = None,
    ):
        # The type of the Insights event. Valid values:
        # 
        # *   IpInsight: Insights event on IP address
        # *   ApiCallRateInsight: Insights event on API call rate
        # *   ApiErrorRateInsight: Insights event on API error rate
        self.insight_type = insight_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.insight_type is not None:
            result['InsightType'] = self.insight_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InsightType') is not None:
            self.insight_type = m.get('InsightType')

        return self

