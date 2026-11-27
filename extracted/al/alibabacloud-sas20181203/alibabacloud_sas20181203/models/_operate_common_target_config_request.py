# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class OperateCommonTargetConfigRequest(DaraModel):
    def __init__(
        self,
        field_name: str = None,
        field_value: str = None,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        target_operations: str = None,
        target_type: str = None,
        type: str = None,
    ):
        # The target type of the image switch. Valid values:
        # - **repoName**: the repository name
        # - **repoNamespace**: the repository namespace name
        self.field_name = field_name
        # The repository name or the repository namespace name.
        self.field_value = field_value
        # The ID of the member accounts in the resource folder (Alibaba Cloud account).
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to retrieve this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The source IP address.
        self.source_ip = source_ip
        # The parameters for configuring proactive defense for servers. This includes the following parameters:
        # 
        # - **targetType**: the dimension of the defense configuration. Currently, only the UUID dimension is supported. Set the value to **uuid**.
        # - **target**: the UUID of the server for which you want to configure defense settings
        # - **flag**: specifies whether to enable or disable proactive defense for the server. Valid values: **add** (enable) and **del** (disable).
        # 
        # This parameter is required.
        self.target_operations = target_operations
        # The target asset type. Valid values:
        # - **uuid**: the server UUID
        # - **Cluster**: the cluster ID
        # - **image_repo**: the image repository name
        self.target_type = target_type
        # The switch type. Valid values:
        # - **alidetect-scan-enable**: local-only file detection
        # - **ACTION-TRIAL-PERMISSION**: ActionTrail data delivery
        # - **alidetect**: the local file detection engine
        # - **container_prevent_escape**: container escape prevention
        # - **image_repo**: repository image scanning
        # - **proc_filter_switch**: log filtering
        # - **agentless**: agentless detection
        # - **rasp**: application protection
        # - **sensitiveFile**: sensitive information scanning
        # - **aliscriptengine**: the deep detection engine
        # - **containerNetwork**: container visualization
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.field_name is not None:
            result['FieldName'] = self.field_name

        if self.field_value is not None:
            result['FieldValue'] = self.field_value

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.target_operations is not None:
            result['TargetOperations'] = self.target_operations

        if self.target_type is not None:
            result['TargetType'] = self.target_type

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FieldName') is not None:
            self.field_name = m.get('FieldName')

        if m.get('FieldValue') is not None:
            self.field_value = m.get('FieldValue')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('TargetOperations') is not None:
            self.target_operations = m.get('TargetOperations')

        if m.get('TargetType') is not None:
            self.target_type = m.get('TargetType')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

