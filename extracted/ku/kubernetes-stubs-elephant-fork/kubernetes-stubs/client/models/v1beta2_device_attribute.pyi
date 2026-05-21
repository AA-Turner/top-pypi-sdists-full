import datetime
import typing

import kubernetes.client

class V1beta2DeviceAttribute:
    bool: typing.Optional[bool]
    bools: typing.Optional[list[bool]]
    int: typing.Optional[int]
    ints: typing.Optional[list[int]]
    string: typing.Optional[str]
    strings: typing.Optional[list[str]]
    version: typing.Optional[str]
    versions: typing.Optional[list[str]]
    
    def __init__(self, *, bool: typing.Optional[bool] = ..., bools: typing.Optional[list[bool]] = ..., int: typing.Optional[int] = ..., ints: typing.Optional[list[int]] = ..., string: typing.Optional[str] = ..., strings: typing.Optional[list[str]] = ..., version: typing.Optional[str] = ..., versions: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceAttributeDict:
        ...
class V1beta2DeviceAttributeDict(typing.TypedDict, total=False):
    bool: typing.Optional[bool]
    bools: typing.Optional[list[bool]]
    int: typing.Optional[int]
    ints: typing.Optional[list[int]]
    string: typing.Optional[str]
    strings: typing.Optional[list[str]]
    version: typing.Optional[str]
    versions: typing.Optional[list[str]]
