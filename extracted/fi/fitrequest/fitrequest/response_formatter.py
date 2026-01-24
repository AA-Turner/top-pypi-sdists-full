from functools import cached_property
from xml.etree.ElementTree import Element as XmlElement

import defusedxml.ElementTree as XmlTree
import httpx
import jsonpath_ng
import orjson
from pydantic import BaseModel


class ResponseFormatter:
    def __init__(
        self,
        httpx_response: httpx.Response,
        json_path: str | None = None,
        response_model: type[BaseModel] | None = None,
    ) -> None:
        self.httpx_response = httpx_response
        self.json_path = json_path
        self.response_model = response_model
        self.content_type = self.httpx_response.headers.get('Content-Type', '').split(';')[0].strip().lower()

    def extract_json_path(self, data: dict | list | None) -> dict | list | None:
        if not data or not self.json_path:
            return data

        json_expr = jsonpath_ng.parse(self.json_path)
        matches = [match.value for match in json_expr.find(data)]

        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        return matches

    def format_json(self) -> dict | list | None:
        data = self.httpx_response.json() if self.httpx_response.content else None
        return self.extract_json_path(data)

    def format_json_lines(self) -> dict | list | None:
        data = [orjson.loads(line) for line in self.httpx_response.content.splitlines()] or None
        return self.extract_json_path(data)

    def format_html(self) -> str | None:
        # For now html formatting is not handled, the raw string is returned
        return self.httpx_response.text or None

    def format_xml(self) -> XmlElement:
        return XmlTree.fromstring(self.httpx_response.content)

    def format_default(self) -> bytes | None:
        # By default, the response content bytes is returned
        return self.httpx_response.content or None

    def format_pydantic(
        self,
        data: dict | list | bytes | XmlElement | str | None,
    ) -> BaseModel | dict | list | bytes | XmlElement | str | None:
        if not self.response_model or not isinstance(self.response_model, type(BaseModel)):
            return data

        if isinstance(data, dict):
            return self.response_model(**data)

        if isinstance(data, list):
            return [self.response_model(**elem) for elem in data]

        return data

    @cached_property
    def data(self) -> BaseModel | dict | list | bytes | XmlElement | str | None:
        if self.content_type.endswith('json'):
            data = self.format_json()
        elif self.content_type.endswith(('json-l', 'jsonlines')):
            data = self.format_json_lines()
        elif self.content_type.endswith(('plain', 'html')):
            data = self.format_html()
        elif self.content_type.endswith('xml'):
            data = self.format_xml()
        else:
            data = self.format_default()

        return self.format_pydantic(data)

    @cached_property
    def data_bytes(self) -> bytes:
        if self.data is None:
            return b''

        if isinstance(self.data, bytes):
            return self.data

        if isinstance(self.data, XmlElement):
            return XmlTree.tostring(self.data, xml_declaration=True, encoding='utf-8')

        if isinstance(self.data, BaseModel):
            return bytes(self.data.model_dump_json(indent=2), encoding='utf-8')

        if isinstance(self.data, list) and len(self.data) > 0 and isinstance(self.data[0], BaseModel):
            dumped_list = [elem.model_dump() for elem in self.data]
            return orjson.dumps(dumped_list, option=orjson.OPT_INDENT_2)

        return orjson.dumps(self.data, option=orjson.OPT_INDENT_2)
