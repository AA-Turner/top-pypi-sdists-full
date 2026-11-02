from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_fork_creation_status_response_200_status import GetForkCreationStatusResponse200Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetForkCreationStatusResponse200")


@_attrs_define
class GetForkCreationStatusResponse200:
    """
    Attributes:
        status (GetForkCreationStatusResponse200Status):
        step (Union[Unset, str]): the part of the copy a running fork is in
        error (Union[Unset, str]):
    """

    status: GetForkCreationStatusResponse200Status
    step: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        step = self.step
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if step is not UNSET:
            field_dict["step"] = step
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = GetForkCreationStatusResponse200Status(d.pop("status"))

        step = d.pop("step", UNSET)

        error = d.pop("error", UNSET)

        get_fork_creation_status_response_200 = cls(
            status=status,
            step=step,
            error=error,
        )

        get_fork_creation_status_response_200.additional_properties = d
        return get_fork_creation_status_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
