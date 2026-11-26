# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class HandleActiveSQLRecordRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        operate_type: int = None,
        pids: str = None,
    ):
        # The instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The operation type for the process ID. Valid values:
        # - **0**: cancel
        # - **1**: terminate
        # - **2**: force terminate
        self.operate_type = operate_type
        # The process IDs, which are the unique identifiers of the queries.
        # 
        # This parameter is required.
        self.pids = pids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.operate_type is not None:
            result['OperateType'] = self.operate_type

        if self.pids is not None:
            result['Pids'] = self.pids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('OperateType') is not None:
            self.operate_type = m.get('OperateType')

        if m.get('Pids') is not None:
            self.pids = m.get('Pids')

        return self

