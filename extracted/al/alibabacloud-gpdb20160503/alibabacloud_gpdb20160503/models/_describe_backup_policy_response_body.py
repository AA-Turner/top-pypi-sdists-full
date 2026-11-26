# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeBackupPolicyResponseBody(DaraModel):
    def __init__(
        self,
        backup_retention_period: int = None,
        enable_recovery_point: bool = None,
        preferred_backup_period: str = None,
        preferred_backup_time: str = None,
        recovery_point_period: str = None,
        request_id: str = None,
    ):
        # The retention period of data backups in days.
        self.backup_retention_period = backup_retention_period
        # Indicates whether automatic recovery points are enabled. Valid values:
        # 
        # - **true**: Enabled.
        # - **false**: Disabled.
        self.enable_recovery_point = enable_recovery_point
        # The backup cycle. Separate multiple values with commas (,). Valid values:
        # 
        # - **Monday**: Monday.
        # - **Tuesday**: Tuesday.
        # - **Wednesday**: Wednesday.
        # - **Thursday**: Thursday.
        # - **Friday**: Friday.
        # - **Saturday**: Saturday.
        # - **Sunday**: Sunday.
        self.preferred_backup_period = preferred_backup_period
        # The backup time. Format: HH:mmZ-HH:mmZ (UTC).
        self.preferred_backup_time = preferred_backup_time
        # The recovery point frequency. Valid values:
        # 
        # - **1**: Every hour.
        # - **2**: Every two hours.
        # - **4**: Every four hours.
        # - **8**: Every eight hours.
        self.recovery_point_period = recovery_point_period
        # The request ID.
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.backup_retention_period is not None:
            result['BackupRetentionPeriod'] = self.backup_retention_period

        if self.enable_recovery_point is not None:
            result['EnableRecoveryPoint'] = self.enable_recovery_point

        if self.preferred_backup_period is not None:
            result['PreferredBackupPeriod'] = self.preferred_backup_period

        if self.preferred_backup_time is not None:
            result['PreferredBackupTime'] = self.preferred_backup_time

        if self.recovery_point_period is not None:
            result['RecoveryPointPeriod'] = self.recovery_point_period

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupRetentionPeriod') is not None:
            self.backup_retention_period = m.get('BackupRetentionPeriod')

        if m.get('EnableRecoveryPoint') is not None:
            self.enable_recovery_point = m.get('EnableRecoveryPoint')

        if m.get('PreferredBackupPeriod') is not None:
            self.preferred_backup_period = m.get('PreferredBackupPeriod')

        if m.get('PreferredBackupTime') is not None:
            self.preferred_backup_time = m.get('PreferredBackupTime')

        if m.get('RecoveryPointPeriod') is not None:
            self.recovery_point_period = m.get('RecoveryPointPeriod')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        return self

