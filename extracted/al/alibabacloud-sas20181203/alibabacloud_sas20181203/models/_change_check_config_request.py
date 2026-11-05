# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class ChangeCheckConfigRequest(DaraModel):
    def __init__(
        self,
        added_check: List[main_models.ChangeCheckConfigRequestAddedCheck] = None,
        client_token: str = None,
        config_id: str = None,
        config_requirement_ids: main_models.ChangeCheckConfigRequestConfigRequirementIds = None,
        config_standard_ids: main_models.ChangeCheckConfigRequestConfigStandardIds = None,
        configure: str = None,
        cycle_days: List[int] = None,
        days_of_month: List[int] = None,
        dry_run: bool = None,
        enable_add_check: bool = None,
        enable_auto_check: bool = None,
        end_time: int = None,
        end_time_seconds: int = None,
        frequency: str = None,
        region_id: str = None,
        removed_check: List[main_models.ChangeCheckConfigRequestRemovedCheck] = None,
        resource_directory_account_id: int = None,
        standard_ids: List[int] = None,
        start_time: int = None,
        start_time_seconds: int = None,
        strategy_name: str = None,
        system_config: bool = None,
        vendors: List[str] = None,
    ):
        # The list of check items to be added to the policy.
        # <notice> If the ConfigStandardIds or ConfigRequirementIds parameter is configured, this parameter does not take effect. </notice>
        self.added_check = added_check
        # The client token that is used to ensure the idempotence of the request. Different requests must use different tokens. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # The policy ID.
        self.config_id = config_id
        # Configures the check policy by using the IDs of the specified regulations.
        # 
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the regulation IDs. If the ConfigStandardIds parameter is configured, this parameter does not take effect.
        self.config_requirement_ids = config_requirement_ids
        # Configures the check policy by using the IDs of the specified standards.
        # 
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the standard IDs.
        self.config_standard_ids = config_standard_ids
        # The field configuration. Valid values:
        # 
        # - **all**: Adds all check items.
        self.configure = configure
        # The periodic check time.
        self.cycle_days = cycle_days
        # The list of days of the month when the policy cycle is monthly.
        self.days_of_month = days_of_month
        # Specifies whether to only precheck the request. Valid values:
        # 
        # - true: Only checks the request without performing the actual operation.
        # - false: Executes the request normally.
        # 
        # Default value: false.
        self.dry_run = dry_run
        # Specifies whether to check new check items by default when new check items are added to the selected regulations. Valid values:
        # 
        # - **true**: Enabled.
        # - **false**: Disabled.
        self.enable_add_check = enable_add_check
        # Specifies whether to enable automatic periodic checks. Valid values:
        # 
        # - **true**: Enabled.
        # - **false**: Disabled.
        self.enable_auto_check = enable_auto_check
        # The end time of the check time period, which indicates the hour of the day. The start time and end time must be selected from the following time intervals. Valid values: 6, 12, 18, and 24.
        # 
        # - **0~6**: If the start time is 0, the end time must be set to 6 on the same day.
        # - **6~12**: If the start time is 6, the end time must be set to 12 on the same day.
        # - **12~18**: If the start time is 12, the end time must be set to 18 on the same day.
        # - **18~24**: If the start time is 18, the end time must be set to 24 on the same day.
        self.end_time = end_time
        # The end time of the check, in seconds from 00:00:00 of the current day. Valid values: 1 to 86400, where 86400 indicates 00:00:00 of the next day. This parameter is optional. If this parameter is not provided, the current value of the policy is retained. This parameter must be paired with StartTimeSeconds. If only one of them is provided, the system returns IllegalParam (paramName=scheduleTime). If both this parameter and StartTime/EndTime are provided, the second-level parameters take precedence, and the hour-level parameters are ignored. The time window span must not be less than 60 seconds. This parameter is not accepted for the system default policy (ConfigId=default) and will be rejected if provided.
        self.end_time_seconds = end_time_seconds
        # The frequency type. Valid values:
        # 
        # - DAILY: Daily.
        # - WEEKLY: Weekly.
        # - MONTHLY: Monthly.
        # - 6HOURLY: Every 6 hours.
        self.frequency = frequency
        # The region of the Security Center instance. Valid values:
        # 
        # - **cn-hangzhou**: Center
        # - **ap-southeast-1**: Singapore
        self.region_id = region_id
        # The list of check items to be removed from the policy.
        # <notice> If the ConfigStandardIds or ConfigRequirementIds parameter is configured, this parameter does not take effect. </notice>
        self.removed_check = removed_check
        # The ID of the member accounts in the resource folder, which is an Alibaba Cloud account ID.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # This parameter is deprecated and can be ignored.
        self.standard_ids = standard_ids
        # The start time of the check time period, which indicates the hour of the day. The start time and end time must be selected from the following time intervals. Valid values: 0, 6, 12, and 18.
        # 
        # - **0~6**: If the start time is 0, the end time must be set to 6 on the same day.
        # - **6~12**: If the start time is 6, the end time must be set to 12 on the same day.
        # - **12~18**: If the start time is 12, the end time must be set to 18 on the same day.
        # - **18~24**: If the start time is 18, the end time must be set to 24 on the same day.
        self.start_time = start_time
        # The start time of the check, in seconds from 00:00:00 of the current day. Valid values: 0 to 86399, which correspond to 00:00:00 to 23:59:59. This parameter is optional. If this parameter is not provided, the current value of the policy is retained. This parameter must be paired with EndTimeSeconds. If only one of them is provided, the system returns IllegalParam (paramName=scheduleTime). If both this parameter and StartTime/EndTime are provided, the second-level parameters take precedence, and the hour-level parameters are ignored. If the two sets of parameters are inconsistent, the server records a WARN log. The time window span must not be less than 60 seconds. The frequency of the system default policy (ConfigId=default) is always 6HOURLY. This parameter is not accepted for the default policy and will be rejected if provided. Under a multi-policy frequency, the actual scan execution time is exactly the second specified by this parameter.
        self.start_time_seconds = start_time_seconds
        # The policy name.
        self.strategy_name = strategy_name
        # Specifies whether to use the automatically generated system configuration. Valid values:
        # 
        # - **true**: Yes.
        # - **false**: No.
        self.system_config = system_config
        # The list of cloud providers.
        self.vendors = vendors

    def validate(self):
        if self.added_check:
            for v1 in self.added_check:
                 if v1:
                    v1.validate()
        if self.config_requirement_ids:
            self.config_requirement_ids.validate()
        if self.config_standard_ids:
            self.config_standard_ids.validate()
        if self.removed_check:
            for v1 in self.removed_check:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        result['AddedCheck'] = []
        if self.added_check is not None:
            for k1 in self.added_check:
                result['AddedCheck'].append(k1.to_map() if k1 else None)

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.config_id is not None:
            result['ConfigId'] = self.config_id

        if self.config_requirement_ids is not None:
            result['ConfigRequirementIds'] = self.config_requirement_ids.to_map()

        if self.config_standard_ids is not None:
            result['ConfigStandardIds'] = self.config_standard_ids.to_map()

        if self.configure is not None:
            result['Configure'] = self.configure

        if self.cycle_days is not None:
            result['CycleDays'] = self.cycle_days

        if self.days_of_month is not None:
            result['DaysOfMonth'] = self.days_of_month

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.enable_add_check is not None:
            result['EnableAddCheck'] = self.enable_add_check

        if self.enable_auto_check is not None:
            result['EnableAutoCheck'] = self.enable_auto_check

        if self.end_time is not None:
            result['EndTime'] = self.end_time

        if self.end_time_seconds is not None:
            result['EndTimeSeconds'] = self.end_time_seconds

        if self.frequency is not None:
            result['Frequency'] = self.frequency

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        result['RemovedCheck'] = []
        if self.removed_check is not None:
            for k1 in self.removed_check:
                result['RemovedCheck'].append(k1.to_map() if k1 else None)

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.standard_ids is not None:
            result['StandardIds'] = self.standard_ids

        if self.start_time is not None:
            result['StartTime'] = self.start_time

        if self.start_time_seconds is not None:
            result['StartTimeSeconds'] = self.start_time_seconds

        if self.strategy_name is not None:
            result['StrategyName'] = self.strategy_name

        if self.system_config is not None:
            result['SystemConfig'] = self.system_config

        if self.vendors is not None:
            result['Vendors'] = self.vendors

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.added_check = []
        if m.get('AddedCheck') is not None:
            for k1 in m.get('AddedCheck'):
                temp_model = main_models.ChangeCheckConfigRequestAddedCheck()
                self.added_check.append(temp_model.from_map(k1))

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('ConfigId') is not None:
            self.config_id = m.get('ConfigId')

        if m.get('ConfigRequirementIds') is not None:
            temp_model = main_models.ChangeCheckConfigRequestConfigRequirementIds()
            self.config_requirement_ids = temp_model.from_map(m.get('ConfigRequirementIds'))

        if m.get('ConfigStandardIds') is not None:
            temp_model = main_models.ChangeCheckConfigRequestConfigStandardIds()
            self.config_standard_ids = temp_model.from_map(m.get('ConfigStandardIds'))

        if m.get('Configure') is not None:
            self.configure = m.get('Configure')

        if m.get('CycleDays') is not None:
            self.cycle_days = m.get('CycleDays')

        if m.get('DaysOfMonth') is not None:
            self.days_of_month = m.get('DaysOfMonth')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('EnableAddCheck') is not None:
            self.enable_add_check = m.get('EnableAddCheck')

        if m.get('EnableAutoCheck') is not None:
            self.enable_auto_check = m.get('EnableAutoCheck')

        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')

        if m.get('EndTimeSeconds') is not None:
            self.end_time_seconds = m.get('EndTimeSeconds')

        if m.get('Frequency') is not None:
            self.frequency = m.get('Frequency')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        self.removed_check = []
        if m.get('RemovedCheck') is not None:
            for k1 in m.get('RemovedCheck'):
                temp_model = main_models.ChangeCheckConfigRequestRemovedCheck()
                self.removed_check.append(temp_model.from_map(k1))

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('StandardIds') is not None:
            self.standard_ids = m.get('StandardIds')

        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')

        if m.get('StartTimeSeconds') is not None:
            self.start_time_seconds = m.get('StartTimeSeconds')

        if m.get('StrategyName') is not None:
            self.strategy_name = m.get('StrategyName')

        if m.get('SystemConfig') is not None:
            self.system_config = m.get('SystemConfig')

        if m.get('Vendors') is not None:
            self.vendors = m.get('Vendors')

        return self

class ChangeCheckConfigRequestRemovedCheck(DaraModel):
    def __init__(
        self,
        check_id: int = None,
        section_id: int = None,
    ):
        # The ID of the check item.
        # 
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the check item ID.
        self.check_id = check_id
        # The section ID of the check item.
        self.section_id = section_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_id is not None:
            result['CheckId'] = self.check_id

        if self.section_id is not None:
            result['SectionId'] = self.section_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        if m.get('SectionId') is not None:
            self.section_id = m.get('SectionId')

        return self

class ChangeCheckConfigRequestConfigStandardIds(DaraModel):
    def __init__(
        self,
        add_ids: List[int] = None,
        remove_ids: List[int] = None,
    ):
        # The list of standard IDs to be added to the policy.
        self.add_ids = add_ids
        # The list of standard IDs to be removed from the policy.
        self.remove_ids = remove_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.add_ids is not None:
            result['AddIds'] = self.add_ids

        if self.remove_ids is not None:
            result['RemoveIds'] = self.remove_ids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AddIds') is not None:
            self.add_ids = m.get('AddIds')

        if m.get('RemoveIds') is not None:
            self.remove_ids = m.get('RemoveIds')

        return self

class ChangeCheckConfigRequestConfigRequirementIds(DaraModel):
    def __init__(
        self,
        add_ids: List[int] = None,
        remove_ids: List[int] = None,
    ):
        # The list of regulation IDs to be added to the policy.
        self.add_ids = add_ids
        # The list of regulation IDs to be removed from the policy.
        self.remove_ids = remove_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.add_ids is not None:
            result['AddIds'] = self.add_ids

        if self.remove_ids is not None:
            result['RemoveIds'] = self.remove_ids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AddIds') is not None:
            self.add_ids = m.get('AddIds')

        if m.get('RemoveIds') is not None:
            self.remove_ids = m.get('RemoveIds')

        return self

class ChangeCheckConfigRequestAddedCheck(DaraModel):
    def __init__(
        self,
        check_id: int = None,
        section_id: int = None,
    ):
        # The ID of the check item.
        # 
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the check item ID.
        self.check_id = check_id
        # The section ID of the check item.
        self.section_id = section_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_id is not None:
            result['CheckId'] = self.check_id

        if self.section_id is not None:
            result['SectionId'] = self.section_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        if m.get('SectionId') is not None:
            self.section_id = m.get('SectionId')

        return self

