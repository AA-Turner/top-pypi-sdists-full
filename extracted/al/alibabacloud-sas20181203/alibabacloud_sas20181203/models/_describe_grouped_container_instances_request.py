# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeGroupedContainerInstancesRequest(DaraModel):
    def __init__(
        self,
        criteria: str = None,
        current_page: int = None,
        field_value: str = None,
        group_field: str = None,
        include_multicloud: bool = None,
        logical_exp: str = None,
        page_size: int = None,
    ):
        # The conditions for searching assets. The value is in JSON format. Separate multiple conditions with commas (,). Example: `[{"name":"riskStatus","value":"YES"},{"name":"riskLevel","value":"2"}]`.
        # > You can search for assets by using conditions such as the instance ID, instance name, VPC ID, region, and public IP address. You can call the [DescribeCriteria](~~DescribeCriteria~~) operation to query the supported search conditions.
        self.criteria = criteria
        # The page number of the page to return. Default value: **1**.
        self.current_page = current_page
        # The search condition for different group types. Specify the search condition based on the value of GroupField:
        # - If **GroupField** is set to **pod**, specify the name of the pod to query.
        # - If **GroupField** is set to **appName**, specify the name of the application to query.
        # - If **GroupField** is set to **namespace**, specify the namespace to query.
        # - If **GroupField** is set to **clusterId**, specify the ID of the cluster to query.
        # - If **GroupField** is set to **image**, specify the name of the image to query.
        # > Fuzzy search is supported for all the preceding search conditions.
        self.field_value = field_value
        # The group type to query. Valid values:
        # - **pod**: pod.
        # - **appName**: application name.
        # - **namespace**: namespace.
        # - **clusterId**: cluster ID.
        # - **image**: image.
        # 
        # This parameter is required.
        self.group_field = group_field
        # Specifies whether to enable the unified multi-cloud directory. This parameter takes effect only when GroupField is set to clusterId. If this parameter is omitted or set to false, the historical query logic is used.
        self.include_multicloud = include_multicloud
        # The logical relationship among multiple search conditions. Valid values:
        # - **OR**: The logical relationship among multiple conditions is **OR**.
        # - **AND**: The logical relationship among multiple conditions is **AND**.
        self.logical_exp = logical_exp
        # Settings for paging in a paged query, specifying the number of container assets to return on each page. Default value: **20**, which indicates that 20 container asset entries are displayed on each page.
        # > Do not leave PageSize empty.
        self.page_size = page_size

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

        if self.field_value is not None:
            result['FieldValue'] = self.field_value

        if self.group_field is not None:
            result['GroupField'] = self.group_field

        if self.include_multicloud is not None:
            result['IncludeMulticloud'] = self.include_multicloud

        if self.logical_exp is not None:
            result['LogicalExp'] = self.logical_exp

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Criteria') is not None:
            self.criteria = m.get('Criteria')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('FieldValue') is not None:
            self.field_value = m.get('FieldValue')

        if m.get('GroupField') is not None:
            self.group_field = m.get('GroupField')

        if m.get('IncludeMulticloud') is not None:
            self.include_multicloud = m.get('IncludeMulticloud')

        if m.get('LogicalExp') is not None:
            self.logical_exp = m.get('LogicalExp')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        return self

