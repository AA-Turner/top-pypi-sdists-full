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


class AccountPrivacyRules(dict):
    __slots__ = ()

    @overload
    def __init__(self, rules: list[aliases.AnyPrivacyRule], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, rules, chats, users, _='account.privacyRules', **kwargs):
        kwargs['rules'] = rules
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def rules(self) -> list[aliases.AnyPrivacyRule]:
        return build_object(self['rules'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountAuthorizations(dict):
    __slots__ = ()

    @overload
    def __init__(self, authorization_ttl_days: int, authorizations: list[aliases.AnyAuthorization]): ...

    def __init__(self, authorization_ttl_days, authorizations, _='account.authorizations', **kwargs):
        kwargs['authorization_ttl_days'] = authorization_ttl_days
        kwargs['authorizations'] = authorizations
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def authorization_ttl_days(self) -> int:
        return self['authorization_ttl_days']

    @property
    def authorizations(self) -> list[aliases.AnyAuthorization]:
        return build_object(self['authorizations'])


class AccountPassword(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_algo: aliases.AnyPasswordKdfAlgo, new_secure_algo: aliases.AnySecurePasswordKdfAlgo, secure_random: bytes, has_recovery: Optional[bool] = ..., has_secure_values: Optional[bool] = ..., has_password: Optional[bool] = ..., current_algo: Optional[aliases.AnyPasswordKdfAlgo] = ..., srp_B: Optional[bytes] = ..., srp_id: Optional[int] = ..., hint: Optional[str] = ..., email_unconfirmed_pattern: Optional[str] = ..., pending_reset_date: Optional[int] = ..., login_email_pattern: Optional[str] = ...): ...

    def __init__(self, new_algo, new_secure_algo, secure_random, _='account.password', **kwargs):
        kwargs['new_algo'] = new_algo
        kwargs['new_secure_algo'] = new_secure_algo
        kwargs['secure_random'] = secure_random
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_recovery(self) -> Optional[bool]:
        return self['has_recovery']

    @property
    def has_secure_values(self) -> Optional[bool]:
        return self['has_secure_values']

    @property
    def has_password(self) -> Optional[bool]:
        return self['has_password']

    @property
    def current_algo(self) -> Optional[aliases.AnyPasswordKdfAlgo]:
        return build_object(self['current_algo'])

    @property
    def srp_B(self) -> Optional[bytes]:
        return self['srp_B']

    @property
    def srp_id(self) -> Optional[int]:
        return self['srp_id']

    @property
    def hint(self) -> Optional[str]:
        return self['hint']

    @property
    def email_unconfirmed_pattern(self) -> Optional[str]:
        return self['email_unconfirmed_pattern']

    @property
    def new_algo(self) -> aliases.AnyPasswordKdfAlgo:
        return build_object(self['new_algo'])

    @property
    def new_secure_algo(self) -> aliases.AnySecurePasswordKdfAlgo:
        return build_object(self['new_secure_algo'])

    @property
    def secure_random(self) -> bytes:
        return self['secure_random']

    @property
    def pending_reset_date(self) -> Optional[int]:
        return self['pending_reset_date']

    @property
    def login_email_pattern(self) -> Optional[str]:
        return self['login_email_pattern']


class AccountPasswordSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, email: Optional[str] = ..., secure_settings: Optional[aliases.AnySecureSecretSettings] = ...): ...

    def __init__(self, _='account.passwordSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email(self) -> Optional[str]:
        return self['email']

    @property
    def secure_settings(self) -> Optional[aliases.AnySecureSecretSettings]:
        return build_object(self['secure_settings'])


class AccountPasswordInputSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_algo: Optional[aliases.AnyPasswordKdfAlgo] = ..., new_password_hash: Optional[bytes] = ..., hint: Optional[str] = ..., email: Optional[str] = ..., new_secure_settings: Optional[aliases.AnySecureSecretSettings] = ...): ...

    def __init__(self, _='account.passwordInputSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_algo(self) -> Optional[aliases.AnyPasswordKdfAlgo]:
        return build_object(self['new_algo'])

    @property
    def new_password_hash(self) -> Optional[bytes]:
        return self['new_password_hash']

    @property
    def hint(self) -> Optional[str]:
        return self['hint']

    @property
    def email(self) -> Optional[str]:
        return self['email']

    @property
    def new_secure_settings(self) -> Optional[aliases.AnySecureSecretSettings]:
        return build_object(self['new_secure_settings'])


class AccountTmpPassword(dict):
    __slots__ = ()

    @overload
    def __init__(self, tmp_password: bytes, valid_until: int): ...

    def __init__(self, tmp_password, valid_until, _='account.tmpPassword', **kwargs):
        kwargs['tmp_password'] = tmp_password
        kwargs['valid_until'] = valid_until
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def tmp_password(self) -> bytes:
        return self['tmp_password']

    @property
    def valid_until(self) -> int:
        return self['valid_until']


class AccountWebAuthorizations(dict):
    __slots__ = ()

    @overload
    def __init__(self, authorizations: list[aliases.AnyWebAuthorization], users: list[aliases.AnyUser]): ...

    def __init__(self, authorizations, users, _='account.webAuthorizations', **kwargs):
        kwargs['authorizations'] = authorizations
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def authorizations(self) -> list[aliases.AnyWebAuthorization]:
        return build_object(self['authorizations'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountAuthorizationForm(dict):
    __slots__ = ()

    @overload
    def __init__(self, required_types: list[aliases.AnySecureRequiredType], values_: list[aliases.AnySecureValue], errors: list[aliases.AnySecureValueError], users: list[aliases.AnyUser], privacy_policy_url: Optional[str] = ...): ...

    def __init__(self, required_types, values_, errors, users, _='account.authorizationForm', **kwargs):
        kwargs['required_types'] = required_types
        kwargs['values'] = values_
        kwargs['errors'] = errors
        kwargs['users'] = users
        if 'values_' in kwargs:
            kwargs['values'] = kwargs.pop('values_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def required_types(self) -> list[aliases.AnySecureRequiredType]:
        return build_object(self['required_types'])

    @property
    def values_(self) -> list[aliases.AnySecureValue]:
        return build_object(self['values'])

    @property
    def errors(self) -> list[aliases.AnySecureValueError]:
        return build_object(self['errors'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def privacy_policy_url(self) -> Optional[str]:
        return self['privacy_policy_url']


class AccountSentEmailCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, email_pattern: str, length: int): ...

    def __init__(self, email_pattern, length, _='account.sentEmailCode', **kwargs):
        kwargs['email_pattern'] = email_pattern
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email_pattern(self) -> str:
        return self['email_pattern']

    @property
    def length(self) -> int:
        return self['length']


class AccountTakeout(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='account.takeout', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class AccountWallPapersNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.wallPapersNotModified'):
        dict.__init__(self, _=_)


class AccountWallPapers(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, wallpapers: list[aliases.AnyWallPaper]): ...

    def __init__(self, hash, wallpapers, _='account.wallPapers', **kwargs):
        kwargs['hash'] = hash
        kwargs['wallpapers'] = wallpapers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def wallpapers(self) -> list[aliases.AnyWallPaper]:
        return build_object(self['wallpapers'])


class AccountAutoDownloadSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, low: aliases.AnyAutoDownloadSettings, medium: aliases.AnyAutoDownloadSettings, high: aliases.AnyAutoDownloadSettings): ...

    def __init__(self, low, medium, high, _='account.autoDownloadSettings', **kwargs):
        kwargs['low'] = low
        kwargs['medium'] = medium
        kwargs['high'] = high
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def low(self) -> aliases.AnyAutoDownloadSettings:
        return build_object(self['low'])

    @property
    def medium(self) -> aliases.AnyAutoDownloadSettings:
        return build_object(self['medium'])

    @property
    def high(self) -> aliases.AnyAutoDownloadSettings:
        return build_object(self['high'])


class AccountThemesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.themesNotModified'):
        dict.__init__(self, _=_)


class AccountThemes(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, themes: list[aliases.AnyTheme]): ...

    def __init__(self, hash, themes, _='account.themes', **kwargs):
        kwargs['hash'] = hash
        kwargs['themes'] = themes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def themes(self) -> list[aliases.AnyTheme]:
        return build_object(self['themes'])


class AccountContentSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, sensitive_enabled: Optional[bool] = ..., sensitive_can_change: Optional[bool] = ...): ...

    def __init__(self, _='account.contentSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sensitive_enabled(self) -> Optional[bool]:
        return self['sensitive_enabled']

    @property
    def sensitive_can_change(self) -> Optional[bool]:
        return self['sensitive_can_change']


class AccountResetPasswordFailedWait(dict):
    __slots__ = ()

    @overload
    def __init__(self, retry_date: int): ...

    def __init__(self, retry_date, _='account.resetPasswordFailedWait', **kwargs):
        kwargs['retry_date'] = retry_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def retry_date(self) -> int:
        return self['retry_date']


class AccountResetPasswordRequestedWait(dict):
    __slots__ = ()

    @overload
    def __init__(self, until_date: int): ...

    def __init__(self, until_date, _='account.resetPasswordRequestedWait', **kwargs):
        kwargs['until_date'] = until_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def until_date(self) -> int:
        return self['until_date']


class AccountResetPasswordOk(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resetPasswordOk'):
        dict.__init__(self, _=_)


class AccountChatThemesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.chatThemesNotModified'):
        dict.__init__(self, _=_)


class AccountChatThemes(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, themes: list[aliases.AnyChatTheme], chats: list[aliases.AnyChat], users: list[aliases.AnyUser], next_offset: Optional[str] = ...): ...

    def __init__(self, hash, themes, chats, users, _='account.chatThemes', **kwargs):
        kwargs['hash'] = hash
        kwargs['themes'] = themes
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def themes(self) -> list[aliases.AnyChatTheme]:
        return build_object(self['themes'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def next_offset(self) -> Optional[str]:
        return self['next_offset']


class AccountSavedRingtonesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.savedRingtonesNotModified'):
        dict.__init__(self, _=_)


class AccountSavedRingtones(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, ringtones: list[aliases.AnyDocument]): ...

    def __init__(self, hash, ringtones, _='account.savedRingtones', **kwargs):
        kwargs['hash'] = hash
        kwargs['ringtones'] = ringtones
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def ringtones(self) -> list[aliases.AnyDocument]:
        return build_object(self['ringtones'])


class AccountSavedRingtone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.savedRingtone'):
        dict.__init__(self, _=_)


class AccountSavedRingtoneConverted(dict):
    __slots__ = ()

    @overload
    def __init__(self, document: aliases.AnyDocument): ...

    def __init__(self, document, _='account.savedRingtoneConverted', **kwargs):
        kwargs['document'] = document
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document(self) -> aliases.AnyDocument:
        return build_object(self['document'])


class AccountEmojiStatusesNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.emojiStatusesNotModified'):
        dict.__init__(self, _=_)


class AccountEmojiStatuses(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, statuses: list[aliases.AnyEmojiStatus]): ...

    def __init__(self, hash, statuses, _='account.emojiStatuses', **kwargs):
        kwargs['hash'] = hash
        kwargs['statuses'] = statuses
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def statuses(self) -> list[aliases.AnyEmojiStatus]:
        return build_object(self['statuses'])


class AccountEmailVerified(dict):
    __slots__ = ()

    @overload
    def __init__(self, email: str): ...

    def __init__(self, email, _='account.emailVerified', **kwargs):
        kwargs['email'] = email
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email(self) -> str:
        return self['email']


class AccountEmailVerifiedLogin(dict):
    __slots__ = ()

    @overload
    def __init__(self, email: str, sent_code: aliases.AnyAuthSentCode): ...

    def __init__(self, email, sent_code, _='account.emailVerifiedLogin', **kwargs):
        kwargs['email'] = email
        kwargs['sent_code'] = sent_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email(self) -> str:
        return self['email']

    @property
    def sent_code(self) -> aliases.AnyAuthSentCode:
        return build_object(self['sent_code'])


class AccountAutoSaveSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, users_settings: aliases.AnyAutoSaveSettings, chats_settings: aliases.AnyAutoSaveSettings, broadcasts_settings: aliases.AnyAutoSaveSettings, exceptions: list[aliases.AnyAutoSaveException], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, users_settings, chats_settings, broadcasts_settings, exceptions, chats, users, _='account.autoSaveSettings', **kwargs):
        kwargs['users_settings'] = users_settings
        kwargs['chats_settings'] = chats_settings
        kwargs['broadcasts_settings'] = broadcasts_settings
        kwargs['exceptions'] = exceptions
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users_settings(self) -> aliases.AnyAutoSaveSettings:
        return build_object(self['users_settings'])

    @property
    def chats_settings(self) -> aliases.AnyAutoSaveSettings:
        return build_object(self['chats_settings'])

    @property
    def broadcasts_settings(self) -> aliases.AnyAutoSaveSettings:
        return build_object(self['broadcasts_settings'])

    @property
    def exceptions(self) -> list[aliases.AnyAutoSaveException]:
        return build_object(self['exceptions'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountConnectedBots(dict):
    __slots__ = ()

    @overload
    def __init__(self, connected_bots: list[aliases.AnyConnectedBot], users: list[aliases.AnyUser]): ...

    def __init__(self, connected_bots, users, _='account.connectedBots', **kwargs):
        kwargs['connected_bots'] = connected_bots
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connected_bots(self) -> list[aliases.AnyConnectedBot]:
        return build_object(self['connected_bots'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountBusinessChatLinks(dict):
    __slots__ = ()

    @overload
    def __init__(self, links: list[aliases.AnyBusinessChatLink], chats: list[aliases.AnyChat], users: list[aliases.AnyUser]): ...

    def __init__(self, links, chats, users, _='account.businessChatLinks', **kwargs):
        kwargs['links'] = links
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def links(self) -> list[aliases.AnyBusinessChatLink]:
        return build_object(self['links'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountResolvedBusinessChatLinks(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, message: str, chats: list[aliases.AnyChat], users: list[aliases.AnyUser], entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, peer, message, chats, users, _='account.resolvedBusinessChatLinks', **kwargs):
        kwargs['peer'] = peer
        kwargs['message'] = message
        kwargs['chats'] = chats
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AccountPaidMessagesRevenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars_amount: int): ...

    def __init__(self, stars_amount, _='account.paidMessagesRevenue', **kwargs):
        kwargs['stars_amount'] = stars_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars_amount(self) -> int:
        return self['stars_amount']


class AccountSavedMusicIdsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.savedMusicIdsNotModified'):
        dict.__init__(self, _=_)


class AccountSavedMusicIds(dict):
    __slots__ = ()

    @overload
    def __init__(self, ids: list[int]): ...

    def __init__(self, ids, _='account.savedMusicIds', **kwargs):
        kwargs['ids'] = ids
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ids(self) -> list[int]:
        return self['ids']


class AccountPasskeys(dict):
    __slots__ = ()

    @overload
    def __init__(self, passkeys: list[aliases.AnyPasskey]): ...

    def __init__(self, passkeys, _='account.passkeys', **kwargs):
        kwargs['passkeys'] = passkeys
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def passkeys(self) -> list[aliases.AnyPasskey]:
        return build_object(self['passkeys'])


class AccountPasskeyRegistrationOptions(dict):
    __slots__ = ()

    @overload
    def __init__(self, options: aliases.AnyDataJSON): ...

    def __init__(self, options, _='account.passkeyRegistrationOptions', **kwargs):
        kwargs['options'] = options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def options(self) -> aliases.AnyDataJSON:
        return build_object(self['options'])
