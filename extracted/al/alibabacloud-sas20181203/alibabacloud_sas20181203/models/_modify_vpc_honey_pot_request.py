# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyVpcHoneyPotRequest(DaraModel):
    def __init__(
        self,
        honey_pot_action: str = None,
        vpc_id: str = None,
    ):
        # Specifies the action to perform on the cloud honeypot instance. Valid values:
        # 
        # - **disable**: Suspends the instance.
        # - **enable**: Starts the instance.
        # 
        # This parameter is required.
        self.honey_pot_action = honey_pot_action
        # The VPC ID of the cloud honeypot instance to take effect.
        # 
        # > You can call the [DescribeVpcHoneyPotList](~~DescribeVpcHoneyPotList~~) operation to obtain the VPC ID.
        # 
        # This parameter is required.
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.honey_pot_action is not None:
            result['HoneyPotAction'] = self.honey_pot_action

        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HoneyPotAction') is not None:
            self.honey_pot_action = m.get('HoneyPotAction')

        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')

        return self

