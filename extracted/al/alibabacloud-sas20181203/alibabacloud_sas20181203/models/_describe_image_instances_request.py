# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeImageInstancesRequest(DaraModel):
    def __init__(
        self,
        criteria: str = None,
        current_page: int = None,
        logical_exp: str = None,
        page_size: int = None,
        scanned: bool = None,
    ):
        # Specifies the conditions for searching assets. This parameter is in JSON format and contains the following fields:
        # - **name**: The search criterion.
        # - **value**: The value of the search criterion.
        # - **logicalExp**: The logical relationship among multiple search criterion values. Valid values:
        #     - **OR**: indicates that the logical relationship among multiple search criterion values is **OR**.
        #     - **AND**: indicates that the logical relationship among multiple search criterion values is **AND**.
        # > You can call the [DescribeImageCriteria](~~DescribeImageCriteria~~) operation to query the supported search criteria.
        self.criteria = criteria
        # Specifies the page number of the page to return. Pages start from page **1**. Default value: **1**.
        self.current_page = current_page
        # Specifies the logical relationship among multiple search criteria. Valid values:
        # 
        # - **OR**: indicates that the logical relationship among multiple search criteria is **OR**.
        # - **AND**: indicates that the logical relationship among multiple search criteria is **AND**.
        self.logical_exp = logical_exp
        # Specifies the maximum number of entries to return on each page in a paging query. The default number of entries returned per page is 20. If the PageSize parameter is left empty, 20 entries are returned by default.
        # > Specify a value for this parameter.
        self.page_size = page_size
        # Specifies whether the image has been scanned. Valid values:
        # - **true**: The image has been scanned.
        # - **false**: The image has not been scanned.
        self.scanned = scanned

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.criteria is not None:
            result['Criteria'] = self.criteria

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.logical_exp is not None:
            result['LogicalExp'] = self.logical_exp

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.scanned is not None:
            result['Scanned'] = self.scanned

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Criteria') is not None:
            self.criteria = m.get('Criteria')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('LogicalExp') is not None:
            self.logical_exp = m.get('LogicalExp')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('Scanned') is not None:
            self.scanned = m.get('Scanned')

        return self

