# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class ListCheckResultRequest(DaraModel):
    def __init__(
        self,
        check_ids: List[int] = None,
        check_key: str = None,
        check_types: List[str] = None,
        current_page: int = None,
        custom_param: bool = None,
        instance_ids: List[str] = None,
        instance_types: List[str] = None,
        lang: str = None,
        last_check_time_end: int = None,
        last_check_time_start: int = None,
        operation_types: List[str] = None,
        page_size: int = None,
        region_id: str = None,
        requirement_ids: List[int] = None,
        resource_directory_account_id: int = None,
        risk_levels: List[str] = None,
        sort_types: List[str] = None,
        standard_ids: List[int] = None,
        statuses: List[str] = None,
        task_sources: List[str] = None,
        types: List[str] = None,
        vendors: List[str] = None,
    ):
        # The list of check item IDs.
        self.check_ids = check_ids
        # The keyword for fuzzy search of check items.
        self.check_key = check_key
        # The source type of the Threat Detection Service check item.
        self.check_types = check_types
        # The page number of the current page returned during paging for a paged query.
        self.current_page = current_page
        # Specifies whether the check item supports custom parameters. Valid values:
        # 
        # - **true**: Supported.
        # - **false**: Not supported.
        self.custom_param = custom_param
        # The instance ID of the cloud services to query. Separate multiple instance IDs with commas (,).
        self.instance_ids = instance_ids
        # The asset types of the cloud services. Valid values:
        # 
        # - **ECS**: cloud server.
        # - **SLB**: load balancing.
        # - **RDS**: RDS database.
        # - **MONGODB**: MongoDB database.
        # - **KVSTORE**: Redis database.
        # - **ACR**: ACR.
        # - **CSK**: CSK.
        # - **VPC**: VPC.
        # - **ACTIONTRAIL**: ActionTrail.
        # - **CDN**: CDN.
        # - **CAS**: Certificate Management Service [formerly SSL Certificates Service].
        # - **RDC**: Apsara Devops.
        # - **RAM**: RAM.
        # - **DDOS**: distributed deny service.
        # - **WAF**: WAF.
        # - **OSS**: access control.
        # - **POLARDB**: PolarDB.
        # - **POSTGRESQL**: PostgreSQL.
        # - **MSE**: MSE.
        # - **NAS**: NAS.
        # - **SDDP**: SDDP.
        # - **EIP**: EIP.
        self.instance_types = instance_types
        # The language of the request and response. Default value: **zh**. Valid values:
        # - **zh**: Chinese.
        # - **en**: English.
        self.lang = lang
        # The end time for the last check filter.
        self.last_check_time_end = last_check_time_end
        # The start time for the last check filter.
        self.last_check_time_start = last_check_time_start
        # Specifies whether remediation is supported. Valid values:
        # - **SUPPORT_REPAIR**: Supported.
        # - **NOT_SUPPORT_REPAIR**: Not supported.
        self.operation_types = operation_types
        # The maximum number of entries to return on each page during paging for a paged query. Maximum value: 100.
        self.page_size = page_size
        # The region ID of the instance. Valid values:
        # 
        # - **cn-hangzhou**: China (Hangzhou).
        # - **ap-southeast-1**: Singapore.
        self.region_id = region_id
        # The list of requirement IDs.
        self.requirement_ids = requirement_ids
        # The ID of the member accounts in the Resource Directory folder (Alibaba Cloud account).
        # >You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The risk levels of the check items. Separate multiple risk levels with commas (,). Valid values:
        # 
        # - **HIGH**: High.
        # - **MEDIUM**: Medium.
        # - **LOW**: Low.
        self.risk_levels = risk_levels
        # The sorting type for check items. Valid values:
        # 
        # - **RISK_LEVEL**: Risk level.
        # - **STATUS**: Check item status.
        self.sort_types = sort_types
        # The list of standard IDs.
        self.standard_ids = standard_ids
        # The list of check item statuses. Separate multiple statuses with commas (,). Valid values:
        # 
        # - **PASS**: Passed.
        # - **NOT_PASS**: Not passed.
        # - **CHECKING**: Checking.
        # - **NOT_CHECK**: Not checked.
        # - **WHITELIST**: Whitelisted.
        # - **FAILED**: Failed.
        self.statuses = statuses
        # The custom category of the custom check items to delete.
        self.task_sources = task_sources
        # The list of check standard types.
        self.types = types
        # The cloud provider. Valid values:
        # - **ALIYUN**: Alibaba Cloud.
        # - **TENCENT**: Other cloud providers.
        # - **AWS**: Other cloud providers.
        # - **MICROSOFT**: Other cloud providers.
        self.vendors = vendors

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_ids is not None:
            result['CheckIds'] = self.check_ids

        if self.check_key is not None:
            result['CheckKey'] = self.check_key

        if self.check_types is not None:
            result['CheckTypes'] = self.check_types

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.custom_param is not None:
            result['CustomParam'] = self.custom_param

        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids

        if self.instance_types is not None:
            result['InstanceTypes'] = self.instance_types

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.last_check_time_end is not None:
            result['LastCheckTimeEnd'] = self.last_check_time_end

        if self.last_check_time_start is not None:
            result['LastCheckTimeStart'] = self.last_check_time_start

        if self.operation_types is not None:
            result['OperationTypes'] = self.operation_types

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.requirement_ids is not None:
            result['RequirementIds'] = self.requirement_ids

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.risk_levels is not None:
            result['RiskLevels'] = self.risk_levels

        if self.sort_types is not None:
            result['SortTypes'] = self.sort_types

        if self.standard_ids is not None:
            result['StandardIds'] = self.standard_ids

        if self.statuses is not None:
            result['Statuses'] = self.statuses

        if self.task_sources is not None:
            result['TaskSources'] = self.task_sources

        if self.types is not None:
            result['Types'] = self.types

        if self.vendors is not None:
            result['Vendors'] = self.vendors

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckIds') is not None:
            self.check_ids = m.get('CheckIds')

        if m.get('CheckKey') is not None:
            self.check_key = m.get('CheckKey')

        if m.get('CheckTypes') is not None:
            self.check_types = m.get('CheckTypes')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('CustomParam') is not None:
            self.custom_param = m.get('CustomParam')

        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')

        if m.get('InstanceTypes') is not None:
            self.instance_types = m.get('InstanceTypes')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('LastCheckTimeEnd') is not None:
            self.last_check_time_end = m.get('LastCheckTimeEnd')

        if m.get('LastCheckTimeStart') is not None:
            self.last_check_time_start = m.get('LastCheckTimeStart')

        if m.get('OperationTypes') is not None:
            self.operation_types = m.get('OperationTypes')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('RequirementIds') is not None:
            self.requirement_ids = m.get('RequirementIds')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('RiskLevels') is not None:
            self.risk_levels = m.get('RiskLevels')

        if m.get('SortTypes') is not None:
            self.sort_types = m.get('SortTypes')

        if m.get('StandardIds') is not None:
            self.standard_ids = m.get('StandardIds')

        if m.get('Statuses') is not None:
            self.statuses = m.get('Statuses')

        if m.get('TaskSources') is not None:
            self.task_sources = m.get('TaskSources')

        if m.get('Types') is not None:
            self.types = m.get('Types')

        if m.get('Vendors') is not None:
            self.vendors = m.get('Vendors')

        return self

