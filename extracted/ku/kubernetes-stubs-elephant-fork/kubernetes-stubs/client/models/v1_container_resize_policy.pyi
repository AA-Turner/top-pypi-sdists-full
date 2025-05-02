import datetime
import typing

import kubernetes.client

class V1ContainerResizePolicy:
    resource_name: str
    restart_policy: str
    
    def __init__(self, *, resource_name: str, restart_policy: str) -> None:
        ...
    def to_dict(self) -> V1ContainerResizePolicyDict:
        ...
class V1ContainerResizePolicyDict(typing.TypedDict, total=False):
    resourceName: str
    restartPolicy: str
