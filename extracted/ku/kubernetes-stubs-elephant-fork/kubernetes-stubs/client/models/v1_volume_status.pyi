import datetime
import typing

import kubernetes.client

class V1VolumeStatus:
    image: typing.Optional[kubernetes.client.V1ImageVolumeStatus]
    
    def __init__(self, *, image: typing.Optional[kubernetes.client.V1ImageVolumeStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1VolumeStatusDict:
        ...
class V1VolumeStatusDict(typing.TypedDict, total=False):
    image: typing.Optional[kubernetes.client.V1ImageVolumeStatusDict]
