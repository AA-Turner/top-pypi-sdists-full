import datetime
import typing

import kubernetes.client

class V1alpha1ServerStorageVersion:
    api_server_id: str
    decodable_versions: list[str]
    encoding_version: str
    served_versions: typing.Optional[list[str]]
    
    def __init__(self, *, api_server_id: str, decodable_versions: list[str], encoding_version: str, served_versions: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ServerStorageVersionDict:
        ...
class V1alpha1ServerStorageVersionDict(typing.TypedDict, total=False):
    apiServerID: str
    decodableVersions: list[str]
    encodingVersion: str
    servedVersions: typing.Optional[list[str]]
