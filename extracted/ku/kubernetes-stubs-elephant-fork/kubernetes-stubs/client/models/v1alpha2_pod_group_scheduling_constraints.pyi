import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupSchedulingConstraints:
    topology: typing.Optional[list[kubernetes.client.V1alpha2TopologyConstraint]]
    
    def __init__(self, *, topology: typing.Optional[list[kubernetes.client.V1alpha2TopologyConstraint]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupSchedulingConstraintsDict:
        ...
class V1alpha2PodGroupSchedulingConstraintsDict(typing.TypedDict, total=False):
    topology: typing.Optional[list[kubernetes.client.V1alpha2TopologyConstraintDict]]
