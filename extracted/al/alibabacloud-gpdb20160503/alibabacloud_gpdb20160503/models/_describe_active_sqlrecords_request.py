# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeActiveSQLRecordsRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        database: str = None,
        end_time: str = None,
        keyword: str = None,
        max_duration: str = None,
        min_duration: str = None,
        order: str = None,
        start_time: str = None,
        user: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to view the details of all AnalyticDB for PostgreSQL instances in the target region, including the instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The database name. Default value: all databases.
        self.database = database
        # The end time of the query. Format: `yyyy-MM-ddTHH:mm:ssZ`. The end time must be later than the start time.
        self.end_time = end_time
        # The query keyword.
        self.keyword = keyword
        # The maximum execution duration, in seconds.
        self.max_duration = max_duration
        # The minimum execution duration, in seconds. For example, a value of 100 specifies queries that run for more than 100 seconds.
        self.min_duration = min_duration
        # The sort field and sort order.
        # 
        # Default value: `{"Field":"StartTime","Type":"Desc"}`, which indicates sorting by start time in descending order. Other sort fields and sort orders are not supported.
        self.order = order
        # The start time of the query. Format: `yyyy-MM-ddTHH:mm:ssZ`.
        self.start_time = start_time
        # The username.
        self.user = user

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.database is not None:
            result['Database'] = self.database

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.keyword is not None:
            result['Keyword'] = self.keyword

        if self.max_duration is not None:
            result['MaxDuration'] = self.max_duration

        if self.min_duration is not None:
            result['MinDuration'] = self.min_duration

        if self.order is not None:
            result['Order'] = self.order

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        if self.user is not None:
            result['User'] = self.user

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('Database') is not None:
            self.database = m.get('Database')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')

        if m.get('MaxDuration') is not None:
            self.max_duration = m.get('MaxDuration')

        if m.get('MinDuration') is not None:
            self.min_duration = m.get('MinDuration')

        if m.get('Order') is not None:
            self.order = m.get('Order')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('User') is not None:
            self.user = m.get('User')

        return self

