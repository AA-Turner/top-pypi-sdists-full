import datetime
import typing

import kubernetes.client

class V1CSINodeStatus:
    storage_health: typing.Optional[list[kubernetes.client.V1StorageHealth]]
    
    def __init__(self, *, storage_health: typing.Optional[list[kubernetes.client.V1StorageHealth]] = ...) -> None:
        ...
    def to_dict(self) -> V1CSINodeStatusDict:
        ...
class V1CSINodeStatusDict(typing.TypedDict, total=False):
    storageHealth: typing.Optional[list[kubernetes.client.V1StorageHealthDict]]
