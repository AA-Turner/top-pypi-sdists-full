# Copyright 2026 zovdev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import TYPE_CHECKING, overload, Optional


from ..builder import build_object
from . import aliases


if TYPE_CHECKING:
    from ..types import *


class UploadFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnyStorageFileType, mtime: int, bytes: bytes): ...

    def __init__(self, type, mtime, bytes, _='upload.file', **kwargs):
        kwargs['type'] = type
        kwargs['mtime'] = mtime
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnyStorageFileType:
        return build_object(self['type'])

    @property
    def mtime(self) -> int:
        return self['mtime']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class UploadFileCdnRedirect(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: list[aliases.AnyFileHash]): ...

    def __init__(self, dc_id, file_token, encryption_key, encryption_iv, file_hashes, _='upload.fileCdnRedirect', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['file_token'] = file_token
        kwargs['encryption_key'] = encryption_key
        kwargs['encryption_iv'] = encryption_iv
        kwargs['file_hashes'] = file_hashes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def file_token(self) -> bytes:
        return self['file_token']

    @property
    def encryption_key(self) -> bytes:
        return self['encryption_key']

    @property
    def encryption_iv(self) -> bytes:
        return self['encryption_iv']

    @property
    def file_hashes(self) -> list[aliases.AnyFileHash]:
        return build_object(self['file_hashes'])


class UploadWebFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, size: int, mime_type: str, file_type: aliases.AnyStorageFileType, mtime: int, bytes: bytes): ...

    def __init__(self, size, mime_type, file_type, mtime, bytes, _='upload.webFile', **kwargs):
        kwargs['size'] = size
        kwargs['mime_type'] = mime_type
        kwargs['file_type'] = file_type
        kwargs['mtime'] = mtime
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def size(self) -> int:
        return self['size']

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def file_type(self) -> aliases.AnyStorageFileType:
        return build_object(self['file_type'])

    @property
    def mtime(self) -> int:
        return self['mtime']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class UploadCdnFileReuploadNeeded(dict):
    __slots__ = ()

    @overload
    def __init__(self, request_token: bytes): ...

    def __init__(self, request_token, _='upload.cdnFileReuploadNeeded', **kwargs):
        kwargs['request_token'] = request_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def request_token(self) -> bytes:
        return self['request_token']


class UploadCdnFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, bytes: bytes): ...

    def __init__(self, bytes, _='upload.cdnFile', **kwargs):
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bytes(self) -> bytes:
        return self['bytes']
