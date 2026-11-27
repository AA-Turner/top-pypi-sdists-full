# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_vpc20160428 import models as main_models
from darabonba.model import DaraModel

class CreateCommonBandwidthPackageRequest(DaraModel):
    def __init__(
        self,
        bandwidth: int = None,
        client_token: str = None,
        description: str = None,
        isp: str = None,
        internet_charge_type: str = None,
        name: str = None,
        owner_account: str = None,
        owner_id: int = None,
        ratio: int = None,
        region_id: str = None,
        resource_group_id: str = None,
        resource_owner_account: str = None,
        resource_owner_id: int = None,
        security_protection_types: List[str] = None,
        tag: List[main_models.CreateCommonBandwidthPackageRequestTag] = None,
        zone: str = None,
    ):
        # The peak bandwidth of the Internet Shared Bandwidth instance. Unit: Mbit/s. 
        # 
        # <props="intl"><ph>Valid values: **1** to **1000**. Default value: **1**.</ph>
        # 
        # <props="china">
        # 
        # - If **InternetChargeType** is set to **PayByBandwidth**, which indicates that the billing method of the Internet Shared Bandwidth instance is pay-by-bandwidth, the valid values of **Bandwidth** are **2** to **20000**.
        # - If **InternetChargeType** is set to **PayBy95**, which indicates that the billing method of the Internet Shared Bandwidth instance is pay-by-enhanced-95th-percentile, the valid values of **Bandwidth** are **200** to **20000**.
        # - If **InternetChargeType** is set to **PayByDominantTraffic**, which indicates that the billing method of the Internet Shared Bandwidth instance is pay-by-dominant-traffic, the valid values of **Bandwidth** are **1** to **2000**.
        # 
        # Default value: **1000**.
        # 
        # This parameter is required.
        self.bandwidth = bandwidth
        # The client token that is used to ensure the idempotence of the request.
        # 
        # You can use the client to generate the value, but you must ensure that it is unique among different requests. The client token can contain only ASCII characters.
        # 
        # > If you do not specify this parameter, the system automatically uses the **RequestId** of the API request as the **ClientToken**. The **RequestId** of each API request is unique.
        self.client_token = client_token
        # The description of the Internet Shared Bandwidth instance.
        # 
        # The description must be 0 to 256 characters in length, and cannot start with `http://` or `https://`.
        self.description = description
        # The line type. Valid values:
        # - **BGP** (default): BGP (multi-ISP) line. BGP (multi-ISP) lines are supported in all regions.
        # - **BGP_PRO**: BGP (multi-ISP) Pro line. BGP (multi-ISP) Pro Internet Shared Bandwidth is supported only in the Hong Kong (China), Singapore, Japan (Tokyo), Philippines (Manila), Malaysia (Kuala Lumpur), Indonesia (Jakarta), and Thailand (Bangkok) regions.
        # 
        # If your account is added to the whitelist for single-ISP bandwidth, you can also select the following values:
        # - **ChinaTelecom**: China Telecom
        # - **ChinaUnicom**: China Unicom
        # - **ChinaMobile**: China Mobile
        # - **ChinaTelecom_L2**: China Telecom L2
        # - **ChinaUnicom_L2**: China Unicom L2
        # - **ChinaMobile_L2**: China Mobile L2
        # 
        # If you use Alibaba Finance Cloud in the China (Hangzhou) region, this parameter is required. Set the value to **BGP_FinanceCloud**.
        self.isp = isp
        # The billing method of the Internet Shared Bandwidth instance. Valid values:
        # <props="intl">**PayByTraffic** (pay-by-data-transfer).
        # 
        # <props="china">
        # 
        # - **PayByBandwidth** (default): pay-by-bandwidth.
        # - **PayBy95**: pay-by-enhanced-95th-percentile.
        # - **PayByDominantTraffic**: pay-by-dominant-traffic.
        self.internet_charge_type = internet_charge_type
        # The name of the Internet Shared Bandwidth instance.
        # 
        # The name must be 0 to 128 characters in length, and cannot start with `http://` or `https://`.
        self.name = name
        self.owner_account = owner_account
        self.owner_id = owner_id
        # The minimum bandwidth percentage of the Internet Shared Bandwidth instance. Set the value to **20**.
        # 
        # <props="china"><ph>This parameter is required when **InternetChargeType** is set to **PayBy95**.</ph>
        # >This parameter is supported only on the Alibaba Cloud China site.
        self.ratio = ratio
        # The region ID of the Internet Shared Bandwidth instance.
        # 
        # You can call the [DescribeRegions](https://help.aliyun.com/document_detail/36063.html) operation to query region IDs.
        # 
        # This parameter is required.
        self.region_id = region_id
        # The ID of the resource group.
        self.resource_group_id = resource_group_id
        self.resource_owner_account = resource_owner_account
        self.resource_owner_id = resource_owner_id
        # The security protection level.
        # 
        # - If this parameter is left empty, Anti-DDoS Basic is used by default.
        # 
        # - If this parameter is set to **AntiDDoS_Enhanced**, Anti-DDoS (Enhanced) is used.
        # 
        # <props="china"><ph>You can configure this parameter when **InternetChargeType** is set to **PayBy95**.</ph>
        # 
        # You can add up to 10 security protection levels.
        # 
        # > **[Deprecated]** This parameter is deprecated.
        self.security_protection_types = security_protection_types
        # The list of tags of the Internet Shared Bandwidth instance.
        self.tag = tag
        # The zone of the Internet Shared Bandwidth instance.
        # This parameter is required when you create an Internet Shared Bandwidth instance for a CloudBox.
        self.zone = zone

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
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.description is not None:
            result['Description'] = self.description

        if self.isp is not None:
            result['ISP'] = self.isp

        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type

        if self.name is not None:
            result['Name'] = self.name

        if self.owner_account is not None:
            result['OwnerAccount'] = self.owner_account

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.ratio is not None:
            result['Ratio'] = self.ratio

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id

        if self.resource_owner_account is not None:
            result['ResourceOwnerAccount'] = self.resource_owner_account

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.security_protection_types is not None:
            result['SecurityProtectionTypes'] = self.security_protection_types

        result['Tag'] = []
        if self.tag is not None:
            for k1 in self.tag:
                result['Tag'].append(k1.to_map() if k1 else None)

        if self.zone is not None:
            result['Zone'] = self.zone

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('Description') is not None:
            self.description = m.get('Description')

        if m.get('ISP') is not None:
            self.isp = m.get('ISP')

        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')

        if m.get('Name') is not None:
            self.name = m.get('Name')

        if m.get('OwnerAccount') is not None:
            self.owner_account = m.get('OwnerAccount')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('Ratio') is not None:
            self.ratio = m.get('Ratio')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')

        if m.get('ResourceOwnerAccount') is not None:
            self.resource_owner_account = m.get('ResourceOwnerAccount')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SecurityProtectionTypes') is not None:
            self.security_protection_types = m.get('SecurityProtectionTypes')

        self.tag = []
        if m.get('Tag') is not None:
            for k1 in m.get('Tag'):
                temp_model = main_models.CreateCommonBandwidthPackageRequestTag()
                self.tag.append(temp_model.from_map(k1))

        if m.get('Zone') is not None:
            self.zone = m.get('Zone')

        return self

class CreateCommonBandwidthPackageRequestTag(DaraModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        # The tag key of the resource. You can specify up to 20 tag keys. If you specify this parameter, you cannot specify an empty string.
        # 
        # A tag key can be up to 128 characters in length. It cannot start with `aliyun` or `acs:`, and cannot contain `http://` or `https://`.
        self.key = key
        # The tag value of the resource. You can specify up to 20 tag values. If you specify this parameter, you can specify an empty string.
        # 
        # A tag value can be up to 128 characters in length. It cannot start with `aliyun` or `acs:`, and cannot contain `http://` or `https://`.
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

