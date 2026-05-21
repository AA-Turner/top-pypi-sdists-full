import datetime
import typing

import kubernetes.client

class V1alpha2TopologyConstraint:
    key: str
    
    def __init__(self, *, key: str) -> None:
        ...
    def to_dict(self) -> V1alpha2TopologyConstraintDict:
        ...
class V1alpha2TopologyConstraintDict(typing.TypedDict, total=False):
    key: str
