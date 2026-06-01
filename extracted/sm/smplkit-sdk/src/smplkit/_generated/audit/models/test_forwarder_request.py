from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from ..models.test_forwarder_request_method import check_test_forwarder_request_method
from ..models.test_forwarder_request_method import TestForwarderRequestMethod
from typing import cast

if TYPE_CHECKING:
    from ..models.http_header import HttpHeader


T = TypeVar("T", bound="TestForwarderRequest")


@_attrs_define
class TestForwarderRequest:
    """Inputs to the test-forwarder action.

    Mirrors a forwarder's HTTP destination configuration with one
    addition: `timeout_ms`, applied per-request and capped server-side.

        Attributes:
            url (str): Destination URL. Must be an absolute `http://` or `https://` URL with a hostname (e.g.
                `https://siem.example.com/in`).
            method (TestForwarderRequestMethod | Unset): HTTP method used for the test request. Default: 'POST'.
            headers (list[HttpHeader] | Unset): HTTP headers attached to the test request.
            success_status (str | Unset): HTTP response status that indicates success. Either a specific status code (e.g.
                `200`, `204`) or a status class (`1xx`, `2xx`, `3xx`, `4xx`, `5xx`). Default: '2xx'.
            timeout_ms (int | None | Unset): Per-request timeout in milliseconds. Capped at 30 seconds.
            tls_verify (bool | Unset): Whether to verify the destination server's TLS certificate. Mirrors the parent
                forwarder field of the same name — see its description for security guidance. Defaults to `true`. Default: True.
            ca_cert (None | str | Unset): Optional PEM-encoded certificate (or bundle) used to verify the destination
                server's TLS certificate. Mirrors the parent forwarder field. Must contain one or more `-----BEGIN
                CERTIFICATE-----` blocks.
            body (None | str | Unset): Request body sent to the destination. When omitted, an empty body is sent (suitable
                for connectivity probes). When set, the body is sent verbatim — pair with an appropriate `Content-Type` entry in
                `headers` so the destination interprets it correctly. Limit 1 MiB.
    """

    url: str
    method: TestForwarderRequestMethod | Unset = "POST"
    headers: list[HttpHeader] | Unset = UNSET
    success_status: str | Unset = "2xx"
    timeout_ms: int | None | Unset = UNSET
    tls_verify: bool | Unset = True
    ca_cert: None | str | Unset = UNSET
    body: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method

        headers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.headers, Unset):
            headers = []
            for headers_item_data in self.headers:
                headers_item = headers_item_data.to_dict()
                headers.append(headers_item)

        success_status = self.success_status

        timeout_ms: int | None | Unset
        if isinstance(self.timeout_ms, Unset):
            timeout_ms = UNSET
        else:
            timeout_ms = self.timeout_ms

        tls_verify = self.tls_verify

        ca_cert: None | str | Unset
        if isinstance(self.ca_cert, Unset):
            ca_cert = UNSET
        else:
            ca_cert = self.ca_cert

        body: None | str | Unset
        if isinstance(self.body, Unset):
            body = UNSET
        else:
            body = self.body

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if headers is not UNSET:
            field_dict["headers"] = headers
        if success_status is not UNSET:
            field_dict["success_status"] = success_status
        if timeout_ms is not UNSET:
            field_dict["timeout_ms"] = timeout_ms
        if tls_verify is not UNSET:
            field_dict["tls_verify"] = tls_verify
        if ca_cert is not UNSET:
            field_dict["ca_cert"] = ca_cert
        if body is not UNSET:
            field_dict["body"] = body

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_header import HttpHeader

        d = dict(src_dict)
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: TestForwarderRequestMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = check_test_forwarder_request_method(_method)

        _headers = d.pop("headers", UNSET)
        headers: list[HttpHeader] | Unset = UNSET
        if _headers is not UNSET:
            headers = []
            for headers_item_data in _headers:
                headers_item = HttpHeader.from_dict(headers_item_data)

                headers.append(headers_item)

        success_status = d.pop("success_status", UNSET)

        def _parse_timeout_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_ms = _parse_timeout_ms(d.pop("timeout_ms", UNSET))

        tls_verify = d.pop("tls_verify", UNSET)

        def _parse_ca_cert(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ca_cert = _parse_ca_cert(d.pop("ca_cert", UNSET))

        def _parse_body(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        body = _parse_body(d.pop("body", UNSET))

        test_forwarder_request = cls(
            url=url,
            method=method,
            headers=headers,
            success_status=success_status,
            timeout_ms=timeout_ms,
            tls_verify=tls_verify,
            ca_cert=ca_cert,
            body=body,
        )

        return test_forwarder_request
