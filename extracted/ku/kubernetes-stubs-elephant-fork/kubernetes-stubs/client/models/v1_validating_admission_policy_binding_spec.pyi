import datetime
import typing

import kubernetes.client

class V1ValidatingAdmissionPolicyBindingSpec:
    match_resources: typing.Optional[kubernetes.client.V1MatchResources]
    param_ref: typing.Optional[kubernetes.client.V1ParamRef]
    policy_name: typing.Optional[str]
    validation_actions: typing.Optional[list[str]]
    
    def __init__(self, *, match_resources: typing.Optional[kubernetes.client.V1MatchResources] = ..., param_ref: typing.Optional[kubernetes.client.V1ParamRef] = ..., policy_name: typing.Optional[str] = ..., validation_actions: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1ValidatingAdmissionPolicyBindingSpecDict:
        ...
class V1ValidatingAdmissionPolicyBindingSpecDict(typing.TypedDict, total=False):
    matchResources: typing.Optional[kubernetes.client.V1MatchResourcesDict]
    paramRef: typing.Optional[kubernetes.client.V1ParamRefDict]
    policyName: typing.Optional[str]
    validationActions: typing.Optional[list[str]]
