import datetime
import typing

import kubernetes.client

class V1ContainerUser:
    linux: typing.Optional[kubernetes.client.V1LinuxContainerUser]
    
    def __init__(self, *, linux: typing.Optional[kubernetes.client.V1LinuxContainerUser] = ...) -> None:
        ...
    def to_dict(self) -> V1ContainerUserDict:
        ...
class V1ContainerUserDict(typing.TypedDict, total=False):
    linux: typing.Optional[kubernetes.client.V1LinuxContainerUserDict]
