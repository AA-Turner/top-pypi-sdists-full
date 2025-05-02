import datetime
import typing

import kubernetes.client

class V1ModifyVolumeStatus:
    status: str
    target_volume_attributes_class_name: typing.Optional[str]
    
    def __init__(self, *, status: str, target_volume_attributes_class_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ModifyVolumeStatusDict:
        ...
class V1ModifyVolumeStatusDict(typing.TypedDict, total=False):
    status: str
    targetVolumeAttributesClassName: typing.Optional[str]
