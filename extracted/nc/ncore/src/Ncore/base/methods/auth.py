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

class AuthSendCode(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, api_id: int, api_hash: str, settings: aliases.AnyCodeSettings): ...

    def __init__(self, phone_number, api_id, api_hash, settings, _='auth.sendCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['api_id'] = api_id
        kwargs['api_hash'] = api_hash
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def api_hash(self) -> str:
        return self['api_hash']

    @property
    def settings(self) -> aliases.AnyCodeSettings:
        return build_object(self['settings'])


class AuthSignUp(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, first_name: str, last_name: str, no_joined_notifications: Optional[bool] = ...): ...

    def __init__(self, phone_number, phone_code_hash, first_name, last_name, _='auth.signUp', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_joined_notifications(self) -> Optional[bool]:
        return self['no_joined_notifications']

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']


class AuthSignIn(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, phone_code: Optional[str] = ..., email_verification: Optional[aliases.AnyEmailVerification] = ...): ...

    def __init__(self, phone_number, phone_code_hash, _='auth.signIn', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def phone_code(self) -> Optional[str]:
        return self['phone_code']

    @property
    def email_verification(self) -> Optional[aliases.AnyEmailVerification]:
        return build_object(self['email_verification'])


class AuthLogOut(TLMethod[aliases.AnyAuthLoggedOut]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.logOut'):
        dict.__init__(self, _=_)


class AuthResetAuthorizations(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.resetAuthorizations'):
        dict.__init__(self, _=_)


class AuthExportAuthorization(TLMethod[aliases.AnyAuthExportedAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int): ...

    def __init__(self, dc_id, _='auth.exportAuthorization', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']


class AuthImportAuthorization(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, id: int, bytes: bytes): ...

    def __init__(self, id, bytes, _='auth.importAuthorization', **kwargs):
        kwargs['id'] = id
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class AuthBindTempAuthKey(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, perm_auth_key_id: int, nonce: int, expires_at: int, encrypted_message: bytes): ...

    def __init__(self, perm_auth_key_id, nonce, expires_at, encrypted_message, _='auth.bindTempAuthKey', **kwargs):
        kwargs['perm_auth_key_id'] = perm_auth_key_id
        kwargs['nonce'] = nonce
        kwargs['expires_at'] = expires_at
        kwargs['encrypted_message'] = encrypted_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def perm_auth_key_id(self) -> int:
        return self['perm_auth_key_id']

    @property
    def nonce(self) -> int:
        return self['nonce']

    @property
    def expires_at(self) -> int:
        return self['expires_at']

    @property
    def encrypted_message(self) -> bytes:
        return self['encrypted_message']


class AuthImportBotAuthorization(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, api_id: int, api_hash: str, bot_auth_token: str): ...

    def __init__(self, api_id, api_hash, bot_auth_token, _='auth.importBotAuthorization', **kwargs):
        kwargs['api_id'] = api_id
        kwargs['api_hash'] = api_hash
        kwargs['bot_auth_token'] = bot_auth_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def api_hash(self) -> str:
        return self['api_hash']

    @property
    def bot_auth_token(self) -> str:
        return self['bot_auth_token']


class AuthCheckPassword(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, password: aliases.AnyInputCheckPasswordSRP): ...

    def __init__(self, password, _='auth.checkPassword', **kwargs):
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def password(self) -> aliases.AnyInputCheckPasswordSRP:
        return build_object(self['password'])


class AuthRequestPasswordRecovery(TLMethod[aliases.AnyAuthPasswordRecovery]):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.requestPasswordRecovery'):
        dict.__init__(self, _=_)


class AuthRecoverPassword(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, code: str, new_settings: Optional[aliases.AnyAccountPasswordInputSettings] = ...): ...

    def __init__(self, code, _='auth.recoverPassword', **kwargs):
        kwargs['code'] = code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def code(self) -> str:
        return self['code']

    @property
    def new_settings(self) -> Optional[aliases.AnyAccountPasswordInputSettings]:
        return build_object(self['new_settings'])


class AuthResendCode(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, reason: Optional[str] = ...): ...

    def __init__(self, phone_number, phone_code_hash, _='auth.resendCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def reason(self) -> Optional[str]:
        return self['reason']


class AuthCancelCode(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str): ...

    def __init__(self, phone_number, phone_code_hash, _='auth.cancelCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']


class AuthDropTempAuthKeys(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, except_auth_keys: list[int]): ...

    def __init__(self, except_auth_keys, _='auth.dropTempAuthKeys', **kwargs):
        kwargs['except_auth_keys'] = except_auth_keys
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def except_auth_keys(self) -> list[int]:
        return self['except_auth_keys']


class AuthExportLoginToken(TLMethod[aliases.AnyAuthLoginToken]):
    __slots__ = ()

    @overload
    def __init__(self, api_id: int, api_hash: str, except_ids: list[int]): ...

    def __init__(self, api_id, api_hash, except_ids, _='auth.exportLoginToken', **kwargs):
        kwargs['api_id'] = api_id
        kwargs['api_hash'] = api_hash
        kwargs['except_ids'] = except_ids
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def api_hash(self) -> str:
        return self['api_hash']

    @property
    def except_ids(self) -> list[int]:
        return self['except_ids']


class AuthImportLoginToken(TLMethod[aliases.AnyAuthLoginToken]):
    __slots__ = ()

    @overload
    def __init__(self, token: bytes): ...

    def __init__(self, token, _='auth.importLoginToken', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> bytes:
        return self['token']


class AuthAcceptLoginToken(TLMethod[aliases.AnyAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, token: bytes): ...

    def __init__(self, token, _='auth.acceptLoginToken', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> bytes:
        return self['token']


class AuthCheckRecoveryPassword(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, code: str): ...

    def __init__(self, code, _='auth.checkRecoveryPassword', **kwargs):
        kwargs['code'] = code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def code(self) -> str:
        return self['code']


class AuthImportWebTokenAuthorization(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, api_id: int, api_hash: str, web_auth_token: str): ...

    def __init__(self, api_id, api_hash, web_auth_token, _='auth.importWebTokenAuthorization', **kwargs):
        kwargs['api_id'] = api_id
        kwargs['api_hash'] = api_hash
        kwargs['web_auth_token'] = web_auth_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def api_hash(self) -> str:
        return self['api_hash']

    @property
    def web_auth_token(self) -> str:
        return self['web_auth_token']


class AuthRequestFirebaseSms(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, safety_net_token: Optional[str] = ..., play_integrity_token: Optional[str] = ..., ios_push_secret: Optional[str] = ...): ...

    def __init__(self, phone_number, phone_code_hash, _='auth.requestFirebaseSms', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def safety_net_token(self) -> Optional[str]:
        return self['safety_net_token']

    @property
    def play_integrity_token(self) -> Optional[str]:
        return self['play_integrity_token']

    @property
    def ios_push_secret(self) -> Optional[str]:
        return self['ios_push_secret']


class AuthResetLoginEmail(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str): ...

    def __init__(self, phone_number, phone_code_hash, _='auth.resetLoginEmail', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']


class AuthReportMissingCode(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, mnc: str): ...

    def __init__(self, phone_number, phone_code_hash, mnc, _='auth.reportMissingCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['mnc'] = mnc
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def mnc(self) -> str:
        return self['mnc']


class AuthCheckPaidAuth(TLMethod[aliases.AnyAuthSentCode]):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, form_id: int): ...

    def __init__(self, phone_number, phone_code_hash, form_id, _='auth.checkPaidAuth', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['form_id'] = form_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def form_id(self) -> int:
        return self['form_id']


class AuthInitPasskeyLogin(TLMethod[aliases.AnyAuthPasskeyLoginOptions]):
    __slots__ = ()

    @overload
    def __init__(self, api_id: int, api_hash: str): ...

    def __init__(self, api_id, api_hash, _='auth.initPasskeyLogin', **kwargs):
        kwargs['api_id'] = api_id
        kwargs['api_hash'] = api_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def api_hash(self) -> str:
        return self['api_hash']


class AuthFinishPasskeyLogin(TLMethod[aliases.AnyAuthAuthorization]):
    __slots__ = ()

    @overload
    def __init__(self, credential: aliases.AnyInputPasskeyCredential, from_dc_id: Optional[int] = ..., from_auth_key_id: Optional[int] = ...): ...

    def __init__(self, credential, _='auth.finishPasskeyLogin', **kwargs):
        kwargs['credential'] = credential
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def credential(self) -> aliases.AnyInputPasskeyCredential:
        return build_object(self['credential'])

    @property
    def from_dc_id(self) -> Optional[int]:
        return self['from_dc_id']

    @property
    def from_auth_key_id(self) -> Optional[int]:
        return self['from_auth_key_id']
