import datetime
import typing

import kubernetes.client

class V1beta1ValidatingAdmissionPolicyBindingSpec:
    match_resources: typing.Optional[kubernetes.client.V1beta1MatchResources]
    param_ref: typing.Optional[kubernetes.client.V1beta1ParamRef]
    policy_name: typing.Optional[str]
    validation_actions: typing.Optional[list[str]]
    
    def __init__(self, *, match_resources: typing.Optional[kubernetes.client.V1beta1MatchResources] = ..., param_ref: typing.Optional[kubernetes.client.V1beta1ParamRef] = ..., policy_name: typing.Optional[str] = ..., validation_actions: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ValidatingAdmissionPolicyBindingSpecDict:
        ...
class V1beta1ValidatingAdmissionPolicyBindingSpecDict(typing.TypedDict, total=False):
    matchResources: typing.Optional[kubernetes.client.V1beta1MatchResourcesDict]
    paramRef: typing.Optional[kubernetes.client.V1beta1ParamRefDict]
    policyName: typing.Optional[str]
    validationActions: typing.Optional[list[str]]
