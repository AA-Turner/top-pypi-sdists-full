import datetime
import typing

import kubernetes.client

class V1Counter:
    value: str
    
    def __init__(self, *, value: str) -> None:
        ...
    def to_dict(self) -> V1CounterDict:
        ...
class V1CounterDict(typing.TypedDict, total=False):
    value: str
