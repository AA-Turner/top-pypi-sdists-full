from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from ..models.http_configuration_method import check_http_configuration_method
from ..models.http_configuration_method import HttpConfigurationMethod
from typing import cast

if TYPE_CHECKING:
    from ..models.http_header import HttpHeader


T = TypeVar("T", bound="HttpConfiguration")


@_attrs_define
class HttpConfiguration:
    """HTTP request configuration used to deliver an event to the destination.

    Used when the parent forwarder's ``forwarder_type`` is one of the
    HTTP-family destinations (``HTTP``, ``DATADOG``, ``SPLUNK_HEC``,
    ``SUMO_LOGIC``, ``NEW_RELIC``, ``HONEYCOMB``, ``ELASTIC``). When other
    transports land (``FTP``, ``SQS``, …) their own configuration schemas
    will join this one as members of a discriminated union under the
    ``configuration`` field of ``Forwarder``.

        Attributes:
            url (str): Destination URL. Must be an absolute `http://` or `https://` URL with a hostname (e.g.
                `https://siem.example.com/in`).
            method (HttpConfigurationMethod | Unset): HTTP method used when delivering an event. Default: 'POST'.
            headers (list[HttpHeader] | Unset): HTTP headers attached to each delivery request.
            success_status (str | Unset): HTTP response status that indicates a successful delivery. Either a specific
                status code (e.g. `200`, `204`) or a status class (`1xx`, `2xx`, `3xx`, `4xx`, `5xx`). Default: '2xx'.
            tls_verify (bool | Unset): Whether to verify the destination server's TLS certificate against trusted
                certificate authorities. Defaults to `true` and should be left on for any production destination. Set to `false`
                only for development or short-lived testing against a destination that presents an untrusted certificate (e.g. a
                Splunk Cloud trial stack on `:8088` serving its default self-signed certificate). When `false`, deliveries
                proceed without certificate verification — they are vulnerable to man-in-the-middle attacks. For long-lived
                self-signed setups, pin the issuing CA via `ca_cert` instead of disabling verification entirely. Default: True.
            ca_cert (None | str | Unset): Optional PEM-encoded certificate (or bundle) used to verify the destination
                server's TLS certificate, in addition to the system trust store. Use this to pin a private or self-signed CA
                (e.g. Splunk's default `SplunkCommonCA`) without disabling verification entirely via `tls_verify`. Must contain
                one or more `-----BEGIN CERTIFICATE-----` blocks. Ignored when `tls_verify` is `false`.
    """

    url: str
    method: HttpConfigurationMethod | Unset = "POST"
    headers: list[HttpHeader] | Unset = UNSET
    success_status: str | Unset = "2xx"
    tls_verify: bool | Unset = True
    ca_cert: None | str | Unset = UNSET

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

        tls_verify = self.tls_verify

        ca_cert: None | str | Unset
        if isinstance(self.ca_cert, Unset):
            ca_cert = UNSET
        else:
            ca_cert = self.ca_cert

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
        if tls_verify is not UNSET:
            field_dict["tls_verify"] = tls_verify
        if ca_cert is not UNSET:
            field_dict["ca_cert"] = ca_cert

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_header import HttpHeader

        d = dict(src_dict)
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: HttpConfigurationMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = check_http_configuration_method(_method)

        _headers = d.pop("headers", UNSET)
        headers: list[HttpHeader] | Unset = UNSET
        if _headers is not UNSET:
            headers = []
            for headers_item_data in _headers:
                headers_item = HttpHeader.from_dict(headers_item_data)

                headers.append(headers_item)

        success_status = d.pop("success_status", UNSET)

        tls_verify = d.pop("tls_verify", UNSET)

        def _parse_ca_cert(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ca_cert = _parse_ca_cert(d.pop("ca_cert", UNSET))

        http_configuration = cls(
            url=url,
            method=method,
            headers=headers,
            success_status=success_status,
            tls_verify=tls_verify,
            ca_cert=ca_cert,
        )

        return http_configuration
