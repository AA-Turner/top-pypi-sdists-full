# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GetDataTrendRequest(DaraModel):
    def __init__(
        self,
        biz_types: str = None,
        end_timestamp: int = None,
        interval: int = None,
        resource_directory_account_id: int = None,
        start_timestamp: int = None,
    ):
        # The security data type. Valid values:
        # - **HC_NEW**: the number of new baseline risks
        # - **HC_OPERATE**: the number of handled baseline risks
        # - **VUL_NEW**: the number of new vulnerability risks
        # - **VUL_OPERATE**: the number of handled vulnerability risks
        # - **SUSP_NEW**: the number of new alerts
        # - **SUSP_OPERATE**: the number of handled alerts
        # 
        # > You can specify multiple values separated by commas (,). Example: HC_NEW,VUL_NEW.
        # 
        # This parameter is required.
        self.biz_types = biz_types
        # The end timestamp of the query. Unit: milliseconds.
        # 
        # > The value of StartTimestamp must be earlier than the value of EndTimestamp. Otherwise, the API returns HTTP 400 and the error code -101.
        # 
        # This parameter is required.
        self.end_timestamp = end_timestamp
        # The interval for querying data. Unit: milliseconds.
        # 
        # > The minimum value is 1000. A maximum of 100 data points are returned. Excess data points are not returned.
        # 
        # This parameter is required.
        self.interval = interval
        # The Alibaba Cloud account ID of member accounts in the resource folder.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The start timestamp of the query. Unit: milliseconds.
        # 
        # This parameter is required.
        self.start_timestamp = start_timestamp

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.biz_types is not None:
            result['BizTypes'] = self.biz_types

        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp

        if self.interval is not None:
            result['Interval'] = self.interval

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BizTypes') is not None:
            self.biz_types = m.get('BizTypes')

        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')

        if m.get('Interval') is not None:
            self.interval = m.get('Interval')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')

        return self

