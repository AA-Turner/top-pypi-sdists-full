"""Response base class"""
from typing import (
    Optional,
    Union,
    Set,
    Sequence,
    Mapping,
    Callable,
    Tuple,
    Any,
    Deque,
    Dict,
    Iterable,
    cast,
    ByteString,
)
import collections
import io
import logging

from libadvian.binpackers import ensure_str

from .utilities import convert_b64

LOGGER = logging.getLogger(__name__)
StrSetSrcTypes = Union[Set[str], Sequence[str]]
IntHeadersType = Sequence[Tuple[str, str]]  # Internal headers repr, list of tuples


class StartResponse:
    """Base class for mapping WSGI to AWS Lambda"""

    def __init__(
        self,
        base64_content_types: Optional[StrSetSrcTypes] = None,
        base64_content_encodings: Optional[StrSetSrcTypes] = None,
    ) -> None:
        """
        Args:
            base64_content_types (set): Set of HTTP Content-Types which should
            return a base64 encoded body. Enables returning binary content from
            API Gateway.
            base64_content_encoding (set): Set of HTTP Content-Encodings which should
            return a base64 encoded body. Enables returning compressed/binary content from
            API Gateway.
        """
        self.status: int = 500
        self.status_line: str = "500 Internal Server Error"
        self.headers: IntHeadersType = []  # This type might be completely wrong
        self.chunks: Deque[bytes] = collections.deque()
        self.base64_content_types: Set[str] = set(base64_content_types or [])
        self.base64_content_encodings: Set[str] = set(base64_content_encodings or ("br", "gzip", "deflate"))

    def __call__(
        self, status: str, headers: IntHeadersType, exc_info: Optional[Exception] = None
    ) -> Callable[..., Any]:
        """Decoration for data receiving"""
        self.status_line = status
        self.status = int(status.split()[0])
        self.headers = headers
        return self.chunks.append

    def use_binary_response(self, headers: Mapping[str, str], _body: bytes) -> bool:
        """Is the response binary or text"""
        content_type = headers.get("Content-Type")
        content_encoding = headers.get("Content-Encoding")
        if content_encoding in self.base64_content_encodings:
            return True

        if content_type and ";" in content_type:
            content_type = content_type.split(";")[0]
        return content_type in self.base64_content_types

    def build_body(
        self, headers: Mapping[str, str], output: Union[bytes, io.BytesIO, Iterable[ByteString]]
    ) -> Mapping[str, Union[bool, str]]:
        """Build the response body, return dict with body and indication whether it was b64 encoded or not"""
        full_body = b"".join(self.chunks)
        if isinstance(output, Iterable):
            full_body += b"".join(cast(Iterable[ByteString], output))
        elif isinstance(output, io.BytesIO):
            full_body += output.read(-1)
        else:
            full_body += output

        is_b64 = self.use_binary_response(headers, full_body)
        if is_b64:
            converted_output = convert_b64(full_body)
        else:
            converted_output = ensure_str(full_body)

        return {
            "isBase64Encoded": is_b64,
            "body": converted_output,
        }

    def response(self, output: Union[bytes, io.BytesIO]) -> Mapping[str, Union[bool, str, int, Mapping[str, str]]]:
        """Create the response dict"""
        headers = cast(Dict[str, str], dict(self.headers))
        resp: Dict[str, Union[bool, str, int, Mapping[str, str]]] = {
            "statusCode": self.status,
            "headers": headers,
        }
        resp.update(self.build_body(headers, output))
        return resp
