# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeHybridProxyLinkedClientListRequest(DaraModel):
    def __init__(
        self,
        cluster_name: str = None,
        current_page: int = None,
        page_size: int = None,
        proxy_uuid: str = None,
        remark: str = None,
        uuid: str = None,
    ):
        # The name of the proxy cluster. You can view the name in the Security Center console.
        # > **ProxyUuid** and **ClusterName** cannot be left empty at the same time. If neither is provided, the API returns an HTTP 400 error with the error code -101.
        self.cluster_name = cluster_name
        # The page number of the current page returned in a paging query.
        self.current_page = current_page
        # The maximum number of entries to return on each page in a paging query.
        self.page_size = page_size
        # The UUID of the proxy node.
        # > You can call the [DescribeHybridProxyList](~~DescribeHybridProxyList~~) operation to obtain this parameter from the ProxyList[].ProxyUuid field in the response.
        # > **ProxyUuid** and **ClusterName** cannot be left empty at the same time. If neither is provided, the API returns an HTTP 400 error with the error code -101.
        self.proxy_uuid = proxy_uuid
        # The remarks.
        self.remark = remark
        # The unique key of the Security Center client. You can obtain the UUID of the Security Center client installed on a server by querying the asset.
        self.uuid = uuid

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.cluster_name is not None:
            result['ClusterName'] = self.cluster_name

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.proxy_uuid is not None:
            result['ProxyUuid'] = self.proxy_uuid

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.uuid is not None:
            result['Uuid'] = self.uuid

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterName') is not None:
            self.cluster_name = m.get('ClusterName')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('ProxyUuid') is not None:
            self.proxy_uuid = m.get('ProxyUuid')

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')

        return self

