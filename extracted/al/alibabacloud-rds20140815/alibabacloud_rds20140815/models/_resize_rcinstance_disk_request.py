# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class ResizeRCInstanceDiskRequest(DaraModel):
    def __init__(
        self,
        auto_pay: bool = None,
        disk_id: str = None,
        dry_run: bool = None,
        instance_id: str = None,
        new_size: int = None,
        region_id: str = None,
        type: str = None,
    ):
        # Specifies whether to enable automatic payment. Valid values:
        # - **true** (default): Automatic payment is enabled. Make sure that your account balance is sufficient.
        # - **false**: Only an order is generated and no payment is deducted.
        # > If your payment method has an insufficient balance, you can set the AutoPay parameter to false. An unpaid order is generated, and you can log on to the ApsaraDB RDS console to complete the payment.
        # >
        self.auto_pay = auto_pay
        # The cloud disk ID.
        self.disk_id = disk_id
        # Specifies whether to perform a precheck on this operation. Valid values:
        # * **true**: A precheck is performed, and the operation is not executed. Check items include request parameters, request format, business limits, and inventory.
        # * **false** (default): A normal request is sent, and the operation is executed after the request passes the precheck.
        self.dry_run = dry_run
        # The instance ID.
        self.instance_id = instance_id
        # The size of the cloud disk after expansion. Unit: GiB.
        self.new_size = new_size
        # The region ID of the instance.
        self.region_id = region_id
        # The method used to expand the cloud disk. Valid values:
        # - **offline** (default): Offline expansion. After the expansion, you must restart the instance for the changes to take effect.
        # - **online**: Online expansion. The expansion is completed without the need to restart the instance.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay

        if self.disk_id is not None:
            result['DiskId'] = self.disk_id

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id

        if self.new_size is not None:
            result['NewSize'] = self.new_size

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')

        if m.get('DiskId') is not None:
            self.disk_id = m.get('DiskId')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')

        if m.get('NewSize') is not None:
            self.new_size = m.get('NewSize')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

