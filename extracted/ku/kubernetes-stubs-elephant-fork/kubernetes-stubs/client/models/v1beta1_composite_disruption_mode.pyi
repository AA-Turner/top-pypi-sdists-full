import datetime
import typing

import kubernetes.client

class V1beta1CompositeDisruptionMode:
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
    
    def __init__(self, *, all: typing.Optional[typing.Any] = ..., single: typing.Optional[typing.Any] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CompositeDisruptionModeDict:
        ...
class V1beta1CompositeDisruptionModeDict(typing.TypedDict, total=False):
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
