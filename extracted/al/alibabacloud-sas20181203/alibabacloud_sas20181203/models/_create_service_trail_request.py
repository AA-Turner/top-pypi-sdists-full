# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateServiceTrailRequest(DaraModel):
    def __init__(
        self,
        region_id: str = None,
        resource_directory_account_id: int = None,
    ):
        # The ID of the region where the instance to query resides. Valid values:
        # 
        # - **cn-hangzhou** (default): China.
        # - **ap-southeast-1**: Global (excluding China).
        self.region_id = region_id
        # The ID of the member accounts in the resource folder. The ID is an Alibaba Cloud account ID.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to query the value of this parameter.
        self.resource_directory_account_id = resource_directory_account_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        return self

