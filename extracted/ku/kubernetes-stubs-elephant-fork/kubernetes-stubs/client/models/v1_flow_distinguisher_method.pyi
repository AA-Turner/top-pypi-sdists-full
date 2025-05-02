import datetime
import typing

import kubernetes.client

class V1FlowDistinguisherMethod:
    type: str
    
    def __init__(self, *, type: str) -> None:
        ...
    def to_dict(self) -> V1FlowDistinguisherMethodDict:
        ...
class V1FlowDistinguisherMethodDict(typing.TypedDict, total=False):
    type: str
