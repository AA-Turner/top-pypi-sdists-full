# (generated with --quick)

import _typeshed
import json.decoder
import json.encoder
import logging
import os
from typing import Any, Callable, IO, Iterable, List, Literal, Optional, TextIO, Tuple, Type, Union

DEBUG: int
OAuth2Session: Any
UploadSecret: Any
copy: Any
environ: os._Environ[str]
stdout: TextIO
token: Any

class TokenStorageFile:
    path: Any
    def Load(self) -> Any: ...
    def Save(self, token_) -> None: ...
    def __init__(self, path) -> None: ...

def Authorize(clientId, clientSecret, redirectUri, storagePath) -> Any: ...
def EscapeForBash(token_) -> Any: ...
def basicConfig(*, filename: Optional[Union[str, os.PathLike[str]]] = ..., filemode: str = ..., format: str = ..., datefmt: Optional[str] = ..., style: Literal['$', '%', '{'] = ..., level: Optional[Union[int, str]] = ..., stream: Optional[_typeshed.SupportsWrite[str]] = ..., handlers: Optional[Iterable[logging.Handler]] = ..., force: bool = ..., encoding: Optional[str] = ..., errors: Optional[str] = ...) -> None: ...
def dump(obj, fp: IO[str], *, skipkeys: bool = ..., ensure_ascii: bool = ..., check_circular: bool = ..., allow_nan: bool = ..., cls: Optional[Type[json.encoder.JSONEncoder]] = ..., indent: Optional[Union[int, str]] = ..., separators: Optional[Tuple[str, str]] = ..., default: Optional[Callable[[Any], Any]] = ..., sort_keys: bool = ..., **kwds) -> None: ...
def load(fp: _typeshed.SupportsRead[Union[bytes, str]], *, cls: Optional[Type[json.decoder.JSONDecoder]] = ..., object_hook: Optional[Callable[[dict], Any]] = ..., parse_float: Optional[Callable[[str], Any]] = ..., parse_int: Optional[Callable[[str], Any]] = ..., parse_constant: Optional[Callable[[str], Any]] = ..., object_pairs_hook: Optional[Callable[[List[Tuple[Any, Any]]], Any]] = ..., **kwds) -> Any: ...
