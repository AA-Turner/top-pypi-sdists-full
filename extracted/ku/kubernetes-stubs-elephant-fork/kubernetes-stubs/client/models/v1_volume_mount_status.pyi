import datetime
import typing

import kubernetes.client

class V1VolumeMountStatus:
    mount_path: str
    name: str
    read_only: typing.Optional[bool]
    recursive_read_only: typing.Optional[str]
    
    def __init__(self, *, mount_path: str, name: str, read_only: typing.Optional[bool] = ..., recursive_read_only: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1VolumeMountStatusDict:
        ...
class V1VolumeMountStatusDict(typing.TypedDict, total=False):
    mountPath: str
    name: str
    readOnly: typing.Optional[bool]
    recursiveReadOnly: typing.Optional[str]
