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


class StatsBroadcastStats(dict):
    __slots__ = ()

    @overload
    def __init__(self, period: aliases.AnyStatsDateRangeDays, followers: aliases.AnyStatsAbsValueAndPrev, views_per_post: aliases.AnyStatsAbsValueAndPrev, shares_per_post: aliases.AnyStatsAbsValueAndPrev, reactions_per_post: aliases.AnyStatsAbsValueAndPrev, views_per_story: aliases.AnyStatsAbsValueAndPrev, shares_per_story: aliases.AnyStatsAbsValueAndPrev, reactions_per_story: aliases.AnyStatsAbsValueAndPrev, enabled_notifications: aliases.AnyStatsPercentValue, growth_graph: aliases.AnyStatsGraph, followers_graph: aliases.AnyStatsGraph, mute_graph: aliases.AnyStatsGraph, top_hours_graph: aliases.AnyStatsGraph, interactions_graph: aliases.AnyStatsGraph, iv_interactions_graph: aliases.AnyStatsGraph, views_by_source_graph: aliases.AnyStatsGraph, new_followers_by_source_graph: aliases.AnyStatsGraph, languages_graph: aliases.AnyStatsGraph, reactions_by_emotion_graph: aliases.AnyStatsGraph, story_interactions_graph: aliases.AnyStatsGraph, story_reactions_by_emotion_graph: aliases.AnyStatsGraph, recent_posts_interactions: list[aliases.AnyPostInteractionCounters]): ...

    def __init__(self, period, followers, views_per_post, shares_per_post, reactions_per_post, views_per_story, shares_per_story, reactions_per_story, enabled_notifications, growth_graph, followers_graph, mute_graph, top_hours_graph, interactions_graph, iv_interactions_graph, views_by_source_graph, new_followers_by_source_graph, languages_graph, reactions_by_emotion_graph, story_interactions_graph, story_reactions_by_emotion_graph, recent_posts_interactions, _='stats.broadcastStats', **kwargs):
        kwargs['period'] = period
        kwargs['followers'] = followers
        kwargs['views_per_post'] = views_per_post
        kwargs['shares_per_post'] = shares_per_post
        kwargs['reactions_per_post'] = reactions_per_post
        kwargs['views_per_story'] = views_per_story
        kwargs['shares_per_story'] = shares_per_story
        kwargs['reactions_per_story'] = reactions_per_story
        kwargs['enabled_notifications'] = enabled_notifications
        kwargs['growth_graph'] = growth_graph
        kwargs['followers_graph'] = followers_graph
        kwargs['mute_graph'] = mute_graph
        kwargs['top_hours_graph'] = top_hours_graph
        kwargs['interactions_graph'] = interactions_graph
        kwargs['iv_interactions_graph'] = iv_interactions_graph
        kwargs['views_by_source_graph'] = views_by_source_graph
        kwargs['new_followers_by_source_graph'] = new_followers_by_source_graph
        kwargs['languages_graph'] = languages_graph
        kwargs['reactions_by_emotion_graph'] = reactions_by_emotion_graph
        kwargs['story_interactions_graph'] = story_interactions_graph
        kwargs['story_reactions_by_emotion_graph'] = story_reactions_by_emotion_graph
        kwargs['recent_posts_interactions'] = recent_posts_interactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> aliases.AnyStatsDateRangeDays:
        return build_object(self['period'])

    @property
    def followers(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['followers'])

    @property
    def views_per_post(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['views_per_post'])

    @property
    def shares_per_post(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['shares_per_post'])

    @property
    def reactions_per_post(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['reactions_per_post'])

    @property
    def views_per_story(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['views_per_story'])

    @property
    def shares_per_story(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['shares_per_story'])

    @property
    def reactions_per_story(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['reactions_per_story'])

    @property
    def enabled_notifications(self) -> aliases.AnyStatsPercentValue:
        return build_object(self['enabled_notifications'])

    @property
    def growth_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['growth_graph'])

    @property
    def followers_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['followers_graph'])

    @property
    def mute_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['mute_graph'])

    @property
    def top_hours_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['top_hours_graph'])

    @property
    def interactions_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['interactions_graph'])

    @property
    def iv_interactions_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['iv_interactions_graph'])

    @property
    def views_by_source_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['views_by_source_graph'])

    @property
    def new_followers_by_source_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['new_followers_by_source_graph'])

    @property
    def languages_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['languages_graph'])

    @property
    def reactions_by_emotion_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['reactions_by_emotion_graph'])

    @property
    def story_interactions_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['story_interactions_graph'])

    @property
    def story_reactions_by_emotion_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['story_reactions_by_emotion_graph'])

    @property
    def recent_posts_interactions(self) -> list[aliases.AnyPostInteractionCounters]:
        return build_object(self['recent_posts_interactions'])


class StatsMegagroupStats(dict):
    __slots__ = ()

    @overload
    def __init__(self, period: aliases.AnyStatsDateRangeDays, members: aliases.AnyStatsAbsValueAndPrev, messages: aliases.AnyStatsAbsValueAndPrev, viewers: aliases.AnyStatsAbsValueAndPrev, posters: aliases.AnyStatsAbsValueAndPrev, growth_graph: aliases.AnyStatsGraph, members_graph: aliases.AnyStatsGraph, new_members_by_source_graph: aliases.AnyStatsGraph, languages_graph: aliases.AnyStatsGraph, messages_graph: aliases.AnyStatsGraph, actions_graph: aliases.AnyStatsGraph, top_hours_graph: aliases.AnyStatsGraph, weekdays_graph: aliases.AnyStatsGraph, top_posters: list[aliases.AnyStatsGroupTopPoster], top_admins: list[aliases.AnyStatsGroupTopAdmin], top_inviters: list[aliases.AnyStatsGroupTopInviter], users: list[aliases.AnyUser]): ...

    def __init__(self, period, members, messages, viewers, posters, growth_graph, members_graph, new_members_by_source_graph, languages_graph, messages_graph, actions_graph, top_hours_graph, weekdays_graph, top_posters, top_admins, top_inviters, users, _='stats.megagroupStats', **kwargs):
        kwargs['period'] = period
        kwargs['members'] = members
        kwargs['messages'] = messages
        kwargs['viewers'] = viewers
        kwargs['posters'] = posters
        kwargs['growth_graph'] = growth_graph
        kwargs['members_graph'] = members_graph
        kwargs['new_members_by_source_graph'] = new_members_by_source_graph
        kwargs['languages_graph'] = languages_graph
        kwargs['messages_graph'] = messages_graph
        kwargs['actions_graph'] = actions_graph
        kwargs['top_hours_graph'] = top_hours_graph
        kwargs['weekdays_graph'] = weekdays_graph
        kwargs['top_posters'] = top_posters
        kwargs['top_admins'] = top_admins
        kwargs['top_inviters'] = top_inviters
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> aliases.AnyStatsDateRangeDays:
        return build_object(self['period'])

    @property
    def members(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['members'])

    @property
    def messages(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['messages'])

    @property
    def viewers(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['viewers'])

    @property
    def posters(self) -> aliases.AnyStatsAbsValueAndPrev:
        return build_object(self['posters'])

    @property
    def growth_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['growth_graph'])

    @property
    def members_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['members_graph'])

    @property
    def new_members_by_source_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['new_members_by_source_graph'])

    @property
    def languages_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['languages_graph'])

    @property
    def messages_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['messages_graph'])

    @property
    def actions_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['actions_graph'])

    @property
    def top_hours_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['top_hours_graph'])

    @property
    def weekdays_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['weekdays_graph'])

    @property
    def top_posters(self) -> list[aliases.AnyStatsGroupTopPoster]:
        return build_object(self['top_posters'])

    @property
    def top_admins(self) -> list[aliases.AnyStatsGroupTopAdmin]:
        return build_object(self['top_admins'])

    @property
    def top_inviters(self) -> list[aliases.AnyStatsGroupTopInviter]:
        return build_object(self['top_inviters'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class StatsMessageStats(dict):
    __slots__ = ()

    @overload
    def __init__(self, views_graph: aliases.AnyStatsGraph, reactions_by_emotion_graph: aliases.AnyStatsGraph): ...

    def __init__(self, views_graph, reactions_by_emotion_graph, _='stats.messageStats', **kwargs):
        kwargs['views_graph'] = views_graph
        kwargs['reactions_by_emotion_graph'] = reactions_by_emotion_graph
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def views_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['views_graph'])

    @property
    def reactions_by_emotion_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['reactions_by_emotion_graph'])


class StatsStoryStats(dict):
    __slots__ = ()

    @overload
    def __init__(self, views_graph: aliases.AnyStatsGraph, reactions_by_emotion_graph: aliases.AnyStatsGraph): ...

    def __init__(self, views_graph, reactions_by_emotion_graph, _='stats.storyStats', **kwargs):
        kwargs['views_graph'] = views_graph
        kwargs['reactions_by_emotion_graph'] = reactions_by_emotion_graph
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def views_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['views_graph'])

    @property
    def reactions_by_emotion_graph(self) -> aliases.AnyStatsGraph:
        return build_object(self['reactions_by_emotion_graph'])


class StatsPublicForwards(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, forwards: list[aliases.AnyPublicForward], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, forwards, chats, users, _='stats.publicForwards', **kwargs):
        kwargs['count'] = count
        kwargs['forwards'] = forwards
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def forwards(self) -> list[aliases.AnyPublicForward]:
        return build_object(self['forwards'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])
