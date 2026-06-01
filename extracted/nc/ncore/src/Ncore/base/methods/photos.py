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

class PhotosUpdateProfilePhoto(TLMethod[aliases.AnyPhotosPhoto]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPhoto, fallback: Optional[bool] = ..., bot: Optional[aliases.AnyInputUser] = ...): ...

    def __init__(self, id, _='photos.updateProfilePhoto', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def fallback(self) -> Optional[bool]:
        return self['fallback']

    @property
    def bot(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['bot'])

    @property
    def id(self) -> aliases.AnyInputPhoto:
        return build_object(self['id'])


class PhotosUploadProfilePhoto(TLMethod[aliases.AnyPhotosPhoto]):
    __slots__ = ()

    @overload
    def __init__(self, fallback: Optional[bool] = ..., bot: Optional[aliases.AnyInputUser] = ..., file: Optional[aliases.AnyInputFile] = ..., video: Optional[aliases.AnyInputFile] = ..., video_start_ts: Optional[float] = ..., video_emoji_markup: Optional[aliases.AnyVideoSize] = ...): ...

    def __init__(self, _='photos.uploadProfilePhoto', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def fallback(self) -> Optional[bool]:
        return self['fallback']

    @property
    def bot(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['bot'])

    @property
    def file(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['file'])

    @property
    def video(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['video'])

    @property
    def video_start_ts(self) -> Optional[float]:
        return self['video_start_ts']

    @property
    def video_emoji_markup(self) -> Optional[aliases.AnyVideoSize]:
        return build_object(self['video_emoji_markup'])


class PhotosDeletePhotos(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputPhoto]): ...

    def __init__(self, id, _='photos.deletePhotos', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputPhoto]:
        return build_object(self['id'])


class PhotosGetUserPhotos(TLMethod[aliases.AnyPhotosPhotos]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, offset: int, max_id: int, limit: int): ...

    def __init__(self, user_id, offset, max_id, limit, _='photos.getUserPhotos', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['offset'] = offset
        kwargs['max_id'] = max_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def limit(self) -> int:
        return self['limit']


class PhotosUploadContactProfilePhoto(TLMethod[aliases.AnyPhotosPhoto]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, suggest: Optional[bool] = ..., save: Optional[bool] = ..., file: Optional[aliases.AnyInputFile] = ..., video: Optional[aliases.AnyInputFile] = ..., video_start_ts: Optional[float] = ..., video_emoji_markup: Optional[aliases.AnyVideoSize] = ...): ...

    def __init__(self, user_id, _='photos.uploadContactProfilePhoto', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def suggest(self) -> Optional[bool]:
        return self['suggest']

    @property
    def save(self) -> Optional[bool]:
        return self['save']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def file(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['file'])

    @property
    def video(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['video'])

    @property
    def video_start_ts(self) -> Optional[float]:
        return self['video_start_ts']

    @property
    def video_emoji_markup(self) -> Optional[aliases.AnyVideoSize]:
        return build_object(self['video_emoji_markup'])
