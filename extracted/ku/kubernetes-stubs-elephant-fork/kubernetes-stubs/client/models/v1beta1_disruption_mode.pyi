import datetime
import typing

import kubernetes.client

class V1beta1DisruptionMode:
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
    
    def __init__(self, *, all: typing.Optional[typing.Any] = ..., single: typing.Optional[typing.Any] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DisruptionModeDict:
        ...
class V1beta1DisruptionModeDict(typing.TypedDict, total=False):
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
