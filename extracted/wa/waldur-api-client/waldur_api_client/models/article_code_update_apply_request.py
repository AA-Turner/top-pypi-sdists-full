from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offering_state import OfferingState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArticleCodeUpdateApplyRequest")


@_attrs_define
class ArticleCodeUpdateApplyRequest:
    """
    Attributes:
        search (str): Substring to search for in article codes.
        component_uuids (list[UUID]): UUIDs of components to update (from preview results).
        replace (Union[Unset, str]): Replacement string. Default: ''.
        offering_category_uuid (Union[Unset, UUID]): Filter by offering category UUID.
        offering_customer_uuid (Union[Unset, UUID]): Filter by service provider (customer) UUID.
        offering_state (Union[Unset, OfferingState]):
        offering_name (Union[Unset, str]): Filter by offering name (case-insensitive substring match).
    """

    search: str
    component_uuids: list[UUID]
    replace: Union[Unset, str] = ""
    offering_category_uuid: Union[Unset, UUID] = UNSET
    offering_customer_uuid: Union[Unset, UUID] = UNSET
    offering_state: Union[Unset, OfferingState] = UNSET
    offering_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        search = self.search

        component_uuids = []
        for component_uuids_item_data in self.component_uuids:
            component_uuids_item = str(component_uuids_item_data)
            component_uuids.append(component_uuids_item)

        replace = self.replace

        offering_category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_category_uuid, Unset):
            offering_category_uuid = str(self.offering_category_uuid)

        offering_customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_customer_uuid, Unset):
            offering_customer_uuid = str(self.offering_customer_uuid)

        offering_state: Union[Unset, str] = UNSET
        if not isinstance(self.offering_state, Unset):
            offering_state = self.offering_state.value

        offering_name = self.offering_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "search": search,
                "component_uuids": component_uuids,
            }
        )
        if replace is not UNSET:
            field_dict["replace"] = replace
        if offering_category_uuid is not UNSET:
            field_dict["offering_category_uuid"] = offering_category_uuid
        if offering_customer_uuid is not UNSET:
            field_dict["offering_customer_uuid"] = offering_customer_uuid
        if offering_state is not UNSET:
            field_dict["offering_state"] = offering_state
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        search = d.pop("search")

        component_uuids = []
        _component_uuids = d.pop("component_uuids")
        for component_uuids_item_data in _component_uuids:
            component_uuids_item = UUID(component_uuids_item_data)

            component_uuids.append(component_uuids_item)

        replace = d.pop("replace", UNSET)

        _offering_category_uuid = d.pop("offering_category_uuid", UNSET)
        offering_category_uuid: Union[Unset, UUID]
        if isinstance(_offering_category_uuid, Unset):
            offering_category_uuid = UNSET
        else:
            offering_category_uuid = UUID(_offering_category_uuid)

        _offering_customer_uuid = d.pop("offering_customer_uuid", UNSET)
        offering_customer_uuid: Union[Unset, UUID]
        if isinstance(_offering_customer_uuid, Unset):
            offering_customer_uuid = UNSET
        else:
            offering_customer_uuid = UUID(_offering_customer_uuid)

        _offering_state = d.pop("offering_state", UNSET)
        offering_state: Union[Unset, OfferingState]
        if isinstance(_offering_state, Unset):
            offering_state = UNSET
        else:
            offering_state = OfferingState(_offering_state)

        offering_name = d.pop("offering_name", UNSET)

        article_code_update_apply_request = cls(
            search=search,
            component_uuids=component_uuids,
            replace=replace,
            offering_category_uuid=offering_category_uuid,
            offering_customer_uuid=offering_customer_uuid,
            offering_state=offering_state,
            offering_name=offering_name,
        )

        article_code_update_apply_request.additional_properties = d
        return article_code_update_apply_request

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
