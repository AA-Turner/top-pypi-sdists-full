# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateAdvancedQueryHistoryRequest(DaraModel):
    def __init__(
        self,
        query_sql: str = None,
        simple_query: bool = None,
    ):
        self.query_sql = query_sql
        # This parameter is required.
        self.simple_query = simple_query

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.query_sql is not None:
            result['QuerySql'] = self.query_sql

        if self.simple_query is not None:
            result['SimpleQuery'] = self.simple_query

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('QuerySql') is not None:
            self.query_sql = m.get('QuerySql')

        if m.get('SimpleQuery') is not None:
            self.simple_query = m.get('SimpleQuery')

        return self

