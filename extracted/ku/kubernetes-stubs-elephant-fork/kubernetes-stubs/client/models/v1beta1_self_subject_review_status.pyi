import datetime
import typing

import kubernetes.client

class V1beta1SelfSubjectReviewStatus:
    user_info: typing.Optional[kubernetes.client.V1UserInfo]
    
    def __init__(self, *, user_info: typing.Optional[kubernetes.client.V1UserInfo] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1SelfSubjectReviewStatusDict:
        ...
class V1beta1SelfSubjectReviewStatusDict(typing.TypedDict, total=False):
    userInfo: typing.Optional[kubernetes.client.V1UserInfoDict]
