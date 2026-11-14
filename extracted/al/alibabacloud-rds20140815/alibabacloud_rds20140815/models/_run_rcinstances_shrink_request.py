# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_rds20140815 import models as main_models
from darabonba.model import DaraModel

class RunRCInstancesShrinkRequest(DaraModel):
    def __init__(
        self,
        acu_type: str = None,
        amount: int = None,
        auto_pay: bool = None,
        auto_renew: bool = None,
        auto_use_coupon: bool = None,
        business_info: str = None,
        client_token: str = None,
        create_ack_edge_param_shrink: str = None,
        create_extra_param: str = None,
        create_mode: str = None,
        data_disk_shrink: str = None,
        deletion_protection: bool = None,
        deployment_set_id: str = None,
        description: str = None,
        dry_run: bool = None,
        host_name: str = None,
        image_id: str = None,
        instance_charge_type: str = None,
        instance_name: str = None,
        instance_type: str = None,
        internet_charge_type: str = None,
        internet_max_bandwidth_out: int = None,
        io_optimized: str = None,
        key_pair_name: str = None,
        network_options_shrink: str = None,
        password: str = None,
        password_inherit: bool = None,
        period: int = None,
        period_unit: str = None,
        private_ip_address: str = None,
        promotion_code: str = None,
        region_id: str = None,
        resource_group_id: str = None,
        scheduled_rule: str = None,
        security_enhancement_strategy: str = None,
        security_group_id: str = None,
        security_group_ids_shrink: str = None,
        spot_strategy: str = None,
        support_case: str = None,
        system_disk_shrink: str = None,
        tag: List[main_models.RunRCInstancesShrinkRequestTag] = None,
        user_data: str = None,
        user_data_in_base_64: bool = None,
        v_switch_id: str = None,
        zone_id: str = None,
    ):
        # The ACU type.
        self.acu_type = acu_type
        # The number of RDS Custom instances to create. This parameter is applicable only when you create multiple RDS Custom instances at a time.
        # 
        # Valid values: **1** to **30**. Default value: **1**.
        self.amount = amount
        # Specifies whether to automatically pay for the order. Valid values:
        # - **true** (default): Automatic payment. You must ensure that your account balance is sufficient.
        # - **false**: The order is generated but no payment is deducted.
        # > If the balance of your payment method is insufficient, you can set the AutoPay parameter to false. In this case, an unpaid order is generated, and you can log on to the ApsaraDB RDS console to complete the payment.
        self.auto_pay = auto_pay
        # Specifies whether to enable auto-renewal for the instance. Valid values:
        # 
        # * **true** (default): Yes.
        # * **false**: No.
        self.auto_renew = auto_renew
        # Specifies whether to automatically use coupons. Valid values:
        # * **true** (default): Yes.
        # * **false**: No.
        # 
        # > If you use a coupon and then downgrade the instance configuration, the amount deducted by the voucher will not be refunded.
        self.auto_use_coupon = auto_use_coupon
        # The business information.
        self.business_info = business_info
        # The client token that is used to ensure the idempotence of the request. You can use the client to generate the token, but you must ensure that the token is unique among different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # The information about the ACK Edge cluster.
        self.create_ack_edge_param_shrink = create_ack_edge_param_shrink
        # A reserved parameter. This parameter is not supported.
        self.create_extra_param = create_extra_param
        # Specifies whether the instance is allowed to be added to an ACK cluster. When the parameter is set to **1**, the created instance can be added to an ACK cluster by calling the **AttachRCInstances** API operation, which enables efficient management of containerized applications.
        # 
        # - **1**: Yes.
        # - **0** (default): No.
        self.create_mode = create_mode
        # The list of data cloud disks.
        self.data_disk_shrink = data_disk_shrink
        # Specifies whether to enable release protection. Valid values:
        # * **true**: Enabled.
        # * **false** (default): Disabled.
        self.deletion_protection = deletion_protection
        # The ID of the deployment set.
        self.deployment_set_id = deployment_set_id
        # The description of the instance. The description must be 2 to 256 characters in length and cannot start with http:// or https://.
        self.description = description
        # Specifies whether to perform a dry run before creating the instance. Valid values:
        # * **true**: Performs a dry run without creating the instance. The check items include the request parameters, request format, service limits, and available resources.
        # * **false** (default): Sends a normal request and creates the instance directly after the request passes the check.
        self.dry_run = dry_run
        # The hostname of the instance. The hostname must be 2 to 64 characters in length.
        # 
        # - It can be separated into multiple segments by periods (.). Each segment can contain letters, digits, and hyphens (-).
        # - It cannot start or end with a period (.) or a hyphen (-), and cannot contain consecutive periods (.) or hyphens (-).
        self.host_name = host_name
        # The ID of the image used by the instance.
        self.image_id = image_id
        # The billing method of the instance. Valid values:
        # * **Prepaid**: Subscription.
        # * **Postpaid**: Pay-as-you-go.
        self.instance_charge_type = instance_charge_type
        # The name must be 2 to 128 characters in length. It must start with a letter or a Chinese character, and can contain letters, Chinese characters, digits, periods (.), underscores (_), colons (:), and hyphens (-). The default value is the instance ID. When you create multiple RDS Custom instances, you can specify sequential instance names in batches. The names can contain square brackets ([]) and commas (,). For more information, see [Create an RDS Custom instance](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/create-an-rds-custom-instance#00481f9ba381u).
        self.instance_name = instance_name
        # The instance type. For more information about the instance types supported by RDS Custom instances, see [RDS Custom instance types](https://help.aliyun.com/document_detail/2844823.html).
        # 
        # This parameter is required.
        self.instance_type = instance_type
        # A reserved parameter. This parameter is not supported.
        self.internet_charge_type = internet_charge_type
        # The maximum outbound public bandwidth for Custom for SQL Server. Unit: Mbit/s.
        # 
        # Valid values: 0 to 1024. Default value: 0.
        self.internet_max_bandwidth_out = internet_max_bandwidth_out
        # A reserved parameter. This parameter is not supported.
        self.io_optimized = io_optimized
        # The name of the key pair. Only a single name is supported.
        self.key_pair_name = key_pair_name
        # The network-related properties.
        self.network_options_shrink = network_options_shrink
        # The password of the instance account. The password must be 8 to 30 characters in length and must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include: `()~!@#$%^&*-_+=|{}[]:;\\"<>,.?/`.
        self.password = password
        # Specifies whether to use the password preset in the image. If you specify this parameter, you must leave the Password parameter empty and ensure that the image has a preset password. Default value: false.
        self.password_inherit = password_inherit
        # The subscription duration of the instance. Default value: **1**.
        self.period = period
        # The time unit of the billing duration for the subscription billing method. Valid values:
        # - **Year**: Year.
        # - **Month** (default): Month.
        self.period_unit = period_unit
        # The private IP address of the instance. When you specify a private IP address for a VPC-connected ECS instance, the IP address must be selected from the idle CIDR block of the vSwitch specified by VSwitchId.
        self.private_ip_address = private_ip_address
        # The coupon code.
        self.promotion_code = promotion_code
        # The region ID. You can call the DescribeRegions operation to query the region ID.
        # 
        # This parameter is required.
        self.region_id = region_id
        # The ID of the resource group.
        self.resource_group_id = resource_group_id
        # The scheduled scaling rule.
        self.scheduled_rule = scheduled_rule
        # A reserved parameter. This parameter is not supported.
        self.security_enhancement_strategy = security_enhancement_strategy
        # The ID of the security group to which the instance belongs. Instances in the same security group can access each other. The maximum number of instances that a security group can contain depends on the security group type. For more information, see the "Security groups" section in [Limits](https://help.aliyun.com/document_detail/25412.html).
        # > The SecurityGroupId parameter determines the network type of the instance. For example, if the network type of the specified security group is VPC, the instance is a VPC-connected instance, and you must also specify the VSwitchId parameter.
        self.security_group_id = security_group_id
        # The security groups to which the instance is added. You can add the instance to up to 10 security groups.
        # Note: You cannot specify both SecurityGroupId and SecurityGroupIds.N at the same time.
        self.security_group_ids_shrink = security_group_ids_shrink
        # The bidding policy for the pay-as-you-go instance. This parameter takes effect only when the **InstanceChargeType** parameter is set to **PostPaid**. Valid values:
        # 
        # - **NoSpot**: Regular pay-as-you-go instance.
        # - **SpotAsPriceGo**: The system automatically places a bid based on the current market price.
        # 
        # Default value: **NoSpot**.
        self.spot_strategy = spot_strategy
        # The form of RDS Custom. Valid values:
        # 
        # - **eni**: Dual ENI.
        # - **edge**: Edge node pool.
        # - **share**: VPC.
        self.support_case = support_case
        # The system cloud disk configurations.
        self.system_disk_shrink = system_disk_shrink
        # The list of tags.
        self.tag = tag
        # The instance user data. The raw data can be up to 32 KB in size.
        # 
        # Do not pass confidential information such as passwords and private keys in plaintext. If you must pass such information, encrypt the information, encode the characters in Base64, and then pass it. Perform decryption inside the instance before use. The following example shows how to transform a script to a Base64 string:
        # 
        # ```
        # echo -n \\"#!/bin/sh
        # echo "Hello World"\\" | base64 -w 0
        # ```
        self.user_data = user_data
        # Specifies whether the user data is encoded in Base64.
        # 
        # - **true**: Yes.
        # - **false** (default): No.
        self.user_data_in_base_64 = user_data_in_base_64
        # The ID of the vSwitch to which the target instance belongs. If you create a VPC-connected RDS Custom instance, you must specify the vSwitch ID, and the security group and the vSwitch must belong to the same VPC.
        # > If you configure the VSwitchId parameter, the ZoneId parameter must be set to the zone where the vSwitch resides. You can also leave the ZoneId parameter empty, and the system automatically selects the zone where the specified vSwitch resides.
        # 
        # This parameter is required.
        self.v_switch_id = v_switch_id
        # The zone ID of the instance. You can call the DescribeZones operation to query the zone list.
        # > If you specify the VSwitchId parameter, the ZoneId parameter must be set to the zone where the vSwitch resides. You can also leave the ZoneId parameter empty, and the system automatically selects the zone where the specified vSwitch resides.
        self.zone_id = zone_id

    def validate(self):
        if self.tag:
            for v1 in self.tag:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.acu_type is not None:
            result['AcuType'] = self.acu_type

        if self.amount is not None:
            result['Amount'] = self.amount

        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay

        if self.auto_renew is not None:
            result['AutoRenew'] = self.auto_renew

        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon

        if self.business_info is not None:
            result['BusinessInfo'] = self.business_info

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.create_ack_edge_param_shrink is not None:
            result['CreateAckEdgeParam'] = self.create_ack_edge_param_shrink

        if self.create_extra_param is not None:
            result['CreateExtraParam'] = self.create_extra_param

        if self.create_mode is not None:
            result['CreateMode'] = self.create_mode

        if self.data_disk_shrink is not None:
            result['DataDisk'] = self.data_disk_shrink

        if self.deletion_protection is not None:
            result['DeletionProtection'] = self.deletion_protection

        if self.deployment_set_id is not None:
            result['DeploymentSetId'] = self.deployment_set_id

        if self.description is not None:
            result['Description'] = self.description

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.host_name is not None:
            result['HostName'] = self.host_name

        if self.image_id is not None:
            result['ImageId'] = self.image_id

        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type

        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name

        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type

        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type

        if self.internet_max_bandwidth_out is not None:
            result['InternetMaxBandwidthOut'] = self.internet_max_bandwidth_out

        if self.io_optimized is not None:
            result['IoOptimized'] = self.io_optimized

        if self.key_pair_name is not None:
            result['KeyPairName'] = self.key_pair_name

        if self.network_options_shrink is not None:
            result['NetworkOptions'] = self.network_options_shrink

        if self.password is not None:
            result['Password'] = self.password

        if self.password_inherit is not None:
            result['PasswordInherit'] = self.password_inherit

        if self.period is not None:
            result['Period'] = self.period

        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit

        if self.private_ip_address is not None:
            result['PrivateIpAddress'] = self.private_ip_address

        if self.promotion_code is not None:
            result['PromotionCode'] = self.promotion_code

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id

        if self.scheduled_rule is not None:
            result['ScheduledRule'] = self.scheduled_rule

        if self.security_enhancement_strategy is not None:
            result['SecurityEnhancementStrategy'] = self.security_enhancement_strategy

        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id

        if self.security_group_ids_shrink is not None:
            result['SecurityGroupIds'] = self.security_group_ids_shrink

        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy

        if self.support_case is not None:
            result['SupportCase'] = self.support_case

        if self.system_disk_shrink is not None:
            result['SystemDisk'] = self.system_disk_shrink

        result['Tag'] = []
        if self.tag is not None:
            for k1 in self.tag:
                result['Tag'].append(k1.to_map() if k1 else None)

        if self.user_data is not None:
            result['UserData'] = self.user_data

        if self.user_data_in_base_64 is not None:
            result['UserDataInBase64'] = self.user_data_in_base_64

        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id

        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcuType') is not None:
            self.acu_type = m.get('AcuType')

        if m.get('Amount') is not None:
            self.amount = m.get('Amount')

        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')

        if m.get('AutoRenew') is not None:
            self.auto_renew = m.get('AutoRenew')

        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')

        if m.get('BusinessInfo') is not None:
            self.business_info = m.get('BusinessInfo')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('CreateAckEdgeParam') is not None:
            self.create_ack_edge_param_shrink = m.get('CreateAckEdgeParam')

        if m.get('CreateExtraParam') is not None:
            self.create_extra_param = m.get('CreateExtraParam')

        if m.get('CreateMode') is not None:
            self.create_mode = m.get('CreateMode')

        if m.get('DataDisk') is not None:
            self.data_disk_shrink = m.get('DataDisk')

        if m.get('DeletionProtection') is not None:
            self.deletion_protection = m.get('DeletionProtection')

        if m.get('DeploymentSetId') is not None:
            self.deployment_set_id = m.get('DeploymentSetId')

        if m.get('Description') is not None:
            self.description = m.get('Description')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')

        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')

        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')

        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')

        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')

        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')

        if m.get('InternetMaxBandwidthOut') is not None:
            self.internet_max_bandwidth_out = m.get('InternetMaxBandwidthOut')

        if m.get('IoOptimized') is not None:
            self.io_optimized = m.get('IoOptimized')

        if m.get('KeyPairName') is not None:
            self.key_pair_name = m.get('KeyPairName')

        if m.get('NetworkOptions') is not None:
            self.network_options_shrink = m.get('NetworkOptions')

        if m.get('Password') is not None:
            self.password = m.get('Password')

        if m.get('PasswordInherit') is not None:
            self.password_inherit = m.get('PasswordInherit')

        if m.get('Period') is not None:
            self.period = m.get('Period')

        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')

        if m.get('PrivateIpAddress') is not None:
            self.private_ip_address = m.get('PrivateIpAddress')

        if m.get('PromotionCode') is not None:
            self.promotion_code = m.get('PromotionCode')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')

        if m.get('ScheduledRule') is not None:
            self.scheduled_rule = m.get('ScheduledRule')

        if m.get('SecurityEnhancementStrategy') is not None:
            self.security_enhancement_strategy = m.get('SecurityEnhancementStrategy')

        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')

        if m.get('SecurityGroupIds') is not None:
            self.security_group_ids_shrink = m.get('SecurityGroupIds')

        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')

        if m.get('SupportCase') is not None:
            self.support_case = m.get('SupportCase')

        if m.get('SystemDisk') is not None:
            self.system_disk_shrink = m.get('SystemDisk')

        self.tag = []
        if m.get('Tag') is not None:
            for k1 in m.get('Tag'):
                temp_model = main_models.RunRCInstancesShrinkRequestTag()
                self.tag.append(temp_model.from_map(k1))

        if m.get('UserData') is not None:
            self.user_data = m.get('UserData')

        if m.get('UserDataInBase64') is not None:
            self.user_data_in_base_64 = m.get('UserDataInBase64')

        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')

        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')

        return self

class RunRCInstancesShrinkRequestTag(DaraModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        # The tag key. You can create up to N tag keys at a time. Valid values of N: **1** to **20**. Empty strings are not allowed.
        self.key = key
        # The tag value that corresponds to the tag key. You can create up to N tag values at a time. Valid values of N: **1** to **20**. Empty strings are allowed.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.key is not None:
            result['Key'] = self.key

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

