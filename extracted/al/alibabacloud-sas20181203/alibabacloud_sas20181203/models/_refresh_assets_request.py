# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class RefreshAssetsRequest(DaraModel):
    def __init__(
        self,
        asset_type: str = None,
        auth_ids: List[int] = None,
        client_token: str = None,
        cloud_asset_sub_type: int = None,
        cloud_asset_type: int = None,
        cluster_ids: List[str] = None,
        resource_directory_account_id: int = None,
        scope_ids: List[str] = None,
        vendor: int = None,
    ):
        # The asset type for synchronization. Default value: **ecs**. Valid values:
        # - **cloud_product**: Cloud service
        # - **ecs**: Server
        # - **container_image**: Container image
        # - **cloud_k8s**: Multi-cloud Kubernetes clusters and nodes. If you specify this value, you must also specify Vendor and ClientToken. The API only accepts asynchronous tasks. You can call the GetCloudK8sSyncTask operation to query the result.
        self.asset_type = asset_type
        # The IDs of the authorization records. You can specify up to 1,000 IDs. This parameter is only used when AssetType is set to cloud_k8s. If you do not specify this parameter or specify an empty array, all available authorizations for the specified cloud provider under the current tenant are selected.
        self.auth_ids = auth_ids
        # The idempotency key that is 1 to 128 characters in length. This parameter is required when AssetType is set to cloud_k8s. For other asset types, this parameter is optional and validated by the backend based on specific conditions.
        self.client_token = client_token
        # The subtype of the cloud service.
        # 
        # > For more information about valid values, see the following list.
        self.cloud_asset_sub_type = cloud_asset_sub_type
        # The type of the cloud service. Valid values:
        # 
        # - **0**: Elastic Compute Service (ECS) server
        # - **1**: Server Load Balancer (SLB)
        # - **3**: ApsaraDB RDS
        # - **4**: ApsaraDB for MongoDB
        # - **5**: Tair (Redis® OSS-Compatible)
        # - **6**: Container Registry
        # - **8**: Container Service for Kubernetes (ACK)
        # - **9**: Virtual Private Cloud (VPC)
        # - **11**: ActionTrail
        # - **12**: Content Delivery Network (CDN)
        # - **13**: SSL Certificates Service
        # - **14**: Apsara DevOps
        # - **15**: Resource Access Management (RAM)
        # - **16**: Anti-DDoS
        # - **17**: Web Application Firewall (WAF)
        # - **18**: Object Storage Service (OSS)
        # - **19**: PolarDB
        # - **20**: ApsaraDB RDS for PostgreSQL
        # - **21**: Microservices Engine (MSE)
        # - **22**: Apsara File Storage NAS
        # - **23**: Data Security Center (DSC)
        # - **24**: Elastic IP Address (EIP)
        self.cloud_asset_type = cloud_asset_type
        # The locators of the cloud provider clusters. You can specify up to 1,000 locators. This parameter is only used when AssetType is set to cloud_k8s. If you do not specify this parameter or specify an empty array, it indicates full coverage of the region.
        self.cluster_ids = cluster_ids
        # The ID of the Alibaba Cloud account that is one of the resource directory member accounts.
        # > You can call the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The regions of the cloud provider. You can specify up to 1,000 regions. This parameter is only used when AssetType is set to cloud_k8s. If you do not specify this parameter or specify an empty array, the regions are expanded by using the region API.
        self.scope_ids = scope_ids
        # The cloud provider of the server. Valid values:
        # 
        # - **0**: Alibaba Cloud assets
        # - **1**: Assets outside Alibaba Cloud
        # - **2**: IDC assets
        # - **3**, **4**, **5**, and **7**: Assets on other cloud platforms
        # - **8**: Simple Application Server assets
        self.vendor = vendor

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.asset_type is not None:
            result['AssetType'] = self.asset_type

        if self.auth_ids is not None:
            result['AuthIds'] = self.auth_ids

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.cloud_asset_sub_type is not None:
            result['CloudAssetSubType'] = self.cloud_asset_sub_type

        if self.cloud_asset_type is not None:
            result['CloudAssetType'] = self.cloud_asset_type

        if self.cluster_ids is not None:
            result['ClusterIds'] = self.cluster_ids

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.scope_ids is not None:
            result['ScopeIds'] = self.scope_ids

        if self.vendor is not None:
            result['Vendor'] = self.vendor

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AssetType') is not None:
            self.asset_type = m.get('AssetType')

        if m.get('AuthIds') is not None:
            self.auth_ids = m.get('AuthIds')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('CloudAssetSubType') is not None:
            self.cloud_asset_sub_type = m.get('CloudAssetSubType')

        if m.get('CloudAssetType') is not None:
            self.cloud_asset_type = m.get('CloudAssetType')

        if m.get('ClusterIds') is not None:
            self.cluster_ids = m.get('ClusterIds')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('ScopeIds') is not None:
            self.scope_ids = m.get('ScopeIds')

        if m.get('Vendor') is not None:
            self.vendor = m.get('Vendor')

        return self

