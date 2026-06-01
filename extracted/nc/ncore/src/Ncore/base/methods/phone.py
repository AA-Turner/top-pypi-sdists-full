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

class PhoneGetCallConfig(TLMethod[aliases.AnyDataJSON]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='phone.getCallConfig'):
        dict.__init__(self, _=_)


class PhoneRequestCall(TLMethod[aliases.AnyPhonePhoneCall]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, random_id: int, g_a_hash: bytes, protocol: aliases.AnyPhoneCallProtocol, video: Optional[bool] = ...): ...

    def __init__(self, user_id, random_id, g_a_hash, protocol, _='phone.requestCall', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['random_id'] = random_id
        kwargs['g_a_hash'] = g_a_hash
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def g_a_hash(self) -> bytes:
        return self['g_a_hash']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])


class PhoneAcceptCall(TLMethod[aliases.AnyPhonePhoneCall]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, g_b: bytes, protocol: aliases.AnyPhoneCallProtocol): ...

    def __init__(self, peer, g_b, protocol, _='phone.acceptCall', **kwargs):
        kwargs['peer'] = peer
        kwargs['g_b'] = g_b
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def g_b(self) -> bytes:
        return self['g_b']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])


class PhoneConfirmCall(TLMethod[aliases.AnyPhonePhoneCall]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, g_a: bytes, key_fingerprint: int, protocol: aliases.AnyPhoneCallProtocol): ...

    def __init__(self, peer, g_a, key_fingerprint, protocol, _='phone.confirmCall', **kwargs):
        kwargs['peer'] = peer
        kwargs['g_a'] = g_a
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def g_a(self) -> bytes:
        return self['g_a']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])


class PhoneReceivedCall(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall): ...

    def __init__(self, peer, _='phone.receivedCall', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])


class PhoneDiscardCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, duration: int, reason: aliases.AnyPhoneCallDiscardReason, connection_id: int, video: Optional[bool] = ...): ...

    def __init__(self, peer, duration, reason, connection_id, _='phone.discardCall', **kwargs):
        kwargs['peer'] = peer
        kwargs['duration'] = duration
        kwargs['reason'] = reason
        kwargs['connection_id'] = connection_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def duration(self) -> int:
        return self['duration']

    @property
    def reason(self) -> aliases.AnyPhoneCallDiscardReason:
        return build_object(self['reason'])

    @property
    def connection_id(self) -> int:
        return self['connection_id']


class PhoneSetCallRating(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, rating: int, comment: str, user_initiative: Optional[bool] = ...): ...

    def __init__(self, peer, rating, comment, _='phone.setCallRating', **kwargs):
        kwargs['peer'] = peer
        kwargs['rating'] = rating
        kwargs['comment'] = comment
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_initiative(self) -> Optional[bool]:
        return self['user_initiative']

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def rating(self) -> int:
        return self['rating']

    @property
    def comment(self) -> str:
        return self['comment']


class PhoneSaveCallDebug(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, debug: aliases.AnyDataJSON): ...

    def __init__(self, peer, debug, _='phone.saveCallDebug', **kwargs):
        kwargs['peer'] = peer
        kwargs['debug'] = debug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def debug(self) -> aliases.AnyDataJSON:
        return build_object(self['debug'])


class PhoneSendSignalingData(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, data: bytes): ...

    def __init__(self, peer, data, _='phone.sendSignalingData', **kwargs):
        kwargs['peer'] = peer
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def data(self) -> bytes:
        return self['data']


class PhoneCreateGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, random_id: int, rtmp_stream: Optional[bool] = ..., title: Optional[str] = ..., schedule_date: Optional[int] = ...): ...

    def __init__(self, peer, random_id, _='phone.createGroupCall', **kwargs):
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def rtmp_stream(self) -> Optional[bool]:
        return self['rtmp_stream']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']


class PhoneJoinGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, join_as: aliases.AnyInputPeer, params: aliases.AnyDataJSON, muted: Optional[bool] = ..., video_stopped: Optional[bool] = ..., invite_hash: Optional[str] = ..., public_key: Optional[int] = ..., block: Optional[bytes] = ...): ...

    def __init__(self, call, join_as, params, _='phone.joinGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['join_as'] = join_as
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def muted(self) -> Optional[bool]:
        return self['muted']

    @property
    def video_stopped(self) -> Optional[bool]:
        return self['video_stopped']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def join_as(self) -> aliases.AnyInputPeer:
        return build_object(self['join_as'])

    @property
    def invite_hash(self) -> Optional[str]:
        return self['invite_hash']

    @property
    def public_key(self) -> Optional[int]:
        return self['public_key']

    @property
    def block(self) -> Optional[bytes]:
        return self['block']

    @property
    def params(self) -> aliases.AnyDataJSON:
        return build_object(self['params'])


class PhoneLeaveGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, source: int): ...

    def __init__(self, call, source, _='phone.leaveGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['source'] = source
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def source(self) -> int:
        return self['source']


class PhoneInviteToGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, users: list[aliases.AnyInputUser]): ...

    def __init__(self, call, users, _='phone.inviteToGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])


class PhoneDiscardGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='phone.discardGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneToggleGroupCallSettings(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, reset_invite_hash: Optional[bool] = ..., join_muted: Optional[bool] = ..., messages_enabled: Optional[bool] = ..., send_paid_messages_stars: Optional[int] = ...): ...

    def __init__(self, call, _='phone.toggleGroupCallSettings', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reset_invite_hash(self) -> Optional[bool]:
        return self['reset_invite_hash']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def join_muted(self) -> Optional[bool]:
        return self['join_muted']

    @property
    def messages_enabled(self) -> Optional[bool]:
        return self['messages_enabled']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']


class PhoneGetGroupCall(TLMethod[aliases.AnyPhoneGroupCall]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, limit: int): ...

    def __init__(self, call, limit, _='phone.getGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def limit(self) -> int:
        return self['limit']


class PhoneGetGroupParticipants(TLMethod[aliases.AnyPhoneGroupParticipants]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, ids: list[aliases.AnyInputPeer], sources: list[int], offset: str, limit: int): ...

    def __init__(self, call, ids, sources, offset, limit, _='phone.getGroupParticipants', **kwargs):
        kwargs['call'] = call
        kwargs['ids'] = ids
        kwargs['sources'] = sources
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def ids(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['ids'])

    @property
    def sources(self) -> list[int]:
        return self['sources']

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PhoneCheckGroupCall(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, sources: list[int]): ...

    def __init__(self, call, sources, _='phone.checkGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['sources'] = sources
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def sources(self) -> list[int]:
        return self['sources']


class PhoneToggleGroupCallRecord(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, start: Optional[bool] = ..., video: Optional[bool] = ..., title: Optional[str] = ..., video_portrait: Optional[bool] = ...): ...

    def __init__(self, call, _='phone.toggleGroupCallRecord', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def start(self) -> Optional[bool]:
        return self['start']

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def video_portrait(self) -> Optional[bool]:
        return self['video_portrait']


class PhoneEditGroupCallParticipant(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, participant: aliases.AnyInputPeer, muted: Optional[bool] = ..., volume: Optional[int] = ..., raise_hand: Optional[bool] = ..., video_stopped: Optional[bool] = ..., video_paused: Optional[bool] = ..., presentation_paused: Optional[bool] = ...): ...

    def __init__(self, call, participant, _='phone.editGroupCallParticipant', **kwargs):
        kwargs['call'] = call
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])

    @property
    def muted(self) -> Optional[bool]:
        return self['muted']

    @property
    def volume(self) -> Optional[int]:
        return self['volume']

    @property
    def raise_hand(self) -> Optional[bool]:
        return self['raise_hand']

    @property
    def video_stopped(self) -> Optional[bool]:
        return self['video_stopped']

    @property
    def video_paused(self) -> Optional[bool]:
        return self['video_paused']

    @property
    def presentation_paused(self) -> Optional[bool]:
        return self['presentation_paused']


class PhoneEditGroupCallTitle(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, title: str): ...

    def __init__(self, call, title, _='phone.editGroupCallTitle', **kwargs):
        kwargs['call'] = call
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def title(self) -> str:
        return self['title']


class PhoneGetGroupCallJoinAs(TLMethod[aliases.AnyPhoneJoinAsPeers]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='phone.getGroupCallJoinAs', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PhoneExportGroupCallInvite(TLMethod[aliases.AnyPhoneExportedGroupCallInvite]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, can_self_unmute: Optional[bool] = ...): ...

    def __init__(self, call, _='phone.exportGroupCallInvite', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_self_unmute(self) -> Optional[bool]:
        return self['can_self_unmute']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneToggleGroupCallStartSubscription(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, subscribed: bool): ...

    def __init__(self, call, subscribed, _='phone.toggleGroupCallStartSubscription', **kwargs):
        kwargs['call'] = call
        kwargs['subscribed'] = subscribed
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def subscribed(self) -> bool:
        return self['subscribed']


class PhoneStartScheduledGroupCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='phone.startScheduledGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneSaveDefaultGroupCallJoinAs(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, join_as: aliases.AnyInputPeer): ...

    def __init__(self, peer, join_as, _='phone.saveDefaultGroupCallJoinAs', **kwargs):
        kwargs['peer'] = peer
        kwargs['join_as'] = join_as
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def join_as(self) -> aliases.AnyInputPeer:
        return build_object(self['join_as'])


class PhoneJoinGroupCallPresentation(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, params: aliases.AnyDataJSON): ...

    def __init__(self, call, params, _='phone.joinGroupCallPresentation', **kwargs):
        kwargs['call'] = call
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def params(self) -> aliases.AnyDataJSON:
        return build_object(self['params'])


class PhoneLeaveGroupCallPresentation(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='phone.leaveGroupCallPresentation', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneGetGroupCallStreamChannels(TLMethod[aliases.AnyPhoneGroupCallStreamChannels]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='phone.getGroupCallStreamChannels', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneGetGroupCallStreamRtmpUrl(TLMethod[aliases.AnyPhoneGroupCallStreamRtmpUrl]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, revoke: bool, live_story: Optional[bool] = ...): ...

    def __init__(self, peer, revoke, _='phone.getGroupCallStreamRtmpUrl', **kwargs):
        kwargs['peer'] = peer
        kwargs['revoke'] = revoke
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def live_story(self) -> Optional[bool]:
        return self['live_story']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def revoke(self) -> bool:
        return self['revoke']


class PhoneSaveCallLog(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPhoneCall, file: aliases.AnyInputFile): ...

    def __init__(self, peer, file, _='phone.saveCallLog', **kwargs):
        kwargs['peer'] = peer
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPhoneCall:
        return build_object(self['peer'])

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])


class PhoneCreateConferenceCall(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, random_id: int, muted: Optional[bool] = ..., video_stopped: Optional[bool] = ..., join: Optional[bool] = ..., public_key: Optional[int] = ..., block: Optional[bytes] = ..., params: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, random_id, _='phone.createConferenceCall', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def muted(self) -> Optional[bool]:
        return self['muted']

    @property
    def video_stopped(self) -> Optional[bool]:
        return self['video_stopped']

    @property
    def join(self) -> Optional[bool]:
        return self['join']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def public_key(self) -> Optional[int]:
        return self['public_key']

    @property
    def block(self) -> Optional[bytes]:
        return self['block']

    @property
    def params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['params'])


class PhoneDeleteConferenceCallParticipants(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, ids: list[int], block: bytes, only_left: Optional[bool] = ..., kick: Optional[bool] = ...): ...

    def __init__(self, call, ids, block, _='phone.deleteConferenceCallParticipants', **kwargs):
        kwargs['call'] = call
        kwargs['ids'] = ids
        kwargs['block'] = block
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def only_left(self) -> Optional[bool]:
        return self['only_left']

    @property
    def kick(self) -> Optional[bool]:
        return self['kick']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def ids(self) -> list[int]:
        return self['ids']

    @property
    def block(self) -> bytes:
        return self['block']


class PhoneSendConferenceCallBroadcast(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, block: bytes): ...

    def __init__(self, call, block, _='phone.sendConferenceCallBroadcast', **kwargs):
        kwargs['call'] = call
        kwargs['block'] = block
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def block(self) -> bytes:
        return self['block']


class PhoneInviteConferenceCallParticipant(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, user_id: aliases.AnyInputUser, video: Optional[bool] = ...): ...

    def __init__(self, call, user_id, _='phone.inviteConferenceCallParticipant', **kwargs):
        kwargs['call'] = call
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class PhoneDeclineConferenceCallInvite(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int): ...

    def __init__(self, msg_id, _='phone.declineConferenceCallInvite', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class PhoneGetGroupCallChainBlocks(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, sub_chain_id: int, offset: int, limit: int): ...

    def __init__(self, call, sub_chain_id, offset, limit, _='phone.getGroupCallChainBlocks', **kwargs):
        kwargs['call'] = call
        kwargs['sub_chain_id'] = sub_chain_id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def sub_chain_id(self) -> int:
        return self['sub_chain_id']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PhoneSendGroupCallMessage(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, random_id: int, message: aliases.AnyTextWithEntities, allow_paid_stars: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, call, random_id, message, _='phone.sendGroupCallMessage', **kwargs):
        kwargs['call'] = call
        kwargs['random_id'] = random_id
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def message(self) -> aliases.AnyTextWithEntities:
        return build_object(self['message'])

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])


class PhoneSendGroupCallEncryptedMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, encrypted_message: bytes): ...

    def __init__(self, call, encrypted_message, _='phone.sendGroupCallEncryptedMessage', **kwargs):
        kwargs['call'] = call
        kwargs['encrypted_message'] = encrypted_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def encrypted_message(self) -> bytes:
        return self['encrypted_message']


class PhoneDeleteGroupCallMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, messages: list[int], report_spam: Optional[bool] = ...): ...

    def __init__(self, call, messages, _='phone.deleteGroupCallMessages', **kwargs):
        kwargs['call'] = call
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def report_spam(self) -> Optional[bool]:
        return self['report_spam']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def messages(self) -> list[int]:
        return self['messages']


class PhoneDeleteGroupCallParticipantMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, participant: aliases.AnyInputPeer, report_spam: Optional[bool] = ...): ...

    def __init__(self, call, participant, _='phone.deleteGroupCallParticipantMessages', **kwargs):
        kwargs['call'] = call
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def report_spam(self) -> Optional[bool]:
        return self['report_spam']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])


class PhoneGetGroupCallStars(TLMethod[aliases.AnyPhoneGroupCallStars]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='phone.getGroupCallStars', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class PhoneSaveDefaultSendAs(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, send_as: aliases.AnyInputPeer): ...

    def __init__(self, call, send_as, _='phone.saveDefaultSendAs', **kwargs):
        kwargs['call'] = call
        kwargs['send_as'] = send_as
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def send_as(self) -> aliases.AnyInputPeer:
        return build_object(self['send_as'])
