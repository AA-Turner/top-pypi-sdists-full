# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyParameterRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        dbinstance_id: str = None,
        forcerestart: bool = None,
        owner_account: str = None,
        owner_id: int = None,
        parameter_group_id: str = None,
        parameters: str = None,
        resource_owner_account: str = None,
        resource_owner_id: int = None,
        switch_time: str = None,
        switch_time_mode: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request and prevent duplicate submissions. You can use the client to generate the value, and you must ensure that the value is unique across different requests. The value can contain a maximum of 64 ASCII characters and cannot contain non-ASCII characters.
        self.client_token = client_token
        # The instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # Specifies whether to restart the database after the parameters are modified. Valid values:
        # * **true**: forces a restart. If any of the modified parameters require a restart, you must set this parameter to true. Otherwise, the modifications do not take effect.
        # * **false**: does not force a restart.
        # 
        # Default value: **false**.
        self.forcerestart = forcerestart
        self.owner_account = owner_account
        self.owner_id = owner_id
        # The ID of the parameter template.
        # 
        # > * If you specify this parameter, you do not need to specify the **Parameters** parameter.
        # > * If the instance must be restarted to apply the parameter template, you must specify the **Forcerestart** parameter.
        self.parameter_group_id = parameter_group_id
        # The JSON string of parameters and their values. All parameter values are of the string type. Format: {"ParameterName1":"ParameterValue1","ParameterName2":"ParameterValue2"...}. You can call the DescribeParameterTemplates operation to query parameter names and values.
        # >If you specify this parameter, you do not need to specify the **ParameterGroupId** parameter.
        self.parameters = parameters
        self.resource_owner_account = resource_owner_account
        self.resource_owner_id = resource_owner_id
        # The time when the parameter modifications take effect. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm:ss</i>Z format. The time must be in UTC.
        # >The specified time must be later than the current time.
        self.switch_time = switch_time
        # The time when the parameter modifications take effect. Valid values:
        # * **Immediate**: takes effect immediately. This is the default value.
        # * **MaintainTime**: takes effect within the maintenance window of the instance. You can call the ModifyDBInstanceMaintainTime operation to modify the maintenance window.
        # * **ScheduleTime**: takes effect at a specified time. If you set this parameter to ScheduleTime, you must also specify the **SwitchTime** parameter.
        self.switch_time_mode = switch_time_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.forcerestart is not None:
            result['Forcerestart'] = self.forcerestart

        if self.owner_account is not None:
            result['OwnerAccount'] = self.owner_account

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.parameter_group_id is not None:
            result['ParameterGroupId'] = self.parameter_group_id

        if self.parameters is not None:
            result['Parameters'] = self.parameters

        if self.resource_owner_account is not None:
            result['ResourceOwnerAccount'] = self.resource_owner_account

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.switch_time is not None:
            result['SwitchTime'] = self.switch_time

        if self.switch_time_mode is not None:
            result['SwitchTimeMode'] = self.switch_time_mode

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('Forcerestart') is not None:
            self.forcerestart = m.get('Forcerestart')

        if m.get('OwnerAccount') is not None:
            self.owner_account = m.get('OwnerAccount')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('ParameterGroupId') is not None:
            self.parameter_group_id = m.get('ParameterGroupId')

        if m.get('Parameters') is not None:
            self.parameters = m.get('Parameters')

        if m.get('ResourceOwnerAccount') is not None:
            self.resource_owner_account = m.get('ResourceOwnerAccount')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SwitchTime') is not None:
            self.switch_time = m.get('SwitchTime')

        if m.get('SwitchTimeMode') is not None:
            self.switch_time_mode = m.get('SwitchTimeMode')

        return self

