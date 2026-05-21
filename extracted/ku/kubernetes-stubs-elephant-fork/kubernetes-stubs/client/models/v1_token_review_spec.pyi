import datetime
import typing

import kubernetes.client

class V1TokenReviewSpec:
    audiences: typing.Optional[list[str]]
    token: str
    
    def __init__(self, *, audiences: typing.Optional[list[str]] = ..., token: str) -> None:
        ...
    def to_dict(self) -> V1TokenReviewSpecDict:
        ...
class V1TokenReviewSpecDict(typing.TypedDict, total=False):
    audiences: typing.Optional[list[str]]
    token: str
