# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class ModifyCheckRuleRequest(DaraModel):
    def __init__(
        self,
        add_instance_list: List[main_models.ModifyCheckRuleRequestAddInstanceList] = None,
        delete_instance_list: List[main_models.ModifyCheckRuleRequestDeleteInstanceList] = None,
        effect_end_time: int = None,
        effect_start_time: int = None,
        effect_type: str = None,
        remark: str = None,
        rule_id: int = None,
        rule_type: str = None,
        scope_type: str = None,
    ):
        # The list of instances to be added in this rule update. If no instances need to be added, you do not need to specify this parameter.
        self.add_instance_list = add_instance_list
        # The list of instances to be removed in this rule update. If no instances need to be removed, you do not need to specify this parameter.
        self.delete_instance_list = delete_instance_list
        # The effective end time of the whitelist rule. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM. The whitelist automatically expires after this time.
        self.effect_end_time = effect_end_time
        # The effective start time of the whitelist rule. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM, and the value must be less than or equal to the value of EffectEndTime.
        self.effect_start_time = effect_start_time
        # The effective pattern of the whitelist rule. Valid values: PERMANENT (permanent, default value) and CUSTOM (custom effective period). If the value is CUSTOM, you must specify both EffectStartTime and EffectEndTime. After the modification, the server immediately recalculates the whitelist status based on the new effective period.
        self.effect_type = effect_type
        # The remark.
        self.remark = remark
        # The rule ID. You can call the [ListCheckRule](https://help.aliyun.com/document_detail/2590599.html) operation to obtain this parameter.
        # 
        # This parameter is required.
        self.rule_id = rule_id
        # The rule type. Default value: **WHITE**. Valid values:
        # - **WHITE**: whitelist.
        self.rule_type = rule_type
        # The effective scope of the modified rule. Valid values:
        # - **INSTNACE**: instance.
        # - **ITEM**: check item.
        self.scope_type = scope_type

    def validate(self):
        if self.add_instance_list:
            for v1 in self.add_instance_list:
                 if v1:
                    v1.validate()
        if self.delete_instance_list:
            for v1 in self.delete_instance_list:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        result['AddInstanceList'] = []
        if self.add_instance_list is not None:
            for k1 in self.add_instance_list:
                result['AddInstanceList'].append(k1.to_map() if k1 else None)

        result['DeleteInstanceList'] = []
        if self.delete_instance_list is not None:
            for k1 in self.delete_instance_list:
                result['DeleteInstanceList'].append(k1.to_map() if k1 else None)

        if self.effect_end_time is not None:
            result['EffectEndTime'] = self.effect_end_time

        if self.effect_start_time is not None:
            result['EffectStartTime'] = self.effect_start_time

        if self.effect_type is not None:
            result['EffectType'] = self.effect_type

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.rule_id is not None:
            result['RuleId'] = self.rule_id

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        if self.scope_type is not None:
            result['ScopeType'] = self.scope_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.add_instance_list = []
        if m.get('AddInstanceList') is not None:
            for k1 in m.get('AddInstanceList'):
                temp_model = main_models.ModifyCheckRuleRequestAddInstanceList()
                self.add_instance_list.append(temp_model.from_map(k1))

        self.delete_instance_list = []
        if m.get('DeleteInstanceList') is not None:
            for k1 in m.get('DeleteInstanceList'):
                temp_model = main_models.ModifyCheckRuleRequestDeleteInstanceList()
                self.delete_instance_list.append(temp_model.from_map(k1))

        if m.get('EffectEndTime') is not None:
            self.effect_end_time = m.get('EffectEndTime')

        if m.get('EffectStartTime') is not None:
            self.effect_start_time = m.get('EffectStartTime')

        if m.get('EffectType') is not None:
            self.effect_type = m.get('EffectType')

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        if m.get('ScopeType') is not None:
            self.scope_type = m.get('ScopeType')

        return self

class ModifyCheckRuleRequestDeleteInstanceList(DaraModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
    ):
        # The instance ID of the asset.
        self.instance_id = instance_id
        # The region ID of the asset.
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

class ModifyCheckRuleRequestAddInstanceList(DaraModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
    ):
        # The instance ID of the asset.
        self.instance_id = instance_id
        # The region ID of the asset.
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

