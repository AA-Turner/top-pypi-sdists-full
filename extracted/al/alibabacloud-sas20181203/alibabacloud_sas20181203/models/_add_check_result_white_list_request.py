# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class AddCheckResultWhiteListRequest(DaraModel):
    def __init__(
        self,
        check_ids: List[int] = None,
        client_token: str = None,
        dry_run: bool = None,
        effect_end_time: int = None,
        effect_start_time: int = None,
        effect_type: str = None,
        instance_ids: List[str] = None,
        remark: str = None,
        rule_type: str = None,
    ):
        # The IDs of the check items.
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the value of this parameter.
        self.check_ids = check_ids
        # The client token that is used to ensure the idempotence of the request. You can use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to only precheck the request. A value of true indicates that only the request is prechecked and no actual operations are performed. A value of false indicates that the request is normally executed. Default value: false.
        self.dry_run = dry_run
        # The effective end time of the whitelist rule. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM. The whitelist automatically expires after the specified end time.
        self.effect_end_time = effect_end_time
        # The effective start time of the whitelist rule. The value is a UNIX timestamp in milliseconds. This parameter is required when EffectType is set to CUSTOM, and the value must be less than or equal to the value of EffectEndTime.
        self.effect_start_time = effect_start_time
        # The effective pattern of the whitelist rule. Valid values: PERMANENT (permanently effective, default value) and CUSTOM (custom effective period). If you set this parameter to CUSTOM, you must specify both EffectStartTime and EffectEndTime.
        self.effect_type = effect_type
        # The instance IDs of the cloud services to be added to the whitelist. Separate multiple instance IDs with commas (,).
        self.instance_ids = instance_ids
        # The remark. The maximum length is 65,535 bytes.
        self.remark = remark
        # The rule type. Default value: **WHITE**. Valid values:
        # - **WHITE**: Adds the check items to the whitelist.
        self.rule_type = rule_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_ids is not None:
            result['CheckIds'] = self.check_ids

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

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckIds') is not None:
            self.check_ids = m.get('CheckIds')

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

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        return self

