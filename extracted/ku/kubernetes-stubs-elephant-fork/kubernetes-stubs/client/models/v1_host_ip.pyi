import datetime
import typing

import kubernetes.client

class V1HostIP:
    ip: str
    
    def __init__(self, *, ip: str) -> None:
        ...
    def to_dict(self) -> V1HostIPDict:
        ...
class V1HostIPDict(typing.TypedDict, total=False):
    ip: str
