# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeModelOperatorUsageShrinkRequest(DaraModel):
    def __init__(
        self,
        api_key_ids_shrink: str = None,
        end_time: str = None,
        group_by: str = None,
        keys_shrink: str = None,
        model_names_shrink: str = None,
        period: int = None,
        start_time: str = None,
    ):
        # The list of API key IDs. Separate multiple IDs with commas (,). If this parameter is not specified, all API key IDs under the instance ID are used by default.
        # 
        # > A maximum of 50 items can be included in the list.
        self.api_key_ids_shrink = api_key_ids_shrink
        # The end time of the query. The format is <i>YYYY-MM-DDThh:mmZ</i> (UTC time).
        # 
        # > The end time must be later than the start time, and the interval between the start time and the end time cannot exceed 7 days.
        self.end_time = end_time
        # The dimension for splitting series. Separate multiple dimensions with commas (,). The order does not matter. Valid values:
        # 
        # - model (default): Splits by model.
        # - api_key: Splits by API key.
        # - model,api_key: Splits by model and API key.
        self.group_by = group_by
        # The list of metrics. Separate multiple metrics with commas (,). Valid values:
        # 
        # - request_count: The number of requests.
        # - success_count: The number of successful requests.
        # - error_count: The number of failed requests.
        # - success_rate: The request success rate.
        # - input_token: The number of input tokens.
        # - output_token: The number of output tokens.
        # - total_token: The total number of tokens.
        self.keys_shrink = keys_shrink
        # The list of model names. Separate multiple names with commas (,).
        self.model_names_shrink = model_names_shrink
        # The time bucket size in seconds. Valid values: 1, 5, 15, 60, 300, and 3600.
        # 
        # >
        # > - 1. If Period is not specified, the default value is selected based on the following rules:
        # > - - If the time window is less than or equal to 1 hour, Period is set to 1.
        # > - - If the time window is less than or equal to 1 day, Period is set to 60.
        # > - - If the time window is less than or equal to 7 days, Period is set to 60.
        # > - 2. If Period is set to 1, the time window must be less than or equal to 1 day.
        self.period = period
        # The start time of the query. The format is <i>YYYY-MM-DDThh:mmZ</i> (UTC time).
        # 
        # > You can query only metrics from the last 30 days.
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.api_key_ids_shrink is not None:
            result['ApiKeyIds'] = self.api_key_ids_shrink

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.group_by is not None:
            result['GroupBy'] = self.group_by

        if self.keys_shrink is not None:
            result['Keys'] = self.keys_shrink

        if self.model_names_shrink is not None:
            result['ModelNames'] = self.model_names_shrink

        if self.period is not None:
            result['Period'] = self.period

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApiKeyIds') is not None:
            self.api_key_ids_shrink = m.get('ApiKeyIds')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('GroupBy') is not None:
            self.group_by = m.get('GroupBy')

        if m.get('Keys') is not None:
            self.keys_shrink = m.get('Keys')

        if m.get('ModelNames') is not None:
            self.model_names_shrink = m.get('ModelNames')

        if m.get('Period') is not None:
            self.period = m.get('Period')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        return self

