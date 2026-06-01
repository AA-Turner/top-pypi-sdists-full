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


class BotsBotInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, about: str, description: str): ...

    def __init__(self, name, about, description, _='bots.botInfo', **kwargs):
        kwargs['name'] = name
        kwargs['about'] = about
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']

    @property
    def about(self) -> str:
        return self['about']

    @property
    def description(self) -> str:
        return self['description']


class BotsPopularAppBots(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, users, _='bots.popularAppBots', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class BotsPreviewInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, media: list[aliases.AnyBotPreviewMedia], lang_codes: list[str]): ...

    def __init__(self, media, lang_codes, _='bots.previewInfo', **kwargs):
        kwargs['media'] = media
        kwargs['lang_codes'] = lang_codes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> list[aliases.AnyBotPreviewMedia]:
        return build_object(self['media'])

    @property
    def lang_codes(self) -> list[str]:
        return self['lang_codes']
