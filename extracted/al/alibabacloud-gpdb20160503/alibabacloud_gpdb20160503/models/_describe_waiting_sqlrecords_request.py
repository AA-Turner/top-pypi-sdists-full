# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeWaitingSQLRecordsRequest(DaraModel):
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
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the IDs of all AnalyticDB for PostgreSQL instances in the specified region.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The name of the database.
        # 
        # This parameter is required.
        self.database = database
        # The end time of the query. The end time must be later than the start time. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        # 
        # If you do not specify this parameter, no end time is set, and all lock diagnosis information after the start time is returned. If the start time is also not specified, all lock diagnosis information is returned.
        self.end_time = end_time
        # The keyword for the query.
        self.keyword = keyword
        # The sort field and sort order.
        # 
        # Default value: `{"Field":"StartTime","Type":"Desc"}`, which indicates that the results are sorted by start time in descending order. Other sort fields and sort orders are not supported.
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
        # The filter condition for the query. Valid values:
        # 
        # - `{"Type":"maxCost","Value":"10"}`: the top 10 queries with the longest wait time.
        # - `{"Type":"status","Value":"LockWaiting"}`: queries that are waiting for locks.
        # - `{"Type":"status","Value":"ResourceWaiting"}`: queries that are waiting for resources.
        # 
        # This parameter is required.
        self.query_condition = query_condition
        # The start time of the query. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm</i>Z format. The time must be in UTC.
        # 
        # If you do not specify this parameter, no start time is set, and all lock diagnosis information before the end time is returned. If the end time is also not specified, all lock diagnosis information is returned.
        self.start_time = start_time
        # The username. If you do not specify this parameter, the lock wait information of all users is queried.
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

