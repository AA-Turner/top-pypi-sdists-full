import datetime
import typing

import kubernetes.client

class V1alpha3CompositeGangSchedulingPolicy:
    min_group_count: int
    
    def __init__(self, *, min_group_count: int) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositeGangSchedulingPolicyDict:
        ...
class V1alpha3CompositeGangSchedulingPolicyDict(typing.TypedDict, total=False):
    minGroupCount: int
