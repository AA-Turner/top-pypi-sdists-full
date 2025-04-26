from logging import Logger
from typing import Any, Optional, Union

import six

logger: Logger

class Request:

    sec: Any
    receiver_addrs: Any
    timeslack: Any
    xmlstr: str
    name_id: str
    message: Optional[Any]
    not_on_or_after: int
    attribute_converters: Optional[Any]
    binding: Optional[Any]
    relay_state: str
    signature_check: Any
    def __init__(
        self, sec_context: Any, receiver_addrs: Any, attribute_converters: Optional[Any] = ..., timeslack: int = ...
    ) -> None: ...
    def issue_instant_ok(self) -> bool: ...
    def loads(
        self,
        xmldata: Union[str, six.binary_type],
        binding: str,
        origdoc: Optional[Any] = ...,
        must: Optional[bool] = ...,
        only_valid_cert: bool = ...,
        relay_state: Optional[Any] = ...,
        sigalg: Optional[str] = ...,
        signature: Optional[Any] = ...,
    ) -> Request: ...
    def verify(self) -> Optional[bool]: ...
    def subject_id(self) -> Optional[str]: ...
    def sender(self) -> str: ...

class AuthnRequest(Request):
    msgtype: str
    signature_check: Any
    def __init__(
        self, sec_context: Any, receiver_addrs: Any, attribute_converters: Any, timeslack: int = ...
    ) -> None: ...
    def attributes(self) -> dict[str, Any]: ...

def __getattr__(name: str) -> Any: ...  # incomplete
