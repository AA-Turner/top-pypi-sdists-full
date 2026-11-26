# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DownloadDiagnosisRecordsRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        database: str = None,
        end_time: str = None,
        lang: str = None,
        query_condition: str = None,
        resource_group_id: str = None,
        start_time: str = None,
        user: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to view the details of all AnalyticDB for PostgreSQL instances in a specific region, including the instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The database name.
        # 
        # This parameter is required.
        self.database = database
        # The end time of the query. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        self.end_time = end_time
        # The language of the downloaded file. Valid values:
        # 
        # - **zh**: Simplified Chinese.
        # - **en**: English.
        # - **ja**: Japanese.
        # - **zh-tw**: Traditional Chinese.
        self.lang = lang
        # The query filter conditions in JSON format. Valid values:
        # 
        # - `{"Type":"maxCost", "Value":"100"}`: The 100 queries with the longest execution duration.
        # - `{"Type":"status","Value":"finished"}`: Completed queries.
        # - `{"Type":"status","Value":"running"}`: Running queries.
        # - `{"Type":"cost","Max":"200"}`: Short-duration queries, which are queries with an execution duration of less than 200 milliseconds.
        # - `{"Type":"cost","Min":"200","Max":"60000"}`: Medium-duration queries, which are queries with an execution duration of 200 milliseconds or more but less than 1 minute.
        # - `{"Type":"cost","Min":"60000"}`: Long-duration queries, which are queries with an execution duration of 1 minute or more.
        # - `{"Type":"cost","Min":"30","Max":"50"}`: Custom-duration queries. You can specify the minimum and maximum execution duration of the queries. **Min** specifies the minimum execution duration, and **Max** specifies the maximum execution duration. Unit: milliseconds.
        self.query_condition = query_condition
        # **[Deprecated]** This parameter is deprecated. You do not need to specify this parameter.
        self.resource_group_id = resource_group_id
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

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.query_condition is not None:
            result['QueryCondition'] = self.query_condition

        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id

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

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('QueryCondition') is not None:
            self.query_condition = m.get('QueryCondition')

        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('User') is not None:
            self.user = m.get('User')

        return self

