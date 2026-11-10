import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.compensate_in_enum import CompensateInEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayEarlierInvoicesRequestRequest")


@_attrs_define
class PayEarlierInvoicesRequestRequest:
    """
    Attributes:
        dry_run (Union[Unset, bool]): Return what would be written without writing anything. Default: False.
        compensate_in (Union[Unset, CompensateInEnum]):
        earlier_invoices_from (Union[None, Unset, datetime.date]): First month to pay, as its first day. Defaults to the
            credit's own; a payment that is not a dry run also stores it.
        earlier_invoices_until (Union[None, Unset, datetime.date]): Last month to pay, as its first day. Defaults to the
            credit's own; a payment that is not a dry run also stores it.
    """

    dry_run: Union[Unset, bool] = False
    compensate_in: Union[Unset, CompensateInEnum] = UNSET
    earlier_invoices_from: Union[None, Unset, datetime.date] = UNSET
    earlier_invoices_until: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        compensate_in: Union[Unset, str] = UNSET
        if not isinstance(self.compensate_in, Unset):
            compensate_in = self.compensate_in.value

        earlier_invoices_from: Union[None, Unset, str]
        if isinstance(self.earlier_invoices_from, Unset):
            earlier_invoices_from = UNSET
        elif isinstance(self.earlier_invoices_from, datetime.date):
            earlier_invoices_from = self.earlier_invoices_from.isoformat()
        else:
            earlier_invoices_from = self.earlier_invoices_from

        earlier_invoices_until: Union[None, Unset, str]
        if isinstance(self.earlier_invoices_until, Unset):
            earlier_invoices_until = UNSET
        elif isinstance(self.earlier_invoices_until, datetime.date):
            earlier_invoices_until = self.earlier_invoices_until.isoformat()
        else:
            earlier_invoices_until = self.earlier_invoices_until

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if compensate_in is not UNSET:
            field_dict["compensate_in"] = compensate_in
        if earlier_invoices_from is not UNSET:
            field_dict["earlier_invoices_from"] = earlier_invoices_from
        if earlier_invoices_until is not UNSET:
            field_dict["earlier_invoices_until"] = earlier_invoices_until

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dry_run = d.pop("dry_run", UNSET)

        _compensate_in = d.pop("compensate_in", UNSET)
        compensate_in: Union[Unset, CompensateInEnum]
        if isinstance(_compensate_in, Unset):
            compensate_in = UNSET
        else:
            compensate_in = CompensateInEnum(_compensate_in)

        def _parse_earlier_invoices_from(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                earlier_invoices_from_type_0 = isoparse(data).date()

                return earlier_invoices_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        earlier_invoices_from = _parse_earlier_invoices_from(d.pop("earlier_invoices_from", UNSET))

        def _parse_earlier_invoices_until(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                earlier_invoices_until_type_0 = isoparse(data).date()

                return earlier_invoices_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        earlier_invoices_until = _parse_earlier_invoices_until(d.pop("earlier_invoices_until", UNSET))

        pay_earlier_invoices_request_request = cls(
            dry_run=dry_run,
            compensate_in=compensate_in,
            earlier_invoices_from=earlier_invoices_from,
            earlier_invoices_until=earlier_invoices_until,
        )

        pay_earlier_invoices_request_request.additional_properties = d
        return pay_earlier_invoices_request_request

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
