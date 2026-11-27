# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GenerateOnceTaskRequest(DaraModel):
    def __init__(
        self,
        param: str = None,
        resource_directory_account_id: int = None,
        source: str = None,
        task_name: str = None,
        task_type: str = None,
    ):
        # The extended information field.
        # 
        # This parameter is required.
        self.param = param
        # The ID of the member accounts (Alibaba Cloud account) in the resource folder.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to query this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The source of the task.
        self.source = source
        # The node name. Valid values:
        # - **CLIENT_PROBLEM_CHECK**: client troubleshooting node
        # - **CLIENT_DEV_OPS**: cloud O&M node
        # - **ASSET_SECURITY_CHECK**: asset collection node
        # - **ASSETS_COLLECTION**: Asset Fingerprints collection node
        # - **IMAGE_SCAN**: container image scan node
        # - **AI_SECURITY_CHECK**: AI asset synchronization node
        # - **IDC_PROBE_SCAN**: IDC probe scan node
        # - **ATTACK_SURFACE_SCAN**: attack surface border asset scan node
        # - **ASSET_EXPOSURE_SCAN**: asset exposure scan node
        # - **VUL_CHECK_TASK**: vulnerability scanning node
        # 
        # This parameter is required.
        self.task_name = task_name
        # The node type. Valid values:
        # - **CLIENT_PROBLEM_CHECK**: client troubleshooting node
        # - **CLIENT_DEV_OPS**: cloud O&M node
        # - **ASSET_SECURITY_CHECK**: asset collection node
        # - **ASSETS_COLLECTION**: Asset Fingerprints collection node
        # - **IMAGE_SCAN**: container image scan node
        # - **AI_SECURITY_CHECK**: AI asset synchronization node
        # - **IDC_PROBE_SCAN**: IDC probe scan node
        # - **ATTACK_SURFACE_SCAN**: attack surface border asset scan node
        # - **ASSET_EXPOSURE_SCAN**: asset exposure scan node
        # - **VUL_CHECK_TASK**: vulnerability scanning node
        # 
        # This parameter is required.
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.param is not None:
            result['Param'] = self.param

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source is not None:
            result['Source'] = self.source

        if self.task_name is not None:
            result['TaskName'] = self.task_name

        if self.task_type is not None:
            result['TaskType'] = self.task_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Param') is not None:
            self.param = m.get('Param')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Source') is not None:
            self.source = m.get('Source')

        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')

        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')

        return self

