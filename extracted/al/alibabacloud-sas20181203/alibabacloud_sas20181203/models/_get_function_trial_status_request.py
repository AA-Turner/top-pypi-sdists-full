# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class GetFunctionTrialStatusRequest(DaraModel):
    def __init__(
        self,
        function_name: str = None,
    ):
        # The name of the feature module. Valid values:
        # 
        # - trail_file_detect_api_reward: File detection API trial.
        # 
        # - trail_honeypot_reward: Honeypot trial.
        # 
        # > This parameter is required. If it is not provided, the API returns an HTTP 400 error with the error code -101.
        self.function_name = function_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.function_name is not None:
            result['FunctionName'] = self.function_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionName') is not None:
            self.function_name = m.get('FunctionName')

        return self

