import datetime
import typing

import kubernetes.client

class V1beta1StorageVersionMigration:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationSpec]
    status: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationSpec] = ..., status: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1StorageVersionMigrationDict:
        ...
class V1beta1StorageVersionMigrationDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationSpecDict]
    status: typing.Optional[kubernetes.client.V1beta1StorageVersionMigrationStatusDict]
