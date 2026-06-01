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


class UpdatesState(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, qts: int, date: int, seq: int, unread_count: int): ...

    def __init__(self, pts, qts, date, seq, unread_count, _='updates.state', **kwargs):
        kwargs['pts'] = pts
        kwargs['qts'] = qts
        kwargs['date'] = date
        kwargs['seq'] = seq
        kwargs['unread_count'] = unread_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def qts(self) -> int:
        return self['qts']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def seq(self) -> int:
        return self['seq']

    @property
    def unread_count(self) -> int:
        return self['unread_count']


class UpdatesDifferenceEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, seq: int): ...

    def __init__(self, date, seq, _='updates.differenceEmpty', **kwargs):
        kwargs['date'] = date
        kwargs['seq'] = seq
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def seq(self) -> int:
        return self['seq']


class UpdatesDifference(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_messages: list[aliases.AnyMessage], new_encrypted_messages: list[aliases.AnyEncryptedMessage], other_updates: list[aliases.AnyUpdate], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], state: aliases.AnyUpdatesState): ...

    def __init__(self, new_messages, new_encrypted_messages, other_updates, chats, users, state, _='updates.difference', **kwargs):
        kwargs['new_messages'] = new_messages
        kwargs['new_encrypted_messages'] = new_encrypted_messages
        kwargs['other_updates'] = other_updates
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['state'] = state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['new_messages'])

    @property
    def new_encrypted_messages(self) -> list[aliases.AnyEncryptedMessage]:
        return build_object(self['new_encrypted_messages'])

    @property
    def other_updates(self) -> list[aliases.AnyUpdate]:
        return build_object(self['other_updates'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def state(self) -> aliases.AnyUpdatesState:
        return build_object(self['state'])


class UpdatesDifferenceSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_messages: list[aliases.AnyMessage], new_encrypted_messages: list[aliases.AnyEncryptedMessage], other_updates: list[aliases.AnyUpdate], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], intermediate_state: aliases.AnyUpdatesState): ...

    def __init__(self, new_messages, new_encrypted_messages, other_updates, chats, users, intermediate_state, _='updates.differenceSlice', **kwargs):
        kwargs['new_messages'] = new_messages
        kwargs['new_encrypted_messages'] = new_encrypted_messages
        kwargs['other_updates'] = other_updates
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['intermediate_state'] = intermediate_state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['new_messages'])

    @property
    def new_encrypted_messages(self) -> list[aliases.AnyEncryptedMessage]:
        return build_object(self['new_encrypted_messages'])

    @property
    def other_updates(self) -> list[aliases.AnyUpdate]:
        return build_object(self['other_updates'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def intermediate_state(self) -> aliases.AnyUpdatesState:
        return build_object(self['intermediate_state'])


class UpdatesDifferenceTooLong(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int): ...

    def __init__(self, pts, _='updates.differenceTooLong', **kwargs):
        kwargs['pts'] = pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']


class UpdatesChannelDifferenceEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, final: Optional[bool] = ..., timeout: Optional[int] = ...): ...

    def __init__(self, pts, _='updates.channelDifferenceEmpty', **kwargs):
        kwargs['pts'] = pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def final(self) -> Optional[bool]:
        return self['final']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def timeout(self) -> Optional[int]:
        return self['timeout']


class UpdatesChannelDifferenceTooLong(dict):
    __slots__ = ()

    @overload
    def __init__(self, dialog: aliases.AnyDialog, messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], final: Optional[bool] = ..., timeout: Optional[int] = ...): ...

    def __init__(self, dialog, messages, chats, users, _='updates.channelDifferenceTooLong', **kwargs):
        kwargs['dialog'] = dialog
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def final(self) -> Optional[bool]:
        return self['final']

    @property
    def timeout(self) -> Optional[int]:
        return self['timeout']

    @property
    def dialog(self) -> aliases.AnyDialog:
        return build_object(self['dialog'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class UpdatesChannelDifference(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, new_messages: list[aliases.AnyMessage], other_updates: list[aliases.AnyUpdate], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], final: Optional[bool] = ..., timeout: Optional[int] = ...): ...

    def __init__(self, pts, new_messages, other_updates, chats, users, _='updates.channelDifference', **kwargs):
        kwargs['pts'] = pts
        kwargs['new_messages'] = new_messages
        kwargs['other_updates'] = other_updates
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def final(self) -> Optional[bool]:
        return self['final']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def timeout(self) -> Optional[int]:
        return self['timeout']

    @property
    def new_messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['new_messages'])

    @property
    def other_updates(self) -> list[aliases.AnyUpdate]:
        return build_object(self['other_updates'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
