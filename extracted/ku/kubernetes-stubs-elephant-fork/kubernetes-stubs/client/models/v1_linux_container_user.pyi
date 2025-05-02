import datetime
import typing

import kubernetes.client

class V1LinuxContainerUser:
    gid: int
    supplemental_groups: typing.Optional[list[int]]
    uid: int
    
    def __init__(self, *, gid: int, supplemental_groups: typing.Optional[list[int]] = ..., uid: int) -> None:
        ...
    def to_dict(self) -> V1LinuxContainerUserDict:
        ...
class V1LinuxContainerUserDict(typing.TypedDict, total=False):
    gid: int
    supplementalGroups: typing.Optional[list[int]]
    uid: int
