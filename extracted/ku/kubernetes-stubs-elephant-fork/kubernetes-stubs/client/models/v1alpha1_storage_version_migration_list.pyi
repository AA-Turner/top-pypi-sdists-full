import datetime
import typing

import kubernetes.client

class V1alpha1StorageVersionMigrationList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1StorageVersionMigration]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha1StorageVersionMigration], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1StorageVersionMigrationListDict:
        ...
class V1alpha1StorageVersionMigrationListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha1StorageVersionMigrationDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
