import datetime
import typing

import kubernetes.client

class V1PodDisruptionBudgetStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    current_healthy: typing.Optional[int]
    desired_healthy: typing.Optional[int]
    disrupted_pods: typing.Optional[dict[str, datetime.datetime]]
    disruptions_allowed: typing.Optional[int]
    expected_pods: typing.Optional[int]
    observed_generation: typing.Optional[int]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., current_healthy: typing.Optional[int] = ..., desired_healthy: typing.Optional[int] = ..., disrupted_pods: typing.Optional[dict[str, datetime.datetime]] = ..., disruptions_allowed: typing.Optional[int] = ..., expected_pods: typing.Optional[int] = ..., observed_generation: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1PodDisruptionBudgetStatusDict:
        ...
class V1PodDisruptionBudgetStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    currentHealthy: typing.Optional[int]
    desiredHealthy: typing.Optional[int]
    disruptedPods: typing.Optional[dict[str, datetime.datetime]]
    disruptionsAllowed: typing.Optional[int]
    expectedPods: typing.Optional[int]
    observedGeneration: typing.Optional[int]
