import datetime
import typing

import kubernetes.client

class V1ImageVolumeStatus:
    image_ref: str
    
    def __init__(self, *, image_ref: str) -> None:
        ...
    def to_dict(self) -> V1ImageVolumeStatusDict:
        ...
class V1ImageVolumeStatusDict(typing.TypedDict, total=False):
    imageRef: str
