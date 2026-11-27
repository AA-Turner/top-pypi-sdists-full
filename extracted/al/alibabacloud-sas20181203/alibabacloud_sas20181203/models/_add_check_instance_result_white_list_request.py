# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class AddCheckInstanceResultWhiteListRequest(DaraModel):
    def __init__(
        self,
        check_group_id: str = None,
        check_id: int = None,
        client_token: str = None,
        dry_run: bool = None,
        effect_end_time: int = None,
        effect_start_time: int = None,
        effect_type: str = None,
        instance_ids: List[str] = None,
        instance_list: List[main_models.AddCheckInstanceResultWhiteListRequestInstanceList] = None,
        remark: str = None,
        rule_type: str = None,
    ):
        # The ID of the check group to which the check item belongs.
        self.check_group_id = check_group_id
        # The ID of the check item.
        # > Call the [ListCheckResult](~~ListCheckResult~~) operation to obtain this parameter.
        self.check_id = check_id
        # The client token that is used to ensure the idempotence of the request. You can use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to only precheck the request. A value of true indicates that only the request is checked and no actual operations are performed. A value of false indicates that the request is normally executed. Default value: false.
        self.dry_run = dry_run
        # The end time when the whitelist rule expires. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM. The whitelist rule automatically expires after this time.
        self.effect_end_time = effect_end_time
        # The start time when the whitelist rule takes effect. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM, and the value must be less than or equal to the value of EffectEndTime.
        self.effect_start_time = effect_start_time
        # The pattern of the whitelist rule. Valid values:
        # - PERMANENT: Permanently effective. This is the default value.
        # - CUSTOM: Custom effective period.
        # If you set this parameter to CUSTOM, you must specify both EffectStartTime and EffectEndTime.
        self.effect_type = effect_type
        # The instance IDs of the assets.
        self.instance_ids = instance_ids
        # The information about the asset instances.
        self.instance_list = instance_list
        # The remarks. The maximum size is 65,535 bytes.
        self.remark = remark
        # The type of the rule. Default value: **WHITE**. Valid values:
        # - WHITE: Adds the instances to the whitelist.
        self.rule_type = rule_type

    def validate(self):
        if self.instance_list:
            for v1 in self.instance_list:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_group_id is not None:
            result['CheckGroupId'] = self.check_group_id

        if self.check_id is not None:
            result['CheckId'] = self.check_id

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.effect_end_time is not None:
            result['EffectEndTime'] = self.effect_end_time

        if self.effect_start_time is not None:
            result['EffectStartTime'] = self.effect_start_time

        if self.effect_type is not None:
            result['EffectType'] = self.effect_type

        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids

        result['InstanceList'] = []
        if self.instance_list is not None:
            for k1 in self.instance_list:
                result['InstanceList'].append(k1.to_map() if k1 else None)

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckGroupId') is not None:
            self.check_group_id = m.get('CheckGroupId')

        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('EffectEndTime') is not None:
            self.effect_end_time = m.get('EffectEndTime')

        if m.get('EffectStartTime') is not None:
            self.effect_start_time = m.get('EffectStartTime')

        if m.get('EffectType') is not None:
            self.effect_type = m.get('EffectType')

        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')

        self.instance_list = []
        if m.get('InstanceList') is not None:
            for k1 in m.get('InstanceList'):
                temp_model = main_models.AddCheckInstanceResultWhiteListRequestInstanceList()
                self.instance_list.append(temp_model.from_map(k1))

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        return self

class AddCheckInstanceResultWhiteListRequestInstanceList(DaraModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
    ):
        # The instance ID of the asset.
        # > Invoke the [ListCheckInstanceResult](~~ListCheckInstanceResult~~) operation to obtain this parameter.
        self.instance_id = instance_id
        # The region where the asset resides.
        # > Call the [ListCheckInstanceResult](~~ListCheckInstanceResult~~) operation to obtain this parameter.
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        return self

