import datetime
import typing

import kubernetes.client

class V1alpha1StorageVersionMigrationSpec:
    continue_token: typing.Optional[str]
    resource: kubernetes.client.V1alpha1GroupVersionResource
    
    def __init__(self, *, continue_token: typing.Optional[str] = ..., resource: kubernetes.client.V1alpha1GroupVersionResource) -> None:
        ...
    def to_dict(self) -> V1alpha1StorageVersionMigrationSpecDict:
        ...
class V1alpha1StorageVersionMigrationSpecDict(typing.TypedDict, total=False):
    continueToken: typing.Optional[str]
    resource: kubernetes.client.V1alpha1GroupVersionResourceDict
