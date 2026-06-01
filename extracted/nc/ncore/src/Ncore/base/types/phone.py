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


class PhonePhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_call: aliases.AnyPhoneCall, users: list[aliases.AnyUser]): ...

    def __init__(self, phone_call, users, _='phone.phoneCall', **kwargs):
        kwargs['phone_call'] = phone_call
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_call(self) -> aliases.AnyPhoneCall:
        return build_object(self['phone_call'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PhoneGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyGroupCall, participants: list[aliases.AnyGroupCallParticipant], participants_next_offset: str, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, call, participants, participants_next_offset, chats, users, _='phone.groupCall', **kwargs):
        kwargs['call'] = call
        kwargs['participants'] = participants
        kwargs['participants_next_offset'] = participants_next_offset
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyGroupCall:
        return build_object(self['call'])

    @property
    def participants(self) -> list[aliases.AnyGroupCallParticipant]:
        return build_object(self['participants'])

    @property
    def participants_next_offset(self) -> str:
        return self['participants_next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PhoneGroupParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, participants: list[aliases.AnyGroupCallParticipant], next_offset: str, chats: list[aliases.AnyChat], users: list[aliases.AnyUser], version: int): ...

    def __init__(self, count, participants, next_offset, chats, users, version, _='phone.groupParticipants', **kwargs):
        kwargs['count'] = count
        kwargs['participants'] = participants
        kwargs['next_offset'] = next_offset
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def participants(self) -> list[aliases.AnyGroupCallParticipant]:
        return build_object(self['participants'])

    @property
    def next_offset(self) -> str:
        return self['next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def version(self) -> int:
        return self['version']


class PhoneJoinAsPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, peers: list[aliases.AnyPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, peers, chats, users, _='phone.joinAsPeers', **kwargs):
        kwargs['peers'] = peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PhoneExportedGroupCallInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, link: str): ...

    def __init__(self, link, _='phone.exportedGroupCallInvite', **kwargs):
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def link(self) -> str:
        return self['link']


class PhoneGroupCallStreamChannels(dict):
    __slots__ = ()

    @overload
    def __init__(self, channels: list[aliases.AnyGroupCallStreamChannel]): ...

    def __init__(self, channels, _='phone.groupCallStreamChannels', **kwargs):
        kwargs['channels'] = channels
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channels(self) -> list[aliases.AnyGroupCallStreamChannel]:
        return build_object(self['channels'])


class PhoneGroupCallStreamRtmpUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, key: str): ...

    def __init__(self, url, key, _='phone.groupCallStreamRtmpUrl', **kwargs):
        kwargs['url'] = url
        kwargs['key'] = key
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def key(self) -> str:
        return self['key']


class PhoneGroupCallStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, total_stars: int, top_donors: list[aliases.AnyGroupCallDonor], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, total_stars, top_donors, chats, users, _='phone.groupCallStars', **kwargs):
        kwargs['total_stars'] = total_stars
        kwargs['top_donors'] = top_donors
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def total_stars(self) -> int:
        return self['total_stars']

    @property
    def top_donors(self) -> list[aliases.AnyGroupCallDonor]:
        return build_object(self['top_donors'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
