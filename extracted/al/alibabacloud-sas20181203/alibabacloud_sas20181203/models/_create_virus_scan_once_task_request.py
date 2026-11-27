# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class CreateVirusScanOnceTaskRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        dry_run: bool = None,
        param: str = None,
        scan_path: List[str] = None,
        scan_type: str = None,
        selection_key: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You must use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to only precheck the request. A value of true indicates that only the request is checked and no actual operation is performed. A value of false indicates that the request is normally executed. Default value: false.
        self.dry_run = dry_run
        # The extended information fields:
        # - **additionType**: The extended scan type.
        self.param = param
        # The scan path information required for a custom scan.
        self.scan_path = scan_path
        # The scan type of the virus scan. Valid values:
        # - **system**: System scan.
        # - **user**: Custom scan.
        self.scan_type = scan_type
        # The key that stores asset information. You can call the [GetAssetSelectionConfig](~~GetAssetSelectionConfig~~) operation to obtain this parameter.
        self.selection_key = selection_key

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

        if self.param is not None:
            result['Param'] = self.param

        if self.scan_path is not None:
            result['ScanPath'] = self.scan_path

        if self.scan_type is not None:
            result['ScanType'] = self.scan_type

        if self.selection_key is not None:
            result['SelectionKey'] = self.selection_key

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('Param') is not None:
            self.param = m.get('Param')

        if m.get('ScanPath') is not None:
            self.scan_path = m.get('ScanPath')

        if m.get('ScanType') is not None:
            self.scan_type = m.get('ScanType')

        if m.get('SelectionKey') is not None:
            self.selection_key = m.get('SelectionKey')

        return self

