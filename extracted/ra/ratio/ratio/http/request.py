from ratio.http.parameters import Parameters
from ratio.http.headers import Headers
import urllib.parse
from asgiref.typing import HTTPScope
from typing import Iterable, TypedDict, NotRequired


class RequestData(TypedDict):
    method: str
    url: str
    headers: NotRequired[Iterable[tuple[str, str]]]


class Request:
    method: str
    url: str
    body: list[str]
    cookies: dict[str, str]
    headers: Headers
    fresh: bool
    path_parameters: dict[str, str]

    __parsed_url: urllib.parse.ParseResult

    def __init__(self, data: RequestData) -> None:
        self.__parsed_url = urllib.parse.urlparse(data["url"])
        self.method = data["method"]
        self.path_parameters = {}
        self.headers = Headers()

        for header in data.get("headers", []):
            self.headers.add(header[0], header[1])

    @property
    def url_hostname(self) -> str | None:
        return self.__parsed_url.hostname

    @property
    def url_port(self) -> int | None:
        return self.__parsed_url.port

    @property
    def url_netloc(self) -> str:
        return self.__parsed_url.netloc

    @property
    def url_path(self) -> str:
        if self.__parsed_url.path == "/":
            return "/index"

        return self.__parsed_url.path

    @property
    def protocol(self) -> str:
        return self.__parsed_url.scheme

    @property
    def query_parameters(self) -> dict[str, str | list[str]]:
        parsed_query_parameters = urllib.parse.parse_qs(self.__parsed_url.query)

        return {
            key: value[0] if len(value) == 1 else value
            for (key, value) in parsed_query_parameters.items()
        }

    @property
    def parameters(self) -> Parameters:
        return {"query": self.query_parameters, "path": self.path_parameters}

    @classmethod
    def from_http_scope(cls, scope: HTTPScope) -> "Request":
        return cls(
            {
                "method": scope["method"],
                "url": scope["path"],
                "headers": map(
                    lambda item: (item[0].decode(), item[1].decode()), scope["headers"]
                ),
            }
        )
