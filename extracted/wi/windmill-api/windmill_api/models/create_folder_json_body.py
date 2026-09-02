from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_folder_json_body_default_permissioned_as_item import (
        CreateFolderJsonBodyDefaultPermissionedAsItem,
    )


T = TypeVar("T", bound="CreateFolderJsonBody")


@_attrs_define
class CreateFolderJsonBody:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        owners (Union[Unset, List[str]]):
        extra_perms (Union[Unset, Any]):
        default_permissioned_as (Union[Unset, List['CreateFolderJsonBodyDefaultPermissionedAsItem']]): Ordered list of
            rules applied at create-time when admins or `wm_deployers` members deploy items in this folder. The first rule
            whose `path_glob` matches the item path (relative to the folder root) wins, and its `permissioned_as` is used as
            the default.
        labels (Union[Unset, List[str]]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    owners: Union[Unset, List[str]] = UNSET
    extra_perms: Union[Unset, Any] = UNSET
    default_permissioned_as: Union[Unset, List["CreateFolderJsonBodyDefaultPermissionedAsItem"]] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        summary = self.summary
        owners: Union[Unset, List[str]] = UNSET
        if not isinstance(self.owners, Unset):
            owners = self.owners

        extra_perms = self.extra_perms
        default_permissioned_as: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.default_permissioned_as, Unset):
            default_permissioned_as = []
            for default_permissioned_as_item_data in self.default_permissioned_as:
                default_permissioned_as_item = default_permissioned_as_item_data.to_dict()

                default_permissioned_as.append(default_permissioned_as_item)

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if owners is not UNSET:
            field_dict["owners"] = owners
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms
        if default_permissioned_as is not UNSET:
            field_dict["default_permissioned_as"] = default_permissioned_as
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_folder_json_body_default_permissioned_as_item import (
            CreateFolderJsonBodyDefaultPermissionedAsItem,
        )

        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        owners = cast(List[str], d.pop("owners", UNSET))

        extra_perms = d.pop("extra_perms", UNSET)

        default_permissioned_as = []
        _default_permissioned_as = d.pop("default_permissioned_as", UNSET)
        for default_permissioned_as_item_data in _default_permissioned_as or []:
            default_permissioned_as_item = CreateFolderJsonBodyDefaultPermissionedAsItem.from_dict(
                default_permissioned_as_item_data
            )

            default_permissioned_as.append(default_permissioned_as_item)

        labels = cast(List[str], d.pop("labels", UNSET))

        create_folder_json_body = cls(
            name=name,
            summary=summary,
            owners=owners,
            extra_perms=extra_perms,
            default_permissioned_as=default_permissioned_as,
            labels=labels,
        )

        create_folder_json_body.additional_properties = d
        return create_folder_json_body

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
