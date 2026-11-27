# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class ModifyClientConfStrategyRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        tag: str = None,
        tag_ext: str = None,
        tag_value: str = None,
        uuid: str = None,
        uuids: List[str] = None,
    ):
        self.resource_directory_account_id = resource_directory_account_id
        # The client configuration tag.
        # 
        # This parameter is required.
        self.tag = tag
        # The extended tag.
        self.tag_ext = tag_ext
        # The client tag value. Valid values:
        # - major
        # - advanced
        # - basic
        # 
        # This parameter is required.
        self.tag_value = tag_value
        # The UUID of the asset to query. You must specify either the Uuid parameter for a single asset or the Uuids parameter for multiple assets. Otherwise, the API returns a 400 error.
        self.uuid = uuid
        # The UUIDs of the asset instances. You can specify up to 500 UUIDs at a time. You must specify either the Uuids parameter for multiple assets or the Uuid parameter for a single asset. Otherwise, the API returns a 400 error.
        self.uuids = uuids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.tag is not None:
            result['Tag'] = self.tag

        if self.tag_ext is not None:
            result['TagExt'] = self.tag_ext

        if self.tag_value is not None:
            result['TagValue'] = self.tag_value

        if self.uuid is not None:
            result['Uuid'] = self.uuid

        if self.uuids is not None:
            result['Uuids'] = self.uuids

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('Tag') is not None:
            self.tag = m.get('Tag')

        if m.get('TagExt') is not None:
            self.tag_ext = m.get('TagExt')

        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')

        if m.get('Uuid') is not None:
            self.uuid = m.get('Uuid')

        if m.get('Uuids') is not None:
            self.uuids = m.get('Uuids')

        return self

