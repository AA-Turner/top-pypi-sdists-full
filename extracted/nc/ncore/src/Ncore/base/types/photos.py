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


class PhotosPhotos(dict):
    __slots__ = ()

    @overload
    def __init__(self, photos: list[aliases.AnyPhoto], users: list[aliases.AnyUser]): ...

    def __init__(self, photos, users, _='photos.photos', **kwargs):
        kwargs['photos'] = photos
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photos(self) -> list[aliases.AnyPhoto]:
        return build_object(self['photos'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PhotosPhotosSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, photos: list[aliases.AnyPhoto], users: list[aliases.AnyUser]): ...

    def __init__(self, count, photos, users, _='photos.photosSlice', **kwargs):
        kwargs['count'] = count
        kwargs['photos'] = photos
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def photos(self) -> list[aliases.AnyPhoto]:
        return build_object(self['photos'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PhotosPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo: aliases.AnyPhoto, users: list[aliases.AnyUser]): ...

    def __init__(self, photo, users, _='photos.photo', **kwargs):
        kwargs['photo'] = photo
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
