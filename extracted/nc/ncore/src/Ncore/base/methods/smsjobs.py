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

class SmsjobsIsEligibleToJoin(TLMethod[aliases.AnySmsjobsEligibilityToJoin]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='smsjobs.isEligibleToJoin'):
        dict.__init__(self, _=_)


class SmsjobsJoin(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='smsjobs.join'):
        dict.__init__(self, _=_)


class SmsjobsLeave(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='smsjobs.leave'):
        dict.__init__(self, _=_)


class SmsjobsUpdateSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, allow_international: Optional[bool] = ...): ...

    def __init__(self, _='smsjobs.updateSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def allow_international(self) -> Optional[bool]:
        return self['allow_international']


class SmsjobsGetStatus(TLMethod[aliases.AnySmsjobsStatus]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='smsjobs.getStatus'):
        dict.__init__(self, _=_)


class SmsjobsGetSmsJob(TLMethod[aliases.AnySmsJob]):
    __slots__ = ()

    @overload
    def __init__(self, job_id: str): ...

    def __init__(self, job_id, _='smsjobs.getSmsJob', **kwargs):
        kwargs['job_id'] = job_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def job_id(self) -> str:
        return self['job_id']


class SmsjobsFinishJob(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, job_id: str, error: Optional[str] = ...): ...

    def __init__(self, job_id, _='smsjobs.finishJob', **kwargs):
        kwargs['job_id'] = job_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def job_id(self) -> str:
        return self['job_id']

    @property
    def error(self) -> Optional[str]:
        return self['error']
