import datetime
import typing

import kubernetes.client

class V1EvictionResponder:
    name: str
    priority: int
    
    def __init__(self, *, name: str, priority: int) -> None:
        ...
    def to_dict(self) -> V1EvictionResponderDict:
        ...
class V1EvictionResponderDict(typing.TypedDict, total=False):
    name: str
    priority: int
