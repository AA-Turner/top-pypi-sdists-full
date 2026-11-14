# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class RestoreTableRequest(DaraModel):
    def __init__(
        self,
        backup_id: str = None,
        client_token: str = None,
        dbinstance_id: str = None,
        instant_recovery: bool = None,
        owner_account: str = None,
        owner_id: int = None,
        resource_owner_account: str = None,
        resource_owner_id: int = None,
        restore_time: str = None,
        table_meta: str = None,
    ):
        # The ID of the backup set. You can call the DescribeBackups operation to query backup sets.
        # 
        # > You must specify at least one of the **BackupId** and **RestoreTime** parameters.
        self.backup_id = backup_id
        # The client token that is used to ensure the idempotence of the request and prevent duplicate submissions. You can use the client to generate the value, and you must ensure that the value is unique among different requests. The value can be up to 64 ASCII characters in length and cannot contain non-ASCII characters.
        self.client_token = client_token
        # The instance ID.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # Specifies whether to enable fast restoration for individual databases and tables. Valid values:
        # * **true**: enables fast restoration.
        # * **false**: disables fast restoration.
        # 
        # > For more information about fast restoration for individual databases and tables, see [Restore databases and tables](https://help.aliyun.com/document_detail/103175.html).
        self.instant_recovery = instant_recovery
        self.owner_account = owner_account
        self.owner_id = owner_id
        self.resource_owner_account = resource_owner_account
        self.resource_owner_id = resource_owner_id
        # The point in time to which you want to restore data. The point in time must be within the backup retention period. Specify the time in the <i>yyyy-MM-dd</i>T<i>HH:mm:ss</i>Z format. The time must be in UTC.
        # 
        # > * You must specify at least one of the **BackupId** and **RestoreTime** parameters.
        # > * [Log backup](https://help.aliyun.com/document_detail/98818.html) must be enabled for the instance.
        self.restore_time = restore_time
        # The databases and tables to be restored.
        # > ApsaraDB RDS for PostgreSQL supports restoring only specific databases and does not support restoring specific tables.
        # 
        # - Format for ApsaraDB RDS for MySQL: ```[{"type":"db","name":"<Name of Database 1>","newname":"<New name of Database 1>","tables":[{"type":"table","name":"<Name of Table 1 in Database 1>","newname":"<New name of Table 1>"},{"type":"table","name":"<Name of Table 2 in Database 1>","newname":"<New name of Table 2>"}]},{"type":"db","name":"<Name of Database 2>","newname":"<New name of Database 2>","tables":[{"type":"table","name":"<Name of Table 3 in Database 2>","newname":"<New name of Table 3>"},{"type":"table","name":"<Name of Table 4 in Database 2>","newname":"<New name of Table 4>"}]}]```
        # 
        # - Format for ApsaraDB RDS for PostgreSQL: ```[{"type":"db","name":"<Name of Database 1>","newname":"<New name of Database 1>"}]```
        # 
        # This parameter is required.
        self.table_meta = table_meta

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.backup_id is not None:
            result['BackupId'] = self.backup_id

        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.instant_recovery is not None:
            result['InstantRecovery'] = self.instant_recovery

        if self.owner_account is not None:
            result['OwnerAccount'] = self.owner_account

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.resource_owner_account is not None:
            result['ResourceOwnerAccount'] = self.resource_owner_account

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.restore_time is not None:
            result['RestoreTime'] = self.restore_time

        if self.table_meta is not None:
            result['TableMeta'] = self.table_meta

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupId') is not None:
            self.backup_id = m.get('BackupId')

        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('InstantRecovery') is not None:
            self.instant_recovery = m.get('InstantRecovery')

        if m.get('OwnerAccount') is not None:
            self.owner_account = m.get('OwnerAccount')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('ResourceOwnerAccount') is not None:
            self.resource_owner_account = m.get('ResourceOwnerAccount')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('RestoreTime') is not None:
            self.restore_time = m.get('RestoreTime')

        if m.get('TableMeta') is not None:
            self.table_meta = m.get('TableMeta')

        return self

