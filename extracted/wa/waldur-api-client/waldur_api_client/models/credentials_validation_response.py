from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.server_info import ServerInfo


T = TypeVar("T", bound="CredentialsValidationResponse")


@_attrs_define
class CredentialsValidationResponse:
    """
    Attributes:
        valid (bool):
        message (Union[Unset, str]):
        error (Union[Unset, str]):
        server_info (Union['ServerInfo', None, Unset]):
    """

    valid: bool
    message: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    server_info: Union["ServerInfo", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.server_info import ServerInfo

        valid = self.valid

        message = self.message

        error = self.error

        server_info: Union[None, Unset, dict[str, Any]]
        if isinstance(self.server_info, Unset):
            server_info = UNSET
        elif isinstance(self.server_info, ServerInfo):
            server_info = self.server_info.to_dict()
        else:
            server_info = self.server_info

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "valid": valid,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if error is not UNSET:
            field_dict["error"] = error
        if server_info is not UNSET:
            field_dict["server_info"] = server_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.server_info import ServerInfo

        d = dict(src_dict)
        valid = d.pop("valid")

        message = d.pop("message", UNSET)

        error = d.pop("error", UNSET)

        def _parse_server_info(data: object) -> Union["ServerInfo", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                server_info_type_1 = ServerInfo.from_dict(data)

                return server_info_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ServerInfo", None, Unset], data)

        server_info = _parse_server_info(d.pop("server_info", UNSET))

        credentials_validation_response = cls(
            valid=valid,
            message=message,
            error=error,
            server_info=server_info,
        )

        credentials_validation_response.additional_properties = d
        return credentials_validation_response

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
