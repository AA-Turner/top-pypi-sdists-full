# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeModelOperatorApiKeyResponseBody(DaraModel):
    def __init__(
        self,
        api_key: str = None,
        api_key_id: int = None,
        create_time: str = None,
        description: str = None,
        endpoint: str = None,
        request_id: str = None,
        status: str = None,
    ):
        # The plaintext API key. This field is returned only when Status is Running.
        self.api_key = api_key
        # The API key ID.
        self.api_key_id = api_key_id
        # The creation time.
        self.create_time = create_time
        # The description.
        self.description = description
        # The endpoint of the model operator service. This field is returned only when Status is Running.
        self.endpoint = endpoint
        # The request ID.
        self.request_id = request_id
        # The status of the API key. Valid values:
        # 
        # - Creating: The API key is being created.
        # - Running: The API key is running.
        # - Locked: The API key is locked and cannot be used to call the model operator service.
        # - Deleting: The API key is being deleted. You can still query it by calling this operation, but it is no longer displayed in the results of ListModelOperatorApiKeys.
        # 
        # The plaintext API key and endpoint are returned only when Status is Running. After the deletion is complete, this operation returns a resource not found error. The status indicates the processing result of the control plane. A short propagation delay may occur before the status takes effect on the data plane.
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.api_key is not None:
            result['ApiKey'] = self.api_key

        if self.api_key_id is not None:
            result['ApiKeyId'] = self.api_key_id

        if self.create_time is not None:
            result['CreateTime'] = self.create_time

        if self.description is not None:
            result['Description'] = self.description

        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.status is not None:
            result['Status'] = self.status

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ApiKey') is not None:
            self.api_key = m.get('ApiKey')

        if m.get('ApiKeyId') is not None:
            self.api_key_id = m.get('ApiKeyId')

        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')

        if m.get('Description') is not None:
            self.description = m.get('Description')

        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('Status') is not None:
            self.status = m.get('Status')

        return self

