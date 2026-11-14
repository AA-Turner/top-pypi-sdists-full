# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class SwitchToPrimaryInstanceRequest(DaraModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        effective_time: str = None,
        force_switch: bool = None,
    ):
        # The instance ID.
        self.dbinstance_id = dbinstance_id
        # The effective period. Valid values:
        # * **Immediate**: Executes immediately.
        # * **MaintainTime**: Executes within the maintenance window.
        # 
        # Default value: **Immediate**.
        self.effective_time = effective_time
        # The switchover mode. Valid values:
        # 
        # **true**: Forced switchover.
        # 
        # **false**: Normal switchover.
        self.force_switch = force_switch

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.effective_time is not None:
            result['EffectiveTime'] = self.effective_time

        if self.force_switch is not None:
            result['ForceSwitch'] = self.force_switch

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('EffectiveTime') is not None:
            self.effective_time = m.get('EffectiveTime')

        if m.get('ForceSwitch') is not None:
            self.force_switch = m.get('ForceSwitch')

        return self

