# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeDiagnosisMonitorPerformanceRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        database: str = None,
        end_time: str = None,
        query_condition: str = None,
        start_time: str = None,
        user: str = None,
    ):
        # The ID of the instance.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the details of all AnalyticDB for PostgreSQL instances in the specified region, including instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The name of the database.
        # 
        # This parameter is required.
        self.database = database
        # The end time of the query. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        self.end_time = end_time
        # The filter conditions for the query. The value must be in JSON format. Valid values:
        # 
        # - `{"Type":"maxCost", "Value":"100"}`: The 100 queries that take the longest time to execute.
        # - `{"Type":"status","Value":"finished"}`: Completed queries.
        # - `{"Type":"status","Value":"running"}`: Running queries.
        # - `{"Type":"cost","Min":"30","Max":"50"}`: Queries with custom execution durations. You can specify the minimum and maximum execution durations. **Min** specifies the minimum execution duration. **Max** specifies the maximum execution duration. Unit: milliseconds.
        #     - If you specify only **Min**, the system returns queries whose execution duration is greater than the specified value.
        #     - If you specify only **Max**, the system returns queries whose execution duration is less than the specified value.
        #     - If you specify both **Min** and **Max**, the system returns queries whose execution duration is greater than or equal to the value of **Min** and less than or equal to the value of **Max**.
        self.query_condition = query_condition
        # The start time of the query. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
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

        if self.query_condition is not None:
            result['QueryCondition'] = self.query_condition

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

        if m.get('QueryCondition') is not None:
            self.query_condition = m.get('QueryCondition')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('User') is not None:
            self.user = m.get('User')

        return self

