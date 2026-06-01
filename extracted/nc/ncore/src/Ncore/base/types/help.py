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


class HelpAppUpdate(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, version: str, text: str, entities: list[aliases.AnyMessageEntity], can_not_skip: Optional[bool] = ..., document: Optional[aliases.AnyDocument] = ..., url: Optional[str] = ..., sticker: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, id, version, text, entities, _='help.appUpdate', **kwargs):
        kwargs['id'] = id
        kwargs['version'] = version
        kwargs['text'] = text
        kwargs['entities'] = entities
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_not_skip(self) -> Optional[bool]:
        return self['can_not_skip']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def version(self) -> str:
        return self['version']

    @property
    def text(self) -> str:
        return self['text']

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def sticker(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['sticker'])


class HelpNoAppUpdate(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.noAppUpdate'):
        dict.__init__(self, _=_)


class HelpInviteText(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str): ...

    def __init__(self, message, _='help.inviteText', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> str:
        return self['message']


class HelpSupport(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, user: aliases.AnyUser): ...

    def __init__(self, phone_number, user, _='help.support', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['user'] = user
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def user(self) -> aliases.AnyUser:
        return build_object(self['user'])


class HelpTermsOfService(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyDataJSON, text: str, entities: list[aliases.AnyMessageEntity], popup: Optional[bool] = ..., min_age_confirm: Optional[int] = ...): ...

    def __init__(self, id, text, entities, _='help.termsOfService', **kwargs):
        kwargs['id'] = id
        kwargs['text'] = text
        kwargs['entities'] = entities
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def popup(self) -> Optional[bool]:
        return self['popup']

    @property
    def id(self) -> aliases.AnyDataJSON:
        return build_object(self['id'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])

    @property
    def min_age_confirm(self) -> Optional[int]:
        return self['min_age_confirm']


class HelpRecentMeUrls(dict):
    __slots__ = ()

    @overload
    def __init__(self, urls: list[aliases.AnyRecentMeUrl], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, urls, chats, users, _='help.recentMeUrls', **kwargs):
        kwargs['urls'] = urls
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def urls(self) -> list[aliases.AnyRecentMeUrl]:
        return build_object(self['urls'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class HelpTermsOfServiceUpdateEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int): ...

    def __init__(self, expires, _='help.termsOfServiceUpdateEmpty', **kwargs):
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']


class HelpTermsOfServiceUpdate(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int, terms_of_service: aliases.AnyHelpTermsOfService): ...

    def __init__(self, expires, terms_of_service, _='help.termsOfServiceUpdate', **kwargs):
        kwargs['expires'] = expires
        kwargs['terms_of_service'] = terms_of_service
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def terms_of_service(self) -> aliases.AnyHelpTermsOfService:
        return build_object(self['terms_of_service'])


class HelpDeepLinkInfoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.deepLinkInfoEmpty'):
        dict.__init__(self, _=_)


class HelpDeepLinkInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, update_app: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, message, _='help.deepLinkInfo', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def update_app(self) -> Optional[bool]:
        return self['update_app']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])


class HelpPassportConfigNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.passportConfigNotModified'):
        dict.__init__(self, _=_)


class HelpPassportConfig(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, countries_langs: aliases.AnyDataJSON): ...

    def __init__(self, hash, countries_langs, _='help.passportConfig', **kwargs):
        kwargs['hash'] = hash
        kwargs['countries_langs'] = countries_langs
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def countries_langs(self) -> aliases.AnyDataJSON:
        return build_object(self['countries_langs'])


class HelpSupportName(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str): ...

    def __init__(self, name, _='help.supportName', **kwargs):
        kwargs['name'] = name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']


class HelpUserInfoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.userInfoEmpty'):
        dict.__init__(self, _=_)


class HelpUserInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, entities: list[aliases.AnyMessageEntity], author: str, date: int): ...

    def __init__(self, message, entities, author, date, _='help.userInfo', **kwargs):
        kwargs['message'] = message
        kwargs['entities'] = entities
        kwargs['author'] = author
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])

    @property
    def author(self) -> str:
        return self['author']

    @property
    def date(self) -> int:
        return self['date']


class HelpPromoDataEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int): ...

    def __init__(self, expires, _='help.promoDataEmpty', **kwargs):
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']


class HelpPromoData(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int, pending_suggestions: list[str], dismissed_suggestions: list[str], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], proxy: Optional[bool] = ..., peer: Optional[aliases.AnyPeer] = ..., psa_type: Optional[str] = ..., psa_message: Optional[str] = ..., custom_pending_suggestion: Optional[aliases.AnyPendingSuggestion] = ...): ...

    def __init__(self, expires, pending_suggestions, dismissed_suggestions, chats, users, _='help.promoData', **kwargs):
        kwargs['expires'] = expires
        kwargs['pending_suggestions'] = pending_suggestions
        kwargs['dismissed_suggestions'] = dismissed_suggestions
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def proxy(self) -> Optional[bool]:
        return self['proxy']

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer'])

    @property
    def psa_type(self) -> Optional[str]:
        return self['psa_type']

    @property
    def psa_message(self) -> Optional[str]:
        return self['psa_message']

    @property
    def pending_suggestions(self) -> list[str]:
        return self['pending_suggestions']

    @property
    def dismissed_suggestions(self) -> list[str]:
        return self['dismissed_suggestions']

    @property
    def custom_pending_suggestion(self) -> Optional[aliases.AnyPendingSuggestion]:
        return build_object(self['custom_pending_suggestion'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class HelpCountryCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, country_code: str, prefixes: Optional[list[str]] = ..., patterns: Optional[list[str]] = ...): ...

    def __init__(self, country_code, _='help.countryCode', **kwargs):
        kwargs['country_code'] = country_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def country_code(self) -> str:
        return self['country_code']

    @property
    def prefixes(self) -> Optional[list[str]]:
        return self['prefixes']

    @property
    def patterns(self) -> Optional[list[str]]:
        return self['patterns']


class HelpCountry(dict):
    __slots__ = ()

    @overload
    def __init__(self, iso2: str, default_name: str, country_codes: list[aliases.AnyHelpCountryCode], hidden: Optional[bool] = ..., name: Optional[str] = ...): ...

    def __init__(self, iso2, default_name, country_codes, _='help.country', **kwargs):
        kwargs['iso2'] = iso2
        kwargs['default_name'] = default_name
        kwargs['country_codes'] = country_codes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']

    @property
    def iso2(self) -> str:
        return self['iso2']

    @property
    def default_name(self) -> str:
        return self['default_name']

    @property
    def name(self) -> Optional[str]:
        return self['name']

    @property
    def country_codes(self) -> list[aliases.AnyHelpCountryCode]:
        return build_object(self['country_codes'])


class HelpCountriesListNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.countriesListNotModified'):
        dict.__init__(self, _=_)


class HelpCountriesList(dict):
    __slots__ = ()

    @overload
    def __init__(self, countries: list[aliases.AnyHelpCountry], hash: int): ...

    def __init__(self, countries, hash, _='help.countriesList', **kwargs):
        kwargs['countries'] = countries
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def countries(self) -> list[aliases.AnyHelpCountry]:
        return build_object(self['countries'])

    @property
    def hash(self) -> int:
        return self['hash']


class HelpPremiumPromo(dict):
    __slots__ = ()

    @overload
    def __init__(self, status_text: str, status_entities: list[aliases.AnyMessageEntity], video_sections: list[str], videos: list[aliases.AnyDocument], period_options: list[aliases.AnyPremiumSubscriptionOption], users: list[aliases.AnyUser]): ...

    def __init__(self, status_text, status_entities, video_sections, videos, period_options, users, _='help.premiumPromo', **kwargs):
        kwargs['status_text'] = status_text
        kwargs['status_entities'] = status_entities
        kwargs['video_sections'] = video_sections
        kwargs['videos'] = videos
        kwargs['period_options'] = period_options
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def status_text(self) -> str:
        return self['status_text']

    @property
    def status_entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['status_entities'])

    @property
    def video_sections(self) -> list[str]:
        return self['video_sections']

    @property
    def videos(self) -> list[aliases.AnyDocument]:
        return build_object(self['videos'])

    @property
    def period_options(self) -> list[aliases.AnyPremiumSubscriptionOption]:
        return build_object(self['period_options'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class HelpAppConfigNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.appConfigNotModified'):
        dict.__init__(self, _=_)


class HelpAppConfig(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, config: aliases.AnyJSONValue): ...

    def __init__(self, hash, config, _='help.appConfig', **kwargs):
        kwargs['hash'] = hash
        kwargs['config'] = config
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def config(self) -> aliases.AnyJSONValue:
        return build_object(self['config'])


class HelpPeerColorSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, colors: list[int]): ...

    def __init__(self, colors, _='help.peerColorSet', **kwargs):
        kwargs['colors'] = colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def colors(self) -> list[int]:
        return self['colors']


class HelpPeerColorProfileSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, palette_colors: list[int], bg_colors: list[int], story_colors: list[int]): ...

    def __init__(self, palette_colors, bg_colors, story_colors, _='help.peerColorProfileSet', **kwargs):
        kwargs['palette_colors'] = palette_colors
        kwargs['bg_colors'] = bg_colors
        kwargs['story_colors'] = story_colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def palette_colors(self) -> list[int]:
        return self['palette_colors']

    @property
    def bg_colors(self) -> list[int]:
        return self['bg_colors']

    @property
    def story_colors(self) -> list[int]:
        return self['story_colors']


class HelpPeerColorOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, color_id: int, hidden: Optional[bool] = ..., colors: Optional[aliases.AnyHelpPeerColorSet] = ..., dark_colors: Optional[aliases.AnyHelpPeerColorSet] = ..., channel_min_level: Optional[int] = ..., group_min_level: Optional[int] = ...): ...

    def __init__(self, color_id, _='help.peerColorOption', **kwargs):
        kwargs['color_id'] = color_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']

    @property
    def color_id(self) -> int:
        return self['color_id']

    @property
    def colors(self) -> Optional[aliases.AnyHelpPeerColorSet]:
        return build_object(self['colors'])

    @property
    def dark_colors(self) -> Optional[aliases.AnyHelpPeerColorSet]:
        return build_object(self['dark_colors'])

    @property
    def channel_min_level(self) -> Optional[int]:
        return self['channel_min_level']

    @property
    def group_min_level(self) -> Optional[int]:
        return self['group_min_level']


class HelpPeerColorsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.peerColorsNotModified'):
        dict.__init__(self, _=_)


class HelpPeerColors(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, colors: list[aliases.AnyHelpPeerColorOption]): ...

    def __init__(self, hash, colors, _='help.peerColors', **kwargs):
        kwargs['hash'] = hash
        kwargs['colors'] = colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def colors(self) -> list[aliases.AnyHelpPeerColorOption]:
        return build_object(self['colors'])


class HelpTimezonesListNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='help.timezonesListNotModified'):
        dict.__init__(self, _=_)


class HelpTimezonesList(dict):
    __slots__ = ()

    @overload
    def __init__(self, timezones: list[aliases.AnyTimezone], hash: int): ...

    def __init__(self, timezones, hash, _='help.timezonesList', **kwargs):
        kwargs['timezones'] = timezones
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def timezones(self) -> list[aliases.AnyTimezone]:
        return build_object(self['timezones'])

    @property
    def hash(self) -> int:
        return self['hash']
