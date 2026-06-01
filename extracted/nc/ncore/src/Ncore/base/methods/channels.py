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

class ChannelsReadHistory(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, max_id: int): ...

    def __init__(self, channel, max_id, _='channels.readHistory', **kwargs):
        kwargs['channel'] = channel
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def max_id(self) -> int:
        return self['max_id']


class ChannelsDeleteMessages(TLMethod[aliases.AnyMessagesAffectedMessages]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, id: list[int]): ...

    def __init__(self, channel, id, _='channels.deleteMessages', **kwargs):
        kwargs['channel'] = channel
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def id(self) -> list[int]:
        return self['id']


class ChannelsReportSpam(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, participant: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, channel, participant, id, _='channels.reportSpam', **kwargs):
        kwargs['channel'] = channel
        kwargs['participant'] = participant
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])

    @property
    def id(self) -> list[int]:
        return self['id']


class ChannelsGetMessages(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, id: list[aliases.AnyInputMessage]): ...

    def __init__(self, channel, id, _='channels.getMessages', **kwargs):
        kwargs['channel'] = channel
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def id(self) -> list[aliases.AnyInputMessage]:
        return build_object(self['id'])


class ChannelsGetParticipants(TLMethod[aliases.AnyChannelsChannelParticipants]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, filter: aliases.AnyChannelParticipantsFilter, offset: int, limit: int, hash: int): ...

    def __init__(self, channel, filter, offset, limit, hash, _='channels.getParticipants', **kwargs):
        kwargs['channel'] = channel
        kwargs['filter'] = filter
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def filter(self) -> aliases.AnyChannelParticipantsFilter:
        return build_object(self['filter'])

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class ChannelsGetParticipant(TLMethod[aliases.AnyChannelsChannelParticipant]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, participant: aliases.AnyInputPeer): ...

    def __init__(self, channel, participant, _='channels.getParticipant', **kwargs):
        kwargs['channel'] = channel
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])


class ChannelsGetChannels(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputChannel]): ...

    def __init__(self, id, _='channels.getChannels', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputChannel]:
        return build_object(self['id'])


class ChannelsGetFullChannel(TLMethod[aliases.AnyMessagesChatFull]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.getFullChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsCreateChannel(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, title: str, about: str, broadcast: Optional[bool] = ..., megagroup: Optional[bool] = ..., for_import: Optional[bool] = ..., forum: Optional[bool] = ..., geo_point: Optional[aliases.AnyInputGeoPoint] = ..., address: Optional[str] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, title, about, _='channels.createChannel', **kwargs):
        kwargs['title'] = title
        kwargs['about'] = about
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcast(self) -> Optional[bool]:
        return self['broadcast']

    @property
    def megagroup(self) -> Optional[bool]:
        return self['megagroup']

    @property
    def for_import(self) -> Optional[bool]:
        return self['for_import']

    @property
    def forum(self) -> Optional[bool]:
        return self['forum']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def about(self) -> str:
        return self['about']

    @property
    def geo_point(self) -> Optional[aliases.AnyInputGeoPoint]:
        return build_object(self['geo_point'])

    @property
    def address(self) -> Optional[str]:
        return self['address']

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class ChannelsEditAdmin(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, user_id: aliases.AnyInputUser, admin_rights: aliases.AnyChatAdminRights, rank: Optional[str] = ...): ...

    def __init__(self, channel, user_id, admin_rights, _='channels.editAdmin', **kwargs):
        kwargs['channel'] = channel
        kwargs['user_id'] = user_id
        kwargs['admin_rights'] = admin_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def admin_rights(self) -> aliases.AnyChatAdminRights:
        return build_object(self['admin_rights'])

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelsEditTitle(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, title: str): ...

    def __init__(self, channel, title, _='channels.editTitle', **kwargs):
        kwargs['channel'] = channel
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def title(self) -> str:
        return self['title']


class ChannelsEditPhoto(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, photo: aliases.AnyInputChatPhoto): ...

    def __init__(self, channel, photo, _='channels.editPhoto', **kwargs):
        kwargs['channel'] = channel
        kwargs['photo'] = photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def photo(self) -> aliases.AnyInputChatPhoto:
        return build_object(self['photo'])


class ChannelsCheckUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, username: str): ...

    def __init__(self, channel, username, _='channels.checkUsername', **kwargs):
        kwargs['channel'] = channel
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def username(self) -> str:
        return self['username']


class ChannelsUpdateUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, username: str): ...

    def __init__(self, channel, username, _='channels.updateUsername', **kwargs):
        kwargs['channel'] = channel
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def username(self) -> str:
        return self['username']


class ChannelsJoinChannel(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.joinChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsLeaveChannel(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.leaveChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsInviteToChannel(TLMethod[aliases.AnyMessagesInvitedUsers]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, users: list[aliases.AnyInputUser]): ...

    def __init__(self, channel, users, _='channels.inviteToChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])


class ChannelsDeleteChannel(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.deleteChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsExportMessageLink(TLMethod[aliases.AnyExportedMessageLink]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, id: int, grouped: Optional[bool] = ..., thread: Optional[bool] = ...): ...

    def __init__(self, channel, id, _='channels.exportMessageLink', **kwargs):
        kwargs['channel'] = channel
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def grouped(self) -> Optional[bool]:
        return self['grouped']

    @property
    def thread(self) -> Optional[bool]:
        return self['thread']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def id(self) -> int:
        return self['id']


class ChannelsToggleSignatures(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, signatures_enabled: Optional[bool] = ..., profiles_enabled: Optional[bool] = ...): ...

    def __init__(self, channel, _='channels.toggleSignatures', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def signatures_enabled(self) -> Optional[bool]:
        return self['signatures_enabled']

    @property
    def profiles_enabled(self) -> Optional[bool]:
        return self['profiles_enabled']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsGetAdminedPublicChannels(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, by_location: Optional[bool] = ..., check_limit: Optional[bool] = ..., for_personal: Optional[bool] = ...): ...

    def __init__(self, _='channels.getAdminedPublicChannels', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def by_location(self) -> Optional[bool]:
        return self['by_location']

    @property
    def check_limit(self) -> Optional[bool]:
        return self['check_limit']

    @property
    def for_personal(self) -> Optional[bool]:
        return self['for_personal']


class ChannelsEditBanned(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, participant: aliases.AnyInputPeer, banned_rights: aliases.AnyChatBannedRights): ...

    def __init__(self, channel, participant, banned_rights, _='channels.editBanned', **kwargs):
        kwargs['channel'] = channel
        kwargs['participant'] = participant
        kwargs['banned_rights'] = banned_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])

    @property
    def banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['banned_rights'])


class ChannelsGetAdminLog(TLMethod[aliases.AnyChannelsAdminLogResults]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, q: str, max_id: int, min_id: int, limit: int, events_filter: Optional[aliases.AnyChannelAdminLogEventsFilter] = ..., admins: Optional[list[aliases.AnyInputUser]] = ...): ...

    def __init__(self, channel, q, max_id, min_id, limit, _='channels.getAdminLog', **kwargs):
        kwargs['channel'] = channel
        kwargs['q'] = q
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def q(self) -> str:
        return self['q']

    @property
    def events_filter(self) -> Optional[aliases.AnyChannelAdminLogEventsFilter]:
        return build_object(self['events_filter'])

    @property
    def admins(self) -> Optional[list[aliases.AnyInputUser]]:
        return build_object(self['admins'])

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def limit(self) -> int:
        return self['limit']


class ChannelsSetStickers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, channel, stickerset, _='channels.setStickers', **kwargs):
        kwargs['channel'] = channel
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])


class ChannelsReadMessageContents(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, id: list[int]): ...

    def __init__(self, channel, id, _='channels.readMessageContents', **kwargs):
        kwargs['channel'] = channel
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def id(self) -> list[int]:
        return self['id']


class ChannelsDeleteHistory(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, max_id: int, for_everyone: Optional[bool] = ...): ...

    def __init__(self, channel, max_id, _='channels.deleteHistory', **kwargs):
        kwargs['channel'] = channel
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_everyone(self) -> Optional[bool]:
        return self['for_everyone']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def max_id(self) -> int:
        return self['max_id']


class ChannelsTogglePreHistoryHidden(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.togglePreHistoryHidden', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsGetLeftChannels(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, offset: int): ...

    def __init__(self, offset, _='channels.getLeftChannels', **kwargs):
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']


class ChannelsGetGroupsForDiscussion(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channels.getGroupsForDiscussion'):
        dict.__init__(self, _=_)


class ChannelsSetDiscussionGroup(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, broadcast: aliases.AnyInputChannel, group: aliases.AnyInputChannel): ...

    def __init__(self, broadcast, group, _='channels.setDiscussionGroup', **kwargs):
        kwargs['broadcast'] = broadcast
        kwargs['group'] = group
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcast(self) -> aliases.AnyInputChannel:
        return build_object(self['broadcast'])

    @property
    def group(self) -> aliases.AnyInputChannel:
        return build_object(self['group'])


class ChannelsEditLocation(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, geo_point: aliases.AnyInputGeoPoint, address: str): ...

    def __init__(self, channel, geo_point, address, _='channels.editLocation', **kwargs):
        kwargs['channel'] = channel
        kwargs['geo_point'] = geo_point
        kwargs['address'] = address
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def address(self) -> str:
        return self['address']


class ChannelsToggleSlowMode(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, seconds: int): ...

    def __init__(self, channel, seconds, _='channels.toggleSlowMode', **kwargs):
        kwargs['channel'] = channel
        kwargs['seconds'] = seconds
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def seconds(self) -> int:
        return self['seconds']


class ChannelsGetInactiveChannels(TLMethod[aliases.AnyMessagesInactiveChats]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channels.getInactiveChannels'):
        dict.__init__(self, _=_)


class ChannelsConvertToGigagroup(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.convertToGigagroup', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsGetSendAs(TLMethod[aliases.AnyChannelsSendAsPeers]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, for_paid_reactions: Optional[bool] = ..., for_live_stories: Optional[bool] = ...): ...

    def __init__(self, peer, _='channels.getSendAs', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_paid_reactions(self) -> Optional[bool]:
        return self['for_paid_reactions']

    @property
    def for_live_stories(self) -> Optional[bool]:
        return self['for_live_stories']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class ChannelsDeleteParticipantHistory(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, participant: aliases.AnyInputPeer): ...

    def __init__(self, channel, participant, _='channels.deleteParticipantHistory', **kwargs):
        kwargs['channel'] = channel
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])


class ChannelsToggleJoinToSend(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleJoinToSend', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsToggleJoinRequest(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleJoinRequest', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsReorderUsernames(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, order: list[str]): ...

    def __init__(self, channel, order, _='channels.reorderUsernames', **kwargs):
        kwargs['channel'] = channel
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def order(self) -> list[str]:
        return self['order']


class ChannelsToggleUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, username: str, active: bool): ...

    def __init__(self, channel, username, active, _='channels.toggleUsername', **kwargs):
        kwargs['channel'] = channel
        kwargs['username'] = username
        kwargs['active'] = active
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def username(self) -> str:
        return self['username']

    @property
    def active(self) -> bool:
        return self['active']


class ChannelsDeactivateAllUsernames(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='channels.deactivateAllUsernames', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class ChannelsToggleForum(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool, tabs: bool): ...

    def __init__(self, channel, enabled, tabs, _='channels.toggleForum', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['tabs'] = tabs
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']

    @property
    def tabs(self) -> bool:
        return self['tabs']


class ChannelsToggleAntiSpam(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleAntiSpam', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsReportAntiSpamFalsePositive(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, msg_id: int): ...

    def __init__(self, channel, msg_id, _='channels.reportAntiSpamFalsePositive', **kwargs):
        kwargs['channel'] = channel
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class ChannelsToggleParticipantsHidden(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleParticipantsHidden', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsUpdateColor(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, for_profile: Optional[bool] = ..., color: Optional[int] = ..., background_emoji_id: Optional[int] = ...): ...

    def __init__(self, channel, _='channels.updateColor', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_profile(self) -> Optional[bool]:
        return self['for_profile']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def color(self) -> Optional[int]:
        return self['color']

    @property
    def background_emoji_id(self) -> Optional[int]:
        return self['background_emoji_id']


class ChannelsToggleViewForumAsMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleViewForumAsMessages', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsGetChannelRecommendations(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, channel: Optional[aliases.AnyInputChannel] = ...): ...

    def __init__(self, _='channels.getChannelRecommendations', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> Optional[aliases.AnyInputChannel]:
        return build_object(self['channel'])


class ChannelsUpdateEmojiStatus(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, emoji_status: aliases.AnyEmojiStatus): ...

    def __init__(self, channel, emoji_status, _='channels.updateEmojiStatus', **kwargs):
        kwargs['channel'] = channel
        kwargs['emoji_status'] = emoji_status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def emoji_status(self) -> aliases.AnyEmojiStatus:
        return build_object(self['emoji_status'])


class ChannelsSetBoostsToUnblockRestrictions(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, boosts: int): ...

    def __init__(self, channel, boosts, _='channels.setBoostsToUnblockRestrictions', **kwargs):
        kwargs['channel'] = channel
        kwargs['boosts'] = boosts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def boosts(self) -> int:
        return self['boosts']


class ChannelsSetEmojiStickers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, channel, stickerset, _='channels.setEmojiStickers', **kwargs):
        kwargs['channel'] = channel
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])


class ChannelsRestrictSponsoredMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, restricted: bool): ...

    def __init__(self, channel, restricted, _='channels.restrictSponsoredMessages', **kwargs):
        kwargs['channel'] = channel
        kwargs['restricted'] = restricted
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def restricted(self) -> bool:
        return self['restricted']


class ChannelsSearchPosts(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, offset_rate: int, offset_peer: aliases.AnyInputPeer, offset_id: int, limit: int, hashtag: Optional[str] = ..., query: Optional[str] = ..., allow_paid_stars: Optional[int] = ...): ...

    def __init__(self, offset_rate, offset_peer, offset_id, limit, _='channels.searchPosts', **kwargs):
        kwargs['offset_rate'] = offset_rate
        kwargs['offset_peer'] = offset_peer
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hashtag(self) -> Optional[str]:
        return self['hashtag']

    @property
    def query(self) -> Optional[str]:
        return self['query']

    @property
    def offset_rate(self) -> int:
        return self['offset_rate']

    @property
    def offset_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['offset_peer'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']


class ChannelsUpdatePaidMessagesPrice(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, send_paid_messages_stars: int, broadcast_messages_allowed: Optional[bool] = ...): ...

    def __init__(self, channel, send_paid_messages_stars, _='channels.updatePaidMessagesPrice', **kwargs):
        kwargs['channel'] = channel
        kwargs['send_paid_messages_stars'] = send_paid_messages_stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcast_messages_allowed(self) -> Optional[bool]:
        return self['broadcast_messages_allowed']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def send_paid_messages_stars(self) -> int:
        return self['send_paid_messages_stars']


class ChannelsToggleAutotranslation(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, enabled: bool): ...

    def __init__(self, channel, enabled, _='channels.toggleAutotranslation', **kwargs):
        kwargs['channel'] = channel
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class ChannelsGetMessageAuthor(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, id: int): ...

    def __init__(self, channel, id, _='channels.getMessageAuthor', **kwargs):
        kwargs['channel'] = channel
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def id(self) -> int:
        return self['id']


class ChannelsCheckSearchPostsFlood(TLMethod[aliases.AnySearchPostsFlood]):
    __slots__ = ()

    @overload
    def __init__(self, query: Optional[str] = ...): ...

    def __init__(self, _='channels.checkSearchPostsFlood', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query(self) -> Optional[str]:
        return self['query']


class ChannelsSetMainProfileTab(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, tab: aliases.AnyProfileTab): ...

    def __init__(self, channel, tab, _='channels.setMainProfileTab', **kwargs):
        kwargs['channel'] = channel
        kwargs['tab'] = tab
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def tab(self) -> aliases.AnyProfileTab:
        return build_object(self['tab'])
