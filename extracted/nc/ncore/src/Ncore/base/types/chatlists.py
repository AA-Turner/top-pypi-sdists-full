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


class ChatlistsExportedChatlistInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, filter: aliases.AnyDialogFilter, invite: aliases.AnyExportedChatlistInvite): ...

    def __init__(self, filter, invite, _='chatlists.exportedChatlistInvite', **kwargs):
        kwargs['filter'] = filter
        kwargs['invite'] = invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def filter(self) -> aliases.AnyDialogFilter:
        return build_object(self['filter'])

    @property
    def invite(self) -> aliases.AnyExportedChatlistInvite:
        return build_object(self['invite'])


class ChatlistsExportedInvites(dict):
    __slots__ = ()

    @overload
    def __init__(self, invites: list[aliases.AnyExportedChatlistInvite], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, invites, chats, users, _='chatlists.exportedInvites', **kwargs):
        kwargs['invites'] = invites
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invites(self) -> list[aliases.AnyExportedChatlistInvite]:
        return build_object(self['invites'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChatlistsChatlistInviteAlready(dict):
    __slots__ = ()

    @overload
    def __init__(self, filter_id: int, missing_peers: list[aliases.AnyPeer], already_peers: list[aliases.AnyPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, filter_id, missing_peers, already_peers, chats, users, _='chatlists.chatlistInviteAlready', **kwargs):
        kwargs['filter_id'] = filter_id
        kwargs['missing_peers'] = missing_peers
        kwargs['already_peers'] = already_peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def filter_id(self) -> int:
        return self['filter_id']

    @property
    def missing_peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['missing_peers'])

    @property
    def already_peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['already_peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChatlistsChatlistInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: aliases.AnyTextWithEntities, peers: list[aliases.AnyPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], title_noanimate: Optional[bool] = ..., emoticon: Optional[str] = ...): ...

    def __init__(self, title, peers, chats, users, _='chatlists.chatlistInvite', **kwargs):
        kwargs['title'] = title
        kwargs['peers'] = peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title_noanimate(self) -> Optional[bool]:
        return self['title_noanimate']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])

    @property
    def emoticon(self) -> Optional[str]:
        return self['emoticon']

    @property
    def peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChatlistsChatlistUpdates(dict):
    __slots__ = ()

    @overload
    def __init__(self, missing_peers: list[aliases.AnyPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, missing_peers, chats, users, _='chatlists.chatlistUpdates', **kwargs):
        kwargs['missing_peers'] = missing_peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def missing_peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['missing_peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
