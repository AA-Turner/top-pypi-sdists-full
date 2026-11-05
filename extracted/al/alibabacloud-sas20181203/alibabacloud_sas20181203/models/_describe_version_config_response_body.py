# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class DescribeVersionConfigResponseBody(DaraModel):
    def __init__(
        self,
        agentless_capacity: int = None,
        allow_partial_buy: int = None,
        anti_ransomware_capacity: int = None,
        anti_ransomware_service: int = None,
        app_white_list: int = None,
        app_white_list_auth_count: int = None,
        asset_level: int = None,
        buy_sas_edr: str = None,
        can_try_post_paid_package: int = None,
        cspm_capacity: int = None,
        cspm_instance_capacity: int = None,
        highest_version: int = None,
        honeypot_capacity: int = None,
        hybrid_paid_gray_status: main_models.DescribeVersionConfigResponseBodyHybridPaidGrayStatus = None,
        hybrid_paid_module_switch_map: str = None,
        hybrid_paid_status: int = None,
        hybrid_switch: int = None,
        image_scan_capacity: int = None,
        instance_buy_type: int = None,
        instance_id: str = None,
        intelligent_analysis_flow: int = None,
        is_new_container_version: bool = None,
        is_new_multi_version: bool = None,
        is_over_balance: bool = None,
        is_postpay: bool = None,
        is_trial_version: int = None,
        last_trail_end_time: int = None,
        mvauth_count: int = None,
        mvunused_auth_count: int = None,
        merged_version: int = None,
        multi_version: str = None,
        new_post_paid_cspm: int = None,
        new_threat_analysis: int = None,
        onboarded_assets: int = None,
        open_time: int = None,
        post_paid_first_trial_time: int = None,
        post_paid_last_trial_time: int = None,
        post_paid_trial_expired_time: int = None,
        post_pay_host_version: int = None,
        post_pay_instance_id: str = None,
        post_pay_module_switch: str = None,
        post_pay_open_time: int = None,
        post_pay_status: int = None,
        rasp_capacity: int = None,
        release_time: int = None,
        request_id: str = None,
        sas_edr_client_auth_count: str = None,
        sas_edr_post_paid_instance_id: str = None,
        sas_edr_pre_paid_instance_id: str = None,
        sas_edr_pre_paid_instance_status: str = None,
        sas_edr_version: str = None,
        sas_log: int = None,
        sas_screen: int = None,
        sdk_ai_post_paid_gray: int = None,
        sdk_capacity: int = None,
        sls_capacity: int = None,
        threat_analysis_capacity: int = None,
        threat_analysis_flow: int = None,
        trial_module_list: List[main_models.DescribeVersionConfigResponseBodyTrialModuleList] = None,
        trial_version: int = None,
        user_defined_alarms: int = None,
        version: int = None,
        vm_cores: int = None,
        vul_fix_capacity: int = None,
        web_lock: int = None,
        web_lock_auth_count: int = None,
    ):
        # The number of agentless detection licenses.
        # > Agentless detection is not currently available for purchase. You can ignore this field.
        self.agentless_capacity = agentless_capacity
        # Indicates whether pay-as-you-go purchase is allowed. Valid values:
        # - **0**: Not allowed.
        # - **1**: Allowed.
        self.allow_partial_buy = allow_partial_buy
        # The anti-ransomware backup capacity. Unit: GB.
        self.anti_ransomware_capacity = anti_ransomware_capacity
        # The status of the anti-ransomware managed service. Valid values:
        # - **0**: Disabled.
        # - **1**: Enabled.
        self.anti_ransomware_service = anti_ransomware_service
        # Indicates whether the application whitelist is enabled. Valid values:
        # - **0**: Disabled.
        # - **2**: Enabled.
        self.app_white_list = app_white_list
        # The number of application whitelist licenses.
        # > One license allows you to apply a whitelist policy to one server. After you enable the application whitelist feature, your account is granted 20 licenses by default.
        self.app_white_list_auth_count = app_white_list_auth_count
        # The number of purchased server licenses.
        self.asset_level = asset_level
        # Indicates whether Endpoint Detection and Response (EDR) is purchased.
        self.buy_sas_edr = buy_sas_edr
        # Indicates whether the pay-as-you-go trial plan is supported. Valid values:
        # - **0**: Not supported.
        # - **1**: Supported.
        self.can_try_post_paid_package = can_try_post_paid_package
        # The number of purchased Cloud Security Posture Management (CSPM) scans. Unit: scans per month.
        self.cspm_capacity = cspm_capacity
        # The AI digital human analysis traffic.
        self.cspm_instance_capacity = cspm_instance_capacity
        # The highest purchased edition of Security Center. Valid values:
        # - **1**: Free Edition.
        # - **3**: Enterprise Edition.
        # - **5**: Advanced Edition.
        # - **6**: Anti-virus Edition.
        # - **7**: Ultimate Edition.
        # - **10**: Value-added service only.
        # > If a single edition is purchased, this value indicates the corresponding edition. If multiple editions are purchased, this value indicates the highest edition among the purchased Security Center editions.
        self.highest_version = highest_version
        # The number of purchased honeypot licenses.
        self.honeypot_capacity = honeypot_capacity
        # The canary release module for elastic billing.
        self.hybrid_paid_gray_status = hybrid_paid_gray_status
        # The AI digital human analysis traffic.
        self.hybrid_paid_module_switch_map = hybrid_paid_module_switch_map
        # The status of the elastic billing switch.
        self.hybrid_paid_status = hybrid_paid_status
        # The AI digital human analysis traffic.
        self.hybrid_switch = hybrid_switch
        # The number of purchased image scan licenses.
        self.image_scan_capacity = image_scan_capacity
        # The instance purchase type. Valid values:
        # - **0**: Self-purchased.
        # - **1**: Multi-account allocation.
        self.instance_buy_type = instance_buy_type
        # The instance ID of the purchased Security Center.
        self.instance_id = instance_id
        # The AI digital human analysis traffic.
        self.intelligent_analysis_flow = intelligent_analysis_flow
        # Indicates whether the instance is the latest Ultimate Edition. Valid values:
        # - **true**: Latest version.
        # - **false**: Not the latest version.
        self.is_new_container_version = is_new_container_version
        # Indicates whether the instance is the latest multi-edition. Valid values:
        # - **true**: Latest multi-edition.
        # - **false**: Not the latest multi-edition.
        self.is_new_multi_version = is_new_multi_version
        # Indicates whether the current number of servers exceeds the maximum number of purchased licenses. Valid values:
        # - **false**: Not exceeded.
        # - **true**: Exceeded.
        # >Notice: **[Deprecated]** You can ignore this parameter.</notice>
        self.is_over_balance = is_over_balance
        # Indicates whether pay-as-you-go is enabled. Valid values:
        # - **false**: Disabled.
        # - **true**: Enabled.
        self.is_postpay = is_postpay
        # Indicates whether the current Security Center edition is a trial edition. Valid values:
        # - **0**: Non-trial edition.
        # - **1**: Trial edition.
        self.is_trial_version = is_trial_version
        # The end timestamp of the last Security Center trial. Unit: milliseconds.
        self.last_trail_end_time = last_trail_end_time
        # The total number of licenses for the multi-edition purchase.
        self.mvauth_count = mvauth_count
        # The total number of remaining licenses for the multi-edition purchase.
        self.mvunused_auth_count = mvunused_auth_count
        # The higher protection edition between the subscription and pay-as-you-go services when both are enabled for Security Center host and container security. Valid values:
        # - **1**: Free Edition.
        # - **6**: Anti-virus Edition.
        # - **5**: Advanced Edition.
        # - **3**: Enterprise Edition.
        # - **7**: Ultimate Edition.
        self.merged_version = merged_version
        # The multi-edition version numbers and license usage.
        self.multi_version = multi_version
        # The AI digital human analysis traffic.
        self.new_post_paid_cspm = new_post_paid_cspm
        # Indicates whether the new version of Cloud Threat Detection and Response (CTDR) is enabled. The new version of CTDR supports purchasing inbound traffic and log storage capacity. Valid values:
        # - **0**: No.
        # - **1**: Yes.
        self.new_threat_analysis = new_threat_analysis
        # The AI digital human managed instances.
        self.onboarded_assets = onboarded_assets
        # The timestamp when the service is enabled. Unit: milliseconds.
        self.open_time = open_time
        # The first trial time for pay-as-you-go.
        self.post_paid_first_trial_time = post_paid_first_trial_time
        # The latest trial time for pay-as-you-go.
        self.post_paid_last_trial_time = post_paid_last_trial_time
        # The trial expiration time for pay-as-you-go.
        self.post_paid_trial_expired_time = post_paid_trial_expired_time
        # The highest protection edition for bound assets when the pay-as-you-go service for host and container security is enabled. Valid values:
        # - **1**: Free Edition.
        # - **3**: Enterprise Edition.
        # - **5**: Advanced Edition.
        # - **6**: Anti-virus Edition.
        # - **7**: Ultimate Edition.
        self.post_pay_host_version = post_pay_host_version
        # The pay-as-you-go instance ID.
        self.post_pay_instance_id = post_pay_instance_id
        # The switch status of pay-as-you-go modules. The value is a JSON string. Valid values:
        # - Key:
        #   - **VUL**: Vulnerability fixing module.
        #   - **CSPM**: Cloud Security Posture Management (CSPM) module.
        #   - **AGENTLESS**: Agentless detection module.
        #   - **SERVERLESS**: Serverless security module.
        #   - **CTDR**: Cloud Threat Detection and Response (CTDR) module.
        #   - **POST_HOST**: Host and container security module.
        #   - **SDK**: Malicious file detection SDK module.
        #   - **RASP**: Application protection module.
        # - Value: 0 indicates disabled, and 1 indicates enabled.
        self.post_pay_module_switch = post_pay_module_switch
        # The time when pay-as-you-go is enabled. The value is a UNIX timestamp. Unit: milliseconds.
        self.post_pay_open_time = post_pay_open_time
        # The pay-as-you-go instance status. Valid values:
        # - **1**: Normal.
        # - **2**: Stopped due to overdue payment.
        self.post_pay_status = post_pay_status
        # The number of purchased application protection licenses. Unit: licenses per month.
        self.rasp_capacity = rasp_capacity
        # The UNIX timestamp when the instance expires. Unit: milliseconds.
        # > If you do not complete a renewal within 7 days after the instance expires, your paid instance is downgraded to the Free Edition. You will no longer be able to use the paid features, and your previous Security Center configuration data and historical alerting data (such as DDoS alerting) will become inaccessible. In this case, you must repurchase the service to enable the paid edition of Security Center. For more information, see [Purchase Security Center](https://help.aliyun.com/document_detail/42308.html).
        self.release_time = release_time
        # The unique identifier generated by Alibaba Cloud for the request.
        self.request_id = request_id
        # The number of machines purchased for Endpoint Detection and Response (EDR).
        self.sas_edr_client_auth_count = sas_edr_client_auth_count
        # The instance ID of the pay-as-you-go EDR.
        self.sas_edr_post_paid_instance_id = sas_edr_post_paid_instance_id
        # The subscription EDR instance.
        self.sas_edr_pre_paid_instance_id = sas_edr_pre_paid_instance_id
        # The upfront EDR instance status.
        self.sas_edr_pre_paid_instance_status = sas_edr_pre_paid_instance_status
        # The purchased EDR edition.
        self.sas_edr_version = sas_edr_version
        # Indicates whether log analysis is purchased. Valid values:
        # - **0**: Not purchased.
        # - **1**: Purchased.
        self.sas_log = sas_log
        # Indicates whether the security dashboard is purchased. Valid values:
        # - **0**: Not purchased.
        # - **1**: Purchased.
        self.sas_screen = sas_screen
        # The canary release status of the pay-as-you-go SDK.
        self.sdk_ai_post_paid_gray = sdk_ai_post_paid_gray
        # The number of malicious file detection SDK licenses.
        self.sdk_capacity = sdk_capacity
        # The purchased log storage capacity. Unit: GB. Valid values: 0 to 200000.
        self.sls_capacity = sls_capacity
        # The purchased threat analysis capacity. Unit: GB.
        self.threat_analysis_capacity = threat_analysis_capacity
        # The purchased log inbound traffic for Cloud Threat Detection and Response (CTDR). Unit: GB per day.
        self.threat_analysis_flow = threat_analysis_flow
        # The list of child trial modules.
        self.trial_module_list = trial_module_list
        # The trial edition.
        self.trial_version = trial_version
        # Indicates whether the custom alert feature is enabled. Valid values:
        # - **0**: Disabled.
        # - **2**: Enabled.
        self.user_defined_alarms = user_defined_alarms
        # The purchased Security Center edition. Valid values:  
        # - **1**: Free Edition. 
        # - **3**: Enterprise Edition.
        # - **5**: Advanced Edition.
        # - **6**: Anti-virus Edition.    
        # - **7**: Ultimate Edition.   
        # - **8**: Multi-edition.   
        # - **10**: Value-added service only.
        self.version = version
        # The number of purchased licensed cores.
        self.vm_cores = vm_cores
        # The number of purchased vulnerability fixing licenses. Unit: fixes per month.
        self.vul_fix_capacity = vul_fix_capacity
        # Indicates whether the web tamper-proofing service is enabled. Valid values:
        # - **0**: Disabled.
        # - **1**: Enabled.
        self.web_lock = web_lock
        # The number of purchased web tamper-proofing authorizations. One authorization enables web tamper-proofing for one server. Valid values: 0 to N.
        # > N is the number of servers that you own.
        self.web_lock_auth_count = web_lock_auth_count

    def validate(self):
        if self.hybrid_paid_gray_status:
            self.hybrid_paid_gray_status.validate()
        if self.trial_module_list:
            for v1 in self.trial_module_list:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.agentless_capacity is not None:
            result['AgentlessCapacity'] = self.agentless_capacity

        if self.allow_partial_buy is not None:
            result['AllowPartialBuy'] = self.allow_partial_buy

        if self.anti_ransomware_capacity is not None:
            result['AntiRansomwareCapacity'] = self.anti_ransomware_capacity

        if self.anti_ransomware_service is not None:
            result['AntiRansomwareService'] = self.anti_ransomware_service

        if self.app_white_list is not None:
            result['AppWhiteList'] = self.app_white_list

        if self.app_white_list_auth_count is not None:
            result['AppWhiteListAuthCount'] = self.app_white_list_auth_count

        if self.asset_level is not None:
            result['AssetLevel'] = self.asset_level

        if self.buy_sas_edr is not None:
            result['BuySasEdr'] = self.buy_sas_edr

        if self.can_try_post_paid_package is not None:
            result['CanTryPostPaidPackage'] = self.can_try_post_paid_package

        if self.cspm_capacity is not None:
            result['CspmCapacity'] = self.cspm_capacity

        if self.cspm_instance_capacity is not None:
            result['CspmInstanceCapacity'] = self.cspm_instance_capacity

        if self.highest_version is not None:
            result['HighestVersion'] = self.highest_version

        if self.honeypot_capacity is not None:
            result['HoneypotCapacity'] = self.honeypot_capacity

        if self.hybrid_paid_gray_status is not None:
            result['HybridPaidGrayStatus'] = self.hybrid_paid_gray_status.to_map()

        if self.hybrid_paid_module_switch_map is not None:
            result['HybridPaidModuleSwitchMap'] = self.hybrid_paid_module_switch_map

        if self.hybrid_paid_status is not None:
            result['HybridPaidStatus'] = self.hybrid_paid_status

        if self.hybrid_switch is not None:
            result['HybridSwitch'] = self.hybrid_switch

        if self.image_scan_capacity is not None:
            result['ImageScanCapacity'] = self.image_scan_capacity

        if self.instance_buy_type is not None:
            result['InstanceBuyType'] = self.instance_buy_type

        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id

        if self.intelligent_analysis_flow is not None:
            result['IntelligentAnalysisFlow'] = self.intelligent_analysis_flow

        if self.is_new_container_version is not None:
            result['IsNewContainerVersion'] = self.is_new_container_version

        if self.is_new_multi_version is not None:
            result['IsNewMultiVersion'] = self.is_new_multi_version

        if self.is_over_balance is not None:
            result['IsOverBalance'] = self.is_over_balance

        if self.is_postpay is not None:
            result['IsPostpay'] = self.is_postpay

        if self.is_trial_version is not None:
            result['IsTrialVersion'] = self.is_trial_version

        if self.last_trail_end_time is not None:
            result['LastTrailEndTime'] = self.last_trail_end_time

        if self.mvauth_count is not None:
            result['MVAuthCount'] = self.mvauth_count

        if self.mvunused_auth_count is not None:
            result['MVUnusedAuthCount'] = self.mvunused_auth_count

        if self.merged_version is not None:
            result['MergedVersion'] = self.merged_version

        if self.multi_version is not None:
            result['MultiVersion'] = self.multi_version

        if self.new_post_paid_cspm is not None:
            result['NewPostPaidCspm'] = self.new_post_paid_cspm

        if self.new_threat_analysis is not None:
            result['NewThreatAnalysis'] = self.new_threat_analysis

        if self.onboarded_assets is not None:
            result['OnboardedAssets'] = self.onboarded_assets

        if self.open_time is not None:
            result['OpenTime'] = self.open_time

        if self.post_paid_first_trial_time is not None:
            result['PostPaidFirstTrialTime'] = self.post_paid_first_trial_time

        if self.post_paid_last_trial_time is not None:
            result['PostPaidLastTrialTime'] = self.post_paid_last_trial_time

        if self.post_paid_trial_expired_time is not None:
            result['PostPaidTrialExpiredTime'] = self.post_paid_trial_expired_time

        if self.post_pay_host_version is not None:
            result['PostPayHostVersion'] = self.post_pay_host_version

        if self.post_pay_instance_id is not None:
            result['PostPayInstanceId'] = self.post_pay_instance_id

        if self.post_pay_module_switch is not None:
            result['PostPayModuleSwitch'] = self.post_pay_module_switch

        if self.post_pay_open_time is not None:
            result['PostPayOpenTime'] = self.post_pay_open_time

        if self.post_pay_status is not None:
            result['PostPayStatus'] = self.post_pay_status

        if self.rasp_capacity is not None:
            result['RaspCapacity'] = self.rasp_capacity

        if self.release_time is not None:
            result['ReleaseTime'] = self.release_time

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.sas_edr_client_auth_count is not None:
            result['SasEdrClientAuthCount'] = self.sas_edr_client_auth_count

        if self.sas_edr_post_paid_instance_id is not None:
            result['SasEdrPostPaidInstanceId'] = self.sas_edr_post_paid_instance_id

        if self.sas_edr_pre_paid_instance_id is not None:
            result['SasEdrPrePaidInstanceId'] = self.sas_edr_pre_paid_instance_id

        if self.sas_edr_pre_paid_instance_status is not None:
            result['SasEdrPrePaidInstanceStatus'] = self.sas_edr_pre_paid_instance_status

        if self.sas_edr_version is not None:
            result['SasEdrVersion'] = self.sas_edr_version

        if self.sas_log is not None:
            result['SasLog'] = self.sas_log

        if self.sas_screen is not None:
            result['SasScreen'] = self.sas_screen

        if self.sdk_ai_post_paid_gray is not None:
            result['SdkAiPostPaidGray'] = self.sdk_ai_post_paid_gray

        if self.sdk_capacity is not None:
            result['SdkCapacity'] = self.sdk_capacity

        if self.sls_capacity is not None:
            result['SlsCapacity'] = self.sls_capacity

        if self.threat_analysis_capacity is not None:
            result['ThreatAnalysisCapacity'] = self.threat_analysis_capacity

        if self.threat_analysis_flow is not None:
            result['ThreatAnalysisFlow'] = self.threat_analysis_flow

        result['TrialModuleList'] = []
        if self.trial_module_list is not None:
            for k1 in self.trial_module_list:
                result['TrialModuleList'].append(k1.to_map() if k1 else None)

        if self.trial_version is not None:
            result['TrialVersion'] = self.trial_version

        if self.user_defined_alarms is not None:
            result['UserDefinedAlarms'] = self.user_defined_alarms

        if self.version is not None:
            result['Version'] = self.version

        if self.vm_cores is not None:
            result['VmCores'] = self.vm_cores

        if self.vul_fix_capacity is not None:
            result['VulFixCapacity'] = self.vul_fix_capacity

        if self.web_lock is not None:
            result['WebLock'] = self.web_lock

        if self.web_lock_auth_count is not None:
            result['WebLockAuthCount'] = self.web_lock_auth_count

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AgentlessCapacity') is not None:
            self.agentless_capacity = m.get('AgentlessCapacity')

        if m.get('AllowPartialBuy') is not None:
            self.allow_partial_buy = m.get('AllowPartialBuy')

        if m.get('AntiRansomwareCapacity') is not None:
            self.anti_ransomware_capacity = m.get('AntiRansomwareCapacity')

        if m.get('AntiRansomwareService') is not None:
            self.anti_ransomware_service = m.get('AntiRansomwareService')

        if m.get('AppWhiteList') is not None:
            self.app_white_list = m.get('AppWhiteList')

        if m.get('AppWhiteListAuthCount') is not None:
            self.app_white_list_auth_count = m.get('AppWhiteListAuthCount')

        if m.get('AssetLevel') is not None:
            self.asset_level = m.get('AssetLevel')

        if m.get('BuySasEdr') is not None:
            self.buy_sas_edr = m.get('BuySasEdr')

        if m.get('CanTryPostPaidPackage') is not None:
            self.can_try_post_paid_package = m.get('CanTryPostPaidPackage')

        if m.get('CspmCapacity') is not None:
            self.cspm_capacity = m.get('CspmCapacity')

        if m.get('CspmInstanceCapacity') is not None:
            self.cspm_instance_capacity = m.get('CspmInstanceCapacity')

        if m.get('HighestVersion') is not None:
            self.highest_version = m.get('HighestVersion')

        if m.get('HoneypotCapacity') is not None:
            self.honeypot_capacity = m.get('HoneypotCapacity')

        if m.get('HybridPaidGrayStatus') is not None:
            temp_model = main_models.DescribeVersionConfigResponseBodyHybridPaidGrayStatus()
            self.hybrid_paid_gray_status = temp_model.from_map(m.get('HybridPaidGrayStatus'))

        if m.get('HybridPaidModuleSwitchMap') is not None:
            self.hybrid_paid_module_switch_map = m.get('HybridPaidModuleSwitchMap')

        if m.get('HybridPaidStatus') is not None:
            self.hybrid_paid_status = m.get('HybridPaidStatus')

        if m.get('HybridSwitch') is not None:
            self.hybrid_switch = m.get('HybridSwitch')

        if m.get('ImageScanCapacity') is not None:
            self.image_scan_capacity = m.get('ImageScanCapacity')

        if m.get('InstanceBuyType') is not None:
            self.instance_buy_type = m.get('InstanceBuyType')

        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')

        if m.get('IntelligentAnalysisFlow') is not None:
            self.intelligent_analysis_flow = m.get('IntelligentAnalysisFlow')

        if m.get('IsNewContainerVersion') is not None:
            self.is_new_container_version = m.get('IsNewContainerVersion')

        if m.get('IsNewMultiVersion') is not None:
            self.is_new_multi_version = m.get('IsNewMultiVersion')

        if m.get('IsOverBalance') is not None:
            self.is_over_balance = m.get('IsOverBalance')

        if m.get('IsPostpay') is not None:
            self.is_postpay = m.get('IsPostpay')

        if m.get('IsTrialVersion') is not None:
            self.is_trial_version = m.get('IsTrialVersion')

        if m.get('LastTrailEndTime') is not None:
            self.last_trail_end_time = m.get('LastTrailEndTime')

        if m.get('MVAuthCount') is not None:
            self.mvauth_count = m.get('MVAuthCount')

        if m.get('MVUnusedAuthCount') is not None:
            self.mvunused_auth_count = m.get('MVUnusedAuthCount')

        if m.get('MergedVersion') is not None:
            self.merged_version = m.get('MergedVersion')

        if m.get('MultiVersion') is not None:
            self.multi_version = m.get('MultiVersion')

        if m.get('NewPostPaidCspm') is not None:
            self.new_post_paid_cspm = m.get('NewPostPaidCspm')

        if m.get('NewThreatAnalysis') is not None:
            self.new_threat_analysis = m.get('NewThreatAnalysis')

        if m.get('OnboardedAssets') is not None:
            self.onboarded_assets = m.get('OnboardedAssets')

        if m.get('OpenTime') is not None:
            self.open_time = m.get('OpenTime')

        if m.get('PostPaidFirstTrialTime') is not None:
            self.post_paid_first_trial_time = m.get('PostPaidFirstTrialTime')

        if m.get('PostPaidLastTrialTime') is not None:
            self.post_paid_last_trial_time = m.get('PostPaidLastTrialTime')

        if m.get('PostPaidTrialExpiredTime') is not None:
            self.post_paid_trial_expired_time = m.get('PostPaidTrialExpiredTime')

        if m.get('PostPayHostVersion') is not None:
            self.post_pay_host_version = m.get('PostPayHostVersion')

        if m.get('PostPayInstanceId') is not None:
            self.post_pay_instance_id = m.get('PostPayInstanceId')

        if m.get('PostPayModuleSwitch') is not None:
            self.post_pay_module_switch = m.get('PostPayModuleSwitch')

        if m.get('PostPayOpenTime') is not None:
            self.post_pay_open_time = m.get('PostPayOpenTime')

        if m.get('PostPayStatus') is not None:
            self.post_pay_status = m.get('PostPayStatus')

        if m.get('RaspCapacity') is not None:
            self.rasp_capacity = m.get('RaspCapacity')

        if m.get('ReleaseTime') is not None:
            self.release_time = m.get('ReleaseTime')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('SasEdrClientAuthCount') is not None:
            self.sas_edr_client_auth_count = m.get('SasEdrClientAuthCount')

        if m.get('SasEdrPostPaidInstanceId') is not None:
            self.sas_edr_post_paid_instance_id = m.get('SasEdrPostPaidInstanceId')

        if m.get('SasEdrPrePaidInstanceId') is not None:
            self.sas_edr_pre_paid_instance_id = m.get('SasEdrPrePaidInstanceId')

        if m.get('SasEdrPrePaidInstanceStatus') is not None:
            self.sas_edr_pre_paid_instance_status = m.get('SasEdrPrePaidInstanceStatus')

        if m.get('SasEdrVersion') is not None:
            self.sas_edr_version = m.get('SasEdrVersion')

        if m.get('SasLog') is not None:
            self.sas_log = m.get('SasLog')

        if m.get('SasScreen') is not None:
            self.sas_screen = m.get('SasScreen')

        if m.get('SdkAiPostPaidGray') is not None:
            self.sdk_ai_post_paid_gray = m.get('SdkAiPostPaidGray')

        if m.get('SdkCapacity') is not None:
            self.sdk_capacity = m.get('SdkCapacity')

        if m.get('SlsCapacity') is not None:
            self.sls_capacity = m.get('SlsCapacity')

        if m.get('ThreatAnalysisCapacity') is not None:
            self.threat_analysis_capacity = m.get('ThreatAnalysisCapacity')

        if m.get('ThreatAnalysisFlow') is not None:
            self.threat_analysis_flow = m.get('ThreatAnalysisFlow')

        self.trial_module_list = []
        if m.get('TrialModuleList') is not None:
            for k1 in m.get('TrialModuleList'):
                temp_model = main_models.DescribeVersionConfigResponseBodyTrialModuleList()
                self.trial_module_list.append(temp_model.from_map(k1))

        if m.get('TrialVersion') is not None:
            self.trial_version = m.get('TrialVersion')

        if m.get('UserDefinedAlarms') is not None:
            self.user_defined_alarms = m.get('UserDefinedAlarms')

        if m.get('Version') is not None:
            self.version = m.get('Version')

        if m.get('VmCores') is not None:
            self.vm_cores = m.get('VmCores')

        if m.get('VulFixCapacity') is not None:
            self.vul_fix_capacity = m.get('VulFixCapacity')

        if m.get('WebLock') is not None:
            self.web_lock = m.get('WebLock')

        if m.get('WebLockAuthCount') is not None:
            self.web_lock_auth_count = m.get('WebLockAuthCount')

        return self

class DescribeVersionConfigResponseBodyTrialModuleList(DaraModel):
    def __init__(
        self,
        name: str = None,
    ):
        # The name of the child trial module.
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.name is not None:
            result['Name'] = self.name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')

        return self

class DescribeVersionConfigResponseBodyHybridPaidGrayStatus(DaraModel):
    def __init__(
        self,
        anti_ransomware: int = None,
        cspm_instance: int = None,
        host: int = None,
    ):
        # The canary release status of anti-ransomware elastic protection. Valid values:
        # - 1: In canary release.
        # - 0: Not in canary release.
        self.anti_ransomware = anti_ransomware
        # The canary release status of Cloud Security Posture Management (CSPM) elastic protection. Valid values:
        # - 1: In canary release.
        # - 0: Not in canary release.
        self.cspm_instance = cspm_instance
        # The canary release status of server elastic protection. Valid values:
        # - 1: In canary release.
        # - 0: Not in canary release.
        self.host = host

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.anti_ransomware is not None:
            result['ANTI_RANSOMWARE'] = self.anti_ransomware

        if self.cspm_instance is not None:
            result['CSPM_INSTANCE'] = self.cspm_instance

        if self.host is not None:
            result['HOST'] = self.host

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ANTI_RANSOMWARE') is not None:
            self.anti_ransomware = m.get('ANTI_RANSOMWARE')

        if m.get('CSPM_INSTANCE') is not None:
            self.cspm_instance = m.get('CSPM_INSTANCE')

        if m.get('HOST') is not None:
            self.host = m.get('HOST')

        return self

