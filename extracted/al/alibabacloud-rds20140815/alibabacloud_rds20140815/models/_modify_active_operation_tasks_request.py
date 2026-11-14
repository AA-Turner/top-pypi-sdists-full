# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyActiveOperationTasksRequest(DaraModel):
    def __init__(
        self,
        ids: str = None,
        immediate_start: int = None,
        owner_account: str = None,
        owner_id: int = None,
        resource_owner_account: str = None,
        resource_owner_id: int = None,
        security_token: str = None,
        switch_time: str = None,
    ):
        # The IDs of the O&M tasks. Separate multiple IDs with commas (,).
        # > You can call the DescribeActiveOperationTasks operation to obtain the O&M task IDs.
        # 
        # This parameter is required.
        self.ids = ids
        # Specifies whether to immediately schedule the tasks for execution. Valid values:
        # - 0: no. This is the default value.
        # - 1: yes.
        # > - If you set this parameter to 0, the SwitchTime parameter takes effect. If you set this parameter to 1, the SwitchTime parameter does not take effect. The start time of the tasks is set to the current time, and the switchover time is automatically calculated based on the new start time.
        # > - Immediately scheduling the tasks for execution does not mean an immediate switchover. Instead, the tasks immediately enter the Preparing state. After the preparation is complete, the switchover is performed. You can call the DescribeActiveOperationTasks operation and check the value of the PrepareInterval response parameter to obtain the preparation time.
        self.immediate_start = immediate_start
        self.owner_account = owner_account
        self.owner_id = owner_id
        self.resource_owner_account = resource_owner_account
        self.resource_owner_id = resource_owner_id
        self.security_token = security_token
        # The scheduled switchover time to set. Specify the time in the ISO 8601 standard in the yyyy-MM-ddTHH:mm:ssZ format. The time must be in UTC.
        # 
        # > The time cannot be later than the deadline. You can call the DescribeActiveOperationTasks operation and check the value of the Deadline response parameter to obtain the deadline.
        # 
        # This parameter is required.
        self.switch_time = switch_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.ids is not None:
            result['Ids'] = self.ids

        if self.immediate_start is not None:
            result['ImmediateStart'] = self.immediate_start

        if self.owner_account is not None:
            result['OwnerAccount'] = self.owner_account

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.resource_owner_account is not None:
            result['ResourceOwnerAccount'] = self.resource_owner_account

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.security_token is not None:
            result['SecurityToken'] = self.security_token

        if self.switch_time is not None:
            result['SwitchTime'] = self.switch_time

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ids') is not None:
            self.ids = m.get('Ids')

        if m.get('ImmediateStart') is not None:
            self.immediate_start = m.get('ImmediateStart')

        if m.get('OwnerAccount') is not None:
            self.owner_account = m.get('OwnerAccount')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('ResourceOwnerAccount') is not None:
            self.resource_owner_account = m.get('ResourceOwnerAccount')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SecurityToken') is not None:
            self.security_token = m.get('SecurityToken')

        if m.get('SwitchTime') is not None:
            self.switch_time = m.get('SwitchTime')

        return self

