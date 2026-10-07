import datetime
import typing

import kubernetes.client

class V1alpha3TopologyConstraint:
    key: str
    
    def __init__(self, *, key: str) -> None:
        ...
    def to_dict(self) -> V1alpha3TopologyConstraintDict:
        ...
class V1alpha3TopologyConstraintDict(typing.TypedDict, total=False):
    key: str
