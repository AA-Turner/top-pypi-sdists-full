import datetime
import typing

import kubernetes.client

class V1alpha1StorageVersionMigration:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationSpec]
    status: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationSpec] = ..., status: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1StorageVersionMigrationDict:
        ...
class V1alpha1StorageVersionMigrationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationSpecDict]
    status: typing.Optional[kubernetes.client.V1alpha1StorageVersionMigrationStatusDict]
