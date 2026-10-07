import datetime
import typing

import kubernetes.client

class V1beta2DeviceCounterConsumption:
    compatibility_groups: typing.Optional[list[str]]
    counter_set: str
    counters: dict[str, kubernetes.client.V1beta2Counter]
    
    def __init__(self, *, compatibility_groups: typing.Optional[list[str]] = ..., counter_set: str, counters: dict[str, kubernetes.client.V1beta2Counter]) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceCounterConsumptionDict:
        ...
class V1beta2DeviceCounterConsumptionDict(typing.TypedDict, total=False):
    compatibilityGroups: typing.Optional[list[str]]
    counterSet: str
    counters: dict[str, kubernetes.client.V1beta2CounterDict]
