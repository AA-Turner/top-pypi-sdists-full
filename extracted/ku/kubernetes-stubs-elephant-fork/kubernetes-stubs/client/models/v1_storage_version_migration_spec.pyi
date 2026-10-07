import datetime
import typing

import kubernetes.client

class V1StorageVersionMigrationSpec:
    resource: kubernetes.client.V1GroupResource
    
    def __init__(self, *, resource: kubernetes.client.V1GroupResource) -> None:
        ...
    def to_dict(self) -> V1StorageVersionMigrationSpecDict:
        ...
class V1StorageVersionMigrationSpecDict(typing.TypedDict, total=False):
    resource: kubernetes.client.V1GroupResourceDict
