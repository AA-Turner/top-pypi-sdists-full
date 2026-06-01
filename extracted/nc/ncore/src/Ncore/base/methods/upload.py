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
from typing import TYPE_CHECKING, overload, Optional, Union, Generic, TypeVar, TypeAlias


from ..builder import build_object
from ..types import aliases
from . import TLMethod, ReturnT


if TYPE_CHECKING:
    from ..types import *
    from ..methods import *

class UploadSaveFilePart(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, file_id: int, file_part: int, bytes: bytes): ...

    def __init__(self, file_id, file_part, bytes, _='upload.saveFilePart', **kwargs):
        kwargs['file_id'] = file_id
        kwargs['file_part'] = file_part
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_id(self) -> int:
        return self['file_id']

    @property
    def file_part(self) -> int:
        return self['file_part']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class UploadGetFile(TLMethod[aliases.AnyUploadFile]):
    __slots__ = ()

    @overload
    def __init__(self, location: aliases.AnyInputFileLocation, offset: int, limit: int, precise: Optional[bool] = ..., cdn_supported: Optional[bool] = ...): ...

    def __init__(self, location, offset, limit, _='upload.getFile', **kwargs):
        kwargs['location'] = location
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def precise(self) -> Optional[bool]:
        return self['precise']

    @property
    def cdn_supported(self) -> Optional[bool]:
        return self['cdn_supported']

    @property
    def location(self) -> aliases.AnyInputFileLocation:
        return build_object(self['location'])

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class UploadSaveBigFilePart(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, file_id: int, file_part: int, file_total_parts: int, bytes: bytes): ...

    def __init__(self, file_id, file_part, file_total_parts, bytes, _='upload.saveBigFilePart', **kwargs):
        kwargs['file_id'] = file_id
        kwargs['file_part'] = file_part
        kwargs['file_total_parts'] = file_total_parts
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_id(self) -> int:
        return self['file_id']

    @property
    def file_part(self) -> int:
        return self['file_part']

    @property
    def file_total_parts(self) -> int:
        return self['file_total_parts']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class UploadGetWebFile(TLMethod[aliases.AnyUploadWebFile]):
    __slots__ = ()

    @overload
    def __init__(self, location: aliases.AnyInputWebFileLocation, offset: int, limit: int): ...

    def __init__(self, location, offset, limit, _='upload.getWebFile', **kwargs):
        kwargs['location'] = location
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def location(self) -> aliases.AnyInputWebFileLocation:
        return build_object(self['location'])

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class UploadGetCdnFile(TLMethod[aliases.AnyUploadCdnFile]):
    __slots__ = ()

    @overload
    def __init__(self, file_token: bytes, offset: int, limit: int): ...

    def __init__(self, file_token, offset, limit, _='upload.getCdnFile', **kwargs):
        kwargs['file_token'] = file_token
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_token(self) -> bytes:
        return self['file_token']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class UploadReuploadCdnFile(TLMethod[list[aliases.AnyFileHash]]):
    __slots__ = ()

    @overload
    def __init__(self, file_token: bytes, request_token: bytes): ...

    def __init__(self, file_token, request_token, _='upload.reuploadCdnFile', **kwargs):
        kwargs['file_token'] = file_token
        kwargs['request_token'] = request_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_token(self) -> bytes:
        return self['file_token']

    @property
    def request_token(self) -> bytes:
        return self['request_token']


class UploadGetCdnFileHashes(TLMethod[list[aliases.AnyFileHash]]):
    __slots__ = ()

    @overload
    def __init__(self, file_token: bytes, offset: int): ...

    def __init__(self, file_token, offset, _='upload.getCdnFileHashes', **kwargs):
        kwargs['file_token'] = file_token
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_token(self) -> bytes:
        return self['file_token']

    @property
    def offset(self) -> int:
        return self['offset']


class UploadGetFileHashes(TLMethod[list[aliases.AnyFileHash]]):
    __slots__ = ()

    @overload
    def __init__(self, location: aliases.AnyInputFileLocation, offset: int): ...

    def __init__(self, location, offset, _='upload.getFileHashes', **kwargs):
        kwargs['location'] = location
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def location(self) -> aliases.AnyInputFileLocation:
        return build_object(self['location'])

    @property
    def offset(self) -> int:
        return self['offset']
