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


class ChannelsChannelParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, participants: list[aliases.AnyChannelParticipant], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, count, participants, chats, users, _='channels.channelParticipants', **kwargs):
        kwargs['count'] = count
        kwargs['participants'] = participants
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def participants(self) -> list[aliases.AnyChannelParticipant]:
        return build_object(self['participants'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChannelsChannelParticipantsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channels.channelParticipantsNotModified'):
        dict.__init__(self, _=_)


class ChannelsChannelParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, participant: aliases.AnyChannelParticipant, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, participant, chats, users, _='channels.channelParticipant', **kwargs):
        kwargs['participant'] = participant
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['participant'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChannelsAdminLogResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, events: list[aliases.AnyChannelAdminLogEvent], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, events, chats, users, _='channels.adminLogResults', **kwargs):
        kwargs['events'] = events
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def events(self) -> list[aliases.AnyChannelAdminLogEvent]:
        return build_object(self['events'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChannelsSendAsPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, peers: list[aliases.AnySendAsPeer], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, peers, chats, users, _='channels.sendAsPeers', **kwargs):
        kwargs['peers'] = peers
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peers(self) -> list[aliases.AnySendAsPeer]:
        return build_object(self['peers'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class ChannelsSponsoredMessageReportResultChooseOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, options: list[aliases.AnySponsoredMessageReportOption]): ...

    def __init__(self, title, options, _='channels.sponsoredMessageReportResultChooseOption', **kwargs):
        kwargs['title'] = title
        kwargs['options'] = options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def options(self) -> list[aliases.AnySponsoredMessageReportOption]:
        return build_object(self['options'])


class ChannelsSponsoredMessageReportResultAdsHidden(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channels.sponsoredMessageReportResultAdsHidden'):
        dict.__init__(self, _=_)


class ChannelsSponsoredMessageReportResultReported(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channels.sponsoredMessageReportResultReported'):
        dict.__init__(self, _=_)
