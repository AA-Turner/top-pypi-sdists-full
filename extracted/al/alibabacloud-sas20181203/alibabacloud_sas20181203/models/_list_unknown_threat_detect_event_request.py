# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ListUnknownThreatDetectEventRequest(DaraModel):
    def __init__(
        self,
        analyze_result: str = None,
        current_page: int = None,
        hash_key: str = None,
        lang: str = None,
        page_size: int = None,
        parent_process_path: str = None,
        process_path: str = None,
        remark: str = None,
        status: int = None,
        uuid: str = None,
    ):
        # The analysis result. Valid values:
        # - **black**: Abnormal process
        # - **white**: Normal process
        self.analyze_result = analyze_result
        # The page number of the current page for paging in a paged query.
        self.current_page = current_page
        # The unique identifier of the file.
        self.hash_key = hash_key
        # The language of the request and response. Default value: **zh**. Valid values:
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # The maximum number of entries to return on each page for paging in a paged query.
        self.page_size = page_size
        # The path of the parent process.
        self.parent_process_path = parent_process_path
        # The path of the process.
        self.process_path = process_path
        # The keyword used to filter results by instance name or IP address.
        self.remark = remark
        # The status of the event. Valid values:
        # 
        # - **1**: Unhandled.
        # - **2**: Blocked.
        # - **3**: Ignored.
        self.status = status
        # The UUID of the server to query.
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.analyze_result is not None:
            result['AnalyzeResult'] = self.analyze_result

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.hash_key is not None:
            result['HashKey'] = self.hash_key

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.parent_process_path is not None:
            result['ParentProcessPath'] = self.parent_process_path

        if self.process_path is not None:
            result['ProcessPath'] = self.process_path

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.status is not None:
            result['Status'] = self.status

        if self.uuid is not None:
            result['Uuid'] = self.uuid

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnalyzeResult') is not None:
            self.analyze_result = m.get('AnalyzeResult')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('HashKey') is not None:
            self.hash_key = m.get('HashKey')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('ParentProcessPath') is not None:
            self.parent_process_path = m.get('ParentProcessPath')

        if m.get('ProcessPath') is not None:
            self.process_path = m.get('ProcessPath')

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')

        return self

