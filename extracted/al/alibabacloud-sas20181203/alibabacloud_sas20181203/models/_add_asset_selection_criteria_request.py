# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class AddAssetSelectionCriteriaRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        criteria: str = None,
        criteria_operation: str = None,
        dry_run: bool = None,
        selection_key: str = None,
        target_operation_list: List[main_models.AddAssetSelectionCriteriaRequestTargetOperationList] = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You can use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies the conditions for searching for assets. The value of this parameter is in JSON format. Note that the parameter value is case-sensitive.
        # > You can search for assets by using conditions such as the instance ID, instance name, VPC ID, region, and public IP address. You can call the [DescribeCriteria](~~DescribeCriteria~~) operation to query the supported search conditions.
        self.criteria = criteria
        # The operation type for the criteria. Valid values:
        # 
        # - **add**: Adds assets.
        # - **del**: Deletes assets.
        self.criteria_operation = criteria_operation
        # Specifies whether to perform a dry run. Valid values:
        # - true: performs a dry run. The system checks the request but does not perform the actual operation.
        # - false: performs the actual operation.
        # Default value: false.
        self.dry_run = dry_run
        # The unique identifier for this asset selection.
        # 
        # This parameter is required.
        self.selection_key = selection_key
        # The asset list.
        self.target_operation_list = target_operation_list

    def validate(self):
        if self.target_operation_list:
            for v1 in self.target_operation_list:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.criteria is not None:
            result['Criteria'] = self.criteria

        if self.criteria_operation is not None:
            result['CriteriaOperation'] = self.criteria_operation

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.selection_key is not None:
            result['SelectionKey'] = self.selection_key

        result['TargetOperationList'] = []
        if self.target_operation_list is not None:
            for k1 in self.target_operation_list:
                result['TargetOperationList'].append(k1.to_map() if k1 else None)

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('Criteria') is not None:
            self.criteria = m.get('Criteria')

        if m.get('CriteriaOperation') is not None:
            self.criteria_operation = m.get('CriteriaOperation')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('SelectionKey') is not None:
            self.selection_key = m.get('SelectionKey')

        self.target_operation_list = []
        if m.get('TargetOperationList') is not None:
            for k1 in m.get('TargetOperationList'):
                temp_model = main_models.AddAssetSelectionCriteriaRequestTargetOperationList()
                self.target_operation_list.append(temp_model.from_map(k1))

        return self



class AddAssetSelectionCriteriaRequestTargetOperationList(DaraModel):
    def __init__(
        self,
        operation: str = None,
        target: str = None,
    ):
        # The operation type. Valid values:
        # 
        # - **add**: Add.
        # - **del**: Delete.
        self.operation = operation
        # The asset ID. If you select assets by machine, the value is the UUID of the machine. If you select assets by group, the value is the group ID. If you select assets by VPC, the value is the VPC ID.
        self.target = target

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.operation is not None:
            result['Operation'] = self.operation

        if self.target is not None:
            result['Target'] = self.target

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Operation') is not None:
            self.operation = m.get('Operation')

        if m.get('Target') is not None:
            self.target = m.get('Target')

        return self

