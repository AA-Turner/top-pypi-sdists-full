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


class StoriesAllStoriesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, state: str, stealth_mode: aliases.AnyStoriesStealthMode): ...

    def __init__(self, state, stealth_mode, _='stories.allStoriesNotModified', **kwargs):
        kwargs['state'] = state
        kwargs['stealth_mode'] = stealth_mode
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def state(self) -> str:
        return self['state']

    @property
    def stealth_mode(self) -> aliases.AnyStoriesStealthMode:
        return build_object(self['stealth_mode'])


class StoriesAllStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, state: str, peer_stories: list[aliases.AnyPeerStories], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], stealth_mode: aliases.AnyStoriesStealthMode, has_more: Optional[bool] = ...): ...

    def __init__(self, count, state, peer_stories, chats, users, stealth_mode, _='stories.allStories', **kwargs):
        kwargs['count'] = count
        kwargs['state'] = state
        kwargs['peer_stories'] = peer_stories
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['stealth_mode'] = stealth_mode
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_more(self) -> Optional[bool]:
        return self['has_more']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def state(self) -> str:
        return self['state']

    @property
    def peer_stories(self) -> list[aliases.AnyPeerStories]:
        return build_object(self['peer_stories'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def stealth_mode(self) -> aliases.AnyStoriesStealthMode:
        return build_object(self['stealth_mode'])


class StoriesStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, stories: list[aliases.AnyStoryItem], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], pinned_to_top: Optional[list[int]] = ...): ...

    def __init__(self, count, stories, chats, users, _='stories.stories', **kwargs):
        kwargs['count'] = count
        kwargs['stories'] = stories
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def stories(self) -> list[aliases.AnyStoryItem]:
        return build_object(self['stories'])

    @property
    def pinned_to_top(self) -> Optional[list[int]]:
        return self['pinned_to_top']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class StoriesStoryViewsList(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, views_count: int, forwards_count: int, reactions_count: int, views: list[aliases.AnyStoryView], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, views_count, forwards_count, reactions_count, views, chats, users, _='stories.storyViewsList', **kwargs):
        kwargs['count'] = count
        kwargs['views_count'] = views_count
        kwargs['forwards_count'] = forwards_count
        kwargs['reactions_count'] = reactions_count
        kwargs['views'] = views
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def views_count(self) -> int:
        return self['views_count']

    @property
    def forwards_count(self) -> int:
        return self['forwards_count']

    @property
    def reactions_count(self) -> int:
        return self['reactions_count']

    @property
    def views(self) -> list[aliases.AnyStoryView]:
        return build_object(self['views'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']


class StoriesStoryViews(dict):
    __slots__ = ()

    @overload
    def __init__(self, views: list[aliases.AnyStoryViews], users: list[aliases.AnyUser]): ...

    def __init__(self, views, users, _='stories.storyViews', **kwargs):
        kwargs['views'] = views
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def views(self) -> list[aliases.AnyStoryViews]:
        return build_object(self['views'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class StoriesPeerStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, stories: aliases.AnyPeerStories, chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, stories, chats, users, _='stories.peerStories', **kwargs):
        kwargs['stories'] = stories
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stories(self) -> aliases.AnyPeerStories:
        return build_object(self['stories'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class StoriesStoryReactionsList(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, reactions: list[aliases.AnyStoryReaction], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, reactions, chats, users, _='stories.storyReactionsList', **kwargs):
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
    def reactions(self) -> list[aliases.AnyStoryReaction]:
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


class StoriesFoundStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, stories: list[aliases.AnyFoundStory], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, stories, chats, users, _='stories.foundStories', **kwargs):
        kwargs['count'] = count
        kwargs['stories'] = stories
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def stories(self) -> list[aliases.AnyFoundStory]:
        return build_object(self['stories'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class StoriesCanSendStoryCount(dict):
    __slots__ = ()

    @overload
    def __init__(self, count_remains: int): ...

    def __init__(self, count_remains, _='stories.canSendStoryCount', **kwargs):
        kwargs['count_remains'] = count_remains
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count_remains(self) -> int:
        return self['count_remains']


class StoriesAlbumsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='stories.albumsNotModified'):
        dict.__init__(self, _=_)


class StoriesAlbums(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, albums: list[aliases.AnyStoryAlbum]): ...

    def __init__(self, hash, albums, _='stories.albums', **kwargs):
        kwargs['hash'] = hash
        kwargs['albums'] = albums
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def albums(self) -> list[aliases.AnyStoryAlbum]:
        return build_object(self['albums'])
