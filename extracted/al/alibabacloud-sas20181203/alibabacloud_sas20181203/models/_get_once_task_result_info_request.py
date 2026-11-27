# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GetOnceTaskResultInfoRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        task_id: str = None,
        task_name: str = None,
        task_type: str = None,
    ):
        # The ID of the member accounts in the resource folder. The member accounts are Alibaba Cloud accounts.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The ID of the scan task.
        # 
        # This parameter is required.
        self.task_id = task_id
        # The node name. Valid values:
        # - **CLIENT_PROBLEM_CHECK**: Client troubleshooting node.
        # - **CLIENT_DEV_OPS**: Cloud O&M node.
        # - **ASSET_SECURITY_CHECK**: Asset collection node.
        # - **ASSETS_COLLECTION**: Asset Fingerprints collection node.
        # - **IMAGE_SCAN**: Container image scan node.
        # - **AI_SECURITY_CHECK**: AI asset synchronization node.
        # - **IDC_PROBE_SCAN**: IDC probe scan node.
        # - **ATTACK_SURFACE_SCAN**: Attack surface border asset scan node.
        # - **ASSET_EXPOSURE_SCAN**: Asset exposure scan node.
        # - **VUL_CHECK_TASK**: Vulnerability scanning node.
        # 
        # This parameter is required.
        self.task_name = task_name
        # The node type. Valid values:
        # - **CLIENT_PROBLEM_CHECK**: Client troubleshooting node.
        # - **CLIENT_DEV_OPS**: Cloud O&M node.
        # - **ASSET_SECURITY_CHECK**: Asset collection node.
        # - **ASSETS_COLLECTION**: Asset Fingerprints collection node.
        # - **IMAGE_SCAN**: Container image scan node.
        # - **AI_SECURITY_CHECK**: AI asset synchronization node.
        # - **IDC_PROBE_SCAN**: IDC probe scan node.
        # - **ATTACK_SURFACE_SCAN**: Attack surface border asset scan node.
        # - **ASSET_EXPOSURE_SCAN**: Asset exposure scan node.
        # - **VUL_CHECK_TASK**: Vulnerability scanning node.
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
        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.task_id is not None:
            result['TaskId'] = self.task_id

        if self.task_name is not None:
            result['TaskName'] = self.task_name

        if self.task_type is not None:
            result['TaskType'] = self.task_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')

        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')

        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')

        return self

