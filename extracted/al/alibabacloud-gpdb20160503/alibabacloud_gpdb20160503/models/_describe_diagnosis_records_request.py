# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeDiagnosisRecordsRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        database: str = None,
        end_time: str = None,
        keyword: str = None,
        order: str = None,
        page_number: int = None,
        page_size: int = None,
        query_condition: str = None,
        start_time: str = None,
        user: str = None,
    ):
        # The ID of the instance.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to view the details of all AnalyticDB for PostgreSQL instances in a specific region, including the instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The name of the database.
        # 
        # This parameter is required.
        self.database = database
        # The end time of the query. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        self.end_time = end_time
        # The SQL keyword.
        self.keyword = keyword
        # This parameter is used to sort fields in the console. You do not need to specify this parameter.
        self.order = order
        # The page number. The value must be greater than 0 and cannot exceed the maximum value of the Integer type. Default value: **1**.
        self.page_number = page_number
        # The number of entries per page. Valid values:
        # - **30**
        # - **50**
        # - **100**
        # 
        # Default value: **30**.
        self.page_size = page_size
        # The filter conditions for the query. The value must be in JSON format. Valid values:
        # 
        # - `{"Type":"maxCost", "Value":"100"}`: the 100 queries with the longest execution duration
        # - `{"Type":"status","Value":"finished"}`: completed queries
        # - `{"Type":"status","Value":"running"}`: running queries
        # - `{"Type":"cost","Min":"30","Max":"50"}`: queries with a custom execution duration. You can specify the minimum and maximum execution durations. **Min** specifies the minimum execution duration, and **Max** specifies the maximum execution duration. Unit: milliseconds.
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

        if self.keyword is not None:
            result['Keyword'] = self.keyword

        if self.order is not None:
            result['Order'] = self.order

        if self.page_number is not None:
            result['PageNumber'] = self.page_number

        if self.page_size is not None:
            result['PageSize'] = self.page_size

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

        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')

        if m.get('Order') is not None:
            self.order = m.get('Order')

        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('QueryCondition') is not None:
            self.query_condition = m.get('QueryCondition')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('User') is not None:
            self.user = m.get('User')

        return self

