import datetime
import typing

import kubernetes.client

class V1beta1StorageVersionMigrationStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    resource_version: typing.Optional[str]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., resource_version: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1StorageVersionMigrationStatusDict:
        ...
class V1beta1StorageVersionMigrationStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    resourceVersion: typing.Optional[str]
