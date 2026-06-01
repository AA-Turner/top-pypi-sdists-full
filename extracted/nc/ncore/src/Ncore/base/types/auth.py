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


class AuthSentCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnyAuthSentCodeType, phone_code_hash: str, next_type: Optional[aliases.AnyAuthCodeType] = ..., timeout: Optional[int] = ...): ...

    def __init__(self, type, phone_code_hash, _='auth.sentCode', **kwargs):
        kwargs['type'] = type
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnyAuthSentCodeType:
        return build_object(self['type'])

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def next_type(self) -> Optional[aliases.AnyAuthCodeType]:
        return build_object(self['next_type'])

    @property
    def timeout(self) -> Optional[int]:
        return self['timeout']


class AuthSentCodeSuccess(dict):
    __slots__ = ()

    @overload
    def __init__(self, authorization: aliases.AnyAuthAuthorization): ...

    def __init__(self, authorization, _='auth.sentCodeSuccess', **kwargs):
        kwargs['authorization'] = authorization
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def authorization(self) -> aliases.AnyAuthAuthorization:
        return build_object(self['authorization'])


class AuthSentCodePaymentRequired(dict):
    __slots__ = ()

    @overload
    def __init__(self, store_product: str, phone_code_hash: str, support_email_address: str, support_email_subject: str, currency: str, amount: int): ...

    def __init__(self, store_product, phone_code_hash, support_email_address, support_email_subject, currency, amount, _='auth.sentCodePaymentRequired', **kwargs):
        kwargs['store_product'] = store_product
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['support_email_address'] = support_email_address
        kwargs['support_email_subject'] = support_email_subject
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def store_product(self) -> str:
        return self['store_product']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def support_email_address(self) -> str:
        return self['support_email_address']

    @property
    def support_email_subject(self) -> str:
        return self['support_email_subject']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class AuthAuthorization(dict):
    __slots__ = ()

    @overload
    def __init__(self, user: aliases.AnyUser, setup_password_required: Optional[bool] = ..., otherwise_relogin_days: Optional[int] = ..., tmp_sessions: Optional[int] = ..., future_auth_token: Optional[bytes] = ...): ...

    def __init__(self, user, _='auth.authorization', **kwargs):
        kwargs['user'] = user
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def setup_password_required(self) -> Optional[bool]:
        return self['setup_password_required']

    @property
    def otherwise_relogin_days(self) -> Optional[int]:
        return self['otherwise_relogin_days']

    @property
    def tmp_sessions(self) -> Optional[int]:
        return self['tmp_sessions']

    @property
    def future_auth_token(self) -> Optional[bytes]:
        return self['future_auth_token']

    @property
    def user(self) -> aliases.AnyUser:
        return build_object(self['user'])


class AuthAuthorizationSignUpRequired(dict):
    __slots__ = ()

    @overload
    def __init__(self, terms_of_service: Optional[aliases.AnyHelpTermsOfService] = ...): ...

    def __init__(self, _='auth.authorizationSignUpRequired', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def terms_of_service(self) -> Optional[aliases.AnyHelpTermsOfService]:
        return build_object(self['terms_of_service'])


class AuthExportedAuthorization(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, bytes: bytes): ...

    def __init__(self, id, bytes, _='auth.exportedAuthorization', **kwargs):
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


class AuthPasswordRecovery(dict):
    __slots__ = ()

    @overload
    def __init__(self, email_pattern: str): ...

    def __init__(self, email_pattern, _='auth.passwordRecovery', **kwargs):
        kwargs['email_pattern'] = email_pattern
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email_pattern(self) -> str:
        return self['email_pattern']


class AuthCodeTypeSms(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.codeTypeSms'):
        dict.__init__(self, _=_)


class AuthCodeTypeCall(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.codeTypeCall'):
        dict.__init__(self, _=_)


class AuthCodeTypeFlashCall(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.codeTypeFlashCall'):
        dict.__init__(self, _=_)


class AuthCodeTypeMissedCall(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.codeTypeMissedCall'):
        dict.__init__(self, _=_)


class AuthCodeTypeFragmentSms(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='auth.codeTypeFragmentSms'):
        dict.__init__(self, _=_)


class AuthSentCodeTypeApp(dict):
    __slots__ = ()

    @overload
    def __init__(self, length: int): ...

    def __init__(self, length, _='auth.sentCodeTypeApp', **kwargs):
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeSms(dict):
    __slots__ = ()

    @overload
    def __init__(self, length: int): ...

    def __init__(self, length, _='auth.sentCodeTypeSms', **kwargs):
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, length: int): ...

    def __init__(self, length, _='auth.sentCodeTypeCall', **kwargs):
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeFlashCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, pattern: str): ...

    def __init__(self, pattern, _='auth.sentCodeTypeFlashCall', **kwargs):
        kwargs['pattern'] = pattern
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pattern(self) -> str:
        return self['pattern']


class AuthSentCodeTypeMissedCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, prefix: str, length: int): ...

    def __init__(self, prefix, length, _='auth.sentCodeTypeMissedCall', **kwargs):
        kwargs['prefix'] = prefix
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prefix(self) -> str:
        return self['prefix']

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeEmailCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, email_pattern: str, length: int, apple_signin_allowed: Optional[bool] = ..., google_signin_allowed: Optional[bool] = ..., reset_available_period: Optional[int] = ..., reset_pending_date: Optional[int] = ...): ...

    def __init__(self, email_pattern, length, _='auth.sentCodeTypeEmailCode', **kwargs):
        kwargs['email_pattern'] = email_pattern
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def apple_signin_allowed(self) -> Optional[bool]:
        return self['apple_signin_allowed']

    @property
    def google_signin_allowed(self) -> Optional[bool]:
        return self['google_signin_allowed']

    @property
    def email_pattern(self) -> str:
        return self['email_pattern']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def reset_available_period(self) -> Optional[int]:
        return self['reset_available_period']

    @property
    def reset_pending_date(self) -> Optional[int]:
        return self['reset_pending_date']


class AuthSentCodeTypeSetUpEmailRequired(dict):
    __slots__ = ()

    @overload
    def __init__(self, apple_signin_allowed: Optional[bool] = ..., google_signin_allowed: Optional[bool] = ...): ...

    def __init__(self, _='auth.sentCodeTypeSetUpEmailRequired', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def apple_signin_allowed(self) -> Optional[bool]:
        return self['apple_signin_allowed']

    @property
    def google_signin_allowed(self) -> Optional[bool]:
        return self['google_signin_allowed']


class AuthSentCodeTypeFragmentSms(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, length: int): ...

    def __init__(self, url, length, _='auth.sentCodeTypeFragmentSms', **kwargs):
        kwargs['url'] = url
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeFirebaseSms(dict):
    __slots__ = ()

    @overload
    def __init__(self, length: int, nonce: Optional[bytes] = ..., play_integrity_project_id: Optional[int] = ..., play_integrity_nonce: Optional[bytes] = ..., receipt: Optional[str] = ..., push_timeout: Optional[int] = ...): ...

    def __init__(self, length, _='auth.sentCodeTypeFirebaseSms', **kwargs):
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def nonce(self) -> Optional[bytes]:
        return self['nonce']

    @property
    def play_integrity_project_id(self) -> Optional[int]:
        return self['play_integrity_project_id']

    @property
    def play_integrity_nonce(self) -> Optional[bytes]:
        return self['play_integrity_nonce']

    @property
    def receipt(self) -> Optional[str]:
        return self['receipt']

    @property
    def push_timeout(self) -> Optional[int]:
        return self['push_timeout']

    @property
    def length(self) -> int:
        return self['length']


class AuthSentCodeTypeSmsWord(dict):
    __slots__ = ()

    @overload
    def __init__(self, beginning: Optional[str] = ...): ...

    def __init__(self, _='auth.sentCodeTypeSmsWord', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def beginning(self) -> Optional[str]:
        return self['beginning']


class AuthSentCodeTypeSmsPhrase(dict):
    __slots__ = ()

    @overload
    def __init__(self, beginning: Optional[str] = ...): ...

    def __init__(self, _='auth.sentCodeTypeSmsPhrase', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def beginning(self) -> Optional[str]:
        return self['beginning']


class AuthLoginToken(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int, token: bytes): ...

    def __init__(self, expires, token, _='auth.loginToken', **kwargs):
        kwargs['expires'] = expires
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def token(self) -> bytes:
        return self['token']


class AuthLoginTokenMigrateTo(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int, token: bytes): ...

    def __init__(self, dc_id, token, _='auth.loginTokenMigrateTo', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def token(self) -> bytes:
        return self['token']


class AuthLoginTokenSuccess(dict):
    __slots__ = ()

    @overload
    def __init__(self, authorization: aliases.AnyAuthAuthorization): ...

    def __init__(self, authorization, _='auth.loginTokenSuccess', **kwargs):
        kwargs['authorization'] = authorization
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def authorization(self) -> aliases.AnyAuthAuthorization:
        return build_object(self['authorization'])


class AuthLoggedOut(dict):
    __slots__ = ()

    @overload
    def __init__(self, future_auth_token: Optional[bytes] = ...): ...

    def __init__(self, _='auth.loggedOut', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def future_auth_token(self) -> Optional[bytes]:
        return self['future_auth_token']


class AuthPasskeyLoginOptions(dict):
    __slots__ = ()

    @overload
    def __init__(self, options: aliases.AnyDataJSON): ...

    def __init__(self, options, _='auth.passkeyLoginOptions', **kwargs):
        kwargs['options'] = options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def options(self) -> aliases.AnyDataJSON:
        return build_object(self['options'])
