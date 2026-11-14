# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GrantAccountPrivilegeRequest(DaraModel):
    def __init__(
        self,
        account_name: str = None,
        account_privilege: str = None,
        dbinstance_id: str = None,
        dbname: str = None,
        resource_owner_id: int = None,
    ):
        # The name of the account. You can call the [DescribeAccounts](https://help.aliyun.com/document_detail/610454.html) operation to query the account name.
        # 
        # This parameter is required.
        self.account_name = account_name
        # The permission type of the account. If you specify multiple values for DBName, you must specify the same number of permission types in the same order and separate them with commas (,).
        # 
        # The supported permission types vary based on the database engine. Valid values:
        # > For more information about account permissions, see [MySQL and MariaDB permissions](https://help.aliyun.com/document_detail/146395.html), [SQL Server permissions](https://help.aliyun.com/document_detail/95692.html), and [PostgreSQL permissions](https://help.aliyun.com/document_detail/257684.html).
        # <details>
        # <summary>RDS MySQL and RDS MariaDB</summary>
        # 
        # - **ReadWrite**: Read and write.
        # - **ReadOnly**: Read-only.
        # - **DDLOnly**: DDL only.
        # - **DMLOnly**: DML only.
        # 
        # </details>
        # 
        # <details>
        # <summary>RDS SQL Server</summary>
        # 
        # - **ReadWrite**: Read and write. This permission corresponds to the `db_datawriter` and `db_datareader` database roles in SQL Server.
        # - **ReadOnly**: Read-only. This permission corresponds to the `db_datareader` database role in SQL Server.
        # - **DBOwner**: Database owner. This permission corresponds to the `db_owner` database role in SQL Server.
        # > For more information about database-level roles, see [Microsoft documentation](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver16).
        # </details>
        # 
        # <details>
        # <summary>RDS PostgreSQL</summary>
        # 
        # **DBOwner**: Database owner.
        # > For more information about fine-grained management of account permissions, see [Best practices for PostgreSQL permission management](https://help.aliyun.com/document_detail/352149.html).
        # </details>
        # 
        # This parameter is required.
        self.account_privilege = account_privilege
        # Instance ID of the instance. You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/610396.html) operation to query instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The name of the database to which you want to grant access. To grant access to multiple databases at a time, separate multiple database names with commas (,), such as `db1,db2,db3`.
        # 
        # This parameter is required.
        self.dbname = dbname
        self.resource_owner_id = resource_owner_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.account_name is not None:
            result['AccountName'] = self.account_name

        if self.account_privilege is not None:
            result['AccountPrivilege'] = self.account_privilege

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.dbname is not None:
            result['DBName'] = self.dbname

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')

        if m.get('AccountPrivilege') is not None:
            self.account_privilege = m.get('AccountPrivilege')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('DBName') is not None:
            self.dbname = m.get('DBName')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        return self

