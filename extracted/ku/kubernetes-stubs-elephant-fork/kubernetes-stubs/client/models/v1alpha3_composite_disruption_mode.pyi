import datetime
import typing

import kubernetes.client

class V1alpha3CompositeDisruptionMode:
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
    
    def __init__(self, *, all: typing.Optional[typing.Any] = ..., single: typing.Optional[typing.Any] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositeDisruptionModeDict:
        ...
class V1alpha3CompositeDisruptionModeDict(typing.TypedDict, total=False):
    all: typing.Optional[typing.Any]
    single: typing.Optional[typing.Any]
