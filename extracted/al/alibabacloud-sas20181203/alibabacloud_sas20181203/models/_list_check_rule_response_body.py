# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class ListCheckRuleResponseBody(DaraModel):
    def __init__(
        self,
        check_rules: List[main_models.ListCheckRuleResponseBodyCheckRules] = None,
        page_info: main_models.ListCheckRuleResponseBodyPageInfo = None,
        request_id: str = None,
    ):
        # The check rules.
        self.check_rules = check_rules
        # The pagination information.
        self.page_info = page_info
        # The ID of the request.
        self.request_id = request_id

    def validate(self):
        if self.check_rules:
            for v1 in self.check_rules:
                 if v1:
                    v1.validate()
        if self.page_info:
            self.page_info.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        result['CheckRules'] = []
        if self.check_rules is not None:
            for k1 in self.check_rules:
                result['CheckRules'].append(k1.to_map() if k1 else None)

        if self.page_info is not None:
            result['PageInfo'] = self.page_info.to_map()

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.check_rules = []
        if m.get('CheckRules') is not None:
            for k1 in m.get('CheckRules'):
                temp_model = main_models.ListCheckRuleResponseBodyCheckRules()
                self.check_rules.append(temp_model.from_map(k1))

        if m.get('PageInfo') is not None:
            temp_model = main_models.ListCheckRuleResponseBodyPageInfo()
            self.page_info = temp_model.from_map(m.get('PageInfo'))

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        return self

class ListCheckRuleResponseBodyPageInfo(DaraModel):
    def __init__(
        self,
        count: int = None,
        current_page: int = None,
        page_size: int = None,
        total_count: int = None,
    ):
        # The number of entries returned on the current page.
        self.count = count
        # The page number of the current page for a paging query.
        self.current_page = current_page
        # The maximum number of entries returned per page in a paging query.
        self.page_size = page_size
        # The total number of entries.
        self.total_count = total_count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.count is not None:
            result['Count'] = self.count

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.total_count is not None:
            result['TotalCount'] = self.total_count

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')

        return self

class ListCheckRuleResponseBodyCheckRules(DaraModel):
    def __init__(
        self,
        ali_uid: int = None,
        asset_sub_type: int = None,
        asset_type: int = None,
        check_id: int = None,
        check_policies: List[main_models.ListCheckRuleResponseBodyCheckRulesCheckPolicies] = None,
        check_show_name: str = None,
        effect_end_time: int = None,
        effect_start_time: int = None,
        effect_status: str = None,
        effect_type: str = None,
        instance_sub_type: str = None,
        instance_type: str = None,
        remark: str = None,
        rule_id: int = None,
        rule_type: str = None,
        scope_type: str = None,
        vendor: int = None,
        vendor_name: str = None,
    ):
        # The UID of the current user.
        self.ali_uid = ali_uid
        # The subtype of the cloud service.
        # 
        # > For more information, see the AssetSubType parameter in the [GetCloudAssetCriteria](~~GetCloudAssetCriteria~~) operation.
        self.asset_sub_type = asset_sub_type
        # The type of the cloud asset.
        # > For more information, see the AssetType parameter in the [GetCloudAssetCriteria](~~GetCloudAssetCriteria~~) operation.
        self.asset_type = asset_type
        # The ID of the check item.
        self.check_id = check_id
        # The display name of the check item section.
        self.check_policies = check_policies
        # The name of the check item.
        self.check_show_name = check_show_name
        # The effective end time of the whitelist rule. The value is a UNIX timestamp in milliseconds. If EffectType is set to PERMANENT, -1 is returned.
        self.effect_end_time = effect_end_time
        # The effective start time of the whitelist rule. The value is a UNIX timestamp in milliseconds. If EffectType is set to PERMANENT, -1 is returned.
        self.effect_start_time = effect_start_time
        # The effective status of the whitelist rule, which is calculated by the server based on the current time. Valid values: PERMANENT (Permanent), NOT_STARTED (Not started), EFFECTIVE (Effective), and EXPIRED (Expired).
        self.effect_status = effect_status
        # The effective pattern of the whitelist rule. Valid values: PERMANENT (Permanent) and CUSTOM (Custom effective period).
        self.effect_type = effect_type
        # The asset subtype of the cloud service.
        self.instance_sub_type = instance_sub_type
        # The asset type of the cloud service.
        self.instance_type = instance_type
        # The remark.
        self.remark = remark
        # The ID of the rule.
        self.rule_id = rule_id
        # The rule type. Default value: **WHITE**. Valid values:
        # - **WHITE**: Whitelist.
        self.rule_type = rule_type
        # The effective scope of the rule. Valid values:
        # - **INSTNACE**: Instance.
        # - **ITEM**: Check item.
        self.scope_type = scope_type
        # The server vendor. Valid values:
        # 
        # - **0**: Alibaba Cloud asset.
        # - **1**: Non-Alibaba Cloud asset.
        # - **2**: IDC asset.
        # - **3**, **4**, **5**, and **7**: Other cloud assets.
        self.vendor = vendor
        # The name of the server service provider.
        self.vendor_name = vendor_name

    def validate(self):
        if self.check_policies:
            for v1 in self.check_policies:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.ali_uid is not None:
            result['AliUid'] = self.ali_uid

        if self.asset_sub_type is not None:
            result['AssetSubType'] = self.asset_sub_type

        if self.asset_type is not None:
            result['AssetType'] = self.asset_type

        if self.check_id is not None:
            result['CheckId'] = self.check_id

        result['CheckPolicies'] = []
        if self.check_policies is not None:
            for k1 in self.check_policies:
                result['CheckPolicies'].append(k1.to_map() if k1 else None)

        if self.check_show_name is not None:
            result['CheckShowName'] = self.check_show_name

        if self.effect_end_time is not None:
            result['EffectEndTime'] = self.effect_end_time

        if self.effect_start_time is not None:
            result['EffectStartTime'] = self.effect_start_time

        if self.effect_status is not None:
            result['EffectStatus'] = self.effect_status

        if self.effect_type is not None:
            result['EffectType'] = self.effect_type

        if self.instance_sub_type is not None:
            result['InstanceSubType'] = self.instance_sub_type

        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type

        if self.remark is not None:
            result['Remark'] = self.remark

        if self.rule_id is not None:
            result['RuleId'] = self.rule_id

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        if self.scope_type is not None:
            result['ScopeType'] = self.scope_type

        if self.vendor is not None:
            result['Vendor'] = self.vendor

        if self.vendor_name is not None:
            result['VendorName'] = self.vendor_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AliUid') is not None:
            self.ali_uid = m.get('AliUid')

        if m.get('AssetSubType') is not None:
            self.asset_sub_type = m.get('AssetSubType')

        if m.get('AssetType') is not None:
            self.asset_type = m.get('AssetType')

        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        self.check_policies = []
        if m.get('CheckPolicies') is not None:
            for k1 in m.get('CheckPolicies'):
                temp_model = main_models.ListCheckRuleResponseBodyCheckRulesCheckPolicies()
                self.check_policies.append(temp_model.from_map(k1))

        if m.get('CheckShowName') is not None:
            self.check_show_name = m.get('CheckShowName')

        if m.get('EffectEndTime') is not None:
            self.effect_end_time = m.get('EffectEndTime')

        if m.get('EffectStartTime') is not None:
            self.effect_start_time = m.get('EffectStartTime')

        if m.get('EffectStatus') is not None:
            self.effect_status = m.get('EffectStatus')

        if m.get('EffectType') is not None:
            self.effect_type = m.get('EffectType')

        if m.get('InstanceSubType') is not None:
            self.instance_sub_type = m.get('InstanceSubType')

        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')

        if m.get('Remark') is not None:
            self.remark = m.get('Remark')

        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        if m.get('ScopeType') is not None:
            self.scope_type = m.get('ScopeType')

        if m.get('Vendor') is not None:
            self.vendor = m.get('Vendor')

        if m.get('VendorName') is not None:
            self.vendor_name = m.get('VendorName')

        return self

class ListCheckRuleResponseBodyCheckRulesCheckPolicies(DaraModel):
    def __init__(
        self,
        section_show_name: str = None,
    ):
        # The display name of the check item section.
        self.section_show_name = section_show_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.section_show_name is not None:
            result['sectionShowName'] = self.section_show_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('sectionShowName') is not None:
            self.section_show_name = m.get('sectionShowName')

        return self

