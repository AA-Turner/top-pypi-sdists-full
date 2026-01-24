# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contrast_fireball
from contrast_agent_lib import constants
from contrast_fireball import AttackInputType

_AGENT_LIB_INPUT_TYPE = {
    AttackInputType.COOKIE_NAME: constants.InputType["CookieName"],
    AttackInputType.COOKIE_VALUE: constants.InputType["CookieValue"],
    AttackInputType.HEADER: constants.InputType["HeaderValue"],
    AttackInputType.PARAMETER_NAME: constants.InputType["ParameterKey"],
    AttackInputType.PARAMETER_VALUE: constants.InputType["ParameterValue"],
    AttackInputType.URI: constants.InputType["UriPath"],
    AttackInputType.JSON_VALUE: constants.InputType["JsonValue"],
    AttackInputType.MULTIPART_NAME: constants.InputType["MultipartName"],
    AttackInputType.XML_VALUE: constants.InputType["XmlValue"],
    AttackInputType.METHOD: constants.InputType["Method"],
    AttackInputType.URL_PARAMETER: constants.InputType["UrlParameter"],
}
_REVERSE_AGENT_LIB_INPUT_TYPE = {v: k for k, v in _AGENT_LIB_INPUT_TYPE.items()} | {
    constants.InputType["JsonKey"]: AttackInputType.JSON_VALUE
}


def agent_lib_input_type(input_type: AttackInputType) -> int:
    return _AGENT_LIB_INPUT_TYPE[input_type]


def from_agent_lib_input_type(type: int) -> AttackInputType:
    return AttackInputType(_REVERSE_AGENT_LIB_INPUT_TYPE[type])


_CEF_FMT_FROM_INPUT_TYPE = {
    AttackInputType.BODY: "body segment",
    AttackInputType.COOKIE_NAME: "cookie {}",
    AttackInputType.COOKIE_VALUE: "cookie {}",
    AttackInputType.HEADER: "header {}",
    AttackInputType.PARAMETER_NAME: "parameter {}",
    AttackInputType.PARAMETER_VALUE: "parameter {}",
    AttackInputType.QUERYSTRING: "querystring",
    AttackInputType.URI: "URI",
    AttackInputType.SOCKET: "socket",
    AttackInputType.JSON_VALUE: "JSON value {}",
    AttackInputType.JSON_ARRAYED_VALUE: "JSON array value {}",
    AttackInputType.MULTIPART_CONTENT_TYPE: "content-type of the multipart {}",
    AttackInputType.MULTIPART_VALUE: "value of the multipart {}",
    AttackInputType.MULTIPART_FIELD_NAME: "multipart field name {}",
    AttackInputType.MULTIPART_NAME: "name of the multipart {}",
    AttackInputType.XML_VALUE: "XML value {}",
    AttackInputType.METHOD: "method {}",
    AttackInputType.UNKNOWN: "untrusted input",
    None: "untrusted input",
}


def cef_string(input_type: AttackInputType | None, key: str | None) -> str:
    fmt = _CEF_FMT_FROM_INPUT_TYPE.get(input_type, "untrusted input")
    return fmt.format(key) if fmt.endswith("{}") else fmt


def document_type_from_input_type(
    input_type: AttackInputType,
) -> contrast_fireball.DocumentType:
    if input_type == AttackInputType.JSON_VALUE:
        return contrast_fireball.DocumentType.JSON
    elif input_type == AttackInputType.XML_VALUE:
        return contrast_fireball.DocumentType.XML
    else:
        return contrast_fireball.DocumentType.NORMAL
