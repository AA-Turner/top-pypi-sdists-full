from dataclasses import dataclass
from email.message import Message
from typing import Dict


@dataclass
class ParseContentResult:
    """
    Results of parsing an HTTP `Content-Type` header.

    :param content_type: The extracted content type such as "application/json".
    :param attributes: Other key=value attribute pairs such as "charset=UTF-8".
    """

    content_type: str
    attributes: Dict[str, str]


def parse_content_type(content_type_header: str) -> ParseContentResult:
    "Parses an HTTP `Content-Type` header."

    email = Message()
    email["Content-Type"] = content_type_header
    params = email.get_params(failobj=[("application/octet-stream", "")])
    return ParseContentResult(params[0][0], dict(params[1:]))


def get_content_type(content_type_header: str) -> str:
    result = parse_content_type(content_type_header)
    return result.content_type
