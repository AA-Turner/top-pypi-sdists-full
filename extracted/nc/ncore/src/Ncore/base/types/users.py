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


class UsersUserFull(dict):
    __slots__ = ()

    @overload
    def __init__(self, full_user: aliases.AnyUserFull, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, full_user, chats, users, _='users.userFull', **kwargs):
        kwargs['full_user'] = full_user
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def full_user(self) -> aliases.AnyUserFull:
        return build_object(self['full_user'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class UsersUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyUser]): ...

    def __init__(self, users, _='users.users', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class UsersUsersSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, users: list[aliases.AnyUser]): ...

    def __init__(self, count, users, _='users.usersSlice', **kwargs):
        kwargs['count'] = count
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class UsersSavedMusicNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int): ...

    def __init__(self, count, _='users.savedMusicNotModified', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']


class UsersSavedMusic(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, documents: list[aliases.AnyDocument]): ...

    def __init__(self, count, documents, _='users.savedMusic', **kwargs):
        kwargs['count'] = count
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def documents(self) -> list[aliases.AnyDocument]:
        return build_object(self['documents'])
