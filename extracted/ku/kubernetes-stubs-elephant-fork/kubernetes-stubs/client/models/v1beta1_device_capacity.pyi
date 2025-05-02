import datetime
import typing

import kubernetes.client

class V1beta1DeviceCapacity:
    value: str
    
    def __init__(self, *, value: str) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceCapacityDict:
        ...
class V1beta1DeviceCapacityDict(typing.TypedDict, total=False):
    value: str
