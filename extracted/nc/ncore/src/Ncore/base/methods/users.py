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

class UsersGetUsers(TLMethod[list[aliases.AnyUser]]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputUser]): ...

    def __init__(self, id, _='users.getUsers', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputUser]:
        return build_object(self['id'])


class UsersGetFullUser(TLMethod[aliases.AnyUsersUserFull]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser): ...

    def __init__(self, id, _='users.getFullUser', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])


class UsersSetSecureValueErrors(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, errors: list[aliases.AnySecureValueError]): ...

    def __init__(self, id, errors, _='users.setSecureValueErrors', **kwargs):
        kwargs['id'] = id
        kwargs['errors'] = errors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def errors(self) -> list[aliases.AnySecureValueError]:
        return build_object(self['errors'])


class UsersGetRequirementsToContact(TLMethod[list[aliases.AnyRequirementToContact]]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputUser]): ...

    def __init__(self, id, _='users.getRequirementsToContact', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputUser]:
        return build_object(self['id'])


class UsersGetSavedMusic(TLMethod[aliases.AnyUsersSavedMusic]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, offset: int, limit: int, hash: int): ...

    def __init__(self, id, offset, limit, hash, _='users.getSavedMusic', **kwargs):
        kwargs['id'] = id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class UsersGetSavedMusicByID(TLMethod[aliases.AnyUsersSavedMusic]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, documents: list[aliases.AnyInputDocument]): ...

    def __init__(self, id, documents, _='users.getSavedMusicByID', **kwargs):
        kwargs['id'] = id
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def documents(self) -> list[aliases.AnyInputDocument]:
        return build_object(self['documents'])


class UsersSuggestBirthday(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, birthday: aliases.AnyBirthday): ...

    def __init__(self, id, birthday, _='users.suggestBirthday', **kwargs):
        kwargs['id'] = id
        kwargs['birthday'] = birthday
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def birthday(self) -> aliases.AnyBirthday:
        return build_object(self['birthday'])
