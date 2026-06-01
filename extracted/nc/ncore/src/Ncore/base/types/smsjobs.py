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


class SmsjobsEligibleToJoin(dict):
    __slots__ = ()

    @overload
    def __init__(self, terms_url: str, monthly_sent_sms: int): ...

    def __init__(self, terms_url, monthly_sent_sms, _='smsjobs.eligibleToJoin', **kwargs):
        kwargs['terms_url'] = terms_url
        kwargs['monthly_sent_sms'] = monthly_sent_sms
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def terms_url(self) -> str:
        return self['terms_url']

    @property
    def monthly_sent_sms(self) -> int:
        return self['monthly_sent_sms']


class SmsjobsStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, recent_sent: int, recent_since: int, recent_remains: int, total_sent: int, total_since: int, terms_url: str, allow_international: Optional[bool] = ..., last_gift_slug: Optional[str] = ...): ...

    def __init__(self, recent_sent, recent_since, recent_remains, total_sent, total_since, terms_url, _='smsjobs.status', **kwargs):
        kwargs['recent_sent'] = recent_sent
        kwargs['recent_since'] = recent_since
        kwargs['recent_remains'] = recent_remains
        kwargs['total_sent'] = total_sent
        kwargs['total_since'] = total_since
        kwargs['terms_url'] = terms_url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def allow_international(self) -> Optional[bool]:
        return self['allow_international']

    @property
    def recent_sent(self) -> int:
        return self['recent_sent']

    @property
    def recent_since(self) -> int:
        return self['recent_since']

    @property
    def recent_remains(self) -> int:
        return self['recent_remains']

    @property
    def total_sent(self) -> int:
        return self['total_sent']

    @property
    def total_since(self) -> int:
        return self['total_since']

    @property
    def last_gift_slug(self) -> Optional[str]:
        return self['last_gift_slug']

    @property
    def terms_url(self) -> str:
        return self['terms_url']
