import datetime
import typing

import kubernetes.client

class V1beta1ParamKind:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ParamKindDict:
        ...
class V1beta1ParamKindDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
