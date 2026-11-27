# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ListK8sAccessInfoRequest(DaraModel):
    def __init__(
        self,
        aliyun_yundun_gateway_api_name: str = None,
        aliyun_yundun_gateway_pop_name: str = None,
        aliyun_yundun_gateway_project_name: str = None,
        cluster_id: str = None,
        lang: str = None,
    ):
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_api_name = aliyun_yundun_gateway_api_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_pop_name = aliyun_yundun_gateway_pop_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_project_name = aliyun_yundun_gateway_project_name
        # Optional. If you specify this parameter, the system queries only the independent installation records for the current multi-cloud lifecycle under the trusted tenant.
        self.cluster_id = cluster_id
        # The language type of the request and response messages. Valid values:
        # - **zh**: Chinese.
        # - **en**: English.
        self.lang = lang

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

        if self.lang is not None:
            result['Lang'] = self.lang

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

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        return self

