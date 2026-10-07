import datetime
import typing

import kubernetes.client

class V1beta1CompositeGangSchedulingPolicy:
    min_group_count: int
    
    def __init__(self, *, min_group_count: int) -> None:
        ...
    def to_dict(self) -> V1beta1CompositeGangSchedulingPolicyDict:
        ...
class V1beta1CompositeGangSchedulingPolicyDict(typing.TypedDict, total=False):
    minGroupCount: int
