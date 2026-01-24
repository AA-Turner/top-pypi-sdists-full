import datetime
import typing

import kubernetes.client

class V1CounterSet:
    counters: dict[str, kubernetes.client.V1Counter]
    name: str
    
    def __init__(self, *, counters: dict[str, kubernetes.client.V1Counter], name: str) -> None:
        ...
    def to_dict(self) -> V1CounterSetDict:
        ...
class V1CounterSetDict(typing.TypedDict, total=False):
    counters: dict[str, kubernetes.client.V1CounterDict]
    name: str
