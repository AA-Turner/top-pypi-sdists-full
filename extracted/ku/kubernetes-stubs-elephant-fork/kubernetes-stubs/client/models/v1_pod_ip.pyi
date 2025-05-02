import datetime
import typing

import kubernetes.client

class V1PodIP:
    ip: str
    
    def __init__(self, *, ip: str) -> None:
        ...
    def to_dict(self) -> V1PodIPDict:
        ...
class V1PodIPDict(typing.TypedDict, total=False):
    ip: str
