import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadPodGroupSchedulingConstraints:
    topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraint]]
    
    def __init__(self, *, topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraint]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadPodGroupSchedulingConstraintsDict:
        ...
class V1alpha3WorkloadPodGroupSchedulingConstraintsDict(typing.TypedDict, total=False):
    topology: typing.Optional[list[kubernetes.client.V1alpha3TopologyConstraintDict]]
