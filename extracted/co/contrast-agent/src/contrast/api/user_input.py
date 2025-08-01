# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto

from contrast_agent_lib import constants


class DocumentType(Enum):
    NORMAL = auto()
    JSON = auto()
    XML = auto()


class InputType(Enum):
    COOKIE_NAME = auto()
    COOKIE_VALUE = auto()
    HEADER = auto()
    PARAMETER_NAME = auto()
    PARAMETER_VALUE = auto()
    URI = auto()
    JSON_VALUE = auto()
    MULTIPART_NAME = auto()
    XML_VALUE = auto()
    UNKNOWN = auto()
    METHOD = auto()
    URL_PARAMETER = auto()

    def cef_string(self, key: str):
        fmt = _CEF_FMT_FROM_INPUT_TYPE.get(self, "untrusted input")
        return fmt.format(key) if fmt.endswith("{}") else fmt

    @property
    def is_body_based(self) -> bool:
        """
        Indicates if the input can be found in the body of a request.

        This doesn't guarntee that the input is actually from the body,
        for example, a querystring parameter will return True because we
        don't distinguish between querystring and body form parameters.
        """
        return self in (
            InputType.PARAMETER_VALUE,
            InputType.MULTIPART_NAME,
            InputType.JSON_VALUE,
            InputType.XML_VALUE,
        )

    @property
    def agent_lib_type(self) -> int:
        return _AGENT_LIB_INPUT_TYPE[self]

    @classmethod
    def from_agent_lib_type(cls, type: int):
        return cls(_REVERSE_AGENT_LIB_INPUT_TYPE[type])


_AGENT_LIB_INPUT_TYPE = {
    InputType.COOKIE_NAME: constants.InputType["CookieName"],
    InputType.COOKIE_VALUE: constants.InputType["CookieValue"],
    InputType.HEADER: constants.InputType["HeaderValue"],
    InputType.PARAMETER_NAME: constants.InputType["ParameterKey"],
    InputType.PARAMETER_VALUE: constants.InputType["ParameterValue"],
    InputType.URI: constants.InputType["UriPath"],
    InputType.JSON_VALUE: constants.InputType["JsonValue"],
    InputType.MULTIPART_NAME: constants.InputType["MultipartName"],
    InputType.XML_VALUE: constants.InputType["XmlValue"],
    InputType.METHOD: constants.InputType["Method"],
    InputType.URL_PARAMETER: constants.InputType["UrlParameter"],
}
_REVERSE_AGENT_LIB_INPUT_TYPE = {v: k for k, v in _AGENT_LIB_INPUT_TYPE.items()} | {
    constants.InputType["JsonKey"]: InputType.JSON_VALUE
}


_CEF_FMT_FROM_INPUT_TYPE = {
    InputType.COOKIE_NAME: "cookie {}",
    InputType.COOKIE_VALUE: "cookie {}",
    InputType.HEADER: "header {}",
    InputType.PARAMETER_NAME: "parameter {}",
    InputType.PARAMETER_VALUE: "parameter {}",
    InputType.URI: "URI",
    InputType.JSON_VALUE: "JSON value {}",
    InputType.MULTIPART_NAME: "name of the multipart {}",
    InputType.XML_VALUE: "XML value {}",
    InputType.METHOD: "method {}",
    InputType.UNKNOWN: "untrusted input",
}


@dataclass
class UserInput:
    value: str
    type: InputType = InputType.UNKNOWN
    name: str | None = None
    path: str | None = None
    matcher_ids: list[str] = field(default_factory=list)
    document_type: DocumentType = DocumentType.NORMAL

    def __post_init__(self):
        if self.type == InputType.JSON_VALUE:
            self.document_type = DocumentType.JSON
            self.path = self.name
        elif self.type == InputType.XML_VALUE:
            self.document_type = DocumentType.XML
            self.path = self.name

    @property
    def is_name_based(self) -> bool:
        """
        Indicates if the input is based on a name (e.g., parameter name, cookie name).
        """
        return self.type in (
            InputType.COOKIE_NAME,
            InputType.PARAMETER_NAME,
            InputType.MULTIPART_NAME,
        )
