# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeContainerCriteriaRequest(DaraModel):
    def __init__(
        self,
        group_field: str = None,
        include_multicloud: bool = None,
        value: str = None,
    ):
        # The search field. Valid values:
        # - **pod**: Pod.
        # - **appName**: Application name.
        # - **clusterId**: Cluster ID.
        # - **namespace**: Namespace.
        # - **image**: Image.
        # - **containerScan**: Container scan.
        self.group_field = group_field
        # Specifies whether to include connected multi-cloud clusters in the cluster search criteria. If this parameter is set to true, GroupField must be set to clusterId. If this parameter is not specified or is set to false, the original search criteria are used.
        self.include_multicloud = include_multicloud
        # The value of the search field. Fuzzy search is supported for application names, node names, namespaces, cluster names, public IP addresses, pod IP addresses, regions, pods, instance IDs, cluster IDs, and container IDs.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.group_field is not None:
            result['GroupField'] = self.group_field

        if self.include_multicloud is not None:
            result['IncludeMulticloud'] = self.include_multicloud

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupField') is not None:
            self.group_field = m.get('GroupField')

        if m.get('IncludeMulticloud') is not None:
            self.include_multicloud = m.get('IncludeMulticloud')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

