import datetime
import typing

import kubernetes.client

class V1GRPCAction:
    mode: typing.Optional[str]
    port: int
    service: typing.Optional[str]
    
    def __init__(self, *, mode: typing.Optional[str] = ..., port: int, service: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1GRPCActionDict:
        ...
class V1GRPCActionDict(typing.TypedDict, total=False):
    mode: typing.Optional[str]
    port: int
    service: typing.Optional[str]
