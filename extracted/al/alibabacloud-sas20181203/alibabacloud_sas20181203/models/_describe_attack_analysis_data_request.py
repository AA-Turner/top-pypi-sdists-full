# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeAttackAnalysisDataRequest(DaraModel):
    def __init__(
        self,
        base_64: str = None,
        current_page: int = None,
        data: str = None,
        end_time: int = None,
        lang: str = None,
        page_size: int = None,
        start_time: int = None,
        type: str = None,
    ):
        # Specifies whether to perform Base64 encoding on **client_url** in the query results. Valid values:
        # 
        # - **true**: yes
        # - **false**: no
        self.base_64 = base_64
        # The number of the page to return. Pages start from **1**.
        # 
        # > If you set Type to **DETAILS**, this parameter is required.
        self.current_page = current_page
        # The filter conditions for attack events.
        # > Description of the crack_type field:
        # > - 3: MySQL brute-force attacks
        # > - 4: FTP brute-force attacks
        # > - 5: SSH brute-force attacks
        # > - 6: RDP brute-force attacks
        # > - 9: SQL Server brute-force attacks
        # > - 101: Java Struts2 attack interception
        # > - 102: Redis attack interception
        # > - 103: AntSword WebShell communication
        # > - 104: China Chopper WebShell communication
        # > - 133: XISE WebShell communication
        # > - sqli: SQL injection
        # > - codei: code execution
        # > - xss: XSS attack
        # > - lfi: local file inclusion (LFI)
        # > - rfi: remote file inclusion (RFI)
        # > - webshell: web shell
        # > - upload: upload vulnerability
        # > - path: directory traversal
        # > - bypass: unauthorized access
        # > - csrf: CSRF
        # > - crlf: CRLF
        # > - other: other
        self.data = data
        # The timestamp when the attack ended. Unit: seconds.
        # 
        # This parameter is required.
        self.end_time = end_time
        # The language of the request and response messages. Default value: **zh**. Valid values:
        # 
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # Settings for the paged query: the number of attack events to return on each paging page.
        # > If you set Type to **DETAILS**, this parameter is required.
        self.page_size = page_size
        # The timestamp when the attack started. By default, the data of the last 7 days is queried. Unit: seconds.
        # > The start time can only be within the last 40 days.
        # 
        # This parameter is required.
        self.start_time = start_time
        # The details of the attack analysis. Valid values:
        # 
        # - **TOTAL**: the number of attacks
        # - **TREND**: the attack trend
        # - **PIE_CHART**: Attack Type Distribution
        # - **SOURCE_TOP**: the top 5 attack sources
        # - **CLIENT_TOP**: the top 5 attacked assets
        # - **DETAILS**: the list of attack details
        # 
        # > If you set Type to **DETAILS**, the paging parameters are required.
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.base_64 is not None:
            result['Base64'] = self.base_64

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.data is not None:
            result['Data'] = self.data

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Base64') is not None:
            self.base_64 = m.get('Base64')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('Data') is not None:
            self.data = m.get('Data')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

