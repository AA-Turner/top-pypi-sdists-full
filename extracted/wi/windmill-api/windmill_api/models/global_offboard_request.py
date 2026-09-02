from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.global_offboard_request_reassignments import GlobalOffboardRequestReassignments


T = TypeVar("T", bound="GlobalOffboardRequest")


@_attrs_define
class GlobalOffboardRequest:
    """
    Attributes:
        reassignments (Union[Unset, GlobalOffboardRequestReassignments]): Map of workspace_id to reassignment config
        delete_user (Union[Unset, bool]): Whether to also remove the user from the instance Default: True.
    """

    reassignments: Union[Unset, "GlobalOffboardRequestReassignments"] = UNSET
    delete_user: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reassignments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reassignments, Unset):
            reassignments = self.reassignments.to_dict()

        delete_user = self.delete_user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reassignments is not UNSET:
            field_dict["reassignments"] = reassignments
        if delete_user is not UNSET:
            field_dict["delete_user"] = delete_user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.global_offboard_request_reassignments import GlobalOffboardRequestReassignments

        d = src_dict.copy()
        _reassignments = d.pop("reassignments", UNSET)
        reassignments: Union[Unset, GlobalOffboardRequestReassignments]
        if isinstance(_reassignments, Unset):
            reassignments = UNSET
        else:
            reassignments = GlobalOffboardRequestReassignments.from_dict(_reassignments)

        delete_user = d.pop("delete_user", UNSET)

        global_offboard_request = cls(
            reassignments=reassignments,
            delete_user=delete_user,
        )

        global_offboard_request.additional_properties = d
        return global_offboard_request

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
