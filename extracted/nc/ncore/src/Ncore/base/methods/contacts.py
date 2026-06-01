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

class ContactsGetContactIDs(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='contacts.getContactIDs', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class ContactsGetStatuses(TLMethod[list[aliases.AnyContactStatus]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.getStatuses'):
        dict.__init__(self, _=_)


class ContactsGetContacts(TLMethod[aliases.AnyContactsContacts]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='contacts.getContacts', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class ContactsImportContacts(TLMethod[aliases.AnyContactsImportedContacts]):
    __slots__ = ()

    @overload
    def __init__(self, contacts: list[aliases.AnyInputContact]): ...

    def __init__(self, contacts, _='contacts.importContacts', **kwargs):
        kwargs['contacts'] = contacts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contacts(self) -> list[aliases.AnyInputContact]:
        return build_object(self['contacts'])


class ContactsDeleteContacts(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputUser]): ...

    def __init__(self, id, _='contacts.deleteContacts', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputUser]:
        return build_object(self['id'])


class ContactsDeleteByPhones(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phones: list[str]): ...

    def __init__(self, phones, _='contacts.deleteByPhones', **kwargs):
        kwargs['phones'] = phones
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phones(self) -> list[str]:
        return self['phones']


class ContactsBlock(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPeer, my_stories_from: Optional[bool] = ...): ...

    def __init__(self, id, _='contacts.block', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_stories_from(self) -> Optional[bool]:
        return self['my_stories_from']

    @property
    def id(self) -> aliases.AnyInputPeer:
        return build_object(self['id'])


class ContactsUnblock(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPeer, my_stories_from: Optional[bool] = ...): ...

    def __init__(self, id, _='contacts.unblock', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_stories_from(self) -> Optional[bool]:
        return self['my_stories_from']

    @property
    def id(self) -> aliases.AnyInputPeer:
        return build_object(self['id'])


class ContactsGetBlocked(TLMethod[aliases.AnyContactsBlocked]):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, limit: int, my_stories_from: Optional[bool] = ...): ...

    def __init__(self, offset, limit, _='contacts.getBlocked', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_stories_from(self) -> Optional[bool]:
        return self['my_stories_from']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class ContactsSearch(TLMethod[aliases.AnyContactsFound]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, limit: int): ...

    def __init__(self, q, limit, _='contacts.search', **kwargs):
        kwargs['q'] = q
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']

    @property
    def limit(self) -> int:
        return self['limit']


class ContactsResolveUsername(TLMethod[aliases.AnyContactsResolvedPeer]):
    __slots__ = ()

    @overload
    def __init__(self, username: str, referer: Optional[str] = ...): ...

    def __init__(self, username, _='contacts.resolveUsername', **kwargs):
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def username(self) -> str:
        return self['username']

    @property
    def referer(self) -> Optional[str]:
        return self['referer']


class ContactsGetTopPeers(TLMethod[aliases.AnyContactsTopPeers]):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, limit: int, hash: int, correspondents: Optional[bool] = ..., bots_pm: Optional[bool] = ..., bots_inline: Optional[bool] = ..., phone_calls: Optional[bool] = ..., forward_users: Optional[bool] = ..., forward_chats: Optional[bool] = ..., groups: Optional[bool] = ..., channels: Optional[bool] = ..., bots_app: Optional[bool] = ...): ...

    def __init__(self, offset, limit, hash, _='contacts.getTopPeers', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def correspondents(self) -> Optional[bool]:
        return self['correspondents']

    @property
    def bots_pm(self) -> Optional[bool]:
        return self['bots_pm']

    @property
    def bots_inline(self) -> Optional[bool]:
        return self['bots_inline']

    @property
    def phone_calls(self) -> Optional[bool]:
        return self['phone_calls']

    @property
    def forward_users(self) -> Optional[bool]:
        return self['forward_users']

    @property
    def forward_chats(self) -> Optional[bool]:
        return self['forward_chats']

    @property
    def groups(self) -> Optional[bool]:
        return self['groups']

    @property
    def channels(self) -> Optional[bool]:
        return self['channels']

    @property
    def bots_app(self) -> Optional[bool]:
        return self['bots_app']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class ContactsResetTopPeerRating(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, category: aliases.AnyTopPeerCategory, peer: aliases.AnyInputPeer): ...

    def __init__(self, category, peer, _='contacts.resetTopPeerRating', **kwargs):
        kwargs['category'] = category
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def category(self) -> aliases.AnyTopPeerCategory:
        return build_object(self['category'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class ContactsResetSaved(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.resetSaved'):
        dict.__init__(self, _=_)


class ContactsGetSaved(TLMethod[list[aliases.AnySavedContact]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.getSaved'):
        dict.__init__(self, _=_)


class ContactsToggleTopPeers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, enabled: bool): ...

    def __init__(self, enabled, _='contacts.toggleTopPeers', **kwargs):
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ContactsAddContact(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, first_name: str, last_name: str, phone: str, add_phone_privacy_exception: Optional[bool] = ..., note: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, id, first_name, last_name, phone, _='contacts.addContact', **kwargs):
        kwargs['id'] = id
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def add_phone_privacy_exception(self) -> Optional[bool]:
        return self['add_phone_privacy_exception']

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def phone(self) -> str:
        return self['phone']

    @property
    def note(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['note'])


class ContactsAcceptContact(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser): ...

    def __init__(self, id, _='contacts.acceptContact', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])


class ContactsGetLocated(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, background: Optional[bool] = ..., self_expires: Optional[int] = ...): ...

    def __init__(self, geo_point, _='contacts.getLocated', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def self_expires(self) -> Optional[int]:
        return self['self_expires']


class ContactsBlockFromReplies(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int, delete_message: Optional[bool] = ..., delete_history: Optional[bool] = ..., report_spam: Optional[bool] = ...): ...

    def __init__(self, msg_id, _='contacts.blockFromReplies', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def delete_message(self) -> Optional[bool]:
        return self['delete_message']

    @property
    def delete_history(self) -> Optional[bool]:
        return self['delete_history']

    @property
    def report_spam(self) -> Optional[bool]:
        return self['report_spam']

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class ContactsResolvePhone(TLMethod[aliases.AnyContactsResolvedPeer]):
    __slots__ = ()

    @overload
    def __init__(self, phone: str): ...

    def __init__(self, phone, _='contacts.resolvePhone', **kwargs):
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone(self) -> str:
        return self['phone']


class ContactsExportContactToken(TLMethod[aliases.AnyExportedContactToken]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.exportContactToken'):
        dict.__init__(self, _=_)


class ContactsImportContactToken(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, token: str): ...

    def __init__(self, token, _='contacts.importContactToken', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']


class ContactsEditCloseFriends(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[int]): ...

    def __init__(self, id, _='contacts.editCloseFriends', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[int]:
        return self['id']


class ContactsSetBlocked(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputPeer], limit: int, my_stories_from: Optional[bool] = ...): ...

    def __init__(self, id, limit, _='contacts.setBlocked', **kwargs):
        kwargs['id'] = id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_stories_from(self) -> Optional[bool]:
        return self['my_stories_from']

    @property
    def id(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['id'])

    @property
    def limit(self) -> int:
        return self['limit']


class ContactsGetBirthdays(TLMethod[aliases.AnyContactsContactBirthdays]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='contacts.getBirthdays'):
        dict.__init__(self, _=_)


class ContactsGetSponsoredPeers(TLMethod[aliases.AnyContactsSponsoredPeers]):
    __slots__ = ()

    @overload
    def __init__(self, q: str): ...

    def __init__(self, q, _='contacts.getSponsoredPeers', **kwargs):
        kwargs['q'] = q
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']


class ContactsUpdateContactNote(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputUser, note: aliases.AnyTextWithEntities): ...

    def __init__(self, id, note, _='contacts.updateContactNote', **kwargs):
        kwargs['id'] = id
        kwargs['note'] = note
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputUser:
        return build_object(self['id'])

    @property
    def note(self) -> aliases.AnyTextWithEntities:
        return build_object(self['note'])
