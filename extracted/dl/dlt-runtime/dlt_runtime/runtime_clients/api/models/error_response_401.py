from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_response_401_extra import ErrorResponse401Extra


T = TypeVar("T", bound="ErrorResponse401")


@_attrs_define
class ErrorResponse401:
    """Not Authorized Exception

    Attributes:
        detail (Union[Unset, str]):
        extra (Union[Unset, ErrorResponse401Extra]): Additional error details (free-form)
        status_code (Union[Unset, int]):
    """

    detail: Union[Unset, str] = UNSET
    extra: Union[Unset, "ErrorResponse401Extra"] = UNSET
    status_code: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        extra: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        status_code = self.status_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail
        if extra is not UNSET:
            field_dict["extra"] = extra
        if status_code is not UNSET:
            field_dict["status_code"] = status_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_response_401_extra import ErrorResponse401Extra

        d = dict(src_dict)
        detail = d.pop("detail", UNSET)

        _extra = d.pop("extra", UNSET)
        extra: Union[Unset, ErrorResponse401Extra]
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = ErrorResponse401Extra.from_dict(_extra)

        status_code = d.pop("status_code", UNSET)

        error_response_401 = cls(
            detail=detail,
            extra=extra,
            status_code=status_code,
        )

        error_response_401.additional_properties = d
        return error_response_401

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
