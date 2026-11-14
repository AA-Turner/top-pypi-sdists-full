# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_gpdb20160503 import models as main_models
from darabonba.model import DaraModel

class ListModelOperatorApiKeysResponseBody(DaraModel):
    def __init__(
        self,
        api_keys: List[main_models.ListModelOperatorApiKeysResponseBodyApiKeys] = None,
        page_number: int = None,
        page_record_count: int = None,
        request_id: str = None,
        total_record_count: int = None,
    ):
        # The list of API keys for which no deletion request has been initiated. After a deletion request is accepted, the key no longer appears in this list.
        self.api_keys = api_keys
        # The current page number.
        self.page_number = page_number
        # The number of entries on the current page.
        self.page_record_count = page_record_count
        # The request ID.
        self.request_id = request_id
        # The total number of entries.
        self.total_record_count = total_record_count

    def validate(self):
        if self.api_keys:
            for v1 in self.api_keys:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        result['ApiKeys'] = []
        if self.api_keys is not None:
            for k1 in self.api_keys:
                result['ApiKeys'].append(k1.to_map() if k1 else None)

        if self.page_number is not None:
            result['PageNumber'] = self.page_number

        if self.page_record_count is not None:
            result['PageRecordCount'] = self.page_record_count

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.total_record_count is not None:
            result['TotalRecordCount'] = self.total_record_count

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.api_keys = []
        if m.get('ApiKeys') is not None:
            for k1 in m.get('ApiKeys'):
                temp_model = main_models.ListModelOperatorApiKeysResponseBodyApiKeys()
                self.api_keys.append(temp_model.from_map(k1))

        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')

        if m.get('PageRecordCount') is not None:
            self.page_record_count = m.get('PageRecordCount')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('TotalRecordCount') is not None:
            self.total_record_count = m.get('TotalRecordCount')

        return self

class ListModelOperatorApiKeysResponseBodyApiKeys(DaraModel):
    def __init__(
        self,
        api_key_id: int = None,
        create_time: str = None,
        description: str = None,
        endpoint: str = None,
        status: str = None,
    ):
        # The API key ID.
        self.api_key_id = api_key_id
        # The creation time.
        self.create_time = create_time
        # The description.
        self.description = description
        # The complete HTTP(S) endpoint for calling the model operator service. This field is returned only when Status is Running. This field is not returned for other statuses. The list operation does not return the plaintext API key. To obtain the plaintext API key, call DescribeModelOperatorApiKey.
        self.endpoint = endpoint
        # The status of the API key. The statuses returned in the list include:
        # 
        # - Creating: The API key is being created.
        # - Running: The API key is running.
        # - Locked: The API key is locked and cannot be used to call the model operator service. This status may also be displayed when the API key is being locked or unlocked.
        # 
        # API keys for which a deletion request has been accepted no longer appear in the list. You can call DescribeModelOperatorApiKey to query the Deleting status. After the cleanup is complete, a detail query returns a resource not found error. The status indicates the processing result on the control plane. A short propagation delay may occur before the status takes effect on the data plane.
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.api_key_id is not None:
            result['ApiKeyId'] = self.api_key_id

        if self.create_time is not None:
            result['CreateTime'] = self.create_time

        if self.description is not None:
            result['Description'] = self.description

        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint

        if self.status is not None:
            result['Status'] = self.status

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApiKeyId') is not None:
            self.api_key_id = m.get('ApiKeyId')

        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')

        if m.get('Description') is not None:
            self.description = m.get('Description')

        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')

        if m.get('Status') is not None:
            self.status = m.get('Status')

        return self

