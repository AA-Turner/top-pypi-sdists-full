from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from typing import cast

if TYPE_CHECKING:
    from ..models.forwarder_type_header import ForwarderTypeHeader


T = TypeVar("T", bound="ForwarderTypeHttpConfiguration")


@_attrs_define
class ForwarderTypeHttpConfiguration:
    """HTTP-base-type delivery template.

    Attributes:
        method (str): HTTP method.
        url (None | str): URL template. `null` for the synthetic `http` (Custom HTTP) entry, where the customer supplies
            the URL from scratch. May contain `{name}` placeholders that map to the `placeholders` block.
        success_status (str): HTTP response status indicating a successful delivery — either a specific code (`200`,
            `204`) or a class (`2xx`).
        headers (list[ForwarderTypeHeader]): Headers attached to each delivery request.
    """

    method: str
    url: None | str
    success_status: str
    headers: list[ForwarderTypeHeader]

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        url: None | str
        url = self.url

        success_status = self.success_status

        headers = []
        for headers_item_data in self.headers:
            headers_item = headers_item_data.to_dict()
            headers.append(headers_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "method": method,
                "url": url,
                "success_status": success_status,
                "headers": headers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_type_header import ForwarderTypeHeader

        d = dict(src_dict)
        method = d.pop("method")

        def _parse_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        url = _parse_url(d.pop("url"))

        success_status = d.pop("success_status")

        headers = []
        _headers = d.pop("headers")
        for headers_item_data in _headers:
            headers_item = ForwarderTypeHeader.from_dict(headers_item_data)

            headers.append(headers_item)

        forwarder_type_http_configuration = cls(
            method=method,
            url=url,
            success_status=success_status,
            headers=headers,
        )

        return forwarder_type_http_configuration
