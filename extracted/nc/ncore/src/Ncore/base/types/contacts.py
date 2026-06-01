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


class ContactsContactsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.contactsNotModified'):
        dict.__init__(self, _=_)


class ContactsContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self, contacts: list[aliases.AnyContact], saved_count: int, users: list[aliases.AnyUser]): ...

    def __init__(self, contacts, saved_count, users, _='contacts.contacts', **kwargs):
        kwargs['contacts'] = contacts
        kwargs['saved_count'] = saved_count
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contacts(self) -> list[aliases.AnyContact]:
        return build_object(self['contacts'])

    @property
    def saved_count(self) -> int:
        return self['saved_count']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsImportedContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self, imported: list[aliases.AnyImportedContact], popular_invites: list[aliases.AnyPopularContact], retry_contacts: list[int], users: list[aliases.AnyUser]): ...

    def __init__(self, imported, popular_invites, retry_contacts, users, _='contacts.importedContacts', **kwargs):
        kwargs['imported'] = imported
        kwargs['popular_invites'] = popular_invites
        kwargs['retry_contacts'] = retry_contacts
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def imported(self) -> list[aliases.AnyImportedContact]:
        return build_object(self['imported'])

    @property
    def popular_invites(self) -> list[aliases.AnyPopularContact]:
        return build_object(self['popular_invites'])

    @property
    def retry_contacts(self) -> list[int]:
        return self['retry_contacts']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsBlocked(dict):
    __slots__ = ()

    @overload
    def __init__(self, blocked: list[aliases.AnyPeerBlocked], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, blocked, chats, users, _='contacts.blocked', **kwargs):
        kwargs['blocked'] = blocked
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> list[aliases.AnyPeerBlocked]:
        return build_object(self['blocked'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsBlockedSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, blocked: list[aliases.AnyPeerBlocked], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, count, blocked, chats, users, _='contacts.blockedSlice', **kwargs):
        kwargs['count'] = count
        kwargs['blocked'] = blocked
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def blocked(self) -> list[aliases.AnyPeerBlocked]:
        return build_object(self['blocked'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsFound(dict):
    __slots__ = ()

    @overload
    def __init__(self, my_results: list[aliases.AnyPeer], results: list[aliases.AnyPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, my_results, results, chats, users, _='contacts.found', **kwargs):
        kwargs['my_results'] = my_results
        kwargs['results'] = results
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_results(self) -> list[aliases.AnyPeer]:
        return build_object(self['my_results'])

    @property
    def results(self) -> list[aliases.AnyPeer]:
        return build_object(self['results'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsResolvedPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, peer, chats, users, _='contacts.resolvedPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsTopPeersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.topPeersNotModified'):
        dict.__init__(self, _=_)


class ContactsTopPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, categories: list[aliases.AnyTopPeerCategoryPeers], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, categories, chats, users, _='contacts.topPeers', **kwargs):
        kwargs['categories'] = categories
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def categories(self) -> list[aliases.AnyTopPeerCategoryPeers]:
        return build_object(self['categories'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsTopPeersDisabled(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.topPeersDisabled'):
        dict.__init__(self, _=_)


class ContactsContactBirthdays(dict):
    __slots__ = ()

    @overload
    def __init__(self, contacts: list[aliases.AnyContactBirthday], users: list[aliases.AnyUser]): ...

    def __init__(self, contacts, users, _='contacts.contactBirthdays', **kwargs):
        kwargs['contacts'] = contacts
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contacts(self) -> list[aliases.AnyContactBirthday]:
        return build_object(self['contacts'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ContactsSponsoredPeersEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.sponsoredPeersEmpty'):
        dict.__init__(self, _=_)


class ContactsSponsoredPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, peers: list[aliases.AnySponsoredPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, peers, chats, users, _='contacts.sponsoredPeers', **kwargs):
        kwargs['peers'] = peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peers(self) -> list[aliases.AnySponsoredPeer]:
        return build_object(self['peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
