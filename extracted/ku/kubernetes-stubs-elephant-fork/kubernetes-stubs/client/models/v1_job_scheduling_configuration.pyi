import datetime
import typing

import kubernetes.client

class V1JobSchedulingConfiguration:
    disruption_mode: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupDisruptionMode]
    resource_claims: typing.Optional[list[kubernetes.client.V1alpha3WorkloadPodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingConstraints]
    scheduling_policy: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingPolicy]
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupDisruptionMode] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1alpha3WorkloadPodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingConstraints] = ..., scheduling_policy: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1JobSchedulingConfigurationDict:
        ...
class V1JobSchedulingConfigurationDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupDisruptionModeDict]
    resourceClaims: typing.Optional[list[kubernetes.client.V1alpha3WorkloadPodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingConstraintsDict]
    schedulingPolicy: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupSchedulingPolicyDict]
