from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.acl_change_request_change_type_2_scope import AclChangeRequestChangeType2Scope
from ..models.acl_change_request_change_type_2_type import AclChangeRequestChangeType2Type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.acl_change_request_change_type_2_objects_item import AclChangeRequestChangeType2ObjectsItem


T = TypeVar("T", bound="AclChangeRequestChangeType2")


@_attrs_define
class AclChangeRequestChangeType2:
    """
    Attributes:
        type (AclChangeRequestChangeType2Type):
        role (str): a data table role of the instance, other than admin
        privileges (List[str]):
        scope (AclChangeRequestChangeType2Scope):
        objects (Union[Unset, List['AclChangeRequestChangeType2ObjectsItem']]): objects inside the target the revoke
            covers, empty for the target itself. Only with the target scope; a revoke on all objects of a kind is refused,
            since it cannot say which grants it takes back.
    """

    type: AclChangeRequestChangeType2Type
    role: str
    privileges: List[str]
    scope: AclChangeRequestChangeType2Scope
    objects: Union[Unset, List["AclChangeRequestChangeType2ObjectsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        role = self.role
        privileges = self.privileges

        scope = self.scope.value

        objects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.objects, Unset):
            objects = []
            for objects_item_data in self.objects:
                objects_item = objects_item_data.to_dict()

                objects.append(objects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "role": role,
                "privileges": privileges,
                "scope": scope,
            }
        )
        if objects is not UNSET:
            field_dict["objects"] = objects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.acl_change_request_change_type_2_objects_item import AclChangeRequestChangeType2ObjectsItem

        d = src_dict.copy()
        type = AclChangeRequestChangeType2Type(d.pop("type"))

        role = d.pop("role")

        privileges = cast(List[str], d.pop("privileges"))

        scope = AclChangeRequestChangeType2Scope(d.pop("scope"))

        objects = []
        _objects = d.pop("objects", UNSET)
        for objects_item_data in _objects or []:
            objects_item = AclChangeRequestChangeType2ObjectsItem.from_dict(objects_item_data)

            objects.append(objects_item)

        acl_change_request_change_type_2 = cls(
            type=type,
            role=role,
            privileges=privileges,
            scope=scope,
            objects=objects,
        )

        acl_change_request_change_type_2.additional_properties = d
        return acl_change_request_change_type_2

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
