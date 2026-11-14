# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_rds20140815 import models as main_models
from darabonba.model import DaraModel

class ModifySecurityIpsRequest(DaraModel):
    def __init__(
        self,
        batch_mode: bool = None,
        dbinstance_iparray_attribute: str = None,
        dbinstance_iparray_name: str = None,
        dbinstance_id: str = None,
        fresh_white_list_readins: str = None,
        group_items: List[main_models.ModifySecurityIpsRequestGroupItems] = None,
        modify_mode: str = None,
        resource_owner_id: int = None,
        security_iptype: str = None,
        security_ips: str = None,
        whitelist_network_type: str = None,
    ):
        # Specifies whether to enable the batch modification mode. Valid values:
        # 
        # true: enables the batch modification mode. You can modify multiple IP whitelist groups at a time based on the GroupItems parameter. In this case, the SecurityIps, DBInstanceIPArrayName, and DBInstanceIPArrayAttribute parameters for a single group do not take effect.
        # 
        # false: disables the batch modification mode. You can modify a single IP whitelist group based on parameters such as SecurityIps. This is the default value.
        self.batch_mode = batch_mode
        # The attribute of the IP whitelist group.
        # 
        # - If you do not specify this parameter, the group is a regular group. This is the default value.
        # - If you set this parameter to `hidden`, the group is a system-generated group that is used by services such as Data Management (DMS), Data Transmission Service (DTS), and Database Autonomy Service (DAS). These groups are not displayed in the console. If you delete or modify these groups, services such as DMS, DTS, and DAS cannot access the ApsaraDB RDS instance. Proceed with caution.
        self.dbinstance_iparray_attribute = dbinstance_iparray_attribute
        # The name of the IP whitelist group to be modified. Default value: Default. If the specified group does not exist, the system automatically creates the group.
        # 
        # >A single instance supports up to 200 IP whitelist groups.
        self.dbinstance_iparray_name = dbinstance_iparray_name
        # The instance ID of the target instance.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The list of read-only instances to which the IP whitelist is synchronized.
        # 
        # - This parameter applies only to ApsaraDB RDS for PostgreSQL instances that have read-only instances.
        # - If multiple read-only instances exist, separate their IDs with commas (,).
        self.fresh_white_list_readins = fresh_white_list_readins
        # The details of the IP whitelist groups. This parameter is required when BatchMode is set to true. The GroupName parameter is required and must be unique for each group. You must specify at least one of the SecurityIPList and GroupTag parameters.
        self.group_items = group_items
        # The modification mode. Valid values:
        # * **Cover**: overwrites the existing IP whitelist with the IP addresses specified by the **SecurityIps** parameter. This is the default value.
        # * **Append**: appends the IP addresses specified by the **SecurityIps** parameter to the existing IP whitelist.
        # * **Delete**: deletes the IP addresses specified by the **SecurityIps** parameter from the existing IP whitelist. You must retain at least one IP address in the whitelist.
        self.modify_mode = modify_mode
        self.resource_owner_id = resource_owner_id
        # The type of the IP address. Set the value to IPv4. IPv6 is not supported.
        self.security_iptype = security_iptype
        # The IP whitelist. Before you modify the IP whitelist, call the [DescribeDBInstanceIPArrayList](https://help.aliyun.com/document_detail/610518.html) operation to query the existing IP whitelist of the instance.
        # 
        # <details>
        # <summary>Configuration rules</summary>
        # 
        # - You can enter IP addresses such as 10.23.XX.XX or CIDR blocks such as 10.23.XX.XX/24.
        # 
        # - Separate multiple IP addresses or CIDR blocks with commas (,). Do not add spaces before or after the commas.
        # 
        # - You can add up to 1,000 IP addresses or CIDR blocks to the whitelist of a single instance. If you have a large number of IP addresses, we recommend that you merge them into CIDR blocks, such as 10.23.XX.XX/24.
        # </details>
        self.security_ips = security_ips
        # The network type of the IP whitelist. Valid values:
        # 
        # * **MIX**: the standard whitelist mode. This is the default value.
        # * **Classic**: the classic network in the enhanced whitelist mode.
        # * **VPC**: the VPC in the enhanced whitelist mode.
        # 
        # > * For ApsaraDB RDS for PostgreSQL instances with cloud disks, the network type is fixed to MIX. If you configure another mode, the system automatically changes it to MIX.
        # > * The enhanced whitelist mode is supported only by ApsaraDB RDS for MySQL 5.1, 5.5, 5.6, and 5.7 instances with Premium Local SSDs, and ApsaraDB RDS for PostgreSQL 9.4 and 10 instances with Premium Local SSDs.
        self.whitelist_network_type = whitelist_network_type

    def validate(self):
        if self.group_items:
            for v1 in self.group_items:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.batch_mode is not None:
            result['BatchMode'] = self.batch_mode

        if self.dbinstance_iparray_attribute is not None:
            result['DBInstanceIPArrayAttribute'] = self.dbinstance_iparray_attribute

        if self.dbinstance_iparray_name is not None:
            result['DBInstanceIPArrayName'] = self.dbinstance_iparray_name

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.fresh_white_list_readins is not None:
            result['FreshWhiteListReadins'] = self.fresh_white_list_readins

        result['GroupItems'] = []
        if self.group_items is not None:
            for k1 in self.group_items:
                result['GroupItems'].append(k1.to_map() if k1 else None)

        if self.modify_mode is not None:
            result['ModifyMode'] = self.modify_mode

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.security_iptype is not None:
            result['SecurityIPType'] = self.security_iptype

        if self.security_ips is not None:
            result['SecurityIps'] = self.security_ips

        if self.whitelist_network_type is not None:
            result['WhitelistNetworkType'] = self.whitelist_network_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BatchMode') is not None:
            self.batch_mode = m.get('BatchMode')

        if m.get('DBInstanceIPArrayAttribute') is not None:
            self.dbinstance_iparray_attribute = m.get('DBInstanceIPArrayAttribute')

        if m.get('DBInstanceIPArrayName') is not None:
            self.dbinstance_iparray_name = m.get('DBInstanceIPArrayName')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('FreshWhiteListReadins') is not None:
            self.fresh_white_list_readins = m.get('FreshWhiteListReadins')

        self.group_items = []
        if m.get('GroupItems') is not None:
            for k1 in m.get('GroupItems'):
                temp_model = main_models.ModifySecurityIpsRequestGroupItems()
                self.group_items.append(temp_model.from_map(k1))

        if m.get('ModifyMode') is not None:
            self.modify_mode = m.get('ModifyMode')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SecurityIPType') is not None:
            self.security_iptype = m.get('SecurityIPType')

        if m.get('SecurityIps') is not None:
            self.security_ips = m.get('SecurityIps')

        if m.get('WhitelistNetworkType') is not None:
            self.whitelist_network_type = m.get('WhitelistNetworkType')

        return self

class ModifySecurityIpsRequestGroupItems(DaraModel):
    def __init__(
        self,
        group_name: str = None,
        group_tag: str = None,
        security_iplist: str = None,
    ):
        # The name of the IP whitelist group. This parameter is required in batch mode and must be unique within the same GroupItems list.
        self.group_name = group_name
        # The attribute of the IP whitelist group. If you set this parameter to hidden, the group is a system-generated group that is used by services such as DMS, DTS, and DAS. These groups are not displayed in the console. Proceed with caution. Generally, you do not need to specify this parameter. You must specify at least one of this parameter and SecurityIPList.
        self.group_tag = group_tag
        # The modified IP address whitelist of the group. Separate multiple IP addresses with commas (,). You must specify at least one of this parameter and GroupTag.
        self.security_iplist = security_iplist

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.group_name is not None:
            result['GroupName'] = self.group_name

        if self.group_tag is not None:
            result['GroupTag'] = self.group_tag

        if self.security_iplist is not None:
            result['SecurityIPList'] = self.security_iplist

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')

        if m.get('GroupTag') is not None:
            self.group_tag = m.get('GroupTag')

        if m.get('SecurityIPList') is not None:
            self.security_iplist = m.get('SecurityIPList')

        return self

