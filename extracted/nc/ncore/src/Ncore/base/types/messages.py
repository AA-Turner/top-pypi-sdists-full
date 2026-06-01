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


class MessagesDialogs(dict):
    __slots__ = ()

    @overload
    def __init__(self, dialogs: list[aliases.AnyDialog], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, dialogs, messages, chats, users, _='messages.dialogs', **kwargs):
        kwargs['dialogs'] = dialogs
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dialogs(self) -> list[aliases.AnyDialog]:
        return build_object(self['dialogs'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesDialogsSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, dialogs: list[aliases.AnyDialog], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, count, dialogs, messages, chats, users, _='messages.dialogsSlice', **kwargs):
        kwargs['count'] = count
        kwargs['dialogs'] = dialogs
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def dialogs(self) -> list[aliases.AnyDialog]:
        return build_object(self['dialogs'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesDialogsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int): ...

    def __init__(self, count, _='messages.dialogsNotModified', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']


class MessagesMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, messages: list[aliases.AnyMessage], topics: list[aliases.AnyForumTopic], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, messages, topics, chats, users, _='messages.messages', **kwargs):
        kwargs['messages'] = messages
        kwargs['topics'] = topics
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def topics(self) -> list[aliases.AnyForumTopic]:
        return build_object(self['topics'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesMessagesSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, messages: list[aliases.AnyMessage], topics: list[aliases.AnyForumTopic], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], inexact: Optional[bool] = ..., next_rate: Optional[int] = ..., offset_id_offset: Optional[int] = ..., search_flood: Optional[aliases.AnySearchPostsFlood] = ...): ...

    def __init__(self, count, messages, topics, chats, users, _='messages.messagesSlice', **kwargs):
        kwargs['count'] = count
        kwargs['messages'] = messages
        kwargs['topics'] = topics
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inexact(self) -> Optional[bool]:
        return self['inexact']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def next_rate(self) -> Optional[int]:
        return self['next_rate']

    @property
    def offset_id_offset(self) -> Optional[int]:
        return self['offset_id_offset']

    @property
    def search_flood(self) -> Optional[aliases.AnySearchPostsFlood]:
        return build_object(self['search_flood'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def topics(self) -> list[aliases.AnyForumTopic]:
        return build_object(self['topics'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesChannelMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, count: int, messages: list[aliases.AnyMessage], topics: list[aliases.AnyForumTopic], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], inexact: Optional[bool] = ..., offset_id_offset: Optional[int] = ...): ...

    def __init__(self, pts, count, messages, topics, chats, users, _='messages.channelMessages', **kwargs):
        kwargs['pts'] = pts
        kwargs['count'] = count
        kwargs['messages'] = messages
        kwargs['topics'] = topics
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inexact(self) -> Optional[bool]:
        return self['inexact']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def offset_id_offset(self) -> Optional[int]:
        return self['offset_id_offset']

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def topics(self) -> list[aliases.AnyForumTopic]:
        return build_object(self['topics'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesMessagesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int): ...

    def __init__(self, count, _='messages.messagesNotModified', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']


class MessagesChats(dict):
    __slots__ = ()

    @overload
    def __init__(self, chats: list[aliases.AnyChat]): ...

    def __init__(self, chats, _='messages.chats', **kwargs):
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])


class MessagesChatsSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, chats: list[aliases.AnyChat]): ...

    def __init__(self, count, chats, _='messages.chatsSlice', **kwargs):
        kwargs['count'] = count
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])


class MessagesChatFull(dict):
    __slots__ = ()

    @overload
    def __init__(self, full_chat: aliases.AnyChatFull, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, full_chat, chats, users, _='messages.chatFull', **kwargs):
        kwargs['full_chat'] = full_chat
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def full_chat(self) -> aliases.AnyChatFull:
        return build_object(self['full_chat'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesAffectedHistory(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, pts_count: int, offset: int): ...

    def __init__(self, pts, pts_count, offset, _='messages.affectedHistory', **kwargs):
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def offset(self) -> int:
        return self['offset']


class MessagesDhConfigNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, random: bytes): ...

    def __init__(self, random, _='messages.dhConfigNotModified', **kwargs):
        kwargs['random'] = random
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random(self) -> bytes:
        return self['random']


class MessagesDhConfig(dict):
    __slots__ = ()

    @overload
    def __init__(self, g: int, p: bytes, version: int, random: bytes): ...

    def __init__(self, g, p, version, random, _='messages.dhConfig', **kwargs):
        kwargs['g'] = g
        kwargs['p'] = p
        kwargs['version'] = version
        kwargs['random'] = random
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def g(self) -> int:
        return self['g']

    @property
    def p(self) -> bytes:
        return self['p']

    @property
    def version(self) -> int:
        return self['version']

    @property
    def random(self) -> bytes:
        return self['random']


class MessagesSentEncryptedMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int): ...

    def __init__(self, date, _='messages.sentEncryptedMessage', **kwargs):
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']


class MessagesSentEncryptedFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, file: aliases.AnyEncryptedFile): ...

    def __init__(self, date, file, _='messages.sentEncryptedFile', **kwargs):
        kwargs['date'] = date
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def file(self) -> aliases.AnyEncryptedFile:
        return build_object(self['file'])


class MessagesStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.stickersNotModified'):
        dict.__init__(self, _=_)


class MessagesStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, stickers: list[aliases.AnyDocument]): ...

    def __init__(self, hash, stickers, _='messages.stickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['stickers'] = stickers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def stickers(self) -> list[aliases.AnyDocument]:
        return build_object(self['stickers'])


class MessagesAllStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.allStickersNotModified'):
        dict.__init__(self, _=_)


class MessagesAllStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, sets: list[aliases.AnyStickerSet]): ...

    def __init__(self, hash, sets, _='messages.allStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['sets'] = sets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def sets(self) -> list[aliases.AnyStickerSet]:
        return build_object(self['sets'])


class MessagesAffectedMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, pts_count: int): ...

    def __init__(self, pts, pts_count, _='messages.affectedMessages', **kwargs):
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class MessagesStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, set: aliases.AnyStickerSet, packs: list[aliases.AnyStickerPack], keywords: list[aliases.AnyStickerKeyword], documents: list[aliases.AnyDocument]): ...

    def __init__(self, set, packs, keywords, documents, _='messages.stickerSet', **kwargs):
        kwargs['set'] = set
        kwargs['packs'] = packs
        kwargs['keywords'] = keywords
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def set(self) -> aliases.AnyStickerSet:
        return build_object(self['set'])

    @property
    def packs(self) -> list[aliases.AnyStickerPack]:
        return build_object(self['packs'])

    @property
    def keywords(self) -> list[aliases.AnyStickerKeyword]:
        return build_object(self['keywords'])

    @property
    def documents(self) -> list[aliases.AnyDocument]:
        return build_object(self['documents'])


class MessagesStickerSetNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.stickerSetNotModified'):
        dict.__init__(self, _=_)


class MessagesSavedGifsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.savedGifsNotModified'):
        dict.__init__(self, _=_)


class MessagesSavedGifs(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, gifs: list[aliases.AnyDocument]): ...

    def __init__(self, hash, gifs, _='messages.savedGifs', **kwargs):
        kwargs['hash'] = hash
        kwargs['gifs'] = gifs
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def gifs(self) -> list[aliases.AnyDocument]:
        return build_object(self['gifs'])


class MessagesBotResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, results: list[aliases.AnyBotInlineResult], cache_time: int, users: list[aliases.AnyUser], gallery: Optional[bool] = ..., next_offset: Optional[str] = ..., switch_pm: Optional[aliases.AnyInlineBotSwitchPM] = ..., switch_webview: Optional[aliases.AnyInlineBotWebView] = ...): ...

    def __init__(self, query_id, results, cache_time, users, _='messages.botResults', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['results'] = results
        kwargs['cache_time'] = cache_time
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gallery(self) -> Optional[bool]:
        return self['gallery']

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def switch_pm(self) -> Optional[aliases.AnyInlineBotSwitchPM]:
        return build_object(self['switch_pm'])

    @property
    def switch_webview(self) -> Optional[aliases.AnyInlineBotWebView]:
        return build_object(self['switch_webview'])

    @property
    def results(self) -> list[aliases.AnyBotInlineResult]:
        return build_object(self['results'])

    @property
    def cache_time(self) -> int:
        return self['cache_time']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesBotCallbackAnswer(dict):
    __slots__ = ()

    @overload
    def __init__(self, cache_time: int, alert: Optional[bool] = ..., has_url: Optional[bool] = ..., native_ui: Optional[bool] = ..., message: Optional[str] = ..., url: Optional[str] = ...): ...

    def __init__(self, cache_time, _='messages.botCallbackAnswer', **kwargs):
        kwargs['cache_time'] = cache_time
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def alert(self) -> Optional[bool]:
        return self['alert']

    @property
    def has_url(self) -> Optional[bool]:
        return self['has_url']

    @property
    def native_ui(self) -> Optional[bool]:
        return self['native_ui']

    @property
    def message(self) -> Optional[str]:
        return self['message']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def cache_time(self) -> int:
        return self['cache_time']


class MessagesMessageEditData(dict):
    __slots__ = ()

    @overload
    def __init__(self, caption: Optional[bool] = ...): ...

    def __init__(self, _='messages.messageEditData', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def caption(self) -> Optional[bool]:
        return self['caption']


class MessagesPeerDialogs(dict):
    __slots__ = ()

    @overload
    def __init__(self, dialogs: list[aliases.AnyDialog], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], state: aliases.AnyUpdatesState): ...

    def __init__(self, dialogs, messages, chats, users, state, _='messages.peerDialogs', **kwargs):
        kwargs['dialogs'] = dialogs
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['state'] = state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dialogs(self) -> list[aliases.AnyDialog]:
        return build_object(self['dialogs'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def state(self) -> aliases.AnyUpdatesState:
        return build_object(self['state'])


class MessagesFeaturedStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int): ...

    def __init__(self, count, _='messages.featuredStickersNotModified', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']


class MessagesFeaturedStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, count: int, sets: list[aliases.AnyStickerSetCovered], unread: list[int], premium: Optional[bool] = ...): ...

    def __init__(self, hash, count, sets, unread, _='messages.featuredStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['count'] = count
        kwargs['sets'] = sets
        kwargs['unread'] = unread
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def premium(self) -> Optional[bool]:
        return self['premium']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def sets(self) -> list[aliases.AnyStickerSetCovered]:
        return build_object(self['sets'])

    @property
    def unread(self) -> list[int]:
        return self['unread']


class MessagesRecentStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.recentStickersNotModified'):
        dict.__init__(self, _=_)


class MessagesRecentStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, packs: list[aliases.AnyStickerPack], stickers: list[aliases.AnyDocument], dates: list[int]): ...

    def __init__(self, hash, packs, stickers, dates, _='messages.recentStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['packs'] = packs
        kwargs['stickers'] = stickers
        kwargs['dates'] = dates
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def packs(self) -> list[aliases.AnyStickerPack]:
        return build_object(self['packs'])

    @property
    def stickers(self) -> list[aliases.AnyDocument]:
        return build_object(self['stickers'])

    @property
    def dates(self) -> list[int]:
        return self['dates']


class MessagesArchivedStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, sets: list[aliases.AnyStickerSetCovered]): ...

    def __init__(self, count, sets, _='messages.archivedStickers', **kwargs):
        kwargs['count'] = count
        kwargs['sets'] = sets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def sets(self) -> list[aliases.AnyStickerSetCovered]:
        return build_object(self['sets'])


class MessagesStickerSetInstallResultSuccess(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.stickerSetInstallResultSuccess'):
        dict.__init__(self, _=_)


class MessagesStickerSetInstallResultArchive(dict):
    __slots__ = ()

    @overload
    def __init__(self, sets: list[aliases.AnyStickerSetCovered]): ...

    def __init__(self, sets, _='messages.stickerSetInstallResultArchive', **kwargs):
        kwargs['sets'] = sets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sets(self) -> list[aliases.AnyStickerSetCovered]:
        return build_object(self['sets'])


class MessagesHighScores(dict):
    __slots__ = ()

    @overload
    def __init__(self, scores: list[aliases.AnyHighScore], users: list[aliases.AnyUser]): ...

    def __init__(self, scores, users, _='messages.highScores', **kwargs):
        kwargs['scores'] = scores
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def scores(self) -> list[aliases.AnyHighScore]:
        return build_object(self['scores'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesFavedStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.favedStickersNotModified'):
        dict.__init__(self, _=_)


class MessagesFavedStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, packs: list[aliases.AnyStickerPack], stickers: list[aliases.AnyDocument]): ...

    def __init__(self, hash, packs, stickers, _='messages.favedStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['packs'] = packs
        kwargs['stickers'] = stickers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def packs(self) -> list[aliases.AnyStickerPack]:
        return build_object(self['packs'])

    @property
    def stickers(self) -> list[aliases.AnyDocument]:
        return build_object(self['stickers'])


class MessagesFoundStickerSetsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.foundStickerSetsNotModified'):
        dict.__init__(self, _=_)


class MessagesFoundStickerSets(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, sets: list[aliases.AnyStickerSetCovered]): ...

    def __init__(self, hash, sets, _='messages.foundStickerSets', **kwargs):
        kwargs['hash'] = hash
        kwargs['sets'] = sets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def sets(self) -> list[aliases.AnyStickerSetCovered]:
        return build_object(self['sets'])


class MessagesSearchCounter(dict):
    __slots__ = ()

    @overload
    def __init__(self, filter: aliases.AnyMessagesFilter, count: int, inexact: Optional[bool] = ...): ...

    def __init__(self, filter, count, _='messages.searchCounter', **kwargs):
        kwargs['filter'] = filter
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inexact(self) -> Optional[bool]:
        return self['inexact']

    @property
    def filter(self) -> aliases.AnyMessagesFilter:
        return build_object(self['filter'])

    @property
    def count(self) -> int:
        return self['count']


class MessagesInactiveChats(dict):
    __slots__ = ()

    @overload
    def __init__(self, dates: list[int], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, dates, chats, users, _='messages.inactiveChats', **kwargs):
        kwargs['dates'] = dates
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dates(self) -> list[int]:
        return self['dates']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesVotesList(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, votes: list[aliases.AnyMessagePeerVote], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, votes, chats, users, _='messages.votesList', **kwargs):
        kwargs['count'] = count
        kwargs['votes'] = votes
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def votes(self) -> list[aliases.AnyMessagePeerVote]:
        return build_object(self['votes'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']


class MessagesMessageViews(dict):
    __slots__ = ()

    @overload
    def __init__(self, views: list[aliases.AnyMessageViews], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, views, chats, users, _='messages.messageViews', **kwargs):
        kwargs['views'] = views
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def views(self) -> list[aliases.AnyMessageViews]:
        return build_object(self['views'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesDiscussionMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, messages: list[aliases.AnyMessage], unread_count: int, chats: list[aliases.AnyChat], users: list[aliases.AnyUser], max_id: Optional[int] = ..., read_inbox_max_id: Optional[int] = ..., read_outbox_max_id: Optional[int] = ...): ...

    def __init__(self, messages, unread_count, chats, users, _='messages.discussionMessage', **kwargs):
        kwargs['messages'] = messages
        kwargs['unread_count'] = unread_count
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def max_id(self) -> Optional[int]:
        return self['max_id']

    @property
    def read_inbox_max_id(self) -> Optional[int]:
        return self['read_inbox_max_id']

    @property
    def read_outbox_max_id(self) -> Optional[int]:
        return self['read_outbox_max_id']

    @property
    def unread_count(self) -> int:
        return self['unread_count']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesHistoryImport(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='messages.historyImport', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class MessagesHistoryImportParsed(dict):
    __slots__ = ()

    @overload
    def __init__(self, pm: Optional[bool] = ..., group: Optional[bool] = ..., title: Optional[str] = ...): ...

    def __init__(self, _='messages.historyImportParsed', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pm(self) -> Optional[bool]:
        return self['pm']

    @property
    def group(self) -> Optional[bool]:
        return self['group']

    @property
    def title(self) -> Optional[str]:
        return self['title']


class MessagesAffectedFoundMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, pts_count: int, offset: int, messages: list[int]): ...

    def __init__(self, pts, pts_count, offset, messages, _='messages.affectedFoundMessages', **kwargs):
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['offset'] = offset
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def messages(self) -> list[int]:
        return self['messages']


class MessagesExportedChatInvites(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, invites: list[aliases.AnyExportedChatInvite], users: list[aliases.AnyUser]): ...

    def __init__(self, count, invites, users, _='messages.exportedChatInvites', **kwargs):
        kwargs['count'] = count
        kwargs['invites'] = invites
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def invites(self) -> list[aliases.AnyExportedChatInvite]:
        return build_object(self['invites'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesExportedChatInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite, users: list[aliases.AnyUser]): ...

    def __init__(self, invite, users, _='messages.exportedChatInvite', **kwargs):
        kwargs['invite'] = invite
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesExportedChatInviteReplaced(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite, new_invite: aliases.AnyExportedChatInvite, users: list[aliases.AnyUser]): ...

    def __init__(self, invite, new_invite, users, _='messages.exportedChatInviteReplaced', **kwargs):
        kwargs['invite'] = invite
        kwargs['new_invite'] = new_invite
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])

    @property
    def new_invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['new_invite'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesChatInviteImporters(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, importers: list[aliases.AnyChatInviteImporter], users: list[aliases.AnyUser]): ...

    def __init__(self, count, importers, users, _='messages.chatInviteImporters', **kwargs):
        kwargs['count'] = count
        kwargs['importers'] = importers
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def importers(self) -> list[aliases.AnyChatInviteImporter]:
        return build_object(self['importers'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesChatAdminsWithInvites(dict):
    __slots__ = ()

    @overload
    def __init__(self, admins: list[aliases.AnyChatAdminWithInvites], users: list[aliases.AnyUser]): ...

    def __init__(self, admins, users, _='messages.chatAdminsWithInvites', **kwargs):
        kwargs['admins'] = admins
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def admins(self) -> list[aliases.AnyChatAdminWithInvites]:
        return build_object(self['admins'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesCheckedHistoryImportPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, confirm_text: str): ...

    def __init__(self, confirm_text, _='messages.checkedHistoryImportPeer', **kwargs):
        kwargs['confirm_text'] = confirm_text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def confirm_text(self) -> str:
        return self['confirm_text']


class MessagesSponsoredMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, messages: list[aliases.AnySponsoredMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], posts_between: Optional[int] = ..., start_delay: Optional[int] = ..., between_delay: Optional[int] = ...): ...

    def __init__(self, messages, chats, users, _='messages.sponsoredMessages', **kwargs):
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def posts_between(self) -> Optional[int]:
        return self['posts_between']

    @property
    def start_delay(self) -> Optional[int]:
        return self['start_delay']

    @property
    def between_delay(self) -> Optional[int]:
        return self['between_delay']

    @property
    def messages(self) -> list[aliases.AnySponsoredMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesSponsoredMessagesEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.sponsoredMessagesEmpty'):
        dict.__init__(self, _=_)


class MessagesSearchResultsCalendar(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, min_date: int, min_msg_id: int, periods: list[aliases.AnySearchResultsCalendarPeriod], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], inexact: Optional[bool] = ..., offset_id_offset: Optional[int] = ...): ...

    def __init__(self, count, min_date, min_msg_id, periods, messages, chats, users, _='messages.searchResultsCalendar', **kwargs):
        kwargs['count'] = count
        kwargs['min_date'] = min_date
        kwargs['min_msg_id'] = min_msg_id
        kwargs['periods'] = periods
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inexact(self) -> Optional[bool]:
        return self['inexact']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def min_date(self) -> int:
        return self['min_date']

    @property
    def min_msg_id(self) -> int:
        return self['min_msg_id']

    @property
    def offset_id_offset(self) -> Optional[int]:
        return self['offset_id_offset']

    @property
    def periods(self) -> list[aliases.AnySearchResultsCalendarPeriod]:
        return build_object(self['periods'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesSearchResultsPositions(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, positions: list[aliases.AnySearchResultsPosition]): ...

    def __init__(self, count, positions, _='messages.searchResultsPositions', **kwargs):
        kwargs['count'] = count
        kwargs['positions'] = positions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def positions(self) -> list[aliases.AnySearchResultsPosition]:
        return build_object(self['positions'])


class MessagesPeerSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, settings: aliases.AnyPeerSettings, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, settings, chats, users, _='messages.peerSettings', **kwargs):
        kwargs['settings'] = settings
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def settings(self) -> aliases.AnyPeerSettings:
        return build_object(self['settings'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesMessageReactionsList(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, reactions: list[aliases.AnyMessagePeerReaction], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, reactions, chats, users, _='messages.messageReactionsList', **kwargs):
        kwargs['count'] = count
        kwargs['reactions'] = reactions
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def reactions(self) -> list[aliases.AnyMessagePeerReaction]:
        return build_object(self['reactions'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']


class MessagesAvailableReactionsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.availableReactionsNotModified'):
        dict.__init__(self, _=_)


class MessagesAvailableReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, reactions: list[aliases.AnyAvailableReaction]): ...

    def __init__(self, hash, reactions, _='messages.availableReactions', **kwargs):
        kwargs['hash'] = hash
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def reactions(self) -> list[aliases.AnyAvailableReaction]:
        return build_object(self['reactions'])


class MessagesTranscribedAudio(dict):
    __slots__ = ()

    @overload
    def __init__(self, transcription_id: int, text: str, pending: Optional[bool] = ..., trial_remains_num: Optional[int] = ..., trial_remains_until_date: Optional[int] = ...): ...

    def __init__(self, transcription_id, text, _='messages.transcribedAudio', **kwargs):
        kwargs['transcription_id'] = transcription_id
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pending(self) -> Optional[bool]:
        return self['pending']

    @property
    def transcription_id(self) -> int:
        return self['transcription_id']

    @property
    def text(self) -> str:
        return self['text']

    @property
    def trial_remains_num(self) -> Optional[int]:
        return self['trial_remains_num']

    @property
    def trial_remains_until_date(self) -> Optional[int]:
        return self['trial_remains_until_date']


class MessagesReactionsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.reactionsNotModified'):
        dict.__init__(self, _=_)


class MessagesReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, reactions: list[aliases.AnyReaction]): ...

    def __init__(self, hash, reactions, _='messages.reactions', **kwargs):
        kwargs['hash'] = hash
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def reactions(self) -> list[aliases.AnyReaction]:
        return build_object(self['reactions'])


class MessagesForumTopics(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, topics: list[aliases.AnyForumTopic], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], pts: int, order_by_create_date: Optional[bool] = ...): ...

    def __init__(self, count, topics, messages, chats, users, pts, _='messages.forumTopics', **kwargs):
        kwargs['count'] = count
        kwargs['topics'] = topics
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['pts'] = pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order_by_create_date(self) -> Optional[bool]:
        return self['order_by_create_date']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def topics(self) -> list[aliases.AnyForumTopic]:
        return build_object(self['topics'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def pts(self) -> int:
        return self['pts']


class MessagesEmojiGroupsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.emojiGroupsNotModified'):
        dict.__init__(self, _=_)


class MessagesEmojiGroups(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, groups: list[aliases.AnyEmojiGroup]): ...

    def __init__(self, hash, groups, _='messages.emojiGroups', **kwargs):
        kwargs['hash'] = hash
        kwargs['groups'] = groups
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def groups(self) -> list[aliases.AnyEmojiGroup]:
        return build_object(self['groups'])


class MessagesTranslateResult(dict):
    __slots__ = ()

    @overload
    def __init__(self, result: list[aliases.AnyTextWithEntities]): ...

    def __init__(self, result, _='messages.translateResult', **kwargs):
        kwargs['result'] = result
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def result(self) -> list[aliases.AnyTextWithEntities]:
        return build_object(self['result'])


class MessagesBotApp(dict):
    __slots__ = ()

    @overload
    def __init__(self, app: aliases.AnyBotApp, inactive: Optional[bool] = ..., request_write_access: Optional[bool] = ..., has_settings: Optional[bool] = ...): ...

    def __init__(self, app, _='messages.botApp', **kwargs):
        kwargs['app'] = app
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inactive(self) -> Optional[bool]:
        return self['inactive']

    @property
    def request_write_access(self) -> Optional[bool]:
        return self['request_write_access']

    @property
    def has_settings(self) -> Optional[bool]:
        return self['has_settings']

    @property
    def app(self) -> aliases.AnyBotApp:
        return build_object(self['app'])


class MessagesWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, webpage: aliases.AnyWebPage, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, webpage, chats, users, _='messages.webPage', **kwargs):
        kwargs['webpage'] = webpage
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def webpage(self) -> aliases.AnyWebPage:
        return build_object(self['webpage'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesSavedDialogs(dict):
    __slots__ = ()

    @overload
    def __init__(self, dialogs: list[aliases.AnySavedDialog], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, dialogs, messages, chats, users, _='messages.savedDialogs', **kwargs):
        kwargs['dialogs'] = dialogs
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dialogs(self) -> list[aliases.AnySavedDialog]:
        return build_object(self['dialogs'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesSavedDialogsSlice(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, dialogs: list[aliases.AnySavedDialog], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, count, dialogs, messages, chats, users, _='messages.savedDialogsSlice', **kwargs):
        kwargs['count'] = count
        kwargs['dialogs'] = dialogs
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def dialogs(self) -> list[aliases.AnySavedDialog]:
        return build_object(self['dialogs'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesSavedDialogsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int): ...

    def __init__(self, count, _='messages.savedDialogsNotModified', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']


class MessagesSavedReactionTagsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.savedReactionTagsNotModified'):
        dict.__init__(self, _=_)


class MessagesSavedReactionTags(dict):
    __slots__ = ()

    @overload
    def __init__(self, tags: list[aliases.AnySavedReactionTag], hash: int): ...

    def __init__(self, tags, hash, _='messages.savedReactionTags', **kwargs):
        kwargs['tags'] = tags
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def tags(self) -> list[aliases.AnySavedReactionTag]:
        return build_object(self['tags'])

    @property
    def hash(self) -> int:
        return self['hash']


class MessagesQuickReplies(dict):
    __slots__ = ()

    @overload
    def __init__(self, quick_replies: list[aliases.AnyQuickReply], messages: list[aliases.AnyMessage], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, quick_replies, messages, chats, users, _='messages.quickReplies', **kwargs):
        kwargs['quick_replies'] = quick_replies
        kwargs['messages'] = messages
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def quick_replies(self) -> list[aliases.AnyQuickReply]:
        return build_object(self['quick_replies'])

    @property
    def messages(self) -> list[aliases.AnyMessage]:
        return build_object(self['messages'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesQuickRepliesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.quickRepliesNotModified'):
        dict.__init__(self, _=_)


class MessagesDialogFilters(dict):
    __slots__ = ()

    @overload
    def __init__(self, filters: list[aliases.AnyDialogFilter], tags_enabled: Optional[bool] = ...): ...

    def __init__(self, filters, _='messages.dialogFilters', **kwargs):
        kwargs['filters'] = filters
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def tags_enabled(self) -> Optional[bool]:
        return self['tags_enabled']

    @property
    def filters(self) -> list[aliases.AnyDialogFilter]:
        return build_object(self['filters'])


class MessagesMyStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, sets: list[aliases.AnyStickerSetCovered]): ...

    def __init__(self, count, sets, _='messages.myStickers', **kwargs):
        kwargs['count'] = count
        kwargs['sets'] = sets
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def sets(self) -> list[aliases.AnyStickerSetCovered]:
        return build_object(self['sets'])


class MessagesInvitedUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, updates: aliases.AnyUpdates, missing_invitees: list[aliases.AnyMissingInvitee]): ...

    def __init__(self, updates, missing_invitees, _='messages.invitedUsers', **kwargs):
        kwargs['updates'] = updates
        kwargs['missing_invitees'] = missing_invitees
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def updates(self) -> aliases.AnyUpdates:
        return build_object(self['updates'])

    @property
    def missing_invitees(self) -> list[aliases.AnyMissingInvitee]:
        return build_object(self['missing_invitees'])


class MessagesAvailableEffectsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.availableEffectsNotModified'):
        dict.__init__(self, _=_)


class MessagesAvailableEffects(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, effects: list[aliases.AnyAvailableEffect], documents: list[aliases.AnyDocument]): ...

    def __init__(self, hash, effects, documents, _='messages.availableEffects', **kwargs):
        kwargs['hash'] = hash
        kwargs['effects'] = effects
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def effects(self) -> list[aliases.AnyAvailableEffect]:
        return build_object(self['effects'])

    @property
    def documents(self) -> list[aliases.AnyDocument]:
        return build_object(self['documents'])


class MessagesBotPreparedInlineMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, expire_date: int): ...

    def __init__(self, id, expire_date, _='messages.botPreparedInlineMessage', **kwargs):
        kwargs['id'] = id
        kwargs['expire_date'] = expire_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def expire_date(self) -> int:
        return self['expire_date']


class MessagesPreparedInlineMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, result: aliases.AnyBotInlineResult, peer_types: list[aliases.AnyInlineQueryPeerType], cache_time: int, users: list[aliases.AnyUser]): ...

    def __init__(self, query_id, result, peer_types, cache_time, users, _='messages.preparedInlineMessage', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['result'] = result
        kwargs['peer_types'] = peer_types
        kwargs['cache_time'] = cache_time
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def result(self) -> aliases.AnyBotInlineResult:
        return build_object(self['result'])

    @property
    def peer_types(self) -> list[aliases.AnyInlineQueryPeerType]:
        return build_object(self['peer_types'])

    @property
    def cache_time(self) -> int:
        return self['cache_time']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesFoundStickersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, next_offset: Optional[int] = ...): ...

    def __init__(self, _='messages.foundStickersNotModified', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def next_offset(self) -> Optional[int]:
        return self['next_offset']


class MessagesFoundStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, stickers: list[aliases.AnyDocument], next_offset: Optional[int] = ...): ...

    def __init__(self, hash, stickers, _='messages.foundStickers', **kwargs):
        kwargs['hash'] = hash
        kwargs['stickers'] = stickers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def next_offset(self) -> Optional[int]:
        return self['next_offset']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def stickers(self) -> list[aliases.AnyDocument]:
        return build_object(self['stickers'])


class MessagesWebPagePreview(dict):
    __slots__ = ()

    @overload
    def __init__(self, media: aliases.AnyMessageMedia, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, media, chats, users, _='messages.webPagePreview', **kwargs):
        kwargs['media'] = media
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> aliases.AnyMessageMedia:
        return build_object(self['media'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class MessagesEmojiGameOutcome(dict):
    __slots__ = ()

    @overload
    def __init__(self, seed: bytes, stake_ton_amount: int, ton_amount: int): ...

    def __init__(self, seed, stake_ton_amount, ton_amount, _='messages.emojiGameOutcome', **kwargs):
        kwargs['seed'] = seed
        kwargs['stake_ton_amount'] = stake_ton_amount
        kwargs['ton_amount'] = ton_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def seed(self) -> bytes:
        return self['seed']

    @property
    def stake_ton_amount(self) -> int:
        return self['stake_ton_amount']

    @property
    def ton_amount(self) -> int:
        return self['ton_amount']


class MessagesEmojiGameUnavailable(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messages.emojiGameUnavailable'):
        dict.__init__(self, _=_)


class MessagesEmojiGameDiceInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, game_hash: str, prev_stake: int, current_streak: int, params: list[int], plays_left: Optional[int] = ...): ...

    def __init__(self, game_hash, prev_stake, current_streak, params, _='messages.emojiGameDiceInfo', **kwargs):
        kwargs['game_hash'] = game_hash
        kwargs['prev_stake'] = prev_stake
        kwargs['current_streak'] = current_streak
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def game_hash(self) -> str:
        return self['game_hash']

    @property
    def prev_stake(self) -> int:
        return self['prev_stake']

    @property
    def current_streak(self) -> int:
        return self['current_streak']

    @property
    def params(self) -> list[int]:
        return self['params']

    @property
    def plays_left(self) -> Optional[int]:
        return self['plays_left']
