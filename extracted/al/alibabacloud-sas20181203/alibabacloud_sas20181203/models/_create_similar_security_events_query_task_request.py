# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateSimilarSecurityEventsQueryTaskRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        dry_run: bool = None,
        resource_directory_account_id: int = None,
        resource_owner_id: int = None,
        security_event_id: int = None,
        similar_event_scenario_code: str = None,
        source_ip: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. You can use different tokens for different requests. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # Specifies whether to precheck the request. Valid values:
        # - true: The system only prechecks the request and does not perform the actual operation.
        # - false: The system performs the actual operation.
        # Default value: false.
        self.dry_run = dry_run
        # The UID of the member accounts in the resource folder. This parameter is used to specify the target member accounts in multi-account scenarios.
        self.resource_directory_account_id = resource_directory_account_id
        self.resource_owner_id = resource_owner_id
        # The ID of the alert event.
        # 
        # This parameter is required.
        self.security_event_id = security_event_id
        # The code of alerting events that hit the same rule or have the same rule hits.
        self.similar_event_scenario_code = similar_event_scenario_code
        # The IP address of the access source.
        self.source_ip = source_ip

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

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.resource_owner_id is not None:
            result['ResourceOwnerId'] = self.resource_owner_id

        if self.security_event_id is not None:
            result['SecurityEventId'] = self.security_event_id

        if self.similar_event_scenario_code is not None:
            result['SimilarEventScenarioCode'] = self.similar_event_scenario_code

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('ResourceOwnerId') is not None:
            self.resource_owner_id = m.get('ResourceOwnerId')

        if m.get('SecurityEventId') is not None:
            self.security_event_id = m.get('SecurityEventId')

        if m.get('SimilarEventScenarioCode') is not None:
            self.similar_event_scenario_code = m.get('SimilarEventScenarioCode')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        return self

