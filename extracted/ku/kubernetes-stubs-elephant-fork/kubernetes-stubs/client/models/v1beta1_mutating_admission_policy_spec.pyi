import datetime
import typing

import kubernetes.client

class V1beta1MutatingAdmissionPolicySpec:
    failure_policy: typing.Optional[str]
    match_conditions: typing.Optional[list[kubernetes.client.V1beta1MatchCondition]]
    match_constraints: typing.Optional[kubernetes.client.V1beta1MatchResources]
    mutations: typing.Optional[list[kubernetes.client.V1beta1Mutation]]
    param_kind: typing.Optional[kubernetes.client.V1beta1ParamKind]
    reinvocation_policy: typing.Optional[str]
    variables: typing.Optional[list[kubernetes.client.V1beta1Variable]]
    
    def __init__(self, *, failure_policy: typing.Optional[str] = ..., match_conditions: typing.Optional[list[kubernetes.client.V1beta1MatchCondition]] = ..., match_constraints: typing.Optional[kubernetes.client.V1beta1MatchResources] = ..., mutations: typing.Optional[list[kubernetes.client.V1beta1Mutation]] = ..., param_kind: typing.Optional[kubernetes.client.V1beta1ParamKind] = ..., reinvocation_policy: typing.Optional[str] = ..., variables: typing.Optional[list[kubernetes.client.V1beta1Variable]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1MutatingAdmissionPolicySpecDict:
        ...
class V1beta1MutatingAdmissionPolicySpecDict(typing.TypedDict, total=False):
    failurePolicy: typing.Optional[str]
    matchConditions: typing.Optional[list[kubernetes.client.V1beta1MatchConditionDict]]
    matchConstraints: typing.Optional[kubernetes.client.V1beta1MatchResourcesDict]
    mutations: typing.Optional[list[kubernetes.client.V1beta1MutationDict]]
    paramKind: typing.Optional[kubernetes.client.V1beta1ParamKindDict]
    reinvocationPolicy: typing.Optional[str]
    variables: typing.Optional[list[kubernetes.client.V1beta1VariableDict]]
