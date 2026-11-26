# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateDBResourceGroupRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        owner_id: int = None,
        resource_group_config: str = None,
        resource_group_name: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the details of all AnalyticDB for PostgreSQL instances in a region, including instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        self.owner_id = owner_id
        # The resource group configuration.
        # > 1. CpuRateLimit: the percentage of CPU resources available to the resource group. Unit: %.
        # > 2. MemoryLimit: the percentage of memory resources available to the resource group. Unit: %.
        # > 3. MemorySharedQuota: the percentage of memory resources shared among transactions submitted to the resource group. Unit: %. Default value: 80.
        # > 4. MemorySpillRatio: the memory usage threshold for memory-intensive transactions. When a transaction reaches this threshold, it spills to disk. Unit: %. Default value: 0.
        # > 5. Concurrency: the maximum number of concurrent transactions allowed for the resource group. Default value: 20.
        # 
        # This parameter is required.
        self.resource_group_config = resource_group_config
        # The name of the resource group.
        # 
        # This parameter is required.
        self.resource_group_name = resource_group_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.resource_group_config is not None:
            result['ResourceGroupConfig'] = self.resource_group_config

        if self.resource_group_name is not None:
            result['ResourceGroupName'] = self.resource_group_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('ResourceGroupConfig') is not None:
            self.resource_group_config = m.get('ResourceGroupConfig')

        if m.get('ResourceGroupName') is not None:
            self.resource_group_name = m.get('ResourceGroupName')

        return self

