from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_users_response_200_item_added_via_source import ListUsersResponse200ItemAddedViaSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListUsersResponse200ItemAddedVia")


@_attrs_define
class ListUsersResponse200ItemAddedVia:
    """
    Attributes:
        source (ListUsersResponse200ItemAddedViaSource): How the user was added to the workspace
        domain (Union[Unset, str]): The domain used for auto-invite (when source is 'domain')
        group (Union[Unset, str]): The instance group name (when source is 'instance_group')
    """

    source: ListUsersResponse200ItemAddedViaSource
    domain: Union[Unset, str] = UNSET
    group: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source.value

        domain = self.domain
        group = self.group

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = ListUsersResponse200ItemAddedViaSource(d.pop("source"))

        domain = d.pop("domain", UNSET)

        group = d.pop("group", UNSET)

        list_users_response_200_item_added_via = cls(
            source=source,
            domain=domain,
            group=group,
        )

        list_users_response_200_item_added_via.additional_properties = d
        return list_users_response_200_item_added_via

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
