import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicyBindingSpec:
    match_resources: typing.Optional[kubernetes.client.V1MatchResources]
    param_ref: typing.Optional[kubernetes.client.V1ParamRef]
    policy_name: typing.Optional[str]
    
    def __init__(self, *, match_resources: typing.Optional[kubernetes.client.V1MatchResources] = ..., param_ref: typing.Optional[kubernetes.client.V1ParamRef] = ..., policy_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicyBindingSpecDict:
        ...
class V1MutatingAdmissionPolicyBindingSpecDict(typing.TypedDict, total=False):
    matchResources: typing.Optional[kubernetes.client.V1MatchResourcesDict]
    paramRef: typing.Optional[kubernetes.client.V1ParamRefDict]
    policyName: typing.Optional[str]
