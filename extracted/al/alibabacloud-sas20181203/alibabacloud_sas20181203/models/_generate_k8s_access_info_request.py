# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class GenerateK8sAccessInfoRequest(DaraModel):
    def __init__(
        self,
        aliyun_yundun_gateway_api_name: str = None,
        aliyun_yundun_gateway_pop_name: str = None,
        aliyun_yundun_gateway_project_name: str = None,
        audit_log_store: str = None,
        audit_project: str = None,
        audit_region_id: str = None,
        cluster_id: str = None,
        cluster_name: str = None,
        cpu_arch: str = None,
        deployment_profile_codes: List[str] = None,
        expire_date: int = None,
        group_id: int = None,
        install_policy_version: str = None,
        vendor: str = None,
    ):
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_api_name = aliyun_yundun_gateway_api_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_pop_name = aliyun_yundun_gateway_pop_name
        # **[Deprecated]** This parameter is deprecated and can be ignored.
        self.aliyun_yundun_gateway_project_name = aliyun_yundun_gateway_project_name
        # The SLS Logstore for the audit log.
        self.audit_log_store = audit_log_store
        # The Simple Log Service (SLS) project for the audit log.
        self.audit_project = audit_project
        # The region of the audit log.
        self.audit_region_id = audit_region_id
        # The multi-cloud cluster ID generated synchronously by the server. This parameter is optional. If provided, the cluster must belong to the current trusted tenant and remain valid.
        self.cluster_id = cluster_id
        # The name of the Kubernetes cluster.
        self.cluster_name = cluster_name
        # The CPU architecture, which can be the ARM architecture or the x86 architecture.
        self.cpu_arch = cpu_arch
        # The expected deployment profiles. The server re-verifies the authorization, directory, and actual capabilities.
        self.deployment_profile_codes = deployment_profile_codes
        # The expiration time for container access. The value is a UNIX timestamp in milliseconds.
        # 
        # This parameter is required.
        self.expire_date = expire_date
        # The ID of the host group.
        self.group_id = group_id
        # The new multi-cloud policy cloud-k8s-install-v2. If omitted, the historical behavior is retained.
        self.install_policy_version = install_policy_version
        # The cloud asset provider. Valid values:
        # - **Tencent**
        # - **HUAWEICLOUD**
        # - **Azure**
        # - **AWS** 
        # - **Other cloud assets**
        self.vendor = vendor

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

        if self.audit_log_store is not None:
            result['AuditLogStore'] = self.audit_log_store

        if self.audit_project is not None:
            result['AuditProject'] = self.audit_project

        if self.audit_region_id is not None:
            result['AuditRegionId'] = self.audit_region_id

        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id

        if self.cluster_name is not None:
            result['ClusterName'] = self.cluster_name

        if self.cpu_arch is not None:
            result['CpuArch'] = self.cpu_arch

        if self.deployment_profile_codes is not None:
            result['DeploymentProfileCodes'] = self.deployment_profile_codes

        if self.expire_date is not None:
            result['ExpireDate'] = self.expire_date

        if self.group_id is not None:
            result['GroupId'] = self.group_id

        if self.install_policy_version is not None:
            result['InstallPolicyVersion'] = self.install_policy_version

        if self.vendor is not None:
            result['Vendor'] = self.vendor

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AliyunYundunGatewayApiName') is not None:
            self.aliyun_yundun_gateway_api_name = m.get('AliyunYundunGatewayApiName')

        if m.get('AliyunYundunGatewayPopName') is not None:
            self.aliyun_yundun_gateway_pop_name = m.get('AliyunYundunGatewayPopName')

        if m.get('AliyunYundunGatewayProjectName') is not None:
            self.aliyun_yundun_gateway_project_name = m.get('AliyunYundunGatewayProjectName')

        if m.get('AuditLogStore') is not None:
            self.audit_log_store = m.get('AuditLogStore')

        if m.get('AuditProject') is not None:
            self.audit_project = m.get('AuditProject')

        if m.get('AuditRegionId') is not None:
            self.audit_region_id = m.get('AuditRegionId')

        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')

        if m.get('ClusterName') is not None:
            self.cluster_name = m.get('ClusterName')

        if m.get('CpuArch') is not None:
            self.cpu_arch = m.get('CpuArch')

        if m.get('DeploymentProfileCodes') is not None:
            self.deployment_profile_codes = m.get('DeploymentProfileCodes')

        if m.get('ExpireDate') is not None:
            self.expire_date = m.get('ExpireDate')

        if m.get('GroupId') is not None:
            self.group_id = m.get('GroupId')

        if m.get('InstallPolicyVersion') is not None:
            self.install_policy_version = m.get('InstallPolicyVersion')

        if m.get('Vendor') is not None:
            self.vendor = m.get('Vendor')

        return self

