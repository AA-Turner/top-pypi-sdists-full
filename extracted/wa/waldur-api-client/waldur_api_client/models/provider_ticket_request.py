import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderTicketRequest")


@_attrs_define
class ProviderTicketRequest:
    """
    Attributes:
        escalated_at (Union[None, Unset, datetime.datetime]): When the issue was escalated.
        customer (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
    """

    escalated_at: Union[None, Unset, datetime.datetime] = UNSET
    customer: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        escalated_at: Union[None, Unset, str]
        if isinstance(self.escalated_at, Unset):
            escalated_at = UNSET
        elif isinstance(self.escalated_at, datetime.datetime):
            escalated_at = self.escalated_at.isoformat()
        else:
            escalated_at = self.escalated_at

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if escalated_at is not UNSET:
            field_dict["escalated_at"] = escalated_at
        if customer is not UNSET:
            field_dict["customer"] = customer
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_escalated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                escalated_at_type_0 = isoparse(data)

                return escalated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        escalated_at = _parse_escalated_at(d.pop("escalated_at", UNSET))

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        provider_ticket_request = cls(
            escalated_at=escalated_at,
            customer=customer,
            project=project,
        )

        provider_ticket_request.additional_properties = d
        return provider_ticket_request

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
