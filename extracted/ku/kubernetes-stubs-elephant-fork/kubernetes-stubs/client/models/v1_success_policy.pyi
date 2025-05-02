import datetime
import typing

import kubernetes.client

class V1SuccessPolicy:
    rules: list[kubernetes.client.V1SuccessPolicyRule]
    
    def __init__(self, *, rules: list[kubernetes.client.V1SuccessPolicyRule]) -> None:
        ...
    def to_dict(self) -> V1SuccessPolicyDict:
        ...
class V1SuccessPolicyDict(typing.TypedDict, total=False):
    rules: list[kubernetes.client.V1SuccessPolicyRuleDict]
