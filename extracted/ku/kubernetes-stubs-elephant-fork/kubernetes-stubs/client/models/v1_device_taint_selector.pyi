import datetime
import typing

import kubernetes.client

class V1DeviceTaintSelector:
    device: typing.Optional[str]
    driver: typing.Optional[str]
    pool: typing.Optional[str]
    
    def __init__(self, *, device: typing.Optional[str] = ..., driver: typing.Optional[str] = ..., pool: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceTaintSelectorDict:
        ...
class V1DeviceTaintSelectorDict(typing.TypedDict, total=False):
    device: typing.Optional[str]
    driver: typing.Optional[str]
    pool: typing.Optional[str]
