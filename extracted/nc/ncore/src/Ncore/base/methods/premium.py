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

class PremiumGetBoostsList(TLMethod[aliases.AnyPremiumBoostsList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, offset: str, limit: int, gifts: Optional[bool] = ...): ...

    def __init__(self, peer, offset, limit, _='premium.getBoostsList', **kwargs):
        kwargs['peer'] = peer
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gifts(self) -> Optional[bool]:
        return self['gifts']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class PremiumGetMyBoosts(TLMethod[aliases.AnyPremiumMyBoosts]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='premium.getMyBoosts'):
        dict.__init__(self, _=_)


class PremiumApplyBoost(TLMethod[aliases.AnyPremiumMyBoosts]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, slots: Optional[list[int]] = ...): ...

    def __init__(self, peer, _='premium.applyBoost', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slots(self) -> Optional[list[int]]:
        return self['slots']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PremiumGetBoostsStatus(TLMethod[aliases.AnyPremiumBoostsStatus]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='premium.getBoostsStatus', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class PremiumGetUserBoosts(TLMethod[aliases.AnyPremiumBoostsList]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, user_id: aliases.AnyInputUser): ...

    def __init__(self, peer, user_id, _='premium.getUserBoosts', **kwargs):
        kwargs['peer'] = peer
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])
