# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class GetDockerhubImageRiskRankInfoRequest(DaraModel):
    def __init__(
        self,
        types: List[str] = None,
    ):
        # The image dimension types to be aggregated.
        # 
        # > This parameter is required. You must specify at least one valid value. If no value is specified or all specified values are invalid, the API returns HTTP 400 with the error code -101.
        self.types = types

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.types is not None:
            result['Types'] = self.types

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Types') is not None:
            self.types = m.get('Types')

        return self

