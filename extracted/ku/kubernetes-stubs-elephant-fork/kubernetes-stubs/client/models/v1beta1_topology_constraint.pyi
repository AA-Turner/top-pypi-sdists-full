import datetime
import typing

import kubernetes.client

class V1beta1TopologyConstraint:
    key: str
    
    def __init__(self, *, key: str) -> None:
        ...
    def to_dict(self) -> V1beta1TopologyConstraintDict:
        ...
class V1beta1TopologyConstraintDict(typing.TypedDict, total=False):
    key: str
