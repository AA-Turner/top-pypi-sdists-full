import datetime
import typing

import kubernetes.client

class V1beta1CompositePodGroupSchedulingConstraints:
    topology: typing.Optional[list[kubernetes.client.V1beta1TopologyConstraint]]
    
    def __init__(self, *, topology: typing.Optional[list[kubernetes.client.V1beta1TopologyConstraint]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CompositePodGroupSchedulingConstraintsDict:
        ...
class V1beta1CompositePodGroupSchedulingConstraintsDict(typing.TypedDict, total=False):
    topology: typing.Optional[list[kubernetes.client.V1beta1TopologyConstraintDict]]
