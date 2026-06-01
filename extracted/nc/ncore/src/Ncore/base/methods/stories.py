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

class StoriesCanSendStory(TLMethod[aliases.AnyStoriesCanSendStoryCount]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='stories.canSendStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class StoriesSendStory(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, media: aliases.AnyInputMedia, privacy_rules: list[aliases.AnyInputPrivacyRule], random_id: int, pinned: Optional[bool] = ..., noforwards: Optional[bool] = ..., fwd_modified: Optional[bool] = ..., media_areas: Optional[list[aliases.AnyMediaArea]] = ..., caption: Optional[str] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., period: Optional[int] = ..., fwd_from_id: Optional[aliases.AnyInputPeer] = ..., fwd_from_story: Optional[int] = ..., albums: Optional[list[int]] = ...): ...

    def __init__(self, peer, media, privacy_rules, random_id, _='stories.sendStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['media'] = media
        kwargs['privacy_rules'] = privacy_rules
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def fwd_modified(self) -> Optional[bool]:
        return self['fwd_modified']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])

    @property
    def media_areas(self) -> Optional[list[aliases.AnyMediaArea]]:
        return build_object(self['media_areas'])

    @property
    def caption(self) -> Optional[str]:
        return self['caption']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def privacy_rules(self) -> list[aliases.AnyInputPrivacyRule]:
        return build_object(self['privacy_rules'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def period(self) -> Optional[int]:
        return self['period']

    @property
    def fwd_from_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['fwd_from_id'])

    @property
    def fwd_from_story(self) -> Optional[int]:
        return self['fwd_from_story']

    @property
    def albums(self) -> Optional[list[int]]:
        return self['albums']


class StoriesEditStory(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, media: Optional[aliases.AnyInputMedia] = ..., media_areas: Optional[list[aliases.AnyMediaArea]] = ..., caption: Optional[str] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., privacy_rules: Optional[list[aliases.AnyInputPrivacyRule]] = ...): ...

    def __init__(self, peer, id, _='stories.editStory', **kwargs):
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
    def media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['media'])

    @property
    def media_areas(self) -> Optional[list[aliases.AnyMediaArea]]:
        return build_object(self['media_areas'])

    @property
    def caption(self) -> Optional[str]:
        return self['caption']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def privacy_rules(self) -> Optional[list[aliases.AnyInputPrivacyRule]]:
        return build_object(self['privacy_rules'])


class StoriesDeleteStories(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='stories.deleteStories', **kwargs):
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


class StoriesTogglePinned(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int], pinned: bool): ...

    def __init__(self, peer, id, pinned, _='stories.togglePinned', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['pinned'] = pinned
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> list[int]:
        return self['id']

    @property
    def pinned(self) -> bool:
        return self['pinned']


class StoriesGetAllStories(TLMethod[aliases.AnyStoriesAllStories]):
    __slots__ = ()

    @overload
    def __init__(self, next: Optional[bool] = ..., hidden: Optional[bool] = ..., state: Optional[str] = ...): ...

    def __init__(self, _='stories.getAllStories', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def next(self) -> Optional[bool]:
        return self['next']

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']

    @property
    def state(self) -> Optional[str]:
        return self['state']


class StoriesGetPinnedStories(TLMethod[aliases.AnyStoriesStories]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, limit: int): ...

    def __init__(self, peer, offset_id, limit, _='stories.getPinnedStories', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']


class StoriesGetStoriesArchive(TLMethod[aliases.AnyStoriesStories]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset_id: int, limit: int): ...

    def __init__(self, peer, offset_id, limit, _='stories.getStoriesArchive', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset_id'] = offset_id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset_id(self) -> int:
        return self['offset_id']

    @property
    def limit(self) -> int:
        return self['limit']


class StoriesGetStoriesByID(TLMethod[aliases.AnyStoriesStories]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='stories.getStoriesByID', **kwargs):
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


class StoriesToggleAllStoriesHidden(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, hidden: bool): ...

    def __init__(self, hidden, _='stories.toggleAllStoriesHidden', **kwargs):
        kwargs['hidden'] = hidden
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hidden(self) -> bool:
        return self['hidden']


class StoriesReadStories(TLMethod[list[int]]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, max_id: int): ...

    def __init__(self, peer, max_id, _='stories.readStories', **kwargs):
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


class StoriesIncrementStoryViews(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='stories.incrementStoryViews', **kwargs):
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


class StoriesGetStoryViewsList(TLMethod[aliases.AnyStoriesStoryViewsList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, offset: str, limit: int, just_contacts: Optional[bool] = ..., reactions_first: Optional[bool] = ..., forwards_first: Optional[bool] = ..., q: Optional[str] = ...): ...

    def __init__(self, peer, id, offset, limit, _='stories.getStoryViewsList', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def just_contacts(self) -> Optional[bool]:
        return self['just_contacts']

    @property
    def reactions_first(self) -> Optional[bool]:
        return self['reactions_first']

    @property
    def forwards_first(self) -> Optional[bool]:
        return self['forwards_first']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def q(self) -> Optional[str]:
        return self['q']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class StoriesGetStoriesViews(TLMethod[aliases.AnyStoriesStoryViews]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='stories.getStoriesViews', **kwargs):
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


class StoriesExportStoryLink(TLMethod[aliases.AnyExportedStoryLink]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int): ...

    def __init__(self, peer, id, _='stories.exportStoryLink', **kwargs):
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


class StoriesReport(TLMethod[aliases.AnyReportResult]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int], option: bytes, message: str): ...

    def __init__(self, peer, id, option, message, _='stories.report', **kwargs):
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


class StoriesActivateStealthMode(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, past: Optional[bool] = ..., future: Optional[bool] = ...): ...

    def __init__(self, _='stories.activateStealthMode', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def past(self) -> Optional[bool]:
        return self['past']

    @property
    def future(self) -> Optional[bool]:
        return self['future']


class StoriesSendReaction(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, story_id: int, reaction: aliases.AnyReaction, add_to_recent: Optional[bool] = ...): ...

    def __init__(self, peer, story_id, reaction, _='stories.sendReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['story_id'] = story_id
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def add_to_recent(self) -> Optional[bool]:
        return self['add_to_recent']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def story_id(self) -> int:
        return self['story_id']

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class StoriesGetPeerStories(TLMethod[aliases.AnyStoriesPeerStories]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='stories.getPeerStories', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class StoriesGetAllReadPeerStories(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='stories.getAllReadPeerStories'):
        dict.__init__(self, _=_)


class StoriesGetPeerMaxIDs(TLMethod[list[aliases.AnyRecentStory]]):
    __slots__ = ()

    @overload
    def __init__(self, id: list[aliases.AnyInputPeer]): ...

    def __init__(self, id, _='stories.getPeerMaxIDs', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['id'])


class StoriesGetChatsToSend(TLMethod[aliases.AnyMessagesChats]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='stories.getChatsToSend'):
        dict.__init__(self, _=_)


class StoriesTogglePeerStoriesHidden(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, hidden: bool): ...

    def __init__(self, peer, hidden, _='stories.togglePeerStoriesHidden', **kwargs):
        kwargs['peer'] = peer
        kwargs['hidden'] = hidden
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def hidden(self) -> bool:
        return self['hidden']


class StoriesGetStoryReactionsList(TLMethod[aliases.AnyStoriesStoryReactionsList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, limit: int, forwards_first: Optional[bool] = ..., reaction: Optional[aliases.AnyReaction] = ..., offset: Optional[str] = ...): ...

    def __init__(self, peer, id, limit, _='stories.getStoryReactionsList', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def forwards_first(self) -> Optional[bool]:
        return self['forwards_first']

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


class StoriesTogglePinnedToTop(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: list[int]): ...

    def __init__(self, peer, id, _='stories.togglePinnedToTop', **kwargs):
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


class StoriesSearchPosts(TLMethod[aliases.AnyStoriesFoundStories]):
    __slots__ = ()

    @overload
    def __init__(self, offset: str, limit: int, hashtag: Optional[str] = ..., area: Optional[aliases.AnyMediaArea] = ..., peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, offset, limit, _='stories.searchPosts', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hashtag(self) -> Optional[str]:
        return self['hashtag']

    @property
    def area(self) -> Optional[aliases.AnyMediaArea]:
        return build_object(self['area'])

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class StoriesCreateAlbum(TLMethod[aliases.AnyStoryAlbum]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, title: str, stories: list[int]): ...

    def __init__(self, peer, title, stories, _='stories.createAlbum', **kwargs):
        kwargs['peer'] = peer
        kwargs['title'] = title
        kwargs['stories'] = stories
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def stories(self) -> list[int]:
        return self['stories']


class StoriesUpdateAlbum(TLMethod[aliases.AnyStoryAlbum]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, album_id: int, title: Optional[str] = ..., delete_stories: Optional[list[int]] = ..., add_stories: Optional[list[int]] = ..., order: Optional[list[int]] = ...): ...

    def __init__(self, peer, album_id, _='stories.updateAlbum', **kwargs):
        kwargs['peer'] = peer
        kwargs['album_id'] = album_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def album_id(self) -> int:
        return self['album_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def delete_stories(self) -> Optional[list[int]]:
        return self['delete_stories']

    @property
    def add_stories(self) -> Optional[list[int]]:
        return self['add_stories']

    @property
    def order(self) -> Optional[list[int]]:
        return self['order']


class StoriesReorderAlbums(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, order: list[int]): ...

    def __init__(self, peer, order, _='stories.reorderAlbums', **kwargs):
        kwargs['peer'] = peer
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def order(self) -> list[int]:
        return self['order']


class StoriesDeleteAlbum(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, album_id: int): ...

    def __init__(self, peer, album_id, _='stories.deleteAlbum', **kwargs):
        kwargs['peer'] = peer
        kwargs['album_id'] = album_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def album_id(self) -> int:
        return self['album_id']


class StoriesGetAlbums(TLMethod[aliases.AnyStoriesAlbums]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, hash: int): ...

    def __init__(self, peer, hash, _='stories.getAlbums', **kwargs):
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


class StoriesGetAlbumStories(TLMethod[aliases.AnyStoriesStories]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, album_id: int, offset: int, limit: int): ...

    def __init__(self, peer, album_id, offset, limit, _='stories.getAlbumStories', **kwargs):
        kwargs['peer'] = peer
        kwargs['album_id'] = album_id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def album_id(self) -> int:
        return self['album_id']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class StoriesStartLive(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, privacy_rules: list[aliases.AnyInputPrivacyRule], random_id: int, pinned: Optional[bool] = ..., noforwards: Optional[bool] = ..., rtmp_stream: Optional[bool] = ..., caption: Optional[str] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., messages_enabled: Optional[bool] = ..., send_paid_messages_stars: Optional[int] = ...): ...

    def __init__(self, peer, privacy_rules, random_id, _='stories.startLive', **kwargs):
        kwargs['peer'] = peer
        kwargs['privacy_rules'] = privacy_rules
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def rtmp_stream(self) -> Optional[bool]:
        return self['rtmp_stream']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def caption(self) -> Optional[str]:
        return self['caption']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def privacy_rules(self) -> list[aliases.AnyInputPrivacyRule]:
        return build_object(self['privacy_rules'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def messages_enabled(self) -> Optional[bool]:
        return self['messages_enabled']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']
