from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_custom_instance_dbs_response_200_additional_property_tag import (
    ListCustomInstanceDbsResponse200AdditionalPropertyTag,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_custom_instance_dbs_response_200_additional_property_logs import (
        ListCustomInstanceDbsResponse200AdditionalPropertyLogs,
    )


T = TypeVar("T", bound="ListCustomInstanceDbsResponse200AdditionalProperty")


@_attrs_define
class ListCustomInstanceDbsResponse200AdditionalProperty:
    """
    Attributes:
        logs (ListCustomInstanceDbsResponse200AdditionalPropertyLogs):
        success (bool): Whether the operation completed successfully Example: True.
        error (Union[Unset, None, str]): Error message if the operation failed Example: Connection timeout.
        tag (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyTag]):
    """

    logs: "ListCustomInstanceDbsResponse200AdditionalPropertyLogs"
    success: bool
    error: Union[Unset, None, str] = UNSET
    tag: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyTag] = UNSET
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
        from ..models.list_custom_instance_dbs_response_200_additional_property_logs import (
            ListCustomInstanceDbsResponse200AdditionalPropertyLogs,
        )

        d = src_dict.copy()
        logs = ListCustomInstanceDbsResponse200AdditionalPropertyLogs.from_dict(d.pop("logs"))

        success = d.pop("success")

        error = d.pop("error", UNSET)

        _tag = d.pop("tag", UNSET)
        tag: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyTag]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = ListCustomInstanceDbsResponse200AdditionalPropertyTag(_tag)

        list_custom_instance_dbs_response_200_additional_property = cls(
            logs=logs,
            success=success,
            error=error,
            tag=tag,
        )

        list_custom_instance_dbs_response_200_additional_property.additional_properties = d
        return list_custom_instance_dbs_response_200_additional_property

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
