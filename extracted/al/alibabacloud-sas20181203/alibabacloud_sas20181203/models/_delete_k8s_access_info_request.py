# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DeleteK8sAccessInfoRequest(DaraModel):
    def __init__(
        self,
        aliyun_yundun_gateway_api_name: str = None,
        aliyun_yundun_gateway_pop_name: str = None,
        aliyun_yundun_gateway_project_name: str = None,
        cluster_id: str = None,
        id: int = None,
    ):
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_api_name = aliyun_yundun_gateway_api_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_pop_name = aliyun_yundun_gateway_pop_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_project_name = aliyun_yundun_gateway_project_name
        # The cluster ID. To delete multi-cloud installation information, you must specify both the ClusterId and Id parameters. If you omit this parameter, the legacy self-managed path is retained.
        self.cluster_id = cluster_id
        # The default value generated when connecting to Kubernetes. You can obtain the ID by calling the [GenerateK8sAccessInfo](https://help.aliyun.com/document_detail/2623602.html) operation.
        # 
        # This parameter is required.
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.aliyun_yundun_gateway_api_name is not None:
            result['AliyunYundunGatewayApiName'] = self.aliyun_yundun_gateway_api_name

        if self.aliyun_yundun_gateway_pop_name is not None:
            result['AliyunYundunGatewayPopName'] = self.aliyun_yundun_gateway_pop_name

        if self.aliyun_yundun_gateway_project_name is not None:
            result['AliyunYundunGatewayProjectName'] = self.aliyun_yundun_gateway_project_name

        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id

        if self.id is not None:
            result['Id'] = self.id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AliyunYundunGatewayApiName') is not None:
            self.aliyun_yundun_gateway_api_name = m.get('AliyunYundunGatewayApiName')

        if m.get('AliyunYundunGatewayPopName') is not None:
            self.aliyun_yundun_gateway_pop_name = m.get('AliyunYundunGatewayPopName')

        if m.get('AliyunYundunGatewayProjectName') is not None:
            self.aliyun_yundun_gateway_project_name = m.get('AliyunYundunGatewayProjectName')

        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')

        if m.get('Id') is not None:
            self.id = m.get('Id')

        return self

