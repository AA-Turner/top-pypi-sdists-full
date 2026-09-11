from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunTicketResponse")


@_attrs_define
class RunTicketResponse:
    """
    Attributes:
        ticket (str): Signed DataplaneRunnerJwt scoped to the run
        ingest_url (None | str | Unset): Where the runner posts (telemetry beacon, log ingest); None when N/A
    """

    ticket: str
    ingest_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket = self.ticket

        ingest_url: None | str | Unset
        if isinstance(self.ingest_url, Unset):
            ingest_url = UNSET
        else:
            ingest_url = self.ingest_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
            }
        )
        if ingest_url is not UNSET:
            field_dict["ingest_url"] = ingest_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket = d.pop("ticket")

        def _parse_ingest_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ingest_url = _parse_ingest_url(d.pop("ingest_url", UNSET))

        run_ticket_response = cls(
            ticket=ticket,
            ingest_url=ingest_url,
        )

        run_ticket_response.additional_properties = d
        return run_ticket_response

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
