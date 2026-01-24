import datetime
import typing

import kubernetes.client

class V1DeviceCounterConsumption:
    counter_set: str
    counters: dict[str, kubernetes.client.V1Counter]
    
    def __init__(self, *, counter_set: str, counters: dict[str, kubernetes.client.V1Counter]) -> None:
        ...
    def to_dict(self) -> V1DeviceCounterConsumptionDict:
        ...
class V1DeviceCounterConsumptionDict(typing.TypedDict, total=False):
    counterSet: str
    counters: dict[str, kubernetes.client.V1CounterDict]
