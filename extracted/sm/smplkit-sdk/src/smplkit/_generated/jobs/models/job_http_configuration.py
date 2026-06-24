from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from ..models.job_http_configuration_method import check_job_http_configuration_method
from ..models.job_http_configuration_method import JobHttpConfigurationMethod
from typing import cast

if TYPE_CHECKING:
    from ..models.job_http_configuration_headers import JobHttpConfigurationHeaders


T = TypeVar("T", bound="JobHttpConfiguration")


@_attrs_define
class JobHttpConfiguration:
    """HTTP request a job performs when it fires.

    Extends the shared HTTP configuration with the two fields a scheduled job
    needs beyond a forwarder (``body`` and ``timeout``); everything else,
    including the shared name→value ``headers`` object, is inherited unchanged.

        Attributes:
            url (str): Destination URL. Must be an absolute `http://` or `https://` URL with a hostname (e.g.
                `https://siem.example.com/in`).
            method (JobHttpConfigurationMethod | Unset): HTTP method used when delivering the request. Default: 'POST'.
            headers (JobHttpConfigurationHeaders | Unset): HTTP headers attached to each request, as a name→value object
                (e.g. `{"Authorization": "Bearer s3cr3t"}`). Override an individual header in a specific environment by its name
                via a `headers.<name>` entry in that environment's overrides; header names match case-insensitively.
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
            body (None | str | Unset): Request body sent on each run. When omitted, an empty body is sent (suitable for a
                connectivity ping). Sent verbatim — pair with a matching `Content-Type` header. Limit 1 MiB.
            timeout (int | Unset): Per-run timeout in **seconds**. A run that does not complete within this many seconds
                fails with reason `TIMEOUT`. Bounded by your plan's maximum timeout. Default: 30.
    """

    url: str
    method: JobHttpConfigurationMethod | Unset = "POST"
    headers: JobHttpConfigurationHeaders | Unset = UNSET
    success_status: str | Unset = "2xx"
    tls_verify: bool | Unset = True
    ca_cert: None | str | Unset = UNSET
    body: None | str | Unset = UNSET
    timeout: int | Unset = 30

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

        body: None | str | Unset
        if isinstance(self.body, Unset):
            body = UNSET
        else:
            body = self.body

        timeout = self.timeout

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
        if body is not UNSET:
            field_dict["body"] = body
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_http_configuration_headers import JobHttpConfigurationHeaders

        d = dict(src_dict)
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: JobHttpConfigurationMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = check_job_http_configuration_method(_method)

        _headers = d.pop("headers", UNSET)
        headers: JobHttpConfigurationHeaders | Unset
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = JobHttpConfigurationHeaders.from_dict(_headers)

        success_status = d.pop("success_status", UNSET)

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

        timeout = d.pop("timeout", UNSET)

        job_http_configuration = cls(
            url=url,
            method=method,
            headers=headers,
            success_status=success_status,
            tls_verify=tls_verify,
            ca_cert=ca_cert,
            body=body,
            timeout=timeout,
        )

        return job_http_configuration
