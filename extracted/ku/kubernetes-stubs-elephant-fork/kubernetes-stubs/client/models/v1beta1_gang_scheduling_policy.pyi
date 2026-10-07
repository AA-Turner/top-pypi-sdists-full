import datetime
import typing

import kubernetes.client

class V1beta1GangSchedulingPolicy:
    min_count: int
    
    def __init__(self, *, min_count: int) -> None:
        ...
    def to_dict(self) -> V1beta1GangSchedulingPolicyDict:
        ...
class V1beta1GangSchedulingPolicyDict(typing.TypedDict, total=False):
    minCount: int
