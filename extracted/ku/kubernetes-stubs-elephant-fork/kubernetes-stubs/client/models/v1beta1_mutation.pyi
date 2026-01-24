import datetime
import typing

import kubernetes.client

class V1beta1Mutation:
    apply_configuration: typing.Optional[kubernetes.client.V1beta1ApplyConfiguration]
    json_patch: typing.Optional[kubernetes.client.V1beta1JSONPatch]
    patch_type: str
    
    def __init__(self, *, apply_configuration: typing.Optional[kubernetes.client.V1beta1ApplyConfiguration] = ..., json_patch: typing.Optional[kubernetes.client.V1beta1JSONPatch] = ..., patch_type: str) -> None:
        ...
    def to_dict(self) -> V1beta1MutationDict:
        ...
class V1beta1MutationDict(typing.TypedDict, total=False):
    applyConfiguration: typing.Optional[kubernetes.client.V1beta1ApplyConfigurationDict]
    jsonPatch: typing.Optional[kubernetes.client.V1beta1JSONPatchDict]
    patchType: str
