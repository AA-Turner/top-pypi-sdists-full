import base64
import json
from io import BytesIO
from typing import TYPE_CHECKING, Dict, List, Tuple, Union

from abstra_internals.email_signer import verify_email
from abstra_internals.environment import IS_PRODUCTION
from abstra_internals.utils.insensitive_dict import CaseInsensitiveDict

if TYPE_CHECKING:
    from abstra_internals.controllers.execution.execution_client_hook import HookClient


class HookSDKController:
    def __init__(self, client: "HookClient") -> None:
        self.client = client

    def set_response(self, status: int, body: str, headers: Dict[str, str]):
        self.client.set_response(status, body, headers)

    def get_raw_request(self) -> Tuple[str, Dict[str, str], CaseInsensitiveDict]:
        body, query, headers = self._get_body_and_headers()
        ct = (headers.get("Content-Type") or "").lower()
        if ct.startswith("multipart/form-data"):
            body = base64.b64decode(body).decode("latin-1")
        return body, query, headers

    def _get_body_and_headers(self):
        if self.client.context.mock_execution.test_request:
            test_request = self.client.context.mock_execution.test_request
            return (
                test_request.body,
                test_request.query_params,
                CaseInsensitiveDict(test_request.headers),
            )
        request = self.client.get_request()
        return (
            request.body,
            request.query_params,
            CaseInsensitiveDict(request.headers),
        )

    def get_request(
        self,
    ) -> Tuple[Union[str, List, Dict], Dict[str, str], CaseInsensitiveDict]:
        body, query, headers = self._get_body_and_headers()
        try:
            if "application/json" in headers["Content-Type"]:
                return json.loads(body), query, headers
            elif "multipart/form-data" in headers["Content-Type"]:
                return self._multipart_form_parse(body, headers), query, headers
            else:
                return body, query, headers
        except Exception:
            return body, query, headers

    def _multipart_form_parse(self, body: str, headers: CaseInsensitiveDict):
        from multipart import (
            MultipartParser,
            MultipartPart,
            parse_options_header,
        )

        raw_bytes = base64.b64decode(body)
        _, options = parse_options_header(headers["Content-Type"])
        boundary = options["boundary"].encode("utf-8")
        p = MultipartParser(BytesIO(raw_bytes), boundary)
        parts = []
        for i in p:
            if not isinstance(i, MultipartPart):
                continue
            filename = getattr(i, "filename", None)
            if filename:
                raw = getattr(i, "raw", b"")
                parts.append(
                    {
                        "name": i.name,
                        "filename": filename,
                        "content_type": getattr(
                            i, "content_type", "application/octet-stream"
                        ),
                        "content": base64.b64encode(raw).decode("ascii"),
                    }
                )
            else:
                parts.append({"name": i.name, "value": i.value})
        return parts

    def get_email_request(self):
        body, _, headers = self.get_raw_request()
        b64content: str = json.loads(body).get("content")
        if not b64content:
            raise Exception("Bad request")

        signed_hash = headers.get("x-abstra-notification-signed-hash")
        if not signed_hash and IS_PRODUCTION:
            raise Exception("Email verification failed")

        if signed_hash:
            if not verify_email(jwt_header=signed_hash, content=b64content):
                raise Exception("Email verification failed")

        from mailparser import parse_from_string

        return parse_from_string(base64.b64decode(b64content).decode("utf-8"))
