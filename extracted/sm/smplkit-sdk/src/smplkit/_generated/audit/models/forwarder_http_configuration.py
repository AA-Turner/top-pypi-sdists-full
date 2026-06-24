from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from ..models.forwarder_http_configuration_method import check_forwarder_http_configuration_method
from ..models.forwarder_http_configuration_method import ForwarderHttpConfigurationMethod
from typing import cast

if TYPE_CHECKING:
    from ..models.forwarder_http_configuration_headers import ForwarderHttpConfigurationHeaders


T = TypeVar("T", bound="ForwarderHttpConfiguration")


@_attrs_define
class ForwarderHttpConfiguration:
    """HTTP request a forwarder makes to deliver an event.

    The shared HTTP configuration, unchanged — including the name→value
    ``headers`` object whose entries can be overridden per environment by name.
    It exists as a distinct subclass only so the spec exposes a
    forwarder-specific schema name; it adds no fields of its own.

        Attributes:
            url (str): Destination URL. Must be an absolute `http://` or `https://` URL with a hostname (e.g.
                `https://siem.example.com/in`).
            method (ForwarderHttpConfigurationMethod | Unset): HTTP method used when delivering the request. Default:
                'POST'.
            headers (ForwarderHttpConfigurationHeaders | Unset): HTTP headers attached to each request, as a name→value
                object (e.g. `{"Authorization": "Bearer s3cr3t"}`). Override an individual header in a specific environment by
                its name via a `headers.<name>` entry in that environment's overrides; header names match case-insensitively.
            success_status (str | Unset): HTTP response status that indicates success. Either a specific status code (e.g.
                `200`, `204`) or a status class (`1xx`, `2xx`, `3xx`, `4xx`, `5xx`). Default: '2xx'.
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
    method: ForwarderHttpConfigurationMethod | Unset = "POST"
    headers: ForwarderHttpConfigurationHeaders | Unset = UNSET
    success_status: str | Unset = "2xx"
    tls_verify: bool | Unset = True
    ca_cert: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method

        headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

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
        from ..models.forwarder_http_configuration_headers import ForwarderHttpConfigurationHeaders

        d = dict(src_dict)
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: ForwarderHttpConfigurationMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = check_forwarder_http_configuration_method(_method)

        _headers = d.pop("headers", UNSET)
        headers: ForwarderHttpConfigurationHeaders | Unset
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = ForwarderHttpConfigurationHeaders.from_dict(_headers)

        success_status = d.pop("success_status", UNSET)

        tls_verify = d.pop("tls_verify", UNSET)

        def _parse_ca_cert(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ca_cert = _parse_ca_cert(d.pop("ca_cert", UNSET))

        forwarder_http_configuration = cls(
            url=url,
            method=method,
            headers=headers,
            success_status=success_status,
            tls_verify=tls_verify,
            ca_cert=ca_cert,
        )

        return forwarder_http_configuration
