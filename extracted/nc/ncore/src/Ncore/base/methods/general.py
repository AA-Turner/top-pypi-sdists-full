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

class InvokeAfterMsg(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int, query: dict): ...

    def __init__(self, msg_id, query, _='invokeAfterMsg', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeAfterMsgs(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, msg_ids: list[int], query: dict): ...

    def __init__(self, msg_ids, query, _='invokeAfterMsgs', **kwargs):
        kwargs['msg_ids'] = msg_ids
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_ids(self) -> list[int]:
        return self['msg_ids']

    @property
    def query(self) -> dict:
        return self['query']


class InitConnection(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, api_id: int, device_model: str, system_version: str, app_version: str, system_lang_code: str, lang_pack: str, lang_code: str, query: dict, proxy: Optional[aliases.AnyInputClientProxy] = ..., params: Optional[aliases.AnyJSONValue] = ...): ...

    def __init__(self, api_id, device_model, system_version, app_version, system_lang_code, lang_pack, lang_code, query, _='initConnection', **kwargs):
        kwargs['api_id'] = api_id
        kwargs['device_model'] = device_model
        kwargs['system_version'] = system_version
        kwargs['app_version'] = app_version
        kwargs['system_lang_code'] = system_lang_code
        kwargs['lang_pack'] = lang_pack
        kwargs['lang_code'] = lang_code
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def device_model(self) -> str:
        return self['device_model']

    @property
    def system_version(self) -> str:
        return self['system_version']

    @property
    def app_version(self) -> str:
        return self['app_version']

    @property
    def system_lang_code(self) -> str:
        return self['system_lang_code']

    @property
    def lang_pack(self) -> str:
        return self['lang_pack']

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def proxy(self) -> Optional[aliases.AnyInputClientProxy]:
        return build_object(self['proxy'])

    @property
    def params(self) -> Optional[aliases.AnyJSONValue]:
        return build_object(self['params'])

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithLayer(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, layer: int, query: dict): ...

    def __init__(self, layer, query, _='invokeWithLayer', **kwargs):
        kwargs['layer'] = layer
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def layer(self) -> int:
        return self['layer']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithoutUpdates(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, query: dict): ...

    def __init__(self, query, _='invokeWithoutUpdates', **kwargs):
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithMessagesRange(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, range: aliases.AnyMessageRange, query: dict): ...

    def __init__(self, range, query, _='invokeWithMessagesRange', **kwargs):
        kwargs['range'] = range
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def range(self) -> aliases.AnyMessageRange:
        return build_object(self['range'])

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithTakeout(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, takeout_id: int, query: dict): ...

    def __init__(self, takeout_id, query, _='invokeWithTakeout', **kwargs):
        kwargs['takeout_id'] = takeout_id
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def takeout_id(self) -> int:
        return self['takeout_id']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithBusinessConnection(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str, query: dict): ...

    def __init__(self, connection_id, query, _='invokeWithBusinessConnection', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithGooglePlayIntegrity(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, nonce: str, token: str, query: dict): ...

    def __init__(self, nonce, token, query, _='invokeWithGooglePlayIntegrity', **kwargs):
        kwargs['nonce'] = nonce
        kwargs['token'] = token
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def nonce(self) -> str:
        return self['nonce']

    @property
    def token(self) -> str:
        return self['token']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithApnsSecret(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, nonce: str, secret: str, query: dict): ...

    def __init__(self, nonce, secret, query, _='invokeWithApnsSecret', **kwargs):
        kwargs['nonce'] = nonce
        kwargs['secret'] = secret
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def nonce(self) -> str:
        return self['nonce']

    @property
    def secret(self) -> str:
        return self['secret']

    @property
    def query(self) -> dict:
        return self['query']


class InvokeWithReCaptcha(TLMethod[dict]):
    __slots__ = ()

    @overload
    def __init__(self, token: str, query: dict): ...

    def __init__(self, token, query, _='invokeWithReCaptcha', **kwargs):
        kwargs['token'] = token
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']

    @property
    def query(self) -> dict:
        return self['query']
