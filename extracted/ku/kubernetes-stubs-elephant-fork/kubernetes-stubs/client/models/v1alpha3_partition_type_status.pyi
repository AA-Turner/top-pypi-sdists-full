import datetime
import typing

import kubernetes.client

class V1alpha3PartitionTypeStatus:
    allocatable: int
    attribute: str
    total: int
    type: str
    
    def __init__(self, *, allocatable: int, attribute: str, total: int, type: str) -> None:
        ...
    def to_dict(self) -> V1alpha3PartitionTypeStatusDict:
        ...
class V1alpha3PartitionTypeStatusDict(typing.TypedDict, total=False):
    allocatable: int
    attribute: str
    total: int
    type: str
