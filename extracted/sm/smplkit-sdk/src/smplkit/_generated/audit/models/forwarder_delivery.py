from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forwarder_delivery_status import check_forwarder_delivery_status
from ..models.forwarder_delivery_status import ForwarderDeliveryStatus
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
    from ..models.forwarder_delivery_request_type_0 import ForwarderDeliveryRequestType0


T = TypeVar("T", bound="ForwarderDelivery")


@_attrs_define
class ForwarderDelivery:
    """A log entry for one attempt to deliver an event to a forwarder.

    Attributes:
        forwarder_id (UUID): Forwarder the delivery belongs to.
        event_id (UUID): Event that was being delivered.
        attempt_number (int): 1 for the initial delivery, incremented for each retry.
        status (ForwarderDeliveryStatus): Delivery outcome. `SUCCEEDED` when the destination accepted the event,
            `FAILED` when the delivery attempt did not succeed. Events that a forwarder's filter rejected are not recorded
            as deliveries.
        request (ForwarderDeliveryRequestType0 | None | Unset): The HTTP request as it was sent to the destination.
            Header values are redacted.
        response_status (int | None | Unset): HTTP status code returned by the destination.
        response_body (None | str | Unset): Response body returned by the destination.
        latency_ms (int | None | Unset): Elapsed time of the delivery attempt in milliseconds.
        error (None | str | Unset): Error message if the delivery did not complete.
        created_at (datetime.datetime | None | Unset): When the delivery attempt was recorded.
    """

    forwarder_id: UUID
    event_id: UUID
    attempt_number: int
    status: ForwarderDeliveryStatus
    request: ForwarderDeliveryRequestType0 | None | Unset = UNSET
    response_status: int | None | Unset = UNSET
    response_body: None | str | Unset = UNSET
    latency_ms: int | None | Unset = UNSET
    error: None | str | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.forwarder_delivery_request_type_0 import ForwarderDeliveryRequestType0

        forwarder_id = str(self.forwarder_id)

        event_id = str(self.event_id)

        attempt_number = self.attempt_number

        status: str = self.status

        request: dict[str, Any] | None | Unset
        if isinstance(self.request, Unset):
            request = UNSET
        elif isinstance(self.request, ForwarderDeliveryRequestType0):
            request = self.request.to_dict()
        else:
            request = self.request

        response_status: int | None | Unset
        if isinstance(self.response_status, Unset):
            response_status = UNSET
        else:
            response_status = self.response_status

        response_body: None | str | Unset
        if isinstance(self.response_body, Unset):
            response_body = UNSET
        else:
            response_body = self.response_body

        latency_ms: int | None | Unset
        if isinstance(self.latency_ms, Unset):
            latency_ms = UNSET
        else:
            latency_ms = self.latency_ms

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "forwarder_id": forwarder_id,
                "event_id": event_id,
                "attempt_number": attempt_number,
                "status": status,
            }
        )
        if request is not UNSET:
            field_dict["request"] = request
        if response_status is not UNSET:
            field_dict["response_status"] = response_status
        if response_body is not UNSET:
            field_dict["response_body"] = response_body
        if latency_ms is not UNSET:
            field_dict["latency_ms"] = latency_ms
        if error is not UNSET:
            field_dict["error"] = error
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_delivery_request_type_0 import ForwarderDeliveryRequestType0

        d = dict(src_dict)
        forwarder_id = UUID(d.pop("forwarder_id"))

        event_id = UUID(d.pop("event_id"))

        attempt_number = d.pop("attempt_number")

        status = check_forwarder_delivery_status(d.pop("status"))

        def _parse_request(data: object) -> ForwarderDeliveryRequestType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                request_type_0 = ForwarderDeliveryRequestType0.from_dict(data)

                return request_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ForwarderDeliveryRequestType0 | None | Unset, data)

        request = _parse_request(d.pop("request", UNSET))

        def _parse_response_status(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        response_status = _parse_response_status(d.pop("response_status", UNSET))

        def _parse_response_body(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response_body = _parse_response_body(d.pop("response_body", UNSET))

        def _parse_latency_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        forwarder_delivery = cls(
            forwarder_id=forwarder_id,
            event_id=event_id,
            attempt_number=attempt_number,
            status=status,
            request=request,
            response_status=response_status,
            response_body=response_body,
            latency_ms=latency_ms,
            error=error,
            created_at=created_at,
        )

        forwarder_delivery.additional_properties = d
        return forwarder_delivery

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
