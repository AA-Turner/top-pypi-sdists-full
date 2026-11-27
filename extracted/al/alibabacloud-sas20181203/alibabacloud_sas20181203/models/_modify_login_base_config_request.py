# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyLoginBaseConfigRequest(DaraModel):
    def __init__(
        self,
        config: str = None,
        target: str = None,
        type: str = None,
    ):
        # The detailed configuration of the unusual logon detection rule for servers. This parameter is in JSON format and includes the following fields:
        # 
        # - **totalCount**: The total number of assets.
        # - **uuidCount**: The number of assets to which the rule applies.
        # - **id**: The ID of the unusual logon rule for servers.
        # - **location**: The name of the common logon location.
        # 
        # > You must set this parameter only when the Type parameter is set to login_common_location.
        # 
        # - **ip**: The common logon IP address.
        # 
        # > You must set this parameter only when the Type parameter is set to login_common_ip.
        # 
        # - **endTime**: The end time of the common logon period.
        # 
        # > You must set this parameter only when the Type parameter is set to login_common_time.
        # 
        # - **startTime**: The start time of the common logon period.
        # 
        # > You must set this parameter only when the Type parameter is set to login_common_time.
        # 
        # - **account**: The common logon account.
        # 
        # > You must set this parameter only when the Type parameter is set to login_common_account.
        # 
        # This parameter is required.
        self.config = config
        # The configuration of the servers to which the unusual logon detection rule applies. This parameter is in JSON format and includes the following fields:
        # 
        # - **Target**: The UUID of the server to add or remove.
        # - **targetType**: The mode in which assets are added. Valid values:
        #     - **uuid**: Add by individual server.
        #     - **groupId**: Add by server group.
        # - **flag**: The specific operation on the asset. Valid values:
        #     - **del**: Remove the server from the rule.
        #     - **add**: Add the server to the rule.
        # 
        # This parameter is required.
        self.target = target
        # The type of unusual logon detection for servers to modify. Valid values:
        # 
        # - **login_common_location**: Common logon location.
        # - **login_common_ip**: Common logon IP address.
        # - **login_common_time**: Common logon time.
        # - **login_common_account**: Common logon account.
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.config is not None:
            result['Config'] = self.config

        if self.target is not None:
            result['Target'] = self.target

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Config') is not None:
            self.config = m.get('Config')

        if m.get('Target') is not None:
            self.target = m.get('Target')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

