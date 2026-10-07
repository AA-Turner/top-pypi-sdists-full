import datetime
import typing

import kubernetes.client

class V1GroupVersionKind:
    group: typing.Optional[str]
    version: typing.Optional[str]
    kind: typing.Optional[str]
    
    def __init__(self, *, group: typing.Optional[str] = ..., version: typing.Optional[str] = ..., kind: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1GroupVersionKindDict:
        ...
class V1GroupVersionKindDict(typing.TypedDict, total=False):
    group: typing.Optional[str]
    version: typing.Optional[str]
    kind: typing.Optional[str]
