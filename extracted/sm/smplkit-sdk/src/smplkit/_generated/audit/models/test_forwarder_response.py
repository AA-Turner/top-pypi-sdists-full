from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.test_forwarder_response_response_headers import TestForwarderResponseResponseHeaders


T = TypeVar("T", bound="TestForwarderResponse")


@_attrs_define
class TestForwarderResponse:
    """Result of a test-forwarder execution.

    Attributes:
        succeeded (bool): True if the destination responded with a status matching `success_status`.
        response_status (int | None): HTTP status code returned by the destination.
        latency_ms (int | None): Elapsed time of the request in milliseconds.
        response_headers (TestForwarderResponseResponseHeaders | Unset): Headers returned by the destination.
        response_body (None | str | Unset): Response body returned by the destination.
        error (None | str | Unset): Error message if the request did not complete.
    """

    succeeded: bool
    response_status: int | None
    latency_ms: int | None
    response_headers: TestForwarderResponseResponseHeaders | Unset = UNSET
    response_body: None | str | Unset = UNSET
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        succeeded = self.succeeded

        response_status: int | None
        response_status = self.response_status

        latency_ms: int | None
        latency_ms = self.latency_ms

        response_headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.response_headers, Unset):
            response_headers = self.response_headers.to_dict()

        response_body: None | str | Unset
        if isinstance(self.response_body, Unset):
            response_body = UNSET
        else:
            response_body = self.response_body

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "succeeded": succeeded,
                "response_status": response_status,
                "latency_ms": latency_ms,
            }
        )
        if response_headers is not UNSET:
            field_dict["response_headers"] = response_headers
        if response_body is not UNSET:
            field_dict["response_body"] = response_body
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.test_forwarder_response_response_headers import TestForwarderResponseResponseHeaders

        d = dict(src_dict)
        succeeded = d.pop("succeeded")

        def _parse_response_status(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        response_status = _parse_response_status(d.pop("response_status"))

        def _parse_latency_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms"))

        _response_headers = d.pop("response_headers", UNSET)
        response_headers: TestForwarderResponseResponseHeaders | Unset
        if isinstance(_response_headers, Unset):
            response_headers = UNSET
        else:
            response_headers = TestForwarderResponseResponseHeaders.from_dict(_response_headers)

        def _parse_response_body(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response_body = _parse_response_body(d.pop("response_body", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        test_forwarder_response = cls(
            succeeded=succeeded,
            response_status=response_status,
            latency_ms=latency_ms,
            response_headers=response_headers,
            response_body=response_body,
            error=error,
        )

        test_forwarder_response.additional_properties = d
        return test_forwarder_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
