# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class ListOperationProcessRequest(DaraModel):
    def __init__(
        self,
        check_id: int = None,
        current_page: int = None,
        end_time: int = None,
        instance_id: str = None,
        page_size: int = None,
        realtime: bool = None,
        service_name: str = None,
        start_time: int = None,
        status_codes: List[int] = None,
        task_ids: List[str] = None,
        task_sources: List[str] = None,
        task_types: List[str] = None,
    ):
        # The real-time check item ID. This parameter takes effect only when Realtime is set to true. It is used to precisely filter specified check items. The value must be greater than 0. If this parameter is not specified, check items are not filtered.
        self.check_id = check_id
        # The page number of the current page returned during paging in a paged query.
        self.current_page = current_page
        # The end time of the query based on the task completion time. Unit: milliseconds.
        self.end_time = end_time
        # The instance ID of the real-time check asset. This parameter takes effect only when Realtime is set to true. An exact match is performed on the original instance ID of the asset. Fuzzy match is not supported. The value can be up to 255 characters in length. If this parameter is not specified, instances are not filtered.
        self.instance_id = instance_id
        # The number of entries per page.
        self.page_size = page_size
        # Specifies whether to query real-time check records. Valid values:
        # - true: queries independent real-time task records. Each record corresponds to one asset and one check item triggered at a time.
        # - false or not specified: queries original periodic or manual tasks. The following real-time specific filter parameters take effect only when this parameter is set to true.
        self.realtime = realtime
        # The original identity of the cloud service that triggers the real-time check. This parameter takes effect only when Realtime is set to true. An exact match is performed on the service name in the ActionTrail event, such as Ecs. The value can be up to 128 characters in length. If this parameter is not specified, cloud services are not filtered.
        self.service_name = service_name
        # The start time of the query based on the task creation time. Unit: milliseconds.
        self.start_time = start_time
        # The list of task status codes.
        self.status_codes = status_codes
        # The list of task IDs.
        self.task_ids = task_ids
        # The list of task sources.
        self.task_sources = task_sources
        # The task types. Valid values:
        # - CHECK_ALL: full check
        # - CHECK_POLICY: check executed based on the check items of the configured policy
        # - CHECK_SCHEDULE: scheduled check
        # - CHECK_ITEM: check executed based on specified check items
        # - CHECK_INSTANCE: check executed based on specified check items and instances
        self.task_types = task_types

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_id is not None:
            result['CheckId'] = self.check_id

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.realtime is not None:
            result['Realtime'] = self.realtime

        if self.service_name is not None:
            result['ServiceName'] = self.service_name

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        if self.status_codes is not None:
            result['StatusCodes'] = self.status_codes

        if self.task_ids is not None:
            result['TaskIds'] = self.task_ids

        if self.task_sources is not None:
            result['TaskSources'] = self.task_sources

        if self.task_types is not None:
            result['TaskTypes'] = self.task_types

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('Realtime') is not None:
            self.realtime = m.get('Realtime')

        if m.get('ServiceName') is not None:
            self.service_name = m.get('ServiceName')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('StatusCodes') is not None:
            self.status_codes = m.get('StatusCodes')

        if m.get('TaskIds') is not None:
            self.task_ids = m.get('TaskIds')

        if m.get('TaskSources') is not None:
            self.task_sources = m.get('TaskSources')

        if m.get('TaskTypes') is not None:
            self.task_types = m.get('TaskTypes')

        return self

