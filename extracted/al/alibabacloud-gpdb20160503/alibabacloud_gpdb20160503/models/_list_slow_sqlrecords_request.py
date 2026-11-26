# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ListSlowSQLRecordsRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        dbname: str = None,
        end_time: str = None,
        keyword: str = None,
        max_duration: str = None,
        min_duration: str = None,
        order_by: str = None,
        page_number: int = None,
        page_size: int = None,
        region_id: str = None,
        start_time: str = None,
        user_name: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the details of all AnalyticDB for PostgreSQL instances in a specific region, including the instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The database name.
        self.dbname = dbname
        # The end time of the query. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        # 
        # Default value: The current time.
        self.end_time = end_time
        # The query keyword.
        self.keyword = keyword
        # The maximum execution duration. Unit: seconds.
        self.max_duration = max_duration
        # The minimum execution duration. Unit: seconds.
        self.min_duration = min_duration
        # The sorting conditions in JSON format. Example: {"Field":"QueryStartTime","Type":"Desc"}.
        # 
        # Field: the field to sort by. Valid values:
        # 
        # - QueryID: the query ID.
        # 
        # - UserName: the username.
        # 
        # - DBName: the database name.
        # 
        # - QueryStartTime: the start time.
        # 
        # - QueryEndTime: the end time.
        # 
        # - DurationTime: the execution duration.
        # 
        # - Optimizer: the optimizer.
        # 
        # - LockWaitTime: the lock wait time.
        # 
        # - QueueWaitTime: the queue wait time.
        # 
        # - CpuTimeMs: the CPU time.
        # 
        # - MemBytes: the memory usage.
        # 
        # - SpillBytes: the size of spilled files.
        # 
        # Type: the sorting order. Valid values:
        # 
        # - Desc: descending order.
        # 
        # - Asc: ascending order.
        self.order_by = order_by
        # The page number. The value must be greater than 0 and less than or equal to 100.
        # 
        # Default value: 1.
        self.page_number = page_number
        # The number of entries per page. Valid values:
        # - **30**
        # - **50**
        # - **100**
        # 
        # Default value: **30**.
        self.page_size = page_size
        # The region ID of the instance.
        self.region_id = region_id
        # The start time of the query. Specify the time in the yyyy-MM-ddTHH:mmZ format. The time must be in UTC.
        # 
        # Default value: 5 minutes before the current time.
        self.start_time = start_time
        # The database username.
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.dbname is not None:
            result['DBName'] = self.dbname

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.keyword is not None:
            result['Keyword'] = self.keyword

        if self.max_duration is not None:
            result['MaxDuration'] = self.max_duration

        if self.min_duration is not None:
            result['MinDuration'] = self.min_duration

        if self.order_by is not None:
            result['OrderBy'] = self.order_by

        if self.page_number is not None:
            result['PageNumber'] = self.page_number

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        if self.user_name is not None:
            result['UserName'] = self.user_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('DBName') is not None:
            self.dbname = m.get('DBName')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')

        if m.get('MaxDuration') is not None:
            self.max_duration = m.get('MaxDuration')

        if m.get('MinDuration') is not None:
            self.min_duration = m.get('MinDuration')

        if m.get('OrderBy') is not None:
            self.order_by = m.get('OrderBy')

        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')

        return self

