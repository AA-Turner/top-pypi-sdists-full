# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class SubmitCheckRequest(DaraModel):
    def __init__(
        self,
        config_id: str = None,
        resource_directory_account_id: int = None,
        scan_range: str = None,
        task_source: str = None,
    ):
        # The policy ID. This parameter takes effect only when ScanRange is set to POLICY. You can obtain the value by calling the ListCheckConfigs operation. If this parameter is not specified or is set to default, the scan is triggered based on the system default policy. If the default policy does not exist, NoDefaultStrategy is returned. If another value is specified, the scan is triggered based on the check items of the specified policy. If the policy does not exist or does not belong to the current account, IllegalParam is returned. This parameter is ignored when ScanRange is set to FULL or FREE.
        self.config_id = config_id
        # The ID of the Alibaba Cloud account to which the member accounts of the resource folder belong.
        # >You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The check scope. Valid values:
        # - **FULL**: Scans all check items.
        # - **POLICY**: Scans check items of custom configurations.
        self.scan_range = scan_range
        # The source of the task. Valid values:
        # 
        # - **YAO_CHI**: ApsaraDB console.
        self.task_source = task_source

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.config_id is not None:
            result['ConfigId'] = self.config_id

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.scan_range is not None:
            result['ScanRange'] = self.scan_range

        if self.task_source is not None:
            result['TaskSource'] = self.task_source

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigId') is not None:
            self.config_id = m.get('ConfigId')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('ScanRange') is not None:
            self.scan_range = m.get('ScanRange')

        if m.get('TaskSource') is not None:
            self.task_source = m.get('TaskSource')

        return self

