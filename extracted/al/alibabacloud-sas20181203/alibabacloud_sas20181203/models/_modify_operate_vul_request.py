# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyOperateVulRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        dry_run: bool = None,
        from_: str = None,
        info: str = None,
        operate_type: str = None,
        reason: str = None,
        resource_directory_account_id: int = None,
        type: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You must use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to only precheck the request. Valid values:
        # - true: Prechecks the request without performing the actual operation.
        # - false: Performs the actual operation.
        self.dry_run = dry_run
        # The source identifier of the request. The value is fixed as **sas**.
        self.from_ = from_
        # The information about the vulnerabilities to be processed. This parameter is in JSON format and contains the following fields:
        # 
        # - **name**: The name of the vulnerability.
        # - **uuid**: The UUID of the server where the vulnerability exists.
        # - **tag**: The tag of the vulnerability. Valid values:
        #     - **oval**: Linux software vulnerability
        #     - **system**: Windows system vulnerability
        #     - **cms**: Web-CMS vulnerability
        # 
        # > For other vulnerability types, you can call the [DescribeVulList](~~DescribeVulList~~) operation to obtain the vulnerability information.
        # 
        # - **isFront**: Specifies whether the Windows patch is a prerequisite patch. This parameter is required only when you process Windows system vulnerabilities. You can ignore this parameter when you process other types of vulnerabilities. Valid values:
        #     - **0**: no
        #     - **1**: yes
        # 
        # > You can process multiple vulnerabilities at a time. Separate multiple vulnerability information entries with commas (,). You can call the [DescribeVulList](~~DescribeVulList~~) operation to obtain the vulnerability information.
        # 
        # This parameter is required.
        self.info = info
        # The processing method for the vulnerability. Valid values:
        # - **vul_fix**: Fixes the vulnerability.
        # - **vul_verify**: Verifies the vulnerability.
        # - **vul_ignore**: Ignores the vulnerability.
        # - **vul_undo_ignore**: Cancels ignoring the vulnerability.
        # - **vul_delete**: Deletes the vulnerability.
        # 
        # This parameter is required.
        self.operate_type = operate_type
        # The reason for ignoring the vulnerability.
        # > This parameter is required only when the processing method is **ignore** (that is, **OperateType** is set to **vul_ignore**).
        self.reason = reason
        # The ID of the Alibaba Cloud account to which the member accounts in the resource folder belong.
        # > You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The type of the vulnerability to be processed. Valid values:
        # - **cve**: Linux software vulnerability
        # - **sys**: Windows system vulnerability
        # - **cms**: Web-CMS vulnerability
        # - **emg**: Emergency vulnerability
        # - **app**: Application vulnerability
        # - **sca**: Software constituency parsing vulnerability
        # 
        # > You cannot execute vulnerability fix operations for emergency vulnerabilities (emg), application vulnerabilities (app), and software constituency parsing vulnerabilities (sca).
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
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.from_ is not None:
            result['From'] = self.from_

        if self.info is not None:
            result['Info'] = self.info

        if self.operate_type is not None:
            result['OperateType'] = self.operate_type

        if self.reason is not None:
            result['Reason'] = self.reason

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('From') is not None:
            self.from_ = m.get('From')

        if m.get('Info') is not None:
            self.info = m.get('Info')

        if m.get('OperateType') is not None:
            self.operate_type = m.get('OperateType')

        if m.get('Reason') is not None:
            self.reason = m.get('Reason')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

