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

class LangpackGetLangPack(TLMethod[aliases.AnyLangPackDifference]):
    __slots__ = ()

    @overload
    def __init__(self, lang_pack: str, lang_code: str): ...

    def __init__(self, lang_pack, lang_code, _='langpack.getLangPack', **kwargs):
        kwargs['lang_pack'] = lang_pack
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class LangpackGetStrings(TLMethod[list[aliases.AnyLangPackString]]):
    __slots__ = ()

    @overload
    def __init__(self, lang_pack: str, lang_code: str, keys_: list[str]): ...

    def __init__(self, lang_pack, lang_code, keys_, _='langpack.getStrings', **kwargs):
        kwargs['lang_pack'] = lang_pack
        kwargs['lang_code'] = lang_code
        kwargs['keys'] = keys_
        if 'keys_' in kwargs:
            kwargs['keys'] = kwargs.pop('keys_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def keys_(self) -> list[str]:
        return self['keys']


class LangpackGetDifference(TLMethod[aliases.AnyLangPackDifference]):
    __slots__ = ()

    @overload
    def __init__(self, lang_pack: str, lang_code: str, from_version: int): ...

    def __init__(self, lang_pack, lang_code, from_version, _='langpack.getDifference', **kwargs):
        kwargs['lang_pack'] = lang_pack
        kwargs['lang_code'] = lang_code
        kwargs['from_version'] = from_version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def from_version(self) -> int:
        return self['from_version']


class LangpackGetLanguages(TLMethod[list[aliases.AnyLangPackLanguage]]):
    __slots__ = ()

    @overload
    def __init__(self, lang_pack: str): ...

    def __init__(self, lang_pack, _='langpack.getLanguages', **kwargs):
        kwargs['lang_pack'] = lang_pack
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']


class LangpackGetLanguage(TLMethod[aliases.AnyLangPackLanguage]):
    __slots__ = ()

    @overload
    def __init__(self, lang_pack: str, lang_code: str): ...

    def __init__(self, lang_pack, lang_code, _='langpack.getLanguage', **kwargs):
        kwargs['lang_pack'] = lang_pack
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']

    @property
    def lang_code(self) -> str:
        return self['lang_code']
