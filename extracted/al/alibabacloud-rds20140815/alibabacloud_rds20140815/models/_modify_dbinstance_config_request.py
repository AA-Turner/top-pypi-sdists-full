# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ModifyDBInstanceConfigRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        config_name: str = None,
        config_value: str = None,
        dbinstance_id: str = None,
        owner_account: str = None,
        owner_id: int = None,
        resource_group_id: str = None,
        resource_owner_account: str = None,
        resource_owner_id: int = None,
        switch_time: str = None,
        switch_time_mode: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request and prevent duplicate submissions. You can use the client to generate the token, but you must ensure that it is unique among different requests. The token can contain a maximum of 64 ASCII characters and cannot contain non-ASCII characters.
        self.client_token = client_token
        # The name of the configuration item to be modified. This parameter must be used together with the ConfigValue parameter.
        # <details>
        # <summary>Configuration items for ApsaraDB RDS for PostgreSQL</summary>
        # 
        # - **pgbouncer**: modifies the PgBouncer feature.
        # - **encryptionKey**: modifies the cloud disk encryption feature.
        # - **duckdb_create_databases**: configures databases on the primary instance as DuckDB column store databases in batches.
        # - **duckdb_prepare_dependency**: configures the primary instance with one click so that its parameters and minor engine version meet the [prerequisites](https://help.aliyun.com/document_detail/2977241.html) for creating a DuckDB-based analytical instance. If read-only instances have been created for the primary instance, the read-only instances are also modified in synchronization.
        # - **enable_db_visible_by_connect_rls**: enables CONNECT RLS to control database visibility for the instance.
        # - **set_db_visible_by_connect_rls**: enables CONNECT RLS to control database visibility for databases. This parameter can be invoked only after CONNECT RLS is enabled for the instance.
        # 
        # </details>
        # 
        # <details>
        # <summary>Configuration items for ApsaraDB RDS for SQL Server</summary>
        # 
        # <props="intl">
        # 
        # - **clear_errorlog**: clears error logs.
        # - **encryptionKey**: modifies the cloud disk encryption feature. This feature is not supported for serverless instances and instances of the shared instance type.
        # 
        # 
        # 
        # <props="china">
        # 
        # 
        # - **backup_recovery_model**: enables the simple recovery model. Only Basic Edition instances support this feature. **This feature cannot be disabled after it is enabled**.
        # - **clear_errorlog**: clears error logs.
        # - **encryptionKey**: modifies the cloud disk encryption feature. This feature is not supported for serverless instances and instances of the shared instance type.
        # 
        # 
        # </details>
        # 
        # This parameter is required.
        self.config_name = config_name
        # The value of the configuration item to be modified. This parameter must be used together with the ConfigName parameter.
        # 
        # <details>
        # <summary>Values of configuration items for ApsaraDB RDS for PostgreSQL</summary>
        # 
        # - PgBouncer feature: **true** (enable) or **false** (disable).
        # - Cloud disk encryption feature:
        #   - **ServiceKey**: uses an automatically generated key from Alibaba Cloud, which is the RDS-managed service key (Default Service CMK), to enable cloud disk encryption.
        #   - **<Key>**: uses a custom key to enable cloud disk encryption or replace the current key. Example: `494c98ce-f2b5-48ab-96ab-36c986b6****`.
        #   - **disabled**: disables cloud disk encryption.
        # - One-click repair of prerequisites for creating a DuckDB-based analytical instance: **duckdb_prepare_dependency**.
        # - Batch configuration of databases on the primary instance as DuckDB column store databases. The value is a JSON string. Example: `{"dbNames": "db1,db2,db3", "accountName": "yourSuperAccountName"}`, where:
        #   - **dbNames**: the names of the databases to be converted to DuckDB column store databases. Separate multiple database names with commas (,).
        #   - **accountName**: the privileged account. You only need to configure one privileged account.
        # - Enable CONNECT RLS to control database visibility for the instance: **true** (enable).
        # - Enable CONNECT RLS to control database visibility for databases: the **names of the databases** managed by CONNECT RLS. Separate multiple database names with commas (,). Example: **testdb1,testdb2**. When a client connects to a database with CONNECT RLS enabled, the database list is correctly displayed based on whether the client has the CONNECT permission on other databases.
        # </details>
        # <details>
        # <summary>Values of configuration items for ApsaraDB RDS for SQL Server</summary>
        # 
        # <props="intl">
        # 
        # - Error log cleanup feature: **1** (confirm cleanup).
        # - Cloud disk encryption feature (**this feature cannot be disabled after it is enabled**):
        #   - **serviceKey**: uses an automatically generated key from Alibaba Cloud, which is the RDS-managed service key (Default Service CMK), to enable cloud disk encryption.
        #   - **<Key>**: uses a custom key to enable cloud disk encryption or replace the current key. Example: `494c98ce-f2b5-48ab-96ab-36c986b6****`.
        # 
        # 
        # 
        # 
        # <props="china">
        # 
        # - Simple recovery feature: **simple** (enable simple recovery).
        # - Error log cleanup feature: **1** (confirm cleanup).
        # - Cloud disk encryption feature (**this feature cannot be disabled after it is enabled**):
        #   - **serviceKey**: uses an automatically generated key from Alibaba Cloud, which is the RDS-managed service key (Default Service CMK), to enable cloud disk encryption.
        #   - **<Key>**: uses a custom key to enable cloud disk encryption or replace the current key. Example: `494c98ce-f2b5-48ab-96ab-36c986b6****`.
        # 
        # 
        # 
        # </details>
        # 
        # This parameter is required.
        self.config_value = config_value
        # Instance ID of the instance. You can call the DescribeDBInstances operation to query instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        self.owner_account = owner_account
        self.owner_id = owner_id
        # The ID of the resource group. You can call the DescribeDBInstanceAttribute operation to query the ID.
        self.resource_group_id = resource_group_id
        self.resource_owner_account = resource_owner_account
        self.resource_owner_id = resource_owner_id
        # The time when the modification is executed. Perform the modification during off-peak hours. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm:ss</i>Z format. The time must be in UTC.
        self.switch_time = switch_time
        # The time when the modification takes effect. Valid values:
        # - **Immediate**: takes effect immediately.
        # - **MaintainTime**: takes effect within the maintenance window. You can call the ModifyDBInstanceMaintainTime operation to modify the maintenance window.
        self.switch_time_mode = switch_time_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.config_name is not None:
            result['ConfigName'] = self.config_name

        if self.config_value is not None:
            result['ConfigValue'] = self.config_value

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.owner_account is not None:
            result['OwnerAccount'] = self.owner_account

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id

        if self.resource_owner_account is not None:
            result['ResourceOwnerAccount'] = self.resource_owner_account

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.switch_time is not None:
            result['SwitchTime'] = self.switch_time

        if self.switch_time_mode is not None:
            result['SwitchTimeMode'] = self.switch_time_mode

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')

        if m.get('ConfigValue') is not None:
            self.config_value = m.get('ConfigValue')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('OwnerAccount') is not None:
            self.owner_account = m.get('OwnerAccount')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')

        if m.get('ResourceOwnerAccount') is not None:
            self.resource_owner_account = m.get('ResourceOwnerAccount')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SwitchTime') is not None:
            self.switch_time = m.get('SwitchTime')

        if m.get('SwitchTimeMode') is not None:
            self.switch_time_mode = m.get('SwitchTimeMode')

        return self

