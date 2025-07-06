# (generated with --quick)

import json.encoder
import os
import requests.auth
import requests.models
from nacl import encoding
from nacl import public
from typing import Any, Callable, Optional, Tuple, Type, Union

HTTPBasicAuth: Type[requests.auth.HTTPBasicAuth]
environ: os._Environ[str]

def UploadSecret(token) -> None: ...
def _EncryptForGithubSecret(publicKey, secretValue) -> str: ...
def b64encode(s: bytes, altchars: Optional[bytes] = ...) -> bytes: ...
def dumps(obj, *, skipkeys: bool = ..., ensure_ascii: bool = ..., check_circular: bool = ..., allow_nan: bool = ..., cls: Optional[Type[json.encoder.JSONEncoder]] = ..., indent: Optional[Union[int, str]] = ..., separators: Optional[Tuple[str, str]] = ..., default: Optional[Callable[[Any], Any]] = ..., sort_keys: bool = ..., **kwds) -> str: ...
def put(url: Union[bytes, str], data = ..., params = ..., headers = ..., cookies = ..., files = ..., auth = ..., timeout = ..., allow_redirects: bool = ..., proxies = ..., hooks = ..., stream = ..., verify = ..., cert = ..., json = ...) -> requests.models.Response: ...
