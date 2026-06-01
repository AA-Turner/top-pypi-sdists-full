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

class AccountRegisterDevice(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, token_type: int, token: str, app_sandbox: bool, secret: bytes, other_uids: list[int], no_muted: Optional[bool] = ...): ...

    def __init__(self, token_type, token, app_sandbox, secret, other_uids, _='account.registerDevice', **kwargs):
        kwargs['token_type'] = token_type
        kwargs['token'] = token
        kwargs['app_sandbox'] = app_sandbox
        kwargs['secret'] = secret
        kwargs['other_uids'] = other_uids
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_muted(self) -> Optional[bool]:
        return self['no_muted']

    @property
    def token_type(self) -> int:
        return self['token_type']

    @property
    def token(self) -> str:
        return self['token']

    @property
    def app_sandbox(self) -> bool:
        return self['app_sandbox']

    @property
    def secret(self) -> bytes:
        return self['secret']

    @property
    def other_uids(self) -> list[int]:
        return self['other_uids']


class AccountUnregisterDevice(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, token_type: int, token: str, other_uids: list[int]): ...

    def __init__(self, token_type, token, other_uids, _='account.unregisterDevice', **kwargs):
        kwargs['token_type'] = token_type
        kwargs['token'] = token
        kwargs['other_uids'] = other_uids
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token_type(self) -> int:
        return self['token_type']

    @property
    def token(self) -> str:
        return self['token']

    @property
    def other_uids(self) -> list[int]:
        return self['other_uids']


class AccountUpdateNotifySettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputNotifyPeer, settings: aliases.AnyInputPeerNotifySettings): ...

    def __init__(self, peer, settings, _='account.updateNotifySettings', **kwargs):
        kwargs['peer'] = peer
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputNotifyPeer:
        return build_object(self['peer'])

    @property
    def settings(self) -> aliases.AnyInputPeerNotifySettings:
        return build_object(self['settings'])


class AccountGetNotifySettings(TLMethod[aliases.AnyPeerNotifySettings]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputNotifyPeer): ...

    def __init__(self, peer, _='account.getNotifySettings', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputNotifyPeer:
        return build_object(self['peer'])


class AccountResetNotifySettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resetNotifySettings'):
        dict.__init__(self, _=_)


class AccountUpdateProfile(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, first_name: Optional[str] = ..., last_name: Optional[str] = ..., about: Optional[str] = ...): ...

    def __init__(self, _='account.updateProfile', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def first_name(self) -> Optional[str]:
        return self['first_name']

    @property
    def last_name(self) -> Optional[str]:
        return self['last_name']

    @property
    def about(self) -> Optional[str]:
        return self['about']


class AccountUpdateStatus(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, offline: bool): ...

    def __init__(self, offline, _='account.updateStatus', **kwargs):
        kwargs['offline'] = offline
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offline(self) -> bool:
        return self['offline']


class AccountGetWallPapers(TLMethod[aliases.AnyAccountWallPapers]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getWallPapers', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountReportPeer(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, reason: aliases.AnyReportReason, message: str): ...

    def __init__(self, peer, reason, message, _='account.reportPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['reason'] = reason
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def reason(self) -> aliases.AnyReportReason:
        return build_object(self['reason'])

    @property
    def message(self) -> str:
        return self['message']


class AccountCheckUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, username: str): ...

    def __init__(self, username, _='account.checkUsername', **kwargs):
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def username(self) -> str:
        return self['username']


class AccountUpdateUsername(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, username: str): ...

    def __init__(self, username, _='account.updateUsername', **kwargs):
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def username(self) -> str:
        return self['username']


class AccountGetPrivacy(TLMethod[aliases.AnyAccountPrivacyRules]):
    __slots__ = ()

    @overload
    def __init__(self, key: aliases.AnyInputPrivacyKey): ...

    def __init__(self, key, _='account.getPrivacy', **kwargs):
        kwargs['key'] = key
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> aliases.AnyInputPrivacyKey:
        return build_object(self['key'])


class AccountSetPrivacy(TLMethod[aliases.AnyAccountPrivacyRules]):
    __slots__ = ()

    @overload
    def __init__(self, key: aliases.AnyInputPrivacyKey, rules: list[aliases.AnyInputPrivacyRule]): ...

    def __init__(self, key, rules, _='account.setPrivacy', **kwargs):
        kwargs['key'] = key
        kwargs['rules'] = rules
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> aliases.AnyInputPrivacyKey:
        return build_object(self['key'])

    @property
    def rules(self) -> list[aliases.AnyInputPrivacyRule]:
        return build_object(self['rules'])


class AccountDeleteAccount(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, reason: str, password: Optional[aliases.AnyInputCheckPasswordSRP] = ...): ...

    def __init__(self, reason, _='account.deleteAccount', **kwargs):
        kwargs['reason'] = reason
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reason(self) -> str:
        return self['reason']

    @property
    def password(self) -> Optional[aliases.AnyInputCheckPasswordSRP]:
        return build_object(self['password'])


class AccountGetAccountTTL(TLMethod[aliases.AnyAccountDaysTTL]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getAccountTTL'):
        dict.__init__(self, _=_)


class AccountSetAccountTTL(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, ttl: aliases.AnyAccountDaysTTL): ...

    def __init__(self, ttl, _='account.setAccountTTL', **kwargs):
        kwargs['ttl'] = ttl
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ttl(self) -> aliases.AnyAccountDaysTTL:
        return build_object(self['ttl'])


class AccountSendChangePhoneCode(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, settings: aliases.AnyCodeSettings): ...

    def __init__(self, phone_number, settings, _='account.sendChangePhoneCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def settings(self) -> aliases.AnyCodeSettings:
        return build_object(self['settings'])


class AccountChangePhone(TLMethod[aliases.AnyUser]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, phone_code: str): ...

    def __init__(self, phone_number, phone_code_hash, phone_code, _='account.changePhone', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['phone_code'] = phone_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def phone_code(self) -> str:
        return self['phone_code']


class AccountUpdateDeviceLocked(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, period: int): ...

    def __init__(self, period, _='account.updateDeviceLocked', **kwargs):
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> int:
        return self['period']


class AccountGetAuthorizations(TLMethod[aliases.AnyAccountAuthorizations]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getAuthorizations'):
        dict.__init__(self, _=_)


class AccountResetAuthorization(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.resetAuthorization', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetPassword(TLMethod[aliases.AnyAccountPassword]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getPassword'):
        dict.__init__(self, _=_)


class AccountGetPasswordSettings(TLMethod[aliases.AnyAccountPasswordSettings]):
    __slots__ = ()

    @overload
    def __init__(self, password: aliases.AnyInputCheckPasswordSRP): ...

    def __init__(self, password, _='account.getPasswordSettings', **kwargs):
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])


class AccountUpdatePasswordSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, password: aliases.AnyInputCheckPasswordSRP, new_settings: aliases.AnyAccountPasswordInputSettings): ...

    def __init__(self, password, new_settings, _='account.updatePasswordSettings', **kwargs):
        kwargs['password'] = password
        kwargs['new_settings'] = new_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])

    @property
    def new_settings(self) -> aliases.AnyAccountPasswordInputSettings:
        return build_object(self['new_settings'])


class AccountSendConfirmPhoneCode(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, hash: str, settings: aliases.AnyCodeSettings): ...

    def __init__(self, hash, settings, _='account.sendConfirmPhoneCode', **kwargs):
        kwargs['hash'] = hash
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> str:
        return self['hash']

    @property
    def settings(self) -> aliases.AnyCodeSettings:
        return build_object(self['settings'])


class AccountConfirmPhone(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phone_code_hash: str, phone_code: str): ...

    def __init__(self, phone_code_hash, phone_code, _='account.confirmPhone', **kwargs):
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['phone_code'] = phone_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def phone_code(self) -> str:
        return self['phone_code']


class AccountGetTmpPassword(TLMethod[aliases.AnyAccountTmpPassword]):
    __slots__ = ()

    @overload
    def __init__(self, password: aliases.AnyInputCheckPasswordSRP, period: int): ...

    def __init__(self, password, period, _='account.getTmpPassword', **kwargs):
        kwargs['password'] = password
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])

    @property
    def period(self) -> int:
        return self['period']


class AccountGetWebAuthorizations(TLMethod[aliases.AnyAccountWebAuthorizations]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getWebAuthorizations'):
        dict.__init__(self, _=_)


class AccountResetWebAuthorization(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.resetWebAuthorization', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountResetWebAuthorizations(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resetWebAuthorizations'):
        dict.__init__(self, _=_)


class AccountGetAllSecureValues(TLMethod[list[aliases.AnySecureValue]]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getAllSecureValues'):
        dict.__init__(self, _=_)


class AccountGetSecureValue(TLMethod[list[aliases.AnySecureValue]]):
    __slots__ = ()

    @overload
    def __init__(self, types: list[aliases.AnySecureValueType]): ...

    def __init__(self, types, _='account.getSecureValue', **kwargs):
        kwargs['types'] = types
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def types(self) -> list[aliases.AnySecureValueType]:
        return build_object(self['types'])


class AccountSaveSecureValue(TLMethod[aliases.AnySecureValue]):
    __slots__ = ()

    @overload
    def __init__(self, value: aliases.AnyInputSecureValue, secure_secret_id: int): ...

    def __init__(self, value, secure_secret_id, _='account.saveSecureValue', **kwargs):
        kwargs['value'] = value
        kwargs['secure_secret_id'] = secure_secret_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> aliases.AnyInputSecureValue:
        return build_object(self['value'])

    @property
    def secure_secret_id(self) -> int:
        return self['secure_secret_id']


class AccountDeleteSecureValue(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, types: list[aliases.AnySecureValueType]): ...

    def __init__(self, types, _='account.deleteSecureValue', **kwargs):
        kwargs['types'] = types
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def types(self) -> list[aliases.AnySecureValueType]:
        return build_object(self['types'])


class AccountGetAuthorizationForm(TLMethod[aliases.AnyAccountAuthorizationForm]):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, scope: str, public_key: str): ...

    def __init__(self, bot_id, scope, public_key, _='account.getAuthorizationForm', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['scope'] = scope
        kwargs['public_key'] = public_key
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def scope(self) -> str:
        return self['scope']

    @property
    def public_key(self) -> str:
        return self['public_key']


class AccountAcceptAuthorization(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, scope: str, public_key: str, value_hashes: list[aliases.AnySecureValueHash], credentials: aliases.AnySecureCredentialsEncrypted): ...

    def __init__(self, bot_id, scope, public_key, value_hashes, credentials, _='account.acceptAuthorization', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['scope'] = scope
        kwargs['public_key'] = public_key
        kwargs['value_hashes'] = value_hashes
        kwargs['credentials'] = credentials
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def scope(self) -> str:
        return self['scope']

    @property
    def public_key(self) -> str:
        return self['public_key']

    @property
    def value_hashes(self) -> list[aliases.AnySecureValueHash]:
        return build_object(self['value_hashes'])

    @property
    def credentials(self) -> aliases.AnySecureCredentialsEncrypted:
        return build_object(self['credentials'])


class AccountSendVerifyPhoneCode(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, settings: aliases.AnyCodeSettings): ...

    def __init__(self, phone_number, settings, _='account.sendVerifyPhoneCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def settings(self) -> aliases.AnyCodeSettings:
        return build_object(self['settings'])


class AccountVerifyPhone(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, phone_code: str): ...

    def __init__(self, phone_number, phone_code_hash, phone_code, _='account.verifyPhone', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['phone_code'] = phone_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def phone_code(self) -> str:
        return self['phone_code']


class AccountSendVerifyEmailCode(TLMethod[aliases.AnyAccountSentEmailCode]):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyEmailVerifyPurpose, email: str): ...

    def __init__(self, purpose, email, _='account.sendVerifyEmailCode', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['email'] = email
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyEmailVerifyPurpose:
        return build_object(self['purpose'])

    @property
    def email(self) -> str:
        return self['email']


class AccountVerifyEmail(TLMethod[aliases.AnyAccountEmailVerified]):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyEmailVerifyPurpose, verification: aliases.AnyEmailVerification): ...

    def __init__(self, purpose, verification, _='account.verifyEmail', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['verification'] = verification
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyEmailVerifyPurpose:
        return build_object(self['purpose'])

    @property
    def verification(self) -> aliases.AnyEmailVerification:
        return build_object(self['verification'])


class AccountInitTakeoutSession(TLMethod[aliases.AnyAccountTakeout]):
    __slots__ = ()

    @overload
    def __init__(self, contacts: Optional[bool] = ..., message_users: Optional[bool] = ..., message_chats: Optional[bool] = ..., message_megagroups: Optional[bool] = ..., message_channels: Optional[bool] = ..., files: Optional[bool] = ..., file_max_size: Optional[int] = ...): ...

    def __init__(self, _='account.initTakeoutSession', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def message_users(self) -> Optional[bool]:
        return self['message_users']

    @property
    def message_chats(self) -> Optional[bool]:
        return self['message_chats']

    @property
    def message_megagroups(self) -> Optional[bool]:
        return self['message_megagroups']

    @property
    def message_channels(self) -> Optional[bool]:
        return self['message_channels']

    @property
    def files(self) -> Optional[bool]:
        return self['files']

    @property
    def file_max_size(self) -> Optional[int]:
        return self['file_max_size']


class AccountFinishTakeoutSession(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, success: Optional[bool] = ...): ...

    def __init__(self, _='account.finishTakeoutSession', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def success(self) -> Optional[bool]:
        return self['success']


class AccountConfirmPasswordEmail(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, code: str): ...

    def __init__(self, code, _='account.confirmPasswordEmail', **kwargs):
        kwargs['code'] = code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def code(self) -> str:
        return self['code']


class AccountResendPasswordEmail(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resendPasswordEmail'):
        dict.__init__(self, _=_)


class AccountCancelPasswordEmail(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.cancelPasswordEmail'):
        dict.__init__(self, _=_)


class AccountGetContactSignUpNotification(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getContactSignUpNotification'):
        dict.__init__(self, _=_)


class AccountSetContactSignUpNotification(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, silent: bool): ...

    def __init__(self, silent, _='account.setContactSignUpNotification', **kwargs):
        kwargs['silent'] = silent
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def silent(self) -> bool:
        return self['silent']


class AccountGetNotifyExceptions(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, compare_sound: Optional[bool] = ..., compare_stories: Optional[bool] = ..., peer: Optional[aliases.AnyInputNotifyPeer] = ...): ...

    def __init__(self, _='account.getNotifyExceptions', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def compare_sound(self) -> Optional[bool]:
        return self['compare_sound']

    @property
    def compare_stories(self) -> Optional[bool]:
        return self['compare_stories']

    @property
    def peer(self) -> Optional[aliases.AnyInputNotifyPeer]:
        return build_object(self['peer'])


class AccountGetWallPaper(TLMethod[aliases.AnyWallPaper]):
    __slots__ = ()

    @overload
    def __init__(self, wallpaper: aliases.AnyInputWallPaper): ...

    def __init__(self, wallpaper, _='account.getWallPaper', **kwargs):
        kwargs['wallpaper'] = wallpaper
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def wallpaper(self) -> aliases.AnyInputWallPaper:
        return build_object(self['wallpaper'])


class AccountUploadWallPaper(TLMethod[aliases.AnyWallPaper]):
    __slots__ = ()

    @overload
    def __init__(self, file: aliases.AnyInputFile, mime_type: str, settings: aliases.AnyWallPaperSettings, for_chat: Optional[bool] = ...): ...

    def __init__(self, file, mime_type, settings, _='account.uploadWallPaper', **kwargs):
        kwargs['file'] = file
        kwargs['mime_type'] = mime_type
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_chat(self) -> Optional[bool]:
        return self['for_chat']

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def settings(self) -> aliases.AnyWallPaperSettings:
        return build_object(self['settings'])


class AccountSaveWallPaper(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, wallpaper: aliases.AnyInputWallPaper, unsave: bool, settings: aliases.AnyWallPaperSettings): ...

    def __init__(self, wallpaper, unsave, settings, _='account.saveWallPaper', **kwargs):
        kwargs['wallpaper'] = wallpaper
        kwargs['unsave'] = unsave
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def wallpaper(self) -> aliases.AnyInputWallPaper:
        return build_object(self['wallpaper'])

    @property
    def unsave(self) -> bool:
        return self['unsave']

    @property
    def settings(self) -> aliases.AnyWallPaperSettings:
        return build_object(self['settings'])


class AccountInstallWallPaper(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, wallpaper: aliases.AnyInputWallPaper, settings: aliases.AnyWallPaperSettings): ...

    def __init__(self, wallpaper, settings, _='account.installWallPaper', **kwargs):
        kwargs['wallpaper'] = wallpaper
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def wallpaper(self) -> aliases.AnyInputWallPaper:
        return build_object(self['wallpaper'])

    @property
    def settings(self) -> aliases.AnyWallPaperSettings:
        return build_object(self['settings'])


class AccountResetWallPapers(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resetWallPapers'):
        dict.__init__(self, _=_)


class AccountGetAutoDownloadSettings(TLMethod[aliases.AnyAccountAutoDownloadSettings]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getAutoDownloadSettings'):
        dict.__init__(self, _=_)


class AccountSaveAutoDownloadSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, settings: aliases.AnyAutoDownloadSettings, low: Optional[bool] = ..., high: Optional[bool] = ...): ...

    def __init__(self, settings, _='account.saveAutoDownloadSettings', **kwargs):
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def low(self) -> Optional[bool]:
        return self['low']

    @property
    def high(self) -> Optional[bool]:
        return self['high']

    @property
    def settings(self) -> aliases.AnyAutoDownloadSettings:
        return build_object(self['settings'])


class AccountUploadTheme(TLMethod[aliases.AnyDocument]):
    __slots__ = ()

    @overload
    def __init__(self, file: aliases.AnyInputFile, file_name: str, mime_type: str, thumb: Optional[aliases.AnyInputFile] = ...): ...

    def __init__(self, file, file_name, mime_type, _='account.uploadTheme', **kwargs):
        kwargs['file'] = file
        kwargs['file_name'] = file_name
        kwargs['mime_type'] = mime_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def thumb(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['thumb'])

    @property
    def file_name(self) -> str:
        return self['file_name']

    @property
    def mime_type(self) -> str:
        return self['mime_type']


class AccountCreateTheme(TLMethod[aliases.AnyTheme]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str, title: str, document: Optional[aliases.AnyInputDocument] = ..., settings: Optional[list[aliases.AnyInputThemeSettings]] = ...): ...

    def __init__(self, slug, title, _='account.createTheme', **kwargs):
        kwargs['slug'] = slug
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def document(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['document'])

    @property
    def settings(self) -> Optional[list[aliases.AnyInputThemeSettings]]:
        return build_object(self['settings'])


class AccountUpdateTheme(TLMethod[aliases.AnyTheme]):
    __slots__ = ()

    @overload
    def __init__(self, format: str, theme: aliases.AnyInputTheme, slug: Optional[str] = ..., title: Optional[str] = ..., document: Optional[aliases.AnyInputDocument] = ..., settings: Optional[list[aliases.AnyInputThemeSettings]] = ...): ...

    def __init__(self, format, theme, _='account.updateTheme', **kwargs):
        kwargs['format'] = format
        kwargs['theme'] = theme
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def format(self) -> str:
        return self['format']

    @property
    def theme(self) -> aliases.AnyInputTheme:
        return build_object(self['theme'])

    @property
    def slug(self) -> Optional[str]:
        return self['slug']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def document(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['document'])

    @property
    def settings(self) -> Optional[list[aliases.AnyInputThemeSettings]]:
        return build_object(self['settings'])


class AccountSaveTheme(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, theme: aliases.AnyInputTheme, unsave: bool): ...

    def __init__(self, theme, unsave, _='account.saveTheme', **kwargs):
        kwargs['theme'] = theme
        kwargs['unsave'] = unsave
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def theme(self) -> aliases.AnyInputTheme:
        return build_object(self['theme'])

    @property
    def unsave(self) -> bool:
        return self['unsave']


class AccountInstallTheme(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, dark: Optional[bool] = ..., theme: Optional[aliases.AnyInputTheme] = ..., format: Optional[str] = ..., base_theme: Optional[aliases.AnyBaseTheme] = ...): ...

    def __init__(self, _='account.installTheme', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def theme(self) -> Optional[aliases.AnyInputTheme]:
        return build_object(self['theme'])

    @property
    def format(self) -> Optional[str]:
        return self['format']

    @property
    def base_theme(self) -> Optional[aliases.AnyBaseTheme]:
        return build_object(self['base_theme'])


class AccountGetTheme(TLMethod[aliases.AnyTheme]):
    __slots__ = ()

    @overload
    def __init__(self, format: str, theme: aliases.AnyInputTheme): ...

    def __init__(self, format, theme, _='account.getTheme', **kwargs):
        kwargs['format'] = format
        kwargs['theme'] = theme
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def format(self) -> str:
        return self['format']

    @property
    def theme(self) -> aliases.AnyInputTheme:
        return build_object(self['theme'])


class AccountGetThemes(TLMethod[aliases.AnyAccountThemes]):
    __slots__ = ()

    @overload
    def __init__(self, format: str, hash: int): ...

    def __init__(self, format, hash, _='account.getThemes', **kwargs):
        kwargs['format'] = format
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def format(self) -> str:
        return self['format']

    @property
    def hash(self) -> int:
        return self['hash']


class AccountSetContentSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, sensitive_enabled: Optional[bool] = ...): ...

    def __init__(self, _='account.setContentSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sensitive_enabled(self) -> Optional[bool]:
        return self['sensitive_enabled']


class AccountGetContentSettings(TLMethod[aliases.AnyAccountContentSettings]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getContentSettings'):
        dict.__init__(self, _=_)


class AccountGetMultiWallPapers(TLMethod[list[aliases.AnyWallPaper]]):
    __slots__ = ()

    @overload
    def __init__(self, wallpapers: list[aliases.AnyInputWallPaper]): ...

    def __init__(self, wallpapers, _='account.getMultiWallPapers', **kwargs):
        kwargs['wallpapers'] = wallpapers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def wallpapers(self) -> list[aliases.AnyInputWallPaper]:
        return build_object(self['wallpapers'])


class AccountGetGlobalPrivacySettings(TLMethod[aliases.AnyGlobalPrivacySettings]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getGlobalPrivacySettings'):
        dict.__init__(self, _=_)


class AccountSetGlobalPrivacySettings(TLMethod[aliases.AnyGlobalPrivacySettings]):
    __slots__ = ()

    @overload
    def __init__(self, settings: aliases.AnyGlobalPrivacySettings): ...

    def __init__(self, settings, _='account.setGlobalPrivacySettings', **kwargs):
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def settings(self) -> aliases.AnyGlobalPrivacySettings:
        return build_object(self['settings'])


class AccountReportProfilePhoto(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, photo_id: aliases.AnyInputPhoto, reason: aliases.AnyReportReason, message: str): ...

    def __init__(self, peer, photo_id, reason, message, _='account.reportProfilePhoto', **kwargs):
        kwargs['peer'] = peer
        kwargs['photo_id'] = photo_id
        kwargs['reason'] = reason
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def photo_id(self) -> aliases.AnyInputPhoto:
        return build_object(self['photo_id'])

    @property
    def reason(self) -> aliases.AnyReportReason:
        return build_object(self['reason'])

    @property
    def message(self) -> str:
        return self['message']


class AccountResetPassword(TLMethod[aliases.AnyAccountResetPasswordResult]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.resetPassword'):
        dict.__init__(self, _=_)


class AccountDeclinePasswordReset(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.declinePasswordReset'):
        dict.__init__(self, _=_)


class AccountGetChatThemes(TLMethod[aliases.AnyAccountThemes]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getChatThemes', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountSetAuthorizationTTL(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, authorization_ttl_days: int): ...

    def __init__(self, authorization_ttl_days, _='account.setAuthorizationTTL', **kwargs):
        kwargs['authorization_ttl_days'] = authorization_ttl_days
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def authorization_ttl_days(self) -> int:
        return self['authorization_ttl_days']


class AccountChangeAuthorizationSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, confirmed: Optional[bool] = ..., encrypted_requests_disabled: Optional[bool] = ..., call_requests_disabled: Optional[bool] = ...): ...

    def __init__(self, hash, _='account.changeAuthorizationSettings', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def confirmed(self) -> Optional[bool]:
        return self['confirmed']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def encrypted_requests_disabled(self) -> Optional[bool]:
        return self['encrypted_requests_disabled']

    @property
    def call_requests_disabled(self) -> Optional[bool]:
        return self['call_requests_disabled']


class AccountGetSavedRingtones(TLMethod[aliases.AnyAccountSavedRingtones]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getSavedRingtones', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountSaveRingtone(TLMethod[aliases.AnyAccountSavedRingtone]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, unsave: bool): ...

    def __init__(self, id, unsave, _='account.saveRingtone', **kwargs):
        kwargs['id'] = id
        kwargs['unsave'] = unsave
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def unsave(self) -> bool:
        return self['unsave']


class AccountUploadRingtone(TLMethod[aliases.AnyDocument]):
    __slots__ = ()

    @overload
    def __init__(self, file: aliases.AnyInputFile, file_name: str, mime_type: str): ...

    def __init__(self, file, file_name, mime_type, _='account.uploadRingtone', **kwargs):
        kwargs['file'] = file
        kwargs['file_name'] = file_name
        kwargs['mime_type'] = mime_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def file_name(self) -> str:
        return self['file_name']

    @property
    def mime_type(self) -> str:
        return self['mime_type']


class AccountUpdateEmojiStatus(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, emoji_status: aliases.AnyEmojiStatus): ...

    def __init__(self, emoji_status, _='account.updateEmojiStatus', **kwargs):
        kwargs['emoji_status'] = emoji_status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoji_status(self) -> aliases.AnyEmojiStatus:
        return build_object(self['emoji_status'])


class AccountGetDefaultEmojiStatuses(TLMethod[aliases.AnyAccountEmojiStatuses]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getDefaultEmojiStatuses', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetRecentEmojiStatuses(TLMethod[aliases.AnyAccountEmojiStatuses]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getRecentEmojiStatuses', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountClearRecentEmojiStatuses(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.clearRecentEmojiStatuses'):
        dict.__init__(self, _=_)


class AccountReorderUsernames(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, order: list[str]): ...

    def __init__(self, order, _='account.reorderUsernames', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order(self) -> list[str]:
        return self['order']


class AccountToggleUsername(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, username: str, active: bool): ...

    def __init__(self, username, active, _='account.toggleUsername', **kwargs):
        kwargs['username'] = username
        kwargs['active'] = active
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def username(self) -> str:
        return self['username']

    @property
    def active(self) -> bool:
        return self['active']


class AccountGetDefaultProfilePhotoEmojis(TLMethod[aliases.AnyEmojiList]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getDefaultProfilePhotoEmojis', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetDefaultGroupPhotoEmojis(TLMethod[aliases.AnyEmojiList]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getDefaultGroupPhotoEmojis', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetAutoSaveSettings(TLMethod[aliases.AnyAccountAutoSaveSettings]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getAutoSaveSettings'):
        dict.__init__(self, _=_)


class AccountSaveAutoSaveSettings(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, settings: aliases.AnyAutoSaveSettings, users: Optional[bool] = ..., chats: Optional[bool] = ..., broadcasts: Optional[bool] = ..., peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, settings, _='account.saveAutoSaveSettings', **kwargs):
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> Optional[bool]:
        return self['users']

    @property
    def chats(self) -> Optional[bool]:
        return self['chats']

    @property
    def broadcasts(self) -> Optional[bool]:
        return self['broadcasts']

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def settings(self) -> aliases.AnyAutoSaveSettings:
        return build_object(self['settings'])


class AccountDeleteAutoSaveExceptions(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.deleteAutoSaveExceptions'):
        dict.__init__(self, _=_)


class AccountInvalidateSignInCodes(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, codes: list[str]): ...

    def __init__(self, codes, _='account.invalidateSignInCodes', **kwargs):
        kwargs['codes'] = codes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def codes(self) -> list[str]:
        return self['codes']


class AccountUpdateColor(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, for_profile: Optional[bool] = ..., color: Optional[aliases.AnyPeerColor] = ...): ...

    def __init__(self, _='account.updateColor', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def for_profile(self) -> Optional[bool]:
        return self['for_profile']

    @property
    def color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['color'])


class AccountGetDefaultBackgroundEmojis(TLMethod[aliases.AnyEmojiList]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getDefaultBackgroundEmojis', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetChannelDefaultEmojiStatuses(TLMethod[aliases.AnyAccountEmojiStatuses]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getChannelDefaultEmojiStatuses', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetChannelRestrictedStatusEmojis(TLMethod[aliases.AnyEmojiList]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getChannelRestrictedStatusEmojis', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountUpdateBusinessWorkHours(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, business_work_hours: Optional[aliases.AnyBusinessWorkHours] = ...): ...

    def __init__(self, _='account.updateBusinessWorkHours', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def business_work_hours(self) -> Optional[aliases.AnyBusinessWorkHours]:
        return build_object(self['business_work_hours'])


class AccountUpdateBusinessLocation(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: Optional[aliases.AnyInputGeoPoint] = ..., address: Optional[str] = ...): ...

    def __init__(self, _='account.updateBusinessLocation', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> Optional[aliases.AnyInputGeoPoint]:
        return build_object(self['geo_point'])

    @property
    def address(self) -> Optional[str]:
        return self['address']


class AccountUpdateBusinessGreetingMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, message: Optional[aliases.AnyInputBusinessGreetingMessage] = ...): ...

    def __init__(self, _='account.updateBusinessGreetingMessage', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> Optional[aliases.AnyInputBusinessGreetingMessage]:
        return build_object(self['message'])


class AccountUpdateBusinessAwayMessage(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, message: Optional[aliases.AnyInputBusinessAwayMessage] = ...): ...

    def __init__(self, _='account.updateBusinessAwayMessage', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> Optional[aliases.AnyInputBusinessAwayMessage]:
        return build_object(self['message'])


class AccountUpdateConnectedBot(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, recipients: aliases.AnyInputBusinessBotRecipients, deleted: Optional[bool] = ..., rights: Optional[aliases.AnyBusinessBotRights] = ...): ...

    def __init__(self, bot, recipients, _='account.updateConnectedBot', **kwargs):
        kwargs['bot'] = bot
        kwargs['recipients'] = recipients
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def deleted(self) -> Optional[bool]:
        return self['deleted']

    @property
    def rights(self) -> Optional[aliases.AnyBusinessBotRights]:
        return build_object(self['rights'])

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def recipients(self) -> aliases.AnyInputBusinessBotRecipients:
        return build_object(self['recipients'])


class AccountGetConnectedBots(TLMethod[aliases.AnyAccountConnectedBots]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getConnectedBots'):
        dict.__init__(self, _=_)


class AccountGetBotBusinessConnection(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str): ...

    def __init__(self, connection_id, _='account.getBotBusinessConnection', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection_id(self) -> str:
        return self['connection_id']


class AccountUpdateBusinessIntro(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, intro: Optional[aliases.AnyInputBusinessIntro] = ...): ...

    def __init__(self, _='account.updateBusinessIntro', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def intro(self) -> Optional[aliases.AnyInputBusinessIntro]:
        return build_object(self['intro'])


class AccountToggleConnectedBotPaused(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, paused: bool): ...

    def __init__(self, peer, paused, _='account.toggleConnectedBotPaused', **kwargs):
        kwargs['peer'] = peer
        kwargs['paused'] = paused
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def paused(self) -> bool:
        return self['paused']


class AccountDisablePeerConnectedBot(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='account.disablePeerConnectedBot', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class AccountUpdateBirthday(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, birthday: Optional[aliases.AnyBirthday] = ...): ...

    def __init__(self, _='account.updateBirthday', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def birthday(self) -> Optional[aliases.AnyBirthday]:
        return build_object(self['birthday'])


class AccountCreateBusinessChatLink(TLMethod[aliases.AnyBusinessChatLink]):
    __slots__ = ()

    @overload
    def __init__(self, link: aliases.AnyInputBusinessChatLink): ...

    def __init__(self, link, _='account.createBusinessChatLink', **kwargs):
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def link(self) -> aliases.AnyInputBusinessChatLink:
        return build_object(self['link'])


class AccountEditBusinessChatLink(TLMethod[aliases.AnyBusinessChatLink]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str, link: aliases.AnyInputBusinessChatLink): ...

    def __init__(self, slug, link, _='account.editBusinessChatLink', **kwargs):
        kwargs['slug'] = slug
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def link(self) -> aliases.AnyInputBusinessChatLink:
        return build_object(self['link'])


class AccountDeleteBusinessChatLink(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='account.deleteBusinessChatLink', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class AccountGetBusinessChatLinks(TLMethod[aliases.AnyAccountBusinessChatLinks]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getBusinessChatLinks'):
        dict.__init__(self, _=_)


class AccountResolveBusinessChatLink(TLMethod[aliases.AnyAccountResolvedBusinessChatLinks]):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='account.resolveBusinessChatLink', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class AccountUpdatePersonalChannel(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyInputChannel): ...

    def __init__(self, channel, _='account.updatePersonalChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])


class AccountToggleSponsoredMessages(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, enabled: bool): ...

    def __init__(self, enabled, _='account.toggleSponsoredMessages', **kwargs):
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def enabled(self) -> bool:
        return self['enabled']


class AccountGetReactionsNotifySettings(TLMethod[aliases.AnyReactionsNotifySettings]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getReactionsNotifySettings'):
        dict.__init__(self, _=_)


class AccountSetReactionsNotifySettings(TLMethod[aliases.AnyReactionsNotifySettings]):
    __slots__ = ()

    @overload
    def __init__(self, settings: aliases.AnyReactionsNotifySettings): ...

    def __init__(self, settings, _='account.setReactionsNotifySettings', **kwargs):
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def settings(self) -> aliases.AnyReactionsNotifySettings:
        return build_object(self['settings'])


class AccountGetCollectibleEmojiStatuses(TLMethod[aliases.AnyAccountEmojiStatuses]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getCollectibleEmojiStatuses', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetPaidMessagesRevenue(TLMethod[aliases.AnyAccountPaidMessagesRevenue]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, user_id, _='account.getPaidMessagesRevenue', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class AccountToggleNoPaidMessagesException(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, refund_charged: Optional[bool] = ..., require_payment: Optional[bool] = ..., parent_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, user_id, _='account.toggleNoPaidMessagesException', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def refund_charged(self) -> Optional[bool]:
        return self['refund_charged']

    @property
    def require_payment(self) -> Optional[bool]:
        return self['require_payment']

    @property
    def parent_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['parent_peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class AccountSetMainProfileTab(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, tab: aliases.AnyProfileTab): ...

    def __init__(self, tab, _='account.setMainProfileTab', **kwargs):
        kwargs['tab'] = tab
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def tab(self) -> aliases.AnyProfileTab:
        return build_object(self['tab'])


class AccountSaveMusic(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, unsave: Optional[bool] = ..., after_id: Optional[aliases.AnyInputDocument] = ...): ...

    def __init__(self, id, _='account.saveMusic', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unsave(self) -> Optional[bool]:
        return self['unsave']

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def after_id(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['after_id'])


class AccountGetSavedMusicIds(TLMethod[aliases.AnyAccountSavedMusicIds]):
    __slots__ = ()

    @overload
    def __init__(self, hash: int): ...

    def __init__(self, hash, _='account.getSavedMusicIds', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']


class AccountGetUniqueGiftChatThemes(TLMethod[aliases.AnyAccountChatThemes]):
    __slots__ = ()

    @overload
    def __init__(self, offset: str, limit: int, hash: int): ...

    def __init__(self, offset, limit, hash, _='account.getUniqueGiftChatThemes', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> str:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> int:
        return self['hash']


class AccountInitPasskeyRegistration(TLMethod[aliases.AnyAccountPasskeyRegistrationOptions]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.initPasskeyRegistration'):
        dict.__init__(self, _=_)


class AccountRegisterPasskey(TLMethod[aliases.AnyPasskey]):
    __slots__ = ()

    @overload
    def __init__(self, credential: aliases.AnyInputPasskeyCredential): ...

    def __init__(self, credential, _='account.registerPasskey', **kwargs):
        kwargs['credential'] = credential
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def credential(self) -> aliases.AnyInputPasskeyCredential:
        return build_object(self['credential'])


class AccountGetPasskeys(TLMethod[aliases.AnyAccountPasskeys]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='account.getPasskeys'):
        dict.__init__(self, _=_)


class AccountDeletePasskey(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, id: str): ...

    def __init__(self, id, _='account.deletePasskey', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']
