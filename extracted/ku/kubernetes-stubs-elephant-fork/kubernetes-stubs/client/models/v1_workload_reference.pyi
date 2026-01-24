import datetime
import typing

import kubernetes.client

class V1WorkloadReference:
    name: str
    pod_group: str
    pod_group_replica_key: typing.Optional[str]
    
    def __init__(self, *, name: str, pod_group: str, pod_group_replica_key: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1WorkloadReferenceDict:
        ...
class V1WorkloadReferenceDict(typing.TypedDict, total=False):
    name: str
    podGroup: str
    podGroupReplicaKey: typing.Optional[str]
