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

class MessagesGetMessages(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputMessage]): ...

    def __init__(self, id, _='messages.getMessages', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputMessage]:
        return build_object(self['id'])


class MessagesGetDialogs(TLMethod[aliases.AnyMessagesDialogs]):
    __slots__ = ()

    @overload
    def __init__(self, offset_date: int, offset_id: int, offset_peer: aliases.AnyInputPeer, limit: int, hash: int, exclude_pinned: Optional[bool] = ..., folder_id: Optional[int] = ...): ...

    def __init__(self, offset_date, offset_id, offset_peer, limit, hash, _='messages.getDialogs', **kwargs):
        kwargs['offset_date'] = offset_date
        kwargs['offset_id'] = offset_id
        kwargs['offset_peer'] = offset_peer
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_pinned(self) -> Optional[bool]:
        return self['exclude_pinned']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['offset_peer'])

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetHistory(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int): ...

    def __init__(self, peer, offset_id, offset_date, add_offset, limit, max_id, min_id, hash, _='messages.getHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['offset_date'] = offset_date
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSearch(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, q: str, filter: aliases.AnyMessagesFilter, min_date: int, max_date: int, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int, from_id: Optional[aliases.AnyInputPeer] = ..., saved_peer_id: Optional[aliases.AnyInputPeer] = ..., saved_reaction: Optional[list[aliases.AnyReaction]] = ..., top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, q, filter, min_date, max_date, offset_id, add_offset, limit, max_id, min_id, hash, _='messages.search', **kwargs):
        kwargs['peer'] = peer
        kwargs['q'] = q
        kwargs['filter'] = filter
        kwargs['min_date'] = min_date
        kwargs['max_date'] = max_date
        kwargs['offset_id'] = offset_id
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def q(self) -> str:
        return self['q']

    @property
    def from_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['from_id'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def saved_reaction(self) -> Optional[list[aliases.AnyReaction]]:
        return build_object(self['saved_reaction'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def min_date(self) -> int:
        return self['min_date']

    @property
    def max_date(self) -> int:
        return self['max_date']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesReadHistory(TLMethod[aliases.AnyMessagesAffectedMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, max_id: int): ...

    def __init__(self, peer, max_id, _='messages.readHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']


class MessagesDeleteHistory(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, max_id: int, just_clear: Optional[bool] = ..., revoke: Optional[bool] = ..., min_date: Optional[int] = ..., max_date: Optional[int] = ...): ...

    def __init__(self, peer, max_id, _='messages.deleteHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def just_clear(self) -> Optional[bool]:
        return self['just_clear']

    @property
    def revoke(self) -> Optional[bool]:
        return self['revoke']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_date(self) -> Optional[int]:
        return self['min_date']

    @property
    def max_date(self) -> Optional[int]:
        return self['max_date']


class MessagesDeleteMessages(TLMethod[aliases.AnyMessagesAffectedMessages]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[int], revoke: Optional[bool] = ...): ...

    def __init__(self, id, _='messages.deleteMessages', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoke(self) -> Optional[bool]:
        return self['revoke']

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesReceivedMessages(TLMethod[list[aliases.AnyReceivedNotifyMessage]]):
    __slots__ = ()

    @overload
    def __init__(self, max_id: int): ...

    def __init__(self, max_id, _='messages.receivedMessages', **kwargs):
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def max_id(self) -> int:
        return self['max_id']


class MessagesSetTyping(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, action: aliases.AnySendMessageAction, top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, action, _='messages.setTyping', **kwargs):
        kwargs['peer'] = peer
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def action(self) -> aliases.AnySendMessageAction:
        return build_object(self['action'])


class MessagesSendMessage(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, message: str, random_id: int, no_webpage: Optional[bool] = ..., silent: Optional[bool] = ..., background: Optional[bool] = ..., clear_draft: Optional[bool] = ..., noforwards: Optional[bool] = ..., update_stickersets_order: Optional[bool] = ..., invert_media: Optional[bool] = ..., allow_paid_floodskip: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., schedule_date: Optional[int] = ..., schedule_repeat_period: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ..., quick_reply_shortcut: Optional[aliases.AnyInputQuickReplyShortcut] = ..., effect: Optional[int] = ..., allow_paid_stars: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ...): ...

    def __init__(self, peer, message, random_id, _='messages.sendMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['message'] = message
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def clear_draft(self) -> Optional[bool]:
        return self['clear_draft']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def update_stickersets_order(self) -> Optional[bool]:
        return self['update_stickersets_order']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def allow_paid_floodskip(self) -> Optional[bool]:
        return self['allow_paid_floodskip']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def schedule_repeat_period(self) -> Optional[int]:
        return self['schedule_repeat_period']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])

    @property
    def quick_reply_shortcut(self) -> Optional[aliases.AnyInputQuickReplyShortcut]:
        return build_object(self['quick_reply_shortcut'])

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])


class MessagesSendMedia(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, media: aliases.AnyInputMedia, message: str, random_id: int, silent: Optional[bool] = ..., background: Optional[bool] = ..., clear_draft: Optional[bool] = ..., noforwards: Optional[bool] = ..., update_stickersets_order: Optional[bool] = ..., invert_media: Optional[bool] = ..., allow_paid_floodskip: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., schedule_date: Optional[int] = ..., schedule_repeat_period: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ..., quick_reply_shortcut: Optional[aliases.AnyInputQuickReplyShortcut] = ..., effect: Optional[int] = ..., allow_paid_stars: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ...): ...

    def __init__(self, peer, media, message, random_id, _='messages.sendMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['media'] = media
        kwargs['message'] = message
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def clear_draft(self) -> Optional[bool]:
        return self['clear_draft']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def update_stickersets_order(self) -> Optional[bool]:
        return self['update_stickersets_order']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def allow_paid_floodskip(self) -> Optional[bool]:
        return self['allow_paid_floodskip']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def schedule_repeat_period(self) -> Optional[int]:
        return self['schedule_repeat_period']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])

    @property
    def quick_reply_shortcut(self) -> Optional[aliases.AnyInputQuickReplyShortcut]:
        return build_object(self['quick_reply_shortcut'])

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])


class MessagesForwardMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, from_peer: aliases.AnyInputPeer, id: list[int], random_id: list[int], to_peer: aliases.AnyInputPeer, silent: Optional[bool] = ..., background: Optional[bool] = ..., with_my_score: Optional[bool] = ..., drop_author: Optional[bool] = ..., drop_media_captions: Optional[bool] = ..., noforwards: Optional[bool] = ..., allow_paid_floodskip: Optional[bool] = ..., top_msg_id: Optional[int] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., schedule_date: Optional[int] = ..., schedule_repeat_period: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ..., quick_reply_shortcut: Optional[aliases.AnyInputQuickReplyShortcut] = ..., effect: Optional[int] = ..., video_timestamp: Optional[int] = ..., allow_paid_stars: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ...): ...

    def __init__(self, from_peer, id, random_id, to_peer, _='messages.forwardMessages', **kwargs):
        kwargs['from_peer'] = from_peer
        kwargs['id'] = id
        kwargs['random_id'] = random_id
        kwargs['to_peer'] = to_peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def with_my_score(self) -> Optional[bool]:
        return self['with_my_score']

    @property
    def drop_author(self) -> Optional[bool]:
        return self['drop_author']

    @property
    def drop_media_captions(self) -> Optional[bool]:
        return self['drop_media_captions']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def allow_paid_floodskip(self) -> Optional[bool]:
        return self['allow_paid_floodskip']

    @property
    def from_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['from_peer'])

    @property
    def id(self) -> list[int]:
        return self['id']

    @property
    def random_id(self) -> list[int]:
        return self['random_id']

    @property
    def to_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['to_peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def schedule_repeat_period(self) -> Optional[int]:
        return self['schedule_repeat_period']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])

    @property
    def quick_reply_shortcut(self) -> Optional[aliases.AnyInputQuickReplyShortcut]:
        return build_object(self['quick_reply_shortcut'])

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def video_timestamp(self) -> Optional[int]:
        return self['video_timestamp']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])


class MessagesReportSpam(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.reportSpam', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesGetPeerSettings(TLMethod[aliases.AnyMessagesPeerSettings]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.getPeerSettings', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesReport(TLMethod[aliases.AnyReportResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int], option: bytes, message: str): ...

    def __init__(self, peer, id, option, message, _='messages.report', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['option'] = option
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']

    @property
    def option(self) -> bytes:
        return self['option']

    @property
    def message(self) -> str:
        return self['message']


class MessagesGetChats(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[int]): ...

    def __init__(self, id, _='messages.getChats', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetFullChat(TLMethod[aliases.AnyMessagesChatFull]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='messages.getFullChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class MessagesEditChatTitle(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, title: str): ...

    def __init__(self, chat_id, title, _='messages.editChatTitle', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def title(self) -> str:
        return self['title']


class MessagesEditChatPhoto(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, photo: aliases.AnyInputChatPhoto): ...

    def __init__(self, chat_id, photo, _='messages.editChatPhoto', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['photo'] = photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def photo(self) -> aliases.AnyInputChatPhoto:
        return build_object(self['photo'])


class MessagesAddChatUser(TLMethod[aliases.AnyMessagesInvitedUsers]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: aliases.AnyInputUser, fwd_limit: int): ...

    def __init__(self, chat_id, user_id, fwd_limit, _='messages.addChatUser', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['fwd_limit'] = fwd_limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def fwd_limit(self) -> int:
        return self['fwd_limit']


class MessagesDeleteChatUser(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: aliases.AnyInputUser, revoke_history: Optional[bool] = ...): ...

    def __init__(self, chat_id, user_id, _='messages.deleteChatUser', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoke_history(self) -> Optional[bool]:
        return self['revoke_history']

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class MessagesCreateChat(TLMethod[aliases.AnyMessagesInvitedUsers]):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyInputUser], title: str, ttl_period: Optional[int] = ...): ...

    def __init__(self, users, title, _='messages.createChat', **kwargs):
        kwargs['users'] = users
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class MessagesGetDhConfig(TLMethod[aliases.AnyMessagesDhConfig]):
    __slots__ = ()

    @overload
    def __init__(self, version: int, random_length: int): ...

    def __init__(self, version, random_length, _='messages.getDhConfig', **kwargs):
        kwargs['version'] = version
        kwargs['random_length'] = random_length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def version(self) -> int:
        return self['version']

    @property
    def random_length(self) -> int:
        return self['random_length']


class MessagesRequestEncryption(TLMethod[aliases.AnyEncryptedChat]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, random_id: int, g_a: bytes): ...

    def __init__(self, user_id, random_id, g_a, _='messages.requestEncryption', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['random_id'] = random_id
        kwargs['g_a'] = g_a
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def g_a(self) -> bytes:
        return self['g_a']


class MessagesAcceptEncryption(TLMethod[aliases.AnyEncryptedChat]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, g_b: bytes, key_fingerprint: int): ...

    def __init__(self, peer, g_b, key_fingerprint, _='messages.acceptEncryption', **kwargs):
        kwargs['peer'] = peer
        kwargs['g_b'] = g_b
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def g_b(self) -> bytes:
        return self['g_b']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']


class MessagesDiscardEncryption(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, delete_history: Optional[bool] = ...): ...

    def __init__(self, chat_id, _='messages.discardEncryption', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def delete_history(self) -> Optional[bool]:
        return self['delete_history']

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class MessagesSetEncryptedTyping(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, typing: bool): ...

    def __init__(self, peer, typing, _='messages.setEncryptedTyping', **kwargs):
        kwargs['peer'] = peer
        kwargs['typing'] = typing
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def typing(self) -> bool:
        return self['typing']


class MessagesReadEncryptedHistory(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, max_date: int): ...

    def __init__(self, peer, max_date, _='messages.readEncryptedHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_date'] = max_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def max_date(self) -> int:
        return self['max_date']


class MessagesSendEncrypted(TLMethod[aliases.AnyMessagesSentEncryptedMessage]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, random_id: int, data: bytes, silent: Optional[bool] = ...): ...

    def __init__(self, peer, random_id, data, _='messages.sendEncrypted', **kwargs):
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def data(self) -> bytes:
        return self['data']


class MessagesSendEncryptedFile(TLMethod[aliases.AnyMessagesSentEncryptedMessage]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, random_id: int, data: bytes, file: aliases.AnyInputEncryptedFile, silent: Optional[bool] = ...): ...

    def __init__(self, peer, random_id, data, file, _='messages.sendEncryptedFile', **kwargs):
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['data'] = data
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def data(self) -> bytes:
        return self['data']

    @property
    def file(self) -> aliases.AnyInputEncryptedFile:
        return build_object(self['file'])


class MessagesSendEncryptedService(TLMethod[aliases.AnyMessagesSentEncryptedMessage]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, random_id: int, data: bytes): ...

    def __init__(self, peer, random_id, data, _='messages.sendEncryptedService', **kwargs):
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def data(self) -> bytes:
        return self['data']


class MessagesReceivedQueue(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, max_qts: int): ...

    def __init__(self, max_qts, _='messages.receivedQueue', **kwargs):
        kwargs['max_qts'] = max_qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def max_qts(self) -> int:
        return self['max_qts']


class MessagesReportEncryptedSpam(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat): ...

    def __init__(self, peer, _='messages.reportEncryptedSpam', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])


class MessagesReadMessageContents(TLMethod[aliases.AnyMessagesAffectedMessages]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[int]): ...

    def __init__(self, id, _='messages.readMessageContents', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetStickers(TLMethod[aliases.AnyMessagesStickers]):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str, hash: int): ...

    def __init__(self, emoticon, hash, _='messages.getStickers', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetAllStickers(TLMethod[aliases.AnyMessagesAllStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getAllStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetWebPagePreview(TLMethod[aliases.AnyMessagesWebPagePreview]):
    __slots__ = ()

    @overload
    def __init__(self, message: str, entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, message, _='messages.getWebPagePreview', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])


class MessagesExportChatInvite(TLMethod[aliases.AnyExportedChatInvite]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, legacy_revoke_permanent: Optional[bool] = ..., request_needed: Optional[bool] = ..., expire_date: Optional[int] = ..., usage_limit: Optional[int] = ..., title: Optional[str] = ..., subscription_pricing: Optional[aliases.AnyStarsSubscriptionPricing] = ...): ...

    def __init__(self, peer, _='messages.exportChatInvite', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def legacy_revoke_permanent(self) -> Optional[bool]:
        return self['legacy_revoke_permanent']

    @property
    def request_needed(self) -> Optional[bool]:
        return self['request_needed']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def expire_date(self) -> Optional[int]:
        return self['expire_date']

    @property
    def usage_limit(self) -> Optional[int]:
        return self['usage_limit']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def subscription_pricing(self) -> Optional[aliases.AnyStarsSubscriptionPricing]:
        return build_object(self['subscription_pricing'])


class MessagesCheckChatInvite(TLMethod[aliases.AnyChatInvite]):
    __slots__ = ()

    @overload
    def __init__(self, hash: str): ...

    def __init__(self, hash, _='messages.checkChatInvite', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> str:
        return self['hash']


class MessagesImportChatInvite(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, hash: str): ...

    def __init__(self, hash, _='messages.importChatInvite', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> str:
        return self['hash']


class MessagesGetStickerSet(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, hash: int): ...

    def __init__(self, stickerset, hash, _='messages.getStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesInstallStickerSet(TLMethod[aliases.AnyMessagesStickerSetInstallResult]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, archived: bool): ...

    def __init__(self, stickerset, archived, _='messages.installStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['archived'] = archived
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def archived(self) -> bool:
        return self['archived']


class MessagesUninstallStickerSet(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, stickerset, _='messages.uninstallStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])


class MessagesStartBot(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, peer: aliases.AnyInputPeer, random_id: int, start_param: str): ...

    def __init__(self, bot, peer, random_id, start_param, _='messages.startBot', **kwargs):
        kwargs['bot'] = bot
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['start_param'] = start_param
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def start_param(self) -> str:
        return self['start_param']


class MessagesGetMessagesViews(TLMethod[aliases.AnyMessagesMessageViews]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int], increment: bool): ...

    def __init__(self, peer, id, increment, _='messages.getMessagesViews', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['increment'] = increment
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']

    @property
    def increment(self) -> bool:
        return self['increment']


class MessagesEditChatAdmin(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: aliases.AnyInputUser, is_admin: bool): ...

    def __init__(self, chat_id, user_id, is_admin, _='messages.editChatAdmin', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['is_admin'] = is_admin
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def is_admin(self) -> bool:
        return self['is_admin']


class MessagesMigrateChat(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='messages.migrateChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class MessagesSearchGlobal(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, filter: aliases.AnyMessagesFilter, min_date: int, max_date: int, offset_rate: int, offset_peer: aliases.AnyInputPeer, offset_id: int, limit: int, broadcasts_only: Optional[bool] = ..., groups_only: Optional[bool] = ..., users_only: Optional[bool] = ..., folder_id: Optional[int] = ...): ...

    def __init__(self, q, filter, min_date, max_date, offset_rate, offset_peer, offset_id, limit, _='messages.searchGlobal', **kwargs):
        kwargs['q'] = q
        kwargs['filter'] = filter
        kwargs['min_date'] = min_date
        kwargs['max_date'] = max_date
        kwargs['offset_rate'] = offset_rate
        kwargs['offset_peer'] = offset_peer
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcasts_only(self) -> Optional[bool]:
        return self['broadcasts_only']

    @property
    def groups_only(self) -> Optional[bool]:
        return self['groups_only']

    @property
    def users_only(self) -> Optional[bool]:
        return self['users_only']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def q(self) -> str:
        return self['q']

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def min_date(self) -> int:
        return self['min_date']

    @property
    def max_date(self) -> int:
        return self['max_date']

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


class MessagesReorderStickerSets(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, order: list[int], masks: Optional[bool] = ..., emojis: Optional[bool] = ...): ...

    def __init__(self, order, _='messages.reorderStickerSets', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def order(self) -> list[int]:
        return self['order']


class MessagesGetDocumentByHash(TLMethod[aliases.AnyDocument]):
    __slots__ = ()

    @overload
    def __init__(self, sha256: bytes, size: int, mime_type: str): ...

    def __init__(self, sha256, size, mime_type, _='messages.getDocumentByHash', **kwargs):
        kwargs['sha256'] = sha256
        kwargs['size'] = size
        kwargs['mime_type'] = mime_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sha256(self) -> bytes:
        return self['sha256']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def mime_type(self) -> str:
        return self['mime_type']


class MessagesGetSavedGifs(TLMethod[aliases.AnyMessagesSavedGifs]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getSavedGifs', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSaveGif(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, unsave: bool): ...

    def __init__(self, id, unsave, _='messages.saveGif', **kwargs):
        kwargs['id'] = id
        kwargs['unsave'] = unsave
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def unsave(self) -> bool:
        return self['unsave']


class MessagesGetInlineBotResults(TLMethod[aliases.AnyMessagesBotResults]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, peer: aliases.AnyInputPeer, query: str, offset: str, geo_point: Optional[aliases.AnyInputGeoPoint] = ...): ...

    def __init__(self, bot, peer, query, offset, _='messages.getInlineBotResults', **kwargs):
        kwargs['bot'] = bot
        kwargs['peer'] = peer
        kwargs['query'] = query
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def geo_point(self) -> Optional[aliases.AnyInputGeoPoint]:
        return build_object(self['geo_point'])

    @property
    def query(self) -> str:
        return self['query']

    @property
    def offset(self) -> str:
        return self['offset']


class MessagesSetInlineBotResults(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, results: list[aliases.AnyInputBotInlineResult], cache_time: int, gallery: Optional[bool] = ..., private: Optional[bool] = ..., next_offset: Optional[str] = ..., switch_pm: Optional[aliases.AnyInlineBotSwitchPM] = ..., switch_webview: Optional[aliases.AnyInlineBotWebView] = ...): ...

    def __init__(self, query_id, results, cache_time, _='messages.setInlineBotResults', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['results'] = results
        kwargs['cache_time'] = cache_time
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gallery(self) -> Optional[bool]:
        return self['gallery']

    @property
    def private(self) -> Optional[bool]:
        return self['private']

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def results(self) -> list[aliases.AnyInputBotInlineResult]:
        return build_object(self['results'])

    @property
    def cache_time(self) -> int:
        return self['cache_time']

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def switch_pm(self) -> Optional[aliases.AnyInlineBotSwitchPM]:
        return build_object(self['switch_pm'])

    @property
    def switch_webview(self) -> Optional[aliases.AnyInlineBotWebView]:
        return build_object(self['switch_webview'])


class MessagesSendInlineBotResult(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, random_id: int, query_id: int, id: str, silent: Optional[bool] = ..., background: Optional[bool] = ..., clear_draft: Optional[bool] = ..., hide_via: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., schedule_date: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ..., quick_reply_shortcut: Optional[aliases.AnyInputQuickReplyShortcut] = ..., allow_paid_stars: Optional[int] = ...): ...

    def __init__(self, peer, random_id, query_id, id, _='messages.sendInlineBotResult', **kwargs):
        kwargs['peer'] = peer
        kwargs['random_id'] = random_id
        kwargs['query_id'] = query_id
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def clear_draft(self) -> Optional[bool]:
        return self['clear_draft']

    @property
    def hide_via(self) -> Optional[bool]:
        return self['hide_via']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def id(self) -> str:
        return self['id']

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])

    @property
    def quick_reply_shortcut(self) -> Optional[aliases.AnyInputQuickReplyShortcut]:
        return build_object(self['quick_reply_shortcut'])

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']


class MessagesGetMessageEditData(TLMethod[aliases.AnyMessagesMessageEditData]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int): ...

    def __init__(self, peer, id, _='messages.getMessageEditData', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']


class MessagesEditMessage(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., message: Optional[str] = ..., media: Optional[aliases.AnyInputMedia] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., schedule_date: Optional[int] = ..., schedule_repeat_period: Optional[int] = ..., quick_reply_shortcut_id: Optional[int] = ...): ...

    def __init__(self, peer, id, _='messages.editMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def message(self) -> Optional[str]:
        return self['message']

    @property
    def media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['media'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def schedule_repeat_period(self) -> Optional[int]:
        return self['schedule_repeat_period']

    @property
    def quick_reply_shortcut_id(self) -> Optional[int]:
        return self['quick_reply_shortcut_id']


class MessagesEditInlineBotMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputBotInlineMessageID, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., message: Optional[str] = ..., media: Optional[aliases.AnyInputMedia] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, id, _='messages.editInlineBotMessage', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def id(self) -> aliases.AnyInputBotInlineMessageID:
        return build_object(self['id'])

    @property
    def message(self) -> Optional[str]:
        return self['message']

    @property
    def media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['media'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])


class MessagesGetBotCallbackAnswer(TLMethod[aliases.AnyMessagesBotCallbackAnswer]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, game: Optional[bool] = ..., data: Optional[bytes] = ..., password: Optional[aliases.AnyInputCheckPasswordSRP] = ...): ...

    def __init__(self, peer, msg_id, _='messages.getBotCallbackAnswer', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def game(self) -> Optional[bool]:
        return self['game']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def data(self) -> Optional[bytes]:
        return self['data']

    @property
    def password(self) -> Optional[aliases.AnyInputCheckPasswordSRP]:
        return build_object(self['password'])


class MessagesSetBotCallbackAnswer(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, cache_time: int, alert: Optional[bool] = ..., message: Optional[str] = ..., url: Optional[str] = ...): ...

    def __init__(self, query_id, cache_time, _='messages.setBotCallbackAnswer', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['cache_time'] = cache_time
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def alert(self) -> Optional[bool]:
        return self['alert']

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def message(self) -> Optional[str]:
        return self['message']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def cache_time(self) -> int:
        return self['cache_time']


class MessagesGetPeerDialogs(TLMethod[aliases.AnyMessagesPeerDialogs]):
    __slots__ = ()

    @overload
    def __init__(self, peers: list[aliases.AnyInputDialogPeer]): ...

    def __init__(self, peers, _='messages.getPeerDialogs', **kwargs):
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peers(self) -> list[aliases.AnyInputDialogPeer]:
        return build_object(self['peers'])


class MessagesSaveDraft(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, message: str, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., media: Optional[aliases.AnyInputMedia] = ..., effect: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ...): ...

    def __init__(self, peer, message, _='messages.saveDraft', **kwargs):
        kwargs['peer'] = peer
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['media'])

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])


class MessagesGetAllDrafts(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getAllDrafts'):
        dict.__init__(self, _=_)


class MessagesGetFeaturedStickers(TLMethod[aliases.AnyMessagesFeaturedStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getFeaturedStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesReadFeaturedStickers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[int]): ...

    def __init__(self, id, _='messages.readFeaturedStickers', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetRecentStickers(TLMethod[aliases.AnyMessagesRecentStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, attached: Optional[bool] = ...): ...

    def __init__(self, hash, _='messages.getRecentStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attached(self) -> Optional[bool]:
        return self['attached']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSaveRecentSticker(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, unsave: bool, attached: Optional[bool] = ...): ...

    def __init__(self, id, unsave, _='messages.saveRecentSticker', **kwargs):
        kwargs['id'] = id
        kwargs['unsave'] = unsave
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attached(self) -> Optional[bool]:
        return self['attached']

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def unsave(self) -> bool:
        return self['unsave']


class MessagesClearRecentStickers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, attached: Optional[bool] = ...): ...

    def __init__(self, _='messages.clearRecentStickers', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attached(self) -> Optional[bool]:
        return self['attached']


class MessagesGetArchivedStickers(TLMethod[aliases.AnyMessagesArchivedStickers]):
    __slots__ = ()

    @overload
    def __init__(self, offset_id: int, limit: int, masks: Optional[bool] = ..., emojis: Optional[bool] = ...): ...

    def __init__(self, offset_id, limit, _='messages.getArchivedStickers', **kwargs):
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetMaskStickers(TLMethod[aliases.AnyMessagesAllStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getMaskStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetAttachedStickers(TLMethod[list[aliases.AnyStickerSetCovered]]):
    __slots__ = ()

    @overload
    def __init__(self, media: aliases.AnyInputStickeredMedia): ...

    def __init__(self, media, _='messages.getAttachedStickers', **kwargs):
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> aliases.AnyInputStickeredMedia:
        return build_object(self['media'])


class MessagesSetGameScore(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, user_id: aliases.AnyInputUser, score: int, edit_message: Optional[bool] = ..., force: Optional[bool] = ...): ...

    def __init__(self, peer, id, user_id, score, _='messages.setGameScore', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['user_id'] = user_id
        kwargs['score'] = score
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def edit_message(self) -> Optional[bool]:
        return self['edit_message']

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def score(self) -> int:
        return self['score']


class MessagesSetInlineGameScore(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputBotInlineMessageID, user_id: aliases.AnyInputUser, score: int, edit_message: Optional[bool] = ..., force: Optional[bool] = ...): ...

    def __init__(self, id, user_id, score, _='messages.setInlineGameScore', **kwargs):
        kwargs['id'] = id
        kwargs['user_id'] = user_id
        kwargs['score'] = score
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def edit_message(self) -> Optional[bool]:
        return self['edit_message']

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def id(self) -> aliases.AnyInputBotInlineMessageID:
        return build_object(self['id'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def score(self) -> int:
        return self['score']


class MessagesGetGameHighScores(TLMethod[aliases.AnyMessagesHighScores]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, user_id: aliases.AnyInputUser): ...

    def __init__(self, peer, id, user_id, _='messages.getGameHighScores', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class MessagesGetInlineGameHighScores(TLMethod[aliases.AnyMessagesHighScores]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputBotInlineMessageID, user_id: aliases.AnyInputUser): ...

    def __init__(self, id, user_id, _='messages.getInlineGameHighScores', **kwargs):
        kwargs['id'] = id
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputBotInlineMessageID:
        return build_object(self['id'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class MessagesGetCommonChats(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, max_id: int, limit: int): ...

    def __init__(self, user_id, max_id, limit, _='messages.getCommonChats', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['max_id'] = max_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetWebPage(TLMethod[aliases.AnyMessagesWebPage]):
    __slots__ = ()

    @overload
    def __init__(self, url: str, hash: int): ...

    def __init__(self, url, hash, _='messages.getWebPage', **kwargs):
        kwargs['url'] = url
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesToggleDialogPin(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputDialogPeer, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, _='messages.toggleDialogPin', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyInputDialogPeer:
        return build_object(self['peer'])


class MessagesReorderPinnedDialogs(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, folder_id: int, order: list[aliases.AnyInputDialogPeer], force: Optional[bool] = ...): ...

    def __init__(self, folder_id, order, _='messages.reorderPinnedDialogs', **kwargs):
        kwargs['folder_id'] = folder_id
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def folder_id(self) -> int:
        return self['folder_id']

    @property
    def order(self) -> list[aliases.AnyInputDialogPeer]:
        return build_object(self['order'])


class MessagesGetPinnedDialogs(TLMethod[aliases.AnyMessagesPeerDialogs]):
    __slots__ = ()

    @overload
    def __init__(self, folder_id: int): ...

    def __init__(self, folder_id, _='messages.getPinnedDialogs', **kwargs):
        kwargs['folder_id'] = folder_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> int:
        return self['folder_id']


class MessagesSetBotShippingResults(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, error: Optional[str] = ..., shipping_options: Optional[list[aliases.AnyShippingOption]] = ...): ...

    def __init__(self, query_id, _='messages.setBotShippingResults', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def error(self) -> Optional[str]:
        return self['error']

    @property
    def shipping_options(self) -> Optional[list[aliases.AnyShippingOption]]:
        return build_object(self['shipping_options'])


class MessagesSetBotPrecheckoutResults(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, success: Optional[bool] = ..., error: Optional[str] = ...): ...

    def __init__(self, query_id, _='messages.setBotPrecheckoutResults', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def success(self) -> Optional[bool]:
        return self['success']

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def error(self) -> Optional[str]:
        return self['error']


class MessagesUploadMedia(TLMethod[aliases.AnyMessageMedia]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, media: aliases.AnyInputMedia, business_connection_id: Optional[str] = ...): ...

    def __init__(self, peer, media, _='messages.uploadMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def business_connection_id(self) -> Optional[str]:
        return self['business_connection_id']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])


class MessagesSendScreenshotNotification(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, reply_to: aliases.AnyInputReplyTo, random_id: int): ...

    def __init__(self, peer, reply_to, random_id, _='messages.sendScreenshotNotification', **kwargs):
        kwargs['peer'] = peer
        kwargs['reply_to'] = reply_to
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reply_to(self) -> aliases.AnyInputReplyTo:
        return build_object(self['reply_to'])

    @property
    def random_id(self) -> int:
        return self['random_id']


class MessagesGetFavedStickers(TLMethod[aliases.AnyMessagesFavedStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getFavedStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesFaveSticker(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, unfave: bool): ...

    def __init__(self, id, unfave, _='messages.faveSticker', **kwargs):
        kwargs['id'] = id
        kwargs['unfave'] = unfave
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def unfave(self) -> bool:
        return self['unfave']


class MessagesGetUnreadMentions(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, offset_id, add_offset, limit, max_id, min_id, _='messages.getUnreadMentions', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']


class MessagesReadMentions(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, _='messages.readMentions', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']


class MessagesGetRecentLocations(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, limit: int, hash: int): ...

    def __init__(self, peer, limit, hash, _='messages.getRecentLocations', **kwargs):
        kwargs['peer'] = peer
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSendMultiMedia(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, multi_media: list[aliases.AnyInputSingleMedia], silent: Optional[bool] = ..., background: Optional[bool] = ..., clear_draft: Optional[bool] = ..., noforwards: Optional[bool] = ..., update_stickersets_order: Optional[bool] = ..., invert_media: Optional[bool] = ..., allow_paid_floodskip: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., schedule_date: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ..., quick_reply_shortcut: Optional[aliases.AnyInputQuickReplyShortcut] = ..., effect: Optional[int] = ..., allow_paid_stars: Optional[int] = ...): ...

    def __init__(self, peer, multi_media, _='messages.sendMultiMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['multi_media'] = multi_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def background(self) -> Optional[bool]:
        return self['background']

    @property
    def clear_draft(self) -> Optional[bool]:
        return self['clear_draft']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def update_stickersets_order(self) -> Optional[bool]:
        return self['update_stickersets_order']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def allow_paid_floodskip(self) -> Optional[bool]:
        return self['allow_paid_floodskip']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def multi_media(self) -> list[aliases.AnyInputSingleMedia]:
        return build_object(self['multi_media'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])

    @property
    def quick_reply_shortcut(self) -> Optional[aliases.AnyInputQuickReplyShortcut]:
        return build_object(self['quick_reply_shortcut'])

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def allow_paid_stars(self) -> Optional[int]:
        return self['allow_paid_stars']


class MessagesUploadEncryptedFile(TLMethod[aliases.AnyEncryptedFile]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputEncryptedChat, file: aliases.AnyInputEncryptedFile): ...

    def __init__(self, peer, file, _='messages.uploadEncryptedFile', **kwargs):
        kwargs['peer'] = peer
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputEncryptedChat:
        return build_object(self['peer'])

    @property
    def file(self) -> aliases.AnyInputEncryptedFile:
        return build_object(self['file'])


class MessagesSearchStickerSets(TLMethod[aliases.AnyMessagesFoundStickerSets]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, hash: int, exclude_featured: Optional[bool] = ...): ...

    def __init__(self, q, hash, _='messages.searchStickerSets', **kwargs):
        kwargs['q'] = q
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_featured(self) -> Optional[bool]:
        return self['exclude_featured']

    @property
    def q(self) -> str:
        return self['q']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetSplitRanges(TLMethod[list[aliases.AnyMessageRange]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getSplitRanges'):
        dict.__init__(self, _=_)


class MessagesMarkDialogUnread(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputDialogPeer, unread: Optional[bool] = ..., parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, _='messages.markDialogUnread', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unread(self) -> Optional[bool]:
        return self['unread']

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def peer(self) -> aliases.AnyInputDialogPeer:
        return build_object(self['peer'])


class MessagesGetDialogUnreadMarks(TLMethod[list[aliases.AnyDialogPeer]]):
    __slots__ = ()

    @overload
    def __init__(self, parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, _='messages.getDialogUnreadMarks', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])


class MessagesClearAllDrafts(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.clearAllDrafts'):
        dict.__init__(self, _=_)


class MessagesUpdatePinnedMessage(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, silent: Optional[bool] = ..., unpin: Optional[bool] = ..., pm_oneside: Optional[bool] = ...): ...

    def __init__(self, peer, id, _='messages.updatePinnedMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def unpin(self) -> Optional[bool]:
        return self['unpin']

    @property
    def pm_oneside(self) -> Optional[bool]:
        return self['pm_oneside']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']


class MessagesSendVote(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, options: list[bytes]): ...

    def __init__(self, peer, msg_id, options, _='messages.sendVote', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['options'] = options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def options(self) -> list[bytes]:
        return self['options']


class MessagesGetPollResults(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.getPollResults', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesGetOnlines(TLMethod[aliases.AnyChatOnlines]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.getOnlines', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesEditChatAbout(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, about: str): ...

    def __init__(self, peer, about, _='messages.editChatAbout', **kwargs):
        kwargs['peer'] = peer
        kwargs['about'] = about
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def about(self) -> str:
        return self['about']


class MessagesEditChatDefaultBannedRights(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, banned_rights: aliases.AnyChatBannedRights): ...

    def __init__(self, peer, banned_rights, _='messages.editChatDefaultBannedRights', **kwargs):
        kwargs['peer'] = peer
        kwargs['banned_rights'] = banned_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['banned_rights'])


class MessagesGetEmojiKeywords(TLMethod[aliases.AnyEmojiKeywordsDifference]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str): ...

    def __init__(self, lang_code, _='messages.getEmojiKeywords', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class MessagesGetEmojiKeywordsDifference(TLMethod[aliases.AnyEmojiKeywordsDifference]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, from_version: int): ...

    def __init__(self, lang_code, from_version, _='messages.getEmojiKeywordsDifference', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['from_version'] = from_version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def from_version(self) -> int:
        return self['from_version']


class MessagesGetEmojiKeywordsLanguages(TLMethod[list[aliases.AnyEmojiLanguage]]):
    __slots__ = ()

    @overload
    def __init__(self, lang_codes: list[str]): ...

    def __init__(self, lang_codes, _='messages.getEmojiKeywordsLanguages', **kwargs):
        kwargs['lang_codes'] = lang_codes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_codes(self) -> list[str]:
        return self['lang_codes']


class MessagesGetEmojiURL(TLMethod[aliases.AnyEmojiURL]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str): ...

    def __init__(self, lang_code, _='messages.getEmojiURL', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class MessagesGetSearchCounters(TLMethod[list[aliases.AnyMessagesSearchCounter]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, filters: list[aliases.AnyMessagesFilter], saved_peer_id: Optional[aliases.AnyInputPeer] = ..., top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, filters, _='messages.getSearchCounters', **kwargs):
        kwargs['peer'] = peer
        kwargs['filters'] = filters
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def filters(self) -> list[aliases.AnyMessagesFilter]:
        return build_object(self['filters'])


class MessagesRequestUrlAuth(TLMethod[aliases.AnyUrlAuthResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: Optional[aliases.AnyInputPeer] = ..., msg_id: Optional[int] = ..., button_id: Optional[int] = ..., url: Optional[str] = ..., in_app_origin: Optional[str] = ...): ...

    def __init__(self, _='messages.requestUrlAuth', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> Optional[int]:
        return self['msg_id']

    @property
    def button_id(self) -> Optional[int]:
        return self['button_id']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def in_app_origin(self) -> Optional[str]:
        return self['in_app_origin']


class MessagesAcceptUrlAuth(TLMethod[aliases.AnyUrlAuthResult]):
    __slots__ = ()

    @overload
    def __init__(self, write_allowed: Optional[bool] = ..., share_phone_number: Optional[bool] = ..., peer: Optional[aliases.AnyInputPeer] = ..., msg_id: Optional[int] = ..., button_id: Optional[int] = ..., url: Optional[str] = ..., match_code: Optional[str] = ...): ...

    def __init__(self, _='messages.acceptUrlAuth', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def write_allowed(self) -> Optional[bool]:
        return self['write_allowed']

    @property
    def share_phone_number(self) -> Optional[bool]:
        return self['share_phone_number']

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> Optional[int]:
        return self['msg_id']

    @property
    def button_id(self) -> Optional[int]:
        return self['button_id']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def match_code(self) -> Optional[str]:
        return self['match_code']


class MessagesHidePeerSettingsBar(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.hidePeerSettingsBar', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesGetScheduledHistory(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, hash: int): ...

    def __init__(self, peer, hash, _='messages.getScheduledHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetScheduledMessages(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='messages.getScheduledMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesSendScheduledMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='messages.sendScheduledMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesDeleteScheduledMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='messages.deleteScheduledMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetPollVotes(TLMethod[aliases.AnyMessagesVotesList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, limit: int, option: Optional[bytes] = ..., offset: Optional[str] = ...): ...

    def __init__(self, peer, id, limit, _='messages.getPollVotes', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def option(self) -> Optional[bytes]:
        return self['option']

    @property
    def offset(self) -> Optional[str]:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesToggleStickerSets(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, stickersets: list[aliases.AnyInputStickerSet], uninstall: Optional[bool] = ..., archive: Optional[bool] = ..., unarchive: Optional[bool] = ...): ...

    def __init__(self, stickersets, _='messages.toggleStickerSets', **kwargs):
        kwargs['stickersets'] = stickersets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def uninstall(self) -> Optional[bool]:
        return self['uninstall']

    @property
    def archive(self) -> Optional[bool]:
        return self['archive']

    @property
    def unarchive(self) -> Optional[bool]:
        return self['unarchive']

    @property
    def stickersets(self) -> list[aliases.AnyInputStickerSet]:
        return build_object(self['stickersets'])


class MessagesGetDialogFilters(TLMethod[aliases.AnyMessagesDialogFilters]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getDialogFilters'):
        dict.__init__(self, _=_)


class MessagesGetSuggestedDialogFilters(TLMethod[list[aliases.AnyDialogFilterSuggested]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getSuggestedDialogFilters'):
        dict.__init__(self, _=_)


class MessagesUpdateDialogFilter(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: int, filter: Optional[aliases.AnyDialogFilter] = ...): ...

    def __init__(self, id, _='messages.updateDialogFilter', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def filter(self) -> Optional[aliases.AnyDialogFilter]:
        return build_object(self['filter'])


class MessagesUpdateDialogFiltersOrder(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, order: list[int]): ...

    def __init__(self, order, _='messages.updateDialogFiltersOrder', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order(self) -> list[int]:
        return self['order']


class MessagesGetOldFeaturedStickers(TLMethod[aliases.AnyMessagesFeaturedStickers]):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, limit: int, hash: int): ...

    def __init__(self, offset, limit, hash, _='messages.getOldFeaturedStickers', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetReplies(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int): ...

    def __init__(self, peer, msg_id, offset_id, offset_date, add_offset, limit, max_id, min_id, hash, _='messages.getReplies', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['offset_id'] = offset_id
        kwargs['offset_date'] = offset_date
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetDiscussionMessage(TLMethod[aliases.AnyMessagesDiscussionMessage]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.getDiscussionMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesReadDiscussion(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, read_max_id: int): ...

    def __init__(self, peer, msg_id, read_max_id, _='messages.readDiscussion', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['read_max_id'] = read_max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def read_max_id(self) -> int:
        return self['read_max_id']


class MessagesUnpinAllMessages(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, _='messages.unpinAllMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])


class MessagesDeleteChat(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='messages.deleteChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class MessagesDeletePhoneCallHistory(TLMethod[aliases.AnyMessagesAffectedFoundMessages]):
    __slots__ = ()

    @overload
    def __init__(self, revoke: Optional[bool] = ...): ...

    def __init__(self, _='messages.deletePhoneCallHistory', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoke(self) -> Optional[bool]:
        return self['revoke']


class MessagesCheckHistoryImport(TLMethod[aliases.AnyMessagesHistoryImportParsed]):
    __slots__ = ()

    @overload
    def __init__(self, import_head: str): ...

    def __init__(self, import_head, _='messages.checkHistoryImport', **kwargs):
        kwargs['import_head'] = import_head
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def import_head(self) -> str:
        return self['import_head']


class MessagesInitHistoryImport(TLMethod[aliases.AnyMessagesHistoryImport]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, file: aliases.AnyInputFile, media_count: int): ...

    def __init__(self, peer, file, media_count, _='messages.initHistoryImport', **kwargs):
        kwargs['peer'] = peer
        kwargs['file'] = file
        kwargs['media_count'] = media_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def media_count(self) -> int:
        return self['media_count']


class MessagesUploadImportedMedia(TLMethod[aliases.AnyMessageMedia]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, import_id: int, file_name: str, media: aliases.AnyInputMedia): ...

    def __init__(self, peer, import_id, file_name, media, _='messages.uploadImportedMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['import_id'] = import_id
        kwargs['file_name'] = file_name
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def import_id(self) -> int:
        return self['import_id']

    @property
    def file_name(self) -> str:
        return self['file_name']

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])


class MessagesStartHistoryImport(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, import_id: int): ...

    def __init__(self, peer, import_id, _='messages.startHistoryImport', **kwargs):
        kwargs['peer'] = peer
        kwargs['import_id'] = import_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def import_id(self) -> int:
        return self['import_id']


class MessagesGetExportedChatInvites(TLMethod[aliases.AnyMessagesExportedChatInvites]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, admin_id: aliases.AnyInputUser, limit: int, revoked: Optional[bool] = ..., offset_date: Optional[int] = ..., offset_link: Optional[str] = ...): ...

    def __init__(self, peer, admin_id, limit, _='messages.getExportedChatInvites', **kwargs):
        kwargs['peer'] = peer
        kwargs['admin_id'] = admin_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoked(self) -> Optional[bool]:
        return self['revoked']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def admin_id(self) -> aliases.AnyInputUser:
        return build_object(self['admin_id'])

    @property
    def offset_date(self) -> Optional[int]:
        return self['offset_date']

    @property
    def offset_link(self) -> Optional[str]:
        return self['offset_link']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetExportedChatInvite(TLMethod[aliases.AnyMessagesExportedChatInvite]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, link: str): ...

    def __init__(self, peer, link, _='messages.getExportedChatInvite', **kwargs):
        kwargs['peer'] = peer
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> str:
        return self['link']


class MessagesEditExportedChatInvite(TLMethod[aliases.AnyMessagesExportedChatInvite]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, link: str, revoked: Optional[bool] = ..., expire_date: Optional[int] = ..., usage_limit: Optional[int] = ..., request_needed: Optional[bool] = ..., title: Optional[str] = ...): ...

    def __init__(self, peer, link, _='messages.editExportedChatInvite', **kwargs):
        kwargs['peer'] = peer
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoked(self) -> Optional[bool]:
        return self['revoked']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> str:
        return self['link']

    @property
    def expire_date(self) -> Optional[int]:
        return self['expire_date']

    @property
    def usage_limit(self) -> Optional[int]:
        return self['usage_limit']

    @property
    def request_needed(self) -> Optional[bool]:
        return self['request_needed']

    @property
    def title(self) -> Optional[str]:
        return self['title']


class MessagesDeleteRevokedExportedChatInvites(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, admin_id: aliases.AnyInputUser): ...

    def __init__(self, peer, admin_id, _='messages.deleteRevokedExportedChatInvites', **kwargs):
        kwargs['peer'] = peer
        kwargs['admin_id'] = admin_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def admin_id(self) -> aliases.AnyInputUser:
        return build_object(self['admin_id'])


class MessagesDeleteExportedChatInvite(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, link: str): ...

    def __init__(self, peer, link, _='messages.deleteExportedChatInvite', **kwargs):
        kwargs['peer'] = peer
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> str:
        return self['link']


class MessagesGetAdminsWithInvites(TLMethod[aliases.AnyMessagesChatAdminsWithInvites]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.getAdminsWithInvites', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesGetChatInviteImporters(TLMethod[aliases.AnyMessagesChatInviteImporters]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_date: int, offset_user: aliases.AnyInputUser, limit: int, requested: Optional[bool] = ..., subscription_expired: Optional[bool] = ..., link: Optional[str] = ..., q: Optional[str] = ...): ...

    def __init__(self, peer, offset_date, offset_user, limit, _='messages.getChatInviteImporters', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_date'] = offset_date
        kwargs['offset_user'] = offset_user
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def requested(self) -> Optional[bool]:
        return self['requested']

    @property
    def subscription_expired(self) -> Optional[bool]:
        return self['subscription_expired']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> Optional[str]:
        return self['link']

    @property
    def q(self) -> Optional[str]:
        return self['q']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def offset_user(self) -> aliases.AnyInputUser:
        return build_object(self['offset_user'])

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesSetHistoryTTL(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, period: int): ...

    def __init__(self, peer, period, _='messages.setHistoryTTL', **kwargs):
        kwargs['peer'] = peer
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def period(self) -> int:
        return self['period']


class MessagesCheckHistoryImportPeer(TLMethod[aliases.AnyMessagesCheckedHistoryImportPeer]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.checkHistoryImportPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesSetChatTheme(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, theme: aliases.AnyInputChatTheme): ...

    def __init__(self, peer, theme, _='messages.setChatTheme', **kwargs):
        kwargs['peer'] = peer
        kwargs['theme'] = theme
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def theme(self) -> aliases.AnyInputChatTheme:
        return build_object(self['theme'])


class MessagesGetMessageReadParticipants(TLMethod[list[aliases.AnyReadParticipantDate]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.getMessageReadParticipants', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesGetSearchResultsCalendar(TLMethod[aliases.AnyMessagesSearchResultsCalendar]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, filter: aliases.AnyMessagesFilter, offset_id: int, offset_date: int, saved_peer_id: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, filter, offset_id, offset_date, _='messages.getSearchResultsCalendar', **kwargs):
        kwargs['peer'] = peer
        kwargs['filter'] = filter
        kwargs['offset_id'] = offset_id
        kwargs['offset_date'] = offset_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_date(self) -> int:
        return self['offset_date']


class MessagesGetSearchResultsPositions(TLMethod[aliases.AnyMessagesSearchResultsPositions]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, filter: aliases.AnyMessagesFilter, offset_id: int, limit: int, saved_peer_id: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, filter, offset_id, limit, _='messages.getSearchResultsPositions', **kwargs):
        kwargs['peer'] = peer
        kwargs['filter'] = filter
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesHideChatJoinRequest(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, user_id: aliases.AnyInputUser, approved: Optional[bool] = ...): ...

    def __init__(self, peer, user_id, _='messages.hideChatJoinRequest', **kwargs):
        kwargs['peer'] = peer
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def approved(self) -> Optional[bool]:
        return self['approved']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class MessagesHideAllChatJoinRequests(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, approved: Optional[bool] = ..., link: Optional[str] = ...): ...

    def __init__(self, peer, _='messages.hideAllChatJoinRequests', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def approved(self) -> Optional[bool]:
        return self['approved']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def link(self) -> Optional[str]:
        return self['link']


class MessagesToggleNoForwards(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, enabled: bool, request_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, enabled, _='messages.toggleNoForwards', **kwargs):
        kwargs['peer'] = peer
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def enabled(self) -> bool:
        return self['enabled']

    @property
    def request_msg_id(self) -> Optional[int]:
        return self['request_msg_id']


class MessagesSaveDefaultSendAs(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, send_as: aliases.AnyInputPeer): ...

    def __init__(self, peer, send_as, _='messages.saveDefaultSendAs', **kwargs):
        kwargs['peer'] = peer
        kwargs['send_as'] = send_as
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def send_as(self) -> aliases.AnyInputPeer:
        return build_object(self['send_as'])


class MessagesSendReaction(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, big: Optional[bool] = ..., add_to_recent: Optional[bool] = ..., reaction: Optional[list[aliases.AnyReaction]] = ...): ...

    def __init__(self, peer, msg_id, _='messages.sendReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def big(self) -> Optional[bool]:
        return self['big']

    @property
    def add_to_recent(self) -> Optional[bool]:
        return self['add_to_recent']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def reaction(self) -> Optional[list[aliases.AnyReaction]]:
        return build_object(self['reaction'])


class MessagesGetMessagesReactions(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='messages.getMessagesReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetMessageReactionsList(TLMethod[aliases.AnyMessagesMessageReactionsList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, limit: int, reaction: Optional[aliases.AnyReaction] = ..., offset: Optional[str] = ...): ...

    def __init__(self, peer, id, limit, _='messages.getMessageReactionsList', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def reaction(self) -> Optional[aliases.AnyReaction]:
        return build_object(self['reaction'])

    @property
    def offset(self) -> Optional[str]:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesSetChatAvailableReactions(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, available_reactions: aliases.AnyChatReactions, reactions_limit: Optional[int] = ..., paid_enabled: Optional[bool] = ...): ...

    def __init__(self, peer, available_reactions, _='messages.setChatAvailableReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['available_reactions'] = available_reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def available_reactions(self) -> aliases.AnyChatReactions:
        return build_object(self['available_reactions'])

    @property
    def reactions_limit(self) -> Optional[int]:
        return self['reactions_limit']

    @property
    def paid_enabled(self) -> Optional[bool]:
        return self['paid_enabled']


class MessagesGetAvailableReactions(TLMethod[aliases.AnyMessagesAvailableReactions]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getAvailableReactions', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSetDefaultReaction(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, reaction: aliases.AnyReaction): ...

    def __init__(self, reaction, _='messages.setDefaultReaction', **kwargs):
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class MessagesTranslateText(TLMethod[aliases.AnyMessagesTranslatedText]):
    __slots__ = ()

    @overload
    def __init__(self, to_lang: str, peer: Optional[aliases.AnyInputPeer] = ..., id: Optional[list[int]] = ..., text: Optional[list[aliases.AnyTextWithEntities]] = ...): ...

    def __init__(self, to_lang, _='messages.translateText', **kwargs):
        kwargs['to_lang'] = to_lang
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def id(self) -> Optional[list[int]]:
        return self['id']

    @property
    def text(self) -> Optional[list[aliases.AnyTextWithEntities]]:
        return build_object(self['text'])

    @property
    def to_lang(self) -> str:
        return self['to_lang']


class MessagesGetUnreadReactions(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, offset_id, add_offset, limit, max_id, min_id, _='messages.getUnreadReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']


class MessagesReadReactions(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, _='messages.readReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['saved_peer_id'])


class MessagesSearchSentMedia(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, filter: aliases.AnyMessagesFilter, limit: int): ...

    def __init__(self, q, filter, limit, _='messages.searchSentMedia', **kwargs):
        kwargs['q'] = q
        kwargs['filter'] = filter
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetAttachMenuBots(TLMethod[aliases.AnyAttachMenuBots]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getAttachMenuBots', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetAttachMenuBot(TLMethod[aliases.AnyAttachMenuBotsBot]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser): ...

    def __init__(self, bot, _='messages.getAttachMenuBot', **kwargs):
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class MessagesToggleBotInAttachMenu(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, enabled: bool, write_allowed: Optional[bool] = ...): ...

    def __init__(self, bot, enabled, _='messages.toggleBotInAttachMenu', **kwargs):
        kwargs['bot'] = bot
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def write_allowed(self) -> Optional[bool]:
        return self['write_allowed']

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class MessagesRequestWebView(TLMethod[aliases.AnyWebViewResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, bot: aliases.AnyInputUser, platform: str, from_bot_menu: Optional[bool] = ..., silent: Optional[bool] = ..., compact: Optional[bool] = ..., fullscreen: Optional[bool] = ..., url: Optional[str] = ..., start_param: Optional[str] = ..., theme_params: Optional[aliases.AnyDataJSON] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., send_as: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, bot, platform, _='messages.requestWebView', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot'] = bot
        kwargs['platform'] = platform
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def from_bot_menu(self) -> Optional[bool]:
        return self['from_bot_menu']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def compact(self) -> Optional[bool]:
        return self['compact']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def start_param(self) -> Optional[str]:
        return self['start_param']

    @property
    def theme_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['theme_params'])

    @property
    def platform(self) -> str:
        return self['platform']

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])


class MessagesProlongWebView(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, bot: aliases.AnyInputUser, query_id: int, silent: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., send_as: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, bot, query_id, _='messages.prolongWebView', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot'] = bot
        kwargs['query_id'] = query_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])


class MessagesRequestSimpleWebView(TLMethod[aliases.AnyWebViewResult]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, platform: str, from_switch_webview: Optional[bool] = ..., from_side_menu: Optional[bool] = ..., compact: Optional[bool] = ..., fullscreen: Optional[bool] = ..., url: Optional[str] = ..., start_param: Optional[str] = ..., theme_params: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, bot, platform, _='messages.requestSimpleWebView', **kwargs):
        kwargs['bot'] = bot
        kwargs['platform'] = platform
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def from_switch_webview(self) -> Optional[bool]:
        return self['from_switch_webview']

    @property
    def from_side_menu(self) -> Optional[bool]:
        return self['from_side_menu']

    @property
    def compact(self) -> Optional[bool]:
        return self['compact']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def start_param(self) -> Optional[str]:
        return self['start_param']

    @property
    def theme_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['theme_params'])

    @property
    def platform(self) -> str:
        return self['platform']


class MessagesSendWebViewResultMessage(TLMethod[aliases.AnyWebViewMessageSent]):
    __slots__ = ()

    @overload
    def __init__(self, bot_query_id: str, result: aliases.AnyInputBotInlineResult): ...

    def __init__(self, bot_query_id, result, _='messages.sendWebViewResultMessage', **kwargs):
        kwargs['bot_query_id'] = bot_query_id
        kwargs['result'] = result
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_query_id(self) -> str:
        return self['bot_query_id']

    @property
    def result(self) -> aliases.AnyInputBotInlineResult:
        return build_object(self['result'])


class MessagesSendWebViewData(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, random_id: int, button_text: str, data: str): ...

    def __init__(self, bot, random_id, button_text, data, _='messages.sendWebViewData', **kwargs):
        kwargs['bot'] = bot
        kwargs['random_id'] = random_id
        kwargs['button_text'] = button_text
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def button_text(self) -> str:
        return self['button_text']

    @property
    def data(self) -> str:
        return self['data']


class MessagesTranscribeAudio(TLMethod[aliases.AnyMessagesTranscribedAudio]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.transcribeAudio', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesRateTranscribedAudio(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, transcription_id: int, good: bool): ...

    def __init__(self, peer, msg_id, transcription_id, good, _='messages.rateTranscribedAudio', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['transcription_id'] = transcription_id
        kwargs['good'] = good
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def transcription_id(self) -> int:
        return self['transcription_id']

    @property
    def good(self) -> bool:
        return self['good']


class MessagesGetCustomEmojiDocuments(TLMethod[list[aliases.AnyDocument]]):
    __slots__ = ()

    @overload
    def __init__(self, document_id: list[int]): ...

    def __init__(self, document_id, _='messages.getCustomEmojiDocuments', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> list[int]:
        return self['document_id']


class MessagesGetEmojiStickers(TLMethod[aliases.AnyMessagesAllStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getEmojiStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetFeaturedEmojiStickers(TLMethod[aliases.AnyMessagesFeaturedStickers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getFeaturedEmojiStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesReportReaction(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, reaction_peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, id, reaction_peer, _='messages.reportReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['reaction_peer'] = reaction_peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def reaction_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['reaction_peer'])


class MessagesGetTopReactions(TLMethod[aliases.AnyMessagesReactions]):
    __slots__ = ()

    @overload
    def __init__(self, limit: int, hash: int): ...

    def __init__(self, limit, hash, _='messages.getTopReactions', **kwargs):
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetRecentReactions(TLMethod[aliases.AnyMessagesReactions]):
    __slots__ = ()

    @overload
    def __init__(self, limit: int, hash: int): ...

    def __init__(self, limit, hash, _='messages.getRecentReactions', **kwargs):
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesClearRecentReactions(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.clearRecentReactions'):
        dict.__init__(self, _=_)


class MessagesGetExtendedMedia(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='messages.getExtendedMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesSetDefaultHistoryTTL(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, period: int): ...

    def __init__(self, period, _='messages.setDefaultHistoryTTL', **kwargs):
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> int:
        return self['period']


class MessagesGetDefaultHistoryTTL(TLMethod[aliases.AnyDefaultHistoryTTL]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getDefaultHistoryTTL'):
        dict.__init__(self, _=_)


class MessagesSendBotRequestedPeer(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, button_id: int, requested_peers: list[aliases.AnyInputPeer]): ...

    def __init__(self, peer, msg_id, button_id, requested_peers, _='messages.sendBotRequestedPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['button_id'] = button_id
        kwargs['requested_peers'] = requested_peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def button_id(self) -> int:
        return self['button_id']

    @property
    def requested_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['requested_peers'])


class MessagesGetEmojiGroups(TLMethod[aliases.AnyMessagesEmojiGroups]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getEmojiGroups', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetEmojiStatusGroups(TLMethod[aliases.AnyMessagesEmojiGroups]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getEmojiStatusGroups', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetEmojiProfilePhotoGroups(TLMethod[aliases.AnyMessagesEmojiGroups]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getEmojiProfilePhotoGroups', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSearchCustomEmoji(TLMethod[aliases.AnyEmojiList]):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str, hash: int): ...

    def __init__(self, emoticon, hash, _='messages.searchCustomEmoji', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesTogglePeerTranslations(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, disabled: Optional[bool] = ...): ...

    def __init__(self, peer, _='messages.togglePeerTranslations', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def disabled(self) -> Optional[bool]:
        return self['disabled']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesGetBotApp(TLMethod[aliases.AnyMessagesBotApp]):
    __slots__ = ()

    @overload
    def __init__(self, app: aliases.AnyInputBotApp, hash: int): ...

    def __init__(self, app, hash, _='messages.getBotApp', **kwargs):
        kwargs['app'] = app
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def app(self) -> aliases.AnyInputBotApp:
        return build_object(self['app'])

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesRequestAppWebView(TLMethod[aliases.AnyWebViewResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, app: aliases.AnyInputBotApp, platform: str, write_allowed: Optional[bool] = ..., compact: Optional[bool] = ..., fullscreen: Optional[bool] = ..., start_param: Optional[str] = ..., theme_params: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, peer, app, platform, _='messages.requestAppWebView', **kwargs):
        kwargs['peer'] = peer
        kwargs['app'] = app
        kwargs['platform'] = platform
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def write_allowed(self) -> Optional[bool]:
        return self['write_allowed']

    @property
    def compact(self) -> Optional[bool]:
        return self['compact']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def app(self) -> aliases.AnyInputBotApp:
        return build_object(self['app'])

    @property
    def start_param(self) -> Optional[str]:
        return self['start_param']

    @property
    def theme_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['theme_params'])

    @property
    def platform(self) -> str:
        return self['platform']


class MessagesSetChatWallPaper(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, for_both: Optional[bool] = ..., revert: Optional[bool] = ..., wallpaper: Optional[aliases.AnyInputWallPaper] = ..., settings: Optional[aliases.AnyWallPaperSettings] = ..., id: Optional[int] = ...): ...

    def __init__(self, peer, _='messages.setChatWallPaper', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_both(self) -> Optional[bool]:
        return self['for_both']

    @property
    def revert(self) -> Optional[bool]:
        return self['revert']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def wallpaper(self) -> Optional[aliases.AnyInputWallPaper]:
        return build_object(self['wallpaper'])

    @property
    def settings(self) -> Optional[aliases.AnyWallPaperSettings]:
        return build_object(self['settings'])

    @property
    def id(self) -> Optional[int]:
        return self['id']


class MessagesSearchEmojiStickerSets(TLMethod[aliases.AnyMessagesFoundStickerSets]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, hash: int, exclude_featured: Optional[bool] = ...): ...

    def __init__(self, q, hash, _='messages.searchEmojiStickerSets', **kwargs):
        kwargs['q'] = q
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_featured(self) -> Optional[bool]:
        return self['exclude_featured']

    @property
    def q(self) -> str:
        return self['q']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetSavedDialogs(TLMethod[aliases.AnyMessagesSavedDialogs]):
    __slots__ = ()

    @overload
    def __init__(self, offset_date: int, offset_id: int, offset_peer: aliases.AnyInputPeer, limit: int, hash: int, exclude_pinned: Optional[bool] = ..., parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, offset_date, offset_id, offset_peer, limit, hash, _='messages.getSavedDialogs', **kwargs):
        kwargs['offset_date'] = offset_date
        kwargs['offset_id'] = offset_id
        kwargs['offset_peer'] = offset_peer
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_pinned(self) -> Optional[bool]:
        return self['exclude_pinned']

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['offset_peer'])

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetSavedHistory(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int, parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, offset_id, offset_date, add_offset, limit, max_id, min_id, hash, _='messages.getSavedHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['offset_date'] = offset_date
        kwargs['add_offset'] = add_offset
        kwargs['limit'] = limit
        kwargs['max_id'] = max_id
        kwargs['min_id'] = min_id
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def add_offset(self) -> int:
        return self['add_offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesDeleteSavedHistory(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, max_id: int, parent_peer: Optional[aliases.AnyInputPeer] = ..., min_date: Optional[int] = ..., max_date: Optional[int] = ...): ...

    def __init__(self, peer, max_id, _='messages.deleteSavedHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def min_date(self) -> Optional[int]:
        return self['min_date']

    @property
    def max_date(self) -> Optional[int]:
        return self['max_date']


class MessagesGetPinnedSavedDialogs(TLMethod[aliases.AnyMessagesSavedDialogs]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getPinnedSavedDialogs'):
        dict.__init__(self, _=_)


class MessagesToggleSavedDialogPin(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputDialogPeer, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, _='messages.toggleSavedDialogPin', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyInputDialogPeer:
        return build_object(self['peer'])


class MessagesReorderPinnedSavedDialogs(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, order: list[aliases.AnyInputDialogPeer], force: Optional[bool] = ...): ...

    def __init__(self, order, _='messages.reorderPinnedSavedDialogs', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def order(self) -> list[aliases.AnyInputDialogPeer]:
        return build_object(self['order'])


class MessagesGetSavedReactionTags(TLMethod[aliases.AnyMessagesSavedReactionTags]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, hash, _='messages.getSavedReactionTags', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesUpdateSavedReactionTag(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, reaction: aliases.AnyReaction, title: Optional[str] = ...): ...

    def __init__(self, reaction, _='messages.updateSavedReactionTag', **kwargs):
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])

    @property
    def title(self) -> Optional[str]:
        return self['title']


class MessagesGetDefaultTagReactions(TLMethod[aliases.AnyMessagesReactions]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getDefaultTagReactions', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetOutboxReadDate(TLMethod[aliases.AnyOutboxReadDate]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.getOutboxReadDate', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesGetQuickReplies(TLMethod[aliases.AnyMessagesQuickReplies]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getQuickReplies', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesReorderQuickReplies(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, order: list[int]): ...

    def __init__(self, order, _='messages.reorderQuickReplies', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order(self) -> list[int]:
        return self['order']


class MessagesCheckQuickReplyShortcut(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, shortcut: str): ...

    def __init__(self, shortcut, _='messages.checkQuickReplyShortcut', **kwargs):
        kwargs['shortcut'] = shortcut
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut(self) -> str:
        return self['shortcut']


class MessagesEditQuickReplyShortcut(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, shortcut: str): ...

    def __init__(self, shortcut_id, shortcut, _='messages.editQuickReplyShortcut', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['shortcut'] = shortcut
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def shortcut(self) -> str:
        return self['shortcut']


class MessagesDeleteQuickReplyShortcut(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int): ...

    def __init__(self, shortcut_id, _='messages.deleteQuickReplyShortcut', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']


class MessagesGetQuickReplyMessages(TLMethod[aliases.AnyMessagesMessages]):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, hash: int, id: Optional[list[int]] = ...): ...

    def __init__(self, shortcut_id, hash, _='messages.getQuickReplyMessages', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def id(self) -> Optional[list[int]]:
        return self['id']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesSendQuickReplyMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, shortcut_id: int, id: list[int], random_id: list[int]): ...

    def __init__(self, peer, shortcut_id, id, random_id, _='messages.sendQuickReplyMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['shortcut_id'] = shortcut_id
        kwargs['id'] = id
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def id(self) -> list[int]:
        return self['id']

    @property
    def random_id(self) -> list[int]:
        return self['random_id']


class MessagesDeleteQuickReplyMessages(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, id: list[int]): ...

    def __init__(self, shortcut_id, id, _='messages.deleteQuickReplyMessages', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesToggleDialogFilterTags(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, enabled: bool): ...

    def __init__(self, enabled, _='messages.toggleDialogFilterTags', **kwargs):
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def enabled(self) -> bool:
        return self['enabled']


class MessagesGetMyStickers(TLMethod[aliases.AnyMessagesMyStickers]):
    __slots__ = ()

    @overload
    def __init__(self, offset_id: int, limit: int): ...

    def __init__(self, offset_id, limit, _='messages.getMyStickers', **kwargs):
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetEmojiStickerGroups(TLMethod[aliases.AnyMessagesEmojiGroups]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getEmojiStickerGroups', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesGetAvailableEffects(TLMethod[aliases.AnyMessagesAvailableEffects]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='messages.getAvailableEffects', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesEditFactCheck(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, text: aliases.AnyTextWithEntities): ...

    def __init__(self, peer, msg_id, text, _='messages.editFactCheck', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def text(self) -> aliases.AnyTextWithEntities:
        return build_object(self['text'])


class MessagesDeleteFactCheck(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='messages.deleteFactCheck', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MessagesGetFactCheck(TLMethod[list[aliases.AnyFactCheck]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: list[int]): ...

    def __init__(self, peer, msg_id, _='messages.getFactCheck', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> list[int]:
        return self['msg_id']


class MessagesRequestMainWebView(TLMethod[aliases.AnyWebViewResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, bot: aliases.AnyInputUser, platform: str, compact: Optional[bool] = ..., fullscreen: Optional[bool] = ..., start_param: Optional[str] = ..., theme_params: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, peer, bot, platform, _='messages.requestMainWebView', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot'] = bot
        kwargs['platform'] = platform
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def compact(self) -> Optional[bool]:
        return self['compact']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def start_param(self) -> Optional[str]:
        return self['start_param']

    @property
    def theme_params(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['theme_params'])

    @property
    def platform(self) -> str:
        return self['platform']


class MessagesSendPaidReaction(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, count: int, random_id: int, private: Optional[aliases.AnyPaidReactionPrivacy] = ...): ...

    def __init__(self, peer, msg_id, count, random_id, _='messages.sendPaidReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['count'] = count
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def private(self) -> Optional[aliases.AnyPaidReactionPrivacy]:
        return build_object(self['private'])


class MessagesTogglePaidReactionPrivacy(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, private: aliases.AnyPaidReactionPrivacy): ...

    def __init__(self, peer, msg_id, private, _='messages.togglePaidReactionPrivacy', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['private'] = private
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def private(self) -> aliases.AnyPaidReactionPrivacy:
        return build_object(self['private'])


class MessagesGetPaidReactionPrivacy(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getPaidReactionPrivacy'):
        dict.__init__(self, _=_)


class MessagesViewSponsoredMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, random_id: bytes): ...

    def __init__(self, random_id, _='messages.viewSponsoredMessage', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> bytes:
        return self['random_id']


class MessagesClickSponsoredMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, random_id: bytes, media: Optional[bool] = ..., fullscreen: Optional[bool] = ...): ...

    def __init__(self, random_id, _='messages.clickSponsoredMessage', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> Optional[bool]:
        return self['media']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def random_id(self) -> bytes:
        return self['random_id']


class MessagesReportSponsoredMessage(TLMethod[aliases.AnyChannelsSponsoredMessageReportResult]):
    __slots__ = ()

    @overload
    def __init__(self, random_id: bytes, option: bytes): ...

    def __init__(self, random_id, option, _='messages.reportSponsoredMessage', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> bytes:
        return self['random_id']

    @property
    def option(self) -> bytes:
        return self['option']


class MessagesGetSponsoredMessages(TLMethod[aliases.AnyMessagesSponsoredMessages]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: Optional[int] = ...): ...

    def __init__(self, peer, _='messages.getSponsoredMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> Optional[int]:
        return self['msg_id']


class MessagesSavePreparedInlineMessage(TLMethod[aliases.AnyMessagesBotPreparedInlineMessage]):
    __slots__ = ()

    @overload
    def __init__(self, result: aliases.AnyInputBotInlineResult, user_id: aliases.AnyInputUser, peer_types: Optional[list[aliases.AnyInlineQueryPeerType]] = ...): ...

    def __init__(self, result, user_id, _='messages.savePreparedInlineMessage', **kwargs):
        kwargs['result'] = result
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def result(self) -> aliases.AnyInputBotInlineResult:
        return build_object(self['result'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def peer_types(self) -> Optional[list[aliases.AnyInlineQueryPeerType]]:
        return build_object(self['peer_types'])


class MessagesGetPreparedInlineMessage(TLMethod[aliases.AnyMessagesPreparedInlineMessage]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, id: str): ...

    def __init__(self, bot, id, _='messages.getPreparedInlineMessage', **kwargs):
        kwargs['bot'] = bot
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def id(self) -> str:
        return self['id']


class MessagesSearchStickers(TLMethod[aliases.AnyMessagesFoundStickers]):
    __slots__ = ()

    @overload
    def __init__(self, q: str, emoticon: str, lang_code: list[str], offset: int, limit: int, hash: int, emojis: Optional[bool] = ...): ...

    def __init__(self, q, emoticon, lang_code, offset, limit, hash, _='messages.searchStickers', **kwargs):
        kwargs['q'] = q
        kwargs['emoticon'] = emoticon
        kwargs['lang_code'] = lang_code
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def q(self) -> str:
        return self['q']

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def lang_code(self) -> list[str]:
        return self['lang_code']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesReportMessagesDelivery(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int], push: Optional[bool] = ...): ...

    def __init__(self, peer, id, _='messages.reportMessagesDelivery', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def push(self) -> Optional[bool]:
        return self['push']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']


class MessagesGetSavedDialogsByID(TLMethod[aliases.AnyMessagesSavedDialogs]):
    __slots__ = ()

    @overload
    def __init__(self, ids: list[aliases.AnyInputPeer], parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, ids, _='messages.getSavedDialogsByID', **kwargs):
        kwargs['ids'] = ids
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def ids(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['ids'])


class MessagesReadSavedHistory(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, parent_peer: aliases.AnyInputPeer, peer: aliases.AnyInputPeer, max_id: int): ...

    def __init__(self, parent_peer, peer, max_id, _='messages.readSavedHistory', **kwargs):
        kwargs['parent_peer'] = parent_peer
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['parent_peer'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']


class MessagesToggleTodoCompleted(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, completed: list[int], incompleted: list[int]): ...

    def __init__(self, peer, msg_id, completed, incompleted, _='messages.toggleTodoCompleted', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['completed'] = completed
        kwargs['incompleted'] = incompleted
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def completed(self) -> list[int]:
        return self['completed']

    @property
    def incompleted(self) -> list[int]:
        return self['incompleted']


class MessagesAppendTodoList(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, list: list[aliases.AnyTodoItem]): ...

    def __init__(self, peer, msg_id, list, _='messages.appendTodoList', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['list'] = list
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def list(self) -> list[aliases.AnyTodoItem]:
        return build_object(self['list'])


class MessagesToggleSuggestedPostApproval(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, reject: Optional[bool] = ..., schedule_date: Optional[int] = ..., reject_comment: Optional[str] = ...): ...

    def __init__(self, peer, msg_id, _='messages.toggleSuggestedPostApproval', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reject(self) -> Optional[bool]:
        return self['reject']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def reject_comment(self) -> Optional[str]:
        return self['reject_comment']


class MessagesGetForumTopics(TLMethod[aliases.AnyMessagesForumTopics]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_date: int, offset_id: int, offset_topic: int, limit: int, q: Optional[str] = ...): ...

    def __init__(self, peer, offset_date, offset_id, offset_topic, limit, _='messages.getForumTopics', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_date'] = offset_date
        kwargs['offset_id'] = offset_id
        kwargs['offset_topic'] = offset_topic
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def q(self) -> Optional[str]:
        return self['q']

    @property
    def offset_date(self) -> int:
        return self['offset_date']

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def offset_topic(self) -> int:
        return self['offset_topic']

    @property
    def limit(self) -> int:
        return self['limit']


class MessagesGetForumTopicsByID(TLMethod[aliases.AnyMessagesForumTopics]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, topics: list[int]): ...

    def __init__(self, peer, topics, _='messages.getForumTopicsByID', **kwargs):
        kwargs['peer'] = peer
        kwargs['topics'] = topics
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def topics(self) -> list[int]:
        return self['topics']


class MessagesEditForumTopic(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, topic_id: int, title: Optional[str] = ..., icon_emoji_id: Optional[int] = ..., closed: Optional[bool] = ..., hidden: Optional[bool] = ...): ...

    def __init__(self, peer, topic_id, _='messages.editForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['topic_id'] = topic_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def topic_id(self) -> int:
        return self['topic_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def icon_emoji_id(self) -> Optional[int]:
        return self['icon_emoji_id']

    @property
    def closed(self) -> Optional[bool]:
        return self['closed']

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']


class MessagesUpdatePinnedForumTopic(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, topic_id: int, pinned: bool): ...

    def __init__(self, peer, topic_id, pinned, _='messages.updatePinnedForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['topic_id'] = topic_id
        kwargs['pinned'] = pinned
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def topic_id(self) -> int:
        return self['topic_id']

    @property
    def pinned(self) -> bool:
        return self['pinned']


class MessagesReorderPinnedForumTopics(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, order: list[int], force: Optional[bool] = ...): ...

    def __init__(self, peer, order, _='messages.reorderPinnedForumTopics', **kwargs):
        kwargs['peer'] = peer
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def order(self) -> list[int]:
        return self['order']


class MessagesCreateForumTopic(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, title: str, random_id: int, title_missing: Optional[bool] = ..., icon_color: Optional[int] = ..., icon_emoji_id: Optional[int] = ..., send_as: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, peer, title, random_id, _='messages.createForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['title'] = title
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title_missing(self) -> Optional[bool]:
        return self['title_missing']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_color(self) -> Optional[int]:
        return self['icon_color']

    @property
    def icon_emoji_id(self) -> Optional[int]:
        return self['icon_emoji_id']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def send_as(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['send_as'])


class MessagesDeleteTopicHistory(TLMethod[aliases.AnyMessagesAffectedHistory]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, top_msg_id: int): ...

    def __init__(self, peer, top_msg_id, _='messages.deleteTopicHistory', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_msg_id'] = top_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> int:
        return self['top_msg_id']


class MessagesGetEmojiGameInfo(TLMethod[aliases.AnyMessagesEmojiGameInfo]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.getEmojiGameInfo'):
        dict.__init__(self, _=_)


class MessagesSummarizeText(TLMethod[aliases.AnyTextWithEntities]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, to_lang: Optional[str] = ...): ...

    def __init__(self, peer, id, _='messages.summarizeText', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def to_lang(self) -> Optional[str]:
        return self['to_lang']


class MessagesEditChatCreator(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, user_id: aliases.AnyInputUser, password: aliases.AnyInputCheckPasswordSRP): ...

    def __init__(self, peer, user_id, password, _='messages.editChatCreator', **kwargs):
        kwargs['peer'] = peer
        kwargs['user_id'] = user_id
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])


class MessagesGetFutureChatCreatorAfterLeave(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='messages.getFutureChatCreatorAfterLeave', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class MessagesEditChatParticipantRank(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, participant: aliases.AnyInputPeer, rank: str): ...

    def __init__(self, peer, participant, rank, _='messages.editChatParticipantRank', **kwargs):
        kwargs['peer'] = peer
        kwargs['participant'] = participant
        kwargs['rank'] = rank
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def participant(self) -> aliases.AnyInputPeer:
        return build_object(self['participant'])

    @property
    def rank(self) -> str:
        return self['rank']


class MessagesDeclineUrlAuth(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='messages.declineUrlAuth', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class MessagesCheckUrlAuthMatchCode(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, url: str, match_code: str): ...

    def __init__(self, url, match_code, _='messages.checkUrlAuthMatchCode', **kwargs):
        kwargs['url'] = url
        kwargs['match_code'] = match_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def match_code(self) -> str:
        return self['match_code']
