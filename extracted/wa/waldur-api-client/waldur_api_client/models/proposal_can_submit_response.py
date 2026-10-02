from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProposalCanSubmitResponse")


@_attrs_define
class ProposalCanSubmitResponse:
    """
    Attributes:
        can_submit (bool):
        error (Union[None, str]):
    """

    can_submit: bool
    error: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        can_submit = self.can_submit

        error: Union[None, str]
        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "can_submit": can_submit,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        can_submit = d.pop("can_submit")

        def _parse_error(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        error = _parse_error(d.pop("error"))

        proposal_can_submit_response = cls(
            can_submit=can_submit,
            error=error,
        )

        proposal_can_submit_response.additional_properties = d
        return proposal_can_submit_response

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
