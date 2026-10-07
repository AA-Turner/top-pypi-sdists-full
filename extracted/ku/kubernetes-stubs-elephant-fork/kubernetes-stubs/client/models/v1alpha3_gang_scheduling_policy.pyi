import datetime
import typing

import kubernetes.client

class V1alpha3GangSchedulingPolicy:
    min_count: int
    
    def __init__(self, *, min_count: int) -> None:
        ...
    def to_dict(self) -> V1alpha3GangSchedulingPolicyDict:
        ...
class V1alpha3GangSchedulingPolicyDict(typing.TypedDict, total=False):
    minCount: int
