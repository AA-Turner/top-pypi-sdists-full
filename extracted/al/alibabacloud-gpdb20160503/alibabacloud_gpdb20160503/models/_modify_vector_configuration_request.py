# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyVectorConfigurationRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        owner_id: int = None,
        vector_configuration_status: str = None,
    ):
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the IDs of all AnalyticDB for PostgreSQL instances in a specific region.
        self.dbinstance_id = dbinstance_id
        self.owner_id = owner_id
        # Specifies whether to enable the vector engine optimization configuration. Valid values:
        # 
        # - **enabled**: Enables vector engine optimization.
        # - **disabled**: Disables vector engine optimization.
        # 
        # > - For mainstream analytics, data warehouse, and real-time data warehouse scenarios, **do not enable** vector engine optimization.
        # - For users who use the vector analysis engine for AIGC and vector retrieval scenarios, **enable** vector engine optimization.
        self.vector_configuration_status = vector_configuration_status

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

        if self.vector_configuration_status is not None:
            result['VectorConfigurationStatus'] = self.vector_configuration_status

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('VectorConfigurationStatus') is not None:
            self.vector_configuration_status = m.get('VectorConfigurationStatus')

        return self

