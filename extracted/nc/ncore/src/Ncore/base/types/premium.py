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


class PremiumBoostsList(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, boosts: list[aliases.AnyBoost], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, count, boosts, users, _='premium.boostsList', **kwargs):
        kwargs['count'] = count
        kwargs['boosts'] = boosts
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def boosts(self) -> list[aliases.AnyBoost]:
        return build_object(self['boosts'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PremiumMyBoosts(dict):
    __slots__ = ()

    @overload
    def __init__(self, my_boosts: list[aliases.AnyMyBoost], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, my_boosts, chats, users, _='premium.myBoosts', **kwargs):
        kwargs['my_boosts'] = my_boosts
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_boosts(self) -> list[aliases.AnyMyBoost]:
        return build_object(self['my_boosts'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class PremiumBoostsStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, level: int, current_level_boosts: int, boosts: int, boost_url: str, my_boost: Optional[bool] = ..., gift_boosts: Optional[int] = ..., next_level_boosts: Optional[int] = ..., premium_audience: Optional[aliases.AnyStatsPercentValue] = ..., prepaid_giveaways: Optional[list[aliases.AnyPrepaidGiveaway]] = ..., my_boost_slots: Optional[list[int]] = ...): ...

    def __init__(self, level, current_level_boosts, boosts, boost_url, _='premium.boostsStatus', **kwargs):
        kwargs['level'] = level
        kwargs['current_level_boosts'] = current_level_boosts
        kwargs['boosts'] = boosts
        kwargs['boost_url'] = boost_url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my_boost(self) -> Optional[bool]:
        return self['my_boost']

    @property
    def level(self) -> int:
        return self['level']

    @property
    def current_level_boosts(self) -> int:
        return self['current_level_boosts']

    @property
    def boosts(self) -> int:
        return self['boosts']

    @property
    def gift_boosts(self) -> Optional[int]:
        return self['gift_boosts']

    @property
    def next_level_boosts(self) -> Optional[int]:
        return self['next_level_boosts']

    @property
    def premium_audience(self) -> Optional[aliases.AnyStatsPercentValue]:
        return build_object(self['premium_audience'])

    @property
    def boost_url(self) -> str:
        return self['boost_url']

    @property
    def prepaid_giveaways(self) -> Optional[list[aliases.AnyPrepaidGiveaway]]:
        return build_object(self['prepaid_giveaways'])

    @property
    def my_boost_slots(self) -> Optional[list[int]]:
        return self['my_boost_slots']
