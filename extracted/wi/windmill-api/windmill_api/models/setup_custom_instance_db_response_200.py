from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.setup_custom_instance_db_response_200_tag import SetupCustomInstanceDbResponse200Tag
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.setup_custom_instance_db_response_200_logs import SetupCustomInstanceDbResponse200Logs


T = TypeVar("T", bound="SetupCustomInstanceDbResponse200")


@_attrs_define
class SetupCustomInstanceDbResponse200:
    """
    Attributes:
        logs (SetupCustomInstanceDbResponse200Logs):
        success (bool): Whether the operation completed successfully Example: True.
        error (Union[Unset, None, str]): Error message if the operation failed Example: Connection timeout.
        tag (Union[Unset, SetupCustomInstanceDbResponse200Tag]):
    """

    logs: "SetupCustomInstanceDbResponse200Logs"
    success: bool
    error: Union[Unset, None, str] = UNSET
    tag: Union[Unset, SetupCustomInstanceDbResponse200Tag] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        logs = self.logs.to_dict()

        success = self.success
        error = self.error
        tag: Union[Unset, str] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logs": logs,
                "success": success,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.setup_custom_instance_db_response_200_logs import SetupCustomInstanceDbResponse200Logs

        d = src_dict.copy()
        logs = SetupCustomInstanceDbResponse200Logs.from_dict(d.pop("logs"))

        success = d.pop("success")

        error = d.pop("error", UNSET)

        _tag = d.pop("tag", UNSET)
        tag: Union[Unset, SetupCustomInstanceDbResponse200Tag]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = SetupCustomInstanceDbResponse200Tag(_tag)

        setup_custom_instance_db_response_200 = cls(
            logs=logs,
            success=success,
            error=error,
            tag=tag,
        )

        setup_custom_instance_db_response_200.additional_properties = d
        return setup_custom_instance_db_response_200

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
