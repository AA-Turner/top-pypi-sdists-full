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

class UpdatesGetState(TLMethod[aliases.AnyUpdatesState]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updates.getState'):
        dict.__init__(self, _=_)


class UpdatesGetDifference(TLMethod[aliases.AnyUpdatesDifference]):
    __slots__ = ()

    @overload
    def __init__(self, pts: int, date: int, qts: int, pts_limit: Optional[int] = ..., pts_total_limit: Optional[int] = ..., qts_limit: Optional[int] = ...): ...

    def __init__(self, pts, date, qts, _='updates.getDifference', **kwargs):
        kwargs['pts'] = pts
        kwargs['date'] = date
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_limit(self) -> Optional[int]:
        return self['pts_limit']

    @property
    def pts_total_limit(self) -> Optional[int]:
        return self['pts_total_limit']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def qts(self) -> int:
        return self['qts']

    @property
    def qts_limit(self) -> Optional[int]:
        return self['qts_limit']


class UpdatesGetChannelDifference(TLMethod[aliases.AnyUpdatesChannelDifference]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel, filter: aliases.AnyChannelMessagesFilter, pts: int, limit: int, force: Optional[bool] = ...): ...

    def __init__(self, channel, filter, pts, limit, _='updates.getChannelDifference', **kwargs):
        kwargs['channel'] = channel
        kwargs['filter'] = filter
        kwargs['pts'] = pts
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force(self) -> Optional[bool]:
        return self['force']

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def filter(self) -> aliases.AnyChannelMessagesFilter:
        return build_object(self['filter'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def limit(self) -> int:
        return self['limit']
