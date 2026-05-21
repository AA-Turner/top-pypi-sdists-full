import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicySpec:
    failure_policy: typing.Optional[str]
    match_conditions: typing.Optional[list[kubernetes.client.V1MatchCondition]]
    match_constraints: typing.Optional[kubernetes.client.V1MatchResources]
    mutations: typing.Optional[list[kubernetes.client.V1Mutation]]
    param_kind: typing.Optional[kubernetes.client.V1ParamKind]
    reinvocation_policy: typing.Optional[str]
    variables: typing.Optional[list[kubernetes.client.V1Variable]]
    
    def __init__(self, *, failure_policy: typing.Optional[str] = ..., match_conditions: typing.Optional[list[kubernetes.client.V1MatchCondition]] = ..., match_constraints: typing.Optional[kubernetes.client.V1MatchResources] = ..., mutations: typing.Optional[list[kubernetes.client.V1Mutation]] = ..., param_kind: typing.Optional[kubernetes.client.V1ParamKind] = ..., reinvocation_policy: typing.Optional[str] = ..., variables: typing.Optional[list[kubernetes.client.V1Variable]] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicySpecDict:
        ...
class V1MutatingAdmissionPolicySpecDict(typing.TypedDict, total=False):
    failurePolicy: typing.Optional[str]
    matchConditions: typing.Optional[list[kubernetes.client.V1MatchConditionDict]]
    matchConstraints: typing.Optional[kubernetes.client.V1MatchResourcesDict]
    mutations: typing.Optional[list[kubernetes.client.V1MutationDict]]
    paramKind: typing.Optional[kubernetes.client.V1ParamKindDict]
    reinvocationPolicy: typing.Optional[str]
    variables: typing.Optional[list[kubernetes.client.V1VariableDict]]
