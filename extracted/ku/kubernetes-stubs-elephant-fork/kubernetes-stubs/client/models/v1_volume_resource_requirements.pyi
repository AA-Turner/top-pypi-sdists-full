import datetime
import typing

import kubernetes.client

class V1VolumeResourceRequirements:
    limits: typing.Optional[dict[str, str]]
    requests: typing.Optional[dict[str, str]]
    
    def __init__(self, *, limits: typing.Optional[dict[str, str]] = ..., requests: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> V1VolumeResourceRequirementsDict:
        ...
class V1VolumeResourceRequirementsDict(typing.TypedDict, total=False):
    limits: typing.Optional[dict[str, str]]
    requests: typing.Optional[dict[str, str]]
