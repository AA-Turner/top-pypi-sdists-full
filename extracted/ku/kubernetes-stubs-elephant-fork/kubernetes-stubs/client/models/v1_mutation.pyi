import datetime
import typing

import kubernetes.client

class V1Mutation:
    apply_configuration: typing.Optional[kubernetes.client.V1ApplyConfiguration]
    json_patch: typing.Optional[kubernetes.client.V1JSONPatch]
    patch_type: str
    
    def __init__(self, *, apply_configuration: typing.Optional[kubernetes.client.V1ApplyConfiguration] = ..., json_patch: typing.Optional[kubernetes.client.V1JSONPatch] = ..., patch_type: str) -> None:
        ...
    def to_dict(self) -> V1MutationDict:
        ...
class V1MutationDict(typing.TypedDict, total=False):
    applyConfiguration: typing.Optional[kubernetes.client.V1ApplyConfigurationDict]
    jsonPatch: typing.Optional[kubernetes.client.V1JSONPatchDict]
    patchType: str
