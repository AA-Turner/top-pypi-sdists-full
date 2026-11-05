# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from alibabacloud_sas20181203 import models as main_models
from darabonba.model import DaraModel

class CreateFileDetectUploadUrlRequest(DaraModel):
    def __init__(
        self,
        hash_key_context_list: List[main_models.CreateFileDetectUploadUrlRequestHashKeyContextList] = None,
        hash_key_list: List[str] = None,
        type: int = None,
    ):
        # The file identifier. Only MD5 is supported. You can specify up to 100 elements in the list.
        # > **HashKeyList** and **HashKeyContextList** cannot be empty at the same time.
        self.hash_key_context_list = hash_key_context_list
        # The unique identifier of the file. You can specify up to 100 elements in the list.
        # > **HashKeyList** and **HashKeyContextList** cannot be empty at the same time.
        self.hash_key_list = hash_key_list
        # The file type. Valid values:
        # - **0**: Uncertain file type.
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        if self.hash_key_context_list:
            for v1 in self.hash_key_context_list:
                 if v1:
                    v1.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        result['HashKeyContextList'] = []
        if self.hash_key_context_list is not None:
            for k1 in self.hash_key_context_list:
                result['HashKeyContextList'].append(k1.to_map() if k1 else None)

        if self.hash_key_list is not None:
            result['HashKeyList'] = self.hash_key_list

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.hash_key_context_list = []
        if m.get('HashKeyContextList') is not None:
            for k1 in m.get('HashKeyContextList'):
                temp_model = main_models.CreateFileDetectUploadUrlRequestHashKeyContextList()
                self.hash_key_context_list.append(temp_model.from_map(k1))

        if m.get('HashKeyList') is not None:
            self.hash_key_list = m.get('HashKeyList')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

class CreateFileDetectUploadUrlRequestHashKeyContextList(DaraModel):
    def __init__(
        self,
        file_size: int = None,
        hash_key: str = None,
    ):
        # The file size. If the file size exceeds the limit, the upload parameters are not returned. Unit: bytes.
        self.file_size = file_size
        # The file hash value.
        self.hash_key = hash_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.file_size is not None:
            result['FileSize'] = self.file_size

        if self.hash_key is not None:
            result['HashKey'] = self.hash_key

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FileSize') is not None:
            self.file_size = m.get('FileSize')

        if m.get('HashKey') is not None:
            self.hash_key = m.get('HashKey')

        return self

