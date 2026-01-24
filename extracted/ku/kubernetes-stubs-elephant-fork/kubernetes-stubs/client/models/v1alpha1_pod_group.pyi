import datetime
import typing

import kubernetes.client

class V1alpha1PodGroup:
    name: str
    policy: kubernetes.client.V1alpha1PodGroupPolicy
    
    def __init__(self, *, name: str, policy: kubernetes.client.V1alpha1PodGroupPolicy) -> None:
        ...
    def to_dict(self) -> V1alpha1PodGroupDict:
        ...
class V1alpha1PodGroupDict(typing.TypedDict, total=False):
    name: str
    policy: kubernetes.client.V1alpha1PodGroupPolicyDict
