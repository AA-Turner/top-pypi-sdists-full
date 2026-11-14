# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateAccountRequest(DaraModel):
    def __init__(
        self,
        account_description: str = None,
        account_name: str = None,
        account_password: str = None,
        account_type: str = None,
        dbinstance_id: str = None,
        database_name: str = None,
        owner_id: int = None,
    ):
        # The description of the initial account. The description must meet the following requirements:
        # - It must start with a Chinese or English letter.
        # - It cannot start with `http://` or `https://`.
        # - It can contain Chinese characters, English letters, underscores (_), hyphens (-), and digits.
        # - It must be 2 to 256 characters in length.
        self.account_description = account_description
        # The name of the initial account. The name must meet the following requirements:
        # 
        # - It can contain only lowercase letters, digits, and underscores (_).
        # - It must start with a lowercase letter and end with a lowercase letter or a digit.
        # - It cannot start with gp.
        # - It must be 2 to 16 characters in length.
        # 
        # This parameter is required.
        self.account_name = account_name
        # The password of the initial account.
        # 
        # - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters.
        # - Supported special characters: `!@#$%^&*()_+-=`
        # - The password must be 8 to 32 characters in length.
        # 
        # This parameter is required.
        self.account_password = account_password
        # The account type. Default value: Super, which creates a privileged account. If you set this parameter to Normal, a standard account is created.
        self.account_type = account_type
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the details of all AnalyticDB for PostgreSQL instances in a specific region, including the instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The database name. The name must meet the following requirements:
        # - It can contain only letters, digits, and underscores (_).
        # - It must start with a letter.
        # - It cannot exceed 63 characters in length.
        self.database_name = database_name
        self.owner_id = owner_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.account_description is not None:
            result['AccountDescription'] = self.account_description

        if self.account_name is not None:
            result['AccountName'] = self.account_name

        if self.account_password is not None:
            result['AccountPassword'] = self.account_password

        if self.account_type is not None:
            result['AccountType'] = self.account_type

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.database_name is not None:
            result['DatabaseName'] = self.database_name

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountDescription') is not None:
            self.account_description = m.get('AccountDescription')

        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')

        if m.get('AccountPassword') is not None:
            self.account_password = m.get('AccountPassword')

        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('DatabaseName') is not None:
            self.database_name = m.get('DatabaseName')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        return self

