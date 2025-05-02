import datetime
import typing

import kubernetes.client

class V1SelectableField:
    json_path: str
    
    def __init__(self, *, json_path: str) -> None:
        ...
    def to_dict(self) -> V1SelectableFieldDict:
        ...
class V1SelectableFieldDict(typing.TypedDict, total=False):
    jsonPath: str
