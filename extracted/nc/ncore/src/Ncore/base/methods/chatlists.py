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

class ChatlistsExportChatlistInvite(TLMethod[aliases.AnyChatlistsExportedChatlistInvite]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist, title: str, peers: list[aliases.AnyInputPeer]): ...

    def __init__(self, chatlist, title, peers, _='chatlists.exportChatlistInvite', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['title'] = title
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['peers'])


class ChatlistsDeleteExportedInvite(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist, slug: str): ...

    def __init__(self, chatlist, slug, _='chatlists.deleteExportedInvite', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])

    @property
    def slug(self) -> str:
        return self['slug']


class ChatlistsEditExportedInvite(TLMethod[aliases.AnyExportedChatlistInvite]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist, slug: str, title: Optional[str] = ..., peers: Optional[list[aliases.AnyInputPeer]] = ...): ...

    def __init__(self, chatlist, slug, _='chatlists.editExportedInvite', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def peers(self) -> Optional[list[aliases.AnyInputPeer]]:
        return build_object(self['peers'])


class ChatlistsGetExportedInvites(TLMethod[aliases.AnyChatlistsExportedInvites]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist): ...

    def __init__(self, chatlist, _='chatlists.getExportedInvites', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])


class ChatlistsCheckChatlistInvite(TLMethod[aliases.AnyChatlistsChatlistInvite]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='chatlists.checkChatlistInvite', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class ChatlistsJoinChatlistInvite(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str, peers: list[aliases.AnyInputPeer]): ...

    def __init__(self, slug, peers, _='chatlists.joinChatlistInvite', **kwargs):
        kwargs['slug'] = slug
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['peers'])


class ChatlistsGetChatlistUpdates(TLMethod[aliases.AnyChatlistsChatlistUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist): ...

    def __init__(self, chatlist, _='chatlists.getChatlistUpdates', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])


class ChatlistsJoinChatlistUpdates(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist, peers: list[aliases.AnyInputPeer]): ...

    def __init__(self, chatlist, peers, _='chatlists.joinChatlistUpdates', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])

    @property
    def peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['peers'])


class ChatlistsHideChatlistUpdates(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist): ...

    def __init__(self, chatlist, _='chatlists.hideChatlistUpdates', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])


class ChatlistsGetLeaveChatlistSuggestions(TLMethod[list[aliases.AnyPeer]]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist): ...

    def __init__(self, chatlist, _='chatlists.getLeaveChatlistSuggestions', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])


class ChatlistsLeaveChatlist(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chatlist: aliases.AnyInputChatlist, peers: list[aliases.AnyInputPeer]): ...

    def __init__(self, chatlist, peers, _='chatlists.leaveChatlist', **kwargs):
        kwargs['chatlist'] = chatlist
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chatlist(self) -> aliases.AnyInputChatlist:
        return build_object(self['chatlist'])

    @property
    def peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['peers'])
