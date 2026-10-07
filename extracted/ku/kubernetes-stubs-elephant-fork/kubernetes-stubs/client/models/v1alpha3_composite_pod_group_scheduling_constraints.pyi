import datetime
import typing

import kubernetes.client

class V1alpha3CompositePodGroupSchedulingConstraints:
    topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraint]]
    
    def __init__(self, *, topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraint]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositePodGroupSchedulingConstraintsDict:
        ...
class V1alpha3CompositePodGroupSchedulingConstraintsDict(typing.TypedDict, total=False):
    topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraintDict]]
