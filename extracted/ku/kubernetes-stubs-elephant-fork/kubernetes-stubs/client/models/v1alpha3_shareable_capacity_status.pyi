import datetime
import typing

import kubernetes.client

class V1alpha3ShareableCapacityStatus:
    available: str
    consumed: str
    name: str
    total: str
    
    def __init__(self, *, available: str, consumed: str, name: str, total: str) -> None:
        ...
    def to_dict(self) -> V1alpha3ShareableCapacityStatusDict:
        ...
class V1alpha3ShareableCapacityStatusDict(typing.TypedDict, total=False):
    available: str
    consumed: str
    name: str
    total: str
