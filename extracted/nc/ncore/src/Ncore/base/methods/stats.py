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

class StatsGetBroadcastStats(TLMethod[aliases.AnyStatsBroadcastStats]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, dark: Optional[bool] = ...): ...

    def __init__(self, channel, _='stats.getBroadcastStats', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class StatsLoadAsyncGraph(TLMethod[aliases.AnyStatsGraph]):
    __slots__ = ()

    @overload
    def __init__(self, token: str, x: Optional[int] = ...): ...

    def __init__(self, token, _='stats.loadAsyncGraph', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']

    @property
    def x(self) -> Optional[int]:
        return self['x']


class StatsGetMegagroupStats(TLMethod[aliases.AnyStatsMegagroupStats]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, dark: Optional[bool] = ...): ...

    def __init__(self, channel, _='stats.getMegagroupStats', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class StatsGetMessagePublicForwards(TLMethod[aliases.AnyStatsPublicForwards]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, msg_id: int, offset: str, limit: int): ...

    def __init__(self, channel, msg_id, offset, limit, _='stats.getMessagePublicForwards', **kwargs):
        kwargs['channel'] = channel
        kwargs['msg_id'] = msg_id
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class StatsGetMessageStats(TLMethod[aliases.AnyStatsMessageStats]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, msg_id: int, dark: Optional[bool] = ...): ...

    def __init__(self, channel, msg_id, _='stats.getMessageStats', **kwargs):
        kwargs['channel'] = channel
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class StatsGetStoryStats(TLMethod[aliases.AnyStatsStoryStats]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, dark: Optional[bool] = ...): ...

    def __init__(self, peer, id, _='stats.getStoryStats', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']


class StatsGetStoryPublicForwards(TLMethod[aliases.AnyStatsPublicForwards]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int, offset: str, limit: int): ...

    def __init__(self, peer, id, offset, limit, _='stats.getStoryPublicForwards', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['offset'] = offset
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
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']
