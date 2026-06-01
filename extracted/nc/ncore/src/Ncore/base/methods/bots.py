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

class BotsSendCustomRequest(TLMethod[aliases.AnyDataJSON]):
    __slots__ = ()

    @overload
    def __init__(self, custom_method: str, params: aliases.AnyDataJSON): ...

    def __init__(self, custom_method, params, _='bots.sendCustomRequest', **kwargs):
        kwargs['custom_method'] = custom_method
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def custom_method(self) -> str:
        return self['custom_method']

    @property
    def params(self) -> aliases.AnyDataJSON:
        return build_object(self['params'])


class BotsAnswerWebhookJSONQuery(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, data: aliases.AnyDataJSON): ...

    def __init__(self, query_id, data, _='bots.answerWebhookJSONQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def data(self) -> aliases.AnyDataJSON:
        return build_object(self['data'])


class BotsSetBotCommands(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, scope: aliases.AnyBotCommandScope, lang_code: str, commands: list[aliases.AnyBotCommand]): ...

    def __init__(self, scope, lang_code, commands, _='bots.setBotCommands', **kwargs):
        kwargs['scope'] = scope
        kwargs['lang_code'] = lang_code
        kwargs['commands'] = commands
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def scope(self) -> aliases.AnyBotCommandScope:
        return build_object(self['scope'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def commands(self) -> list[aliases.AnyBotCommand]:
        return build_object(self['commands'])


class BotsResetBotCommands(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, scope: aliases.AnyBotCommandScope, lang_code: str): ...

    def __init__(self, scope, lang_code, _='bots.resetBotCommands', **kwargs):
        kwargs['scope'] = scope
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def scope(self) -> aliases.AnyBotCommandScope:
        return build_object(self['scope'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class BotsGetBotCommands(TLMethod[list[aliases.AnyBotCommand]]):
    __slots__ = ()

    @overload
    def __init__(self, scope: aliases.AnyBotCommandScope, lang_code: str): ...

    def __init__(self, scope, lang_code, _='bots.getBotCommands', **kwargs):
        kwargs['scope'] = scope
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def scope(self) -> aliases.AnyBotCommandScope:
        return build_object(self['scope'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class BotsSetBotMenuButton(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, button: aliases.AnyBotMenuButton): ...

    def __init__(self, user_id, button, _='bots.setBotMenuButton', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['button'] = button
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def button(self) -> aliases.AnyBotMenuButton:
        return build_object(self['button'])


class BotsGetBotMenuButton(TLMethod[aliases.AnyBotMenuButton]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser): ...

    def __init__(self, user_id, _='bots.getBotMenuButton', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class BotsSetBotBroadcastDefaultAdminRights(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, admin_rights: aliases.AnyChatAdminRights): ...

    def __init__(self, admin_rights, _='bots.setBotBroadcastDefaultAdminRights', **kwargs):
        kwargs['admin_rights'] = admin_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def admin_rights(self) -> aliases.AnyChatAdminRights:
        return build_object(self['admin_rights'])


class BotsSetBotGroupDefaultAdminRights(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, admin_rights: aliases.AnyChatAdminRights): ...

    def __init__(self, admin_rights, _='bots.setBotGroupDefaultAdminRights', **kwargs):
        kwargs['admin_rights'] = admin_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def admin_rights(self) -> aliases.AnyChatAdminRights:
        return build_object(self['admin_rights'])


class BotsSetBotInfo(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, bot: Optional[aliases.AnyInputUser] = ..., name: Optional[str] = ..., about: Optional[str] = ..., description: Optional[str] = ...): ...

    def __init__(self, lang_code, _='bots.setBotInfo', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def name(self) -> Optional[str]:
        return self['name']

    @property
    def about(self) -> Optional[str]:
        return self['about']

    @property
    def description(self) -> Optional[str]:
        return self['description']


class BotsGetBotInfo(TLMethod[aliases.AnyBotsBotInfo]):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, bot: Optional[aliases.AnyInputUser] = ...): ...

    def __init__(self, lang_code, _='bots.getBotInfo', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class BotsReorderUsernames(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, order: list[str]): ...

    def __init__(self, bot, order, _='bots.reorderUsernames', **kwargs):
        kwargs['bot'] = bot
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def order(self) -> list[str]:
        return self['order']


class BotsToggleUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, username: str, active: bool): ...

    def __init__(self, bot, username, active, _='bots.toggleUsername', **kwargs):
        kwargs['bot'] = bot
        kwargs['username'] = username
        kwargs['active'] = active
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def username(self) -> str:
        return self['username']

    @property
    def active(self) -> bool:
        return self['active']


class BotsCanSendMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser): ...

    def __init__(self, bot, _='bots.canSendMessage', **kwargs):
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class BotsAllowSendMessage(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser): ...

    def __init__(self, bot, _='bots.allowSendMessage', **kwargs):
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class BotsInvokeWebViewCustomMethod(TLMethod[aliases.AnyDataJSON]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, custom_method: str, params: aliases.AnyDataJSON): ...

    def __init__(self, bot, custom_method, params, _='bots.invokeWebViewCustomMethod', **kwargs):
        kwargs['bot'] = bot
        kwargs['custom_method'] = custom_method
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def custom_method(self) -> str:
        return self['custom_method']

    @property
    def params(self) -> aliases.AnyDataJSON:
        return build_object(self['params'])


class BotsGetPopularAppBots(TLMethod[aliases.AnyBotsPopularAppBots]):
    __slots__ = ()

    @overload
    def __init__(self, offset: str, limit: int): ...

    def __init__(self, offset, limit, _='bots.getPopularAppBots', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']


class BotsAddPreviewMedia(TLMethod[aliases.AnyBotPreviewMedia]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, lang_code: str, media: aliases.AnyInputMedia): ...

    def __init__(self, bot, lang_code, media, _='bots.addPreviewMedia', **kwargs):
        kwargs['bot'] = bot
        kwargs['lang_code'] = lang_code
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])


class BotsEditPreviewMedia(TLMethod[aliases.AnyBotPreviewMedia]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, lang_code: str, media: aliases.AnyInputMedia, new_media: aliases.AnyInputMedia): ...

    def __init__(self, bot, lang_code, media, new_media, _='bots.editPreviewMedia', **kwargs):
        kwargs['bot'] = bot
        kwargs['lang_code'] = lang_code
        kwargs['media'] = media
        kwargs['new_media'] = new_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])

    @property
    def new_media(self) -> aliases.AnyInputMedia:
        return build_object(self['new_media'])


class BotsDeletePreviewMedia(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, lang_code: str, media: list[aliases.AnyInputMedia]): ...

    def __init__(self, bot, lang_code, media, _='bots.deletePreviewMedia', **kwargs):
        kwargs['bot'] = bot
        kwargs['lang_code'] = lang_code
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def media(self) -> list[aliases.AnyInputMedia]:
        return build_object(self['media'])


class BotsReorderPreviewMedias(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, lang_code: str, order: list[aliases.AnyInputMedia]): ...

    def __init__(self, bot, lang_code, order, _='bots.reorderPreviewMedias', **kwargs):
        kwargs['bot'] = bot
        kwargs['lang_code'] = lang_code
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def order(self) -> list[aliases.AnyInputMedia]:
        return build_object(self['order'])


class BotsGetPreviewInfo(TLMethod[aliases.AnyBotsPreviewInfo]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, lang_code: str): ...

    def __init__(self, bot, lang_code, _='bots.getPreviewInfo', **kwargs):
        kwargs['bot'] = bot
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class BotsGetPreviewMedias(TLMethod[list[aliases.AnyBotPreviewMedia]]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser): ...

    def __init__(self, bot, _='bots.getPreviewMedias', **kwargs):
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class BotsUpdateUserEmojiStatus(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, emoji_status: aliases.AnyEmojiStatus): ...

    def __init__(self, user_id, emoji_status, _='bots.updateUserEmojiStatus', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['emoji_status'] = emoji_status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def emoji_status(self) -> aliases.AnyEmojiStatus:
        return build_object(self['emoji_status'])


class BotsToggleUserEmojiStatusPermission(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, enabled: bool): ...

    def __init__(self, bot, enabled, _='bots.toggleUserEmojiStatusPermission', **kwargs):
        kwargs['bot'] = bot
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def enabled(self) -> bool:
        return self['enabled']


class BotsCheckDownloadFileParams(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, file_name: str, url: str): ...

    def __init__(self, bot, file_name, url, _='bots.checkDownloadFileParams', **kwargs):
        kwargs['bot'] = bot
        kwargs['file_name'] = file_name
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def file_name(self) -> str:
        return self['file_name']

    @property
    def url(self) -> str:
        return self['url']


class BotsGetAdminedBots(TLMethod[list[aliases.AnyUser]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='bots.getAdminedBots'):
        dict.__init__(self, _=_)


class BotsUpdateStarRefProgram(TLMethod[aliases.AnyStarRefProgram]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, commission_permille: int, duration_months: Optional[int] = ...): ...

    def __init__(self, bot, commission_permille, _='bots.updateStarRefProgram', **kwargs):
        kwargs['bot'] = bot
        kwargs['commission_permille'] = commission_permille
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def commission_permille(self) -> int:
        return self['commission_permille']

    @property
    def duration_months(self) -> Optional[int]:
        return self['duration_months']


class BotsSetCustomVerification(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, enabled: Optional[bool] = ..., bot: Optional[aliases.AnyInputUser] = ..., custom_description: Optional[str] = ...): ...

    def __init__(self, peer, _='bots.setCustomVerification', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def enabled(self) -> Optional[bool]:
        return self['enabled']

    @property
    def bot(self) -> Optional[aliases.AnyInputUser]:
        return build_object(self['bot'])

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def custom_description(self) -> Optional[str]:
        return self['custom_description']


class BotsGetBotRecommendations(TLMethod[aliases.AnyUsersUsers]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser): ...

    def __init__(self, bot, _='bots.getBotRecommendations', **kwargs):
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])
