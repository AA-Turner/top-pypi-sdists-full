from enum import Enum
from typing import Dict


class HttpHeaders(str, Enum):
    accept = "accept"
    content_type = "Content-Type"
    application_json = "application/json"

    @staticmethod
    def accept_json() -> Dict[str, str]:
        return {HttpHeaders.accept: HttpHeaders.application_json}

    @staticmethod
    def content_type_json() -> Dict[str, str]:
        return {HttpHeaders.content_type: HttpHeaders.application_json}

    @staticmethod
    def json() -> Dict[str, str]:
        return {**HttpHeaders.accept_json(), **HttpHeaders.content_type_json()}
