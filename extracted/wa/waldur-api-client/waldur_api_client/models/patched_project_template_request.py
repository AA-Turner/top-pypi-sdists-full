from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProjectTemplateRequest")


@_attrs_define
class PatchedProjectTemplateRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        offering (Union[None, Unset, str]): The offering for which this template applies.
        provider (Union[Unset, str]):
        portal (Union[Unset, str]):
        key (Union[None, Unset, str]): The key that is used to authenticate requests for this class.
        customer (Union[Unset, str]):
        shortname (Union[None, Unset, str]):
        offerings (Union[Unset, list[str]]):
        approval_limit (Union[None, Unset, str]): The credit limit beyond which requests need to be approved by a local
            admin. If this is None, then no local approval is required. If this is set to 0, then all requests (including
            creating the project) need to be approved.
        max_credit_limit (Union[None, Unset, str]): The maximum credit limit for any projects created in this class. Any
            requests beyond this limit are automatically rejected. If this is None, then no maximum limit is set. If this is
            set to 0, then no projects can be created in this class.
        allocation_units_mapping (Union[Unset, Any]): The mapping of credits to allocation units, i.e. how many
            allocation units to award per credit allocated.
        role_mapping (Union[Unset, Any]): The mapping of role names from the remote portal to role information in this
            portal for users in projects created in this class.
    """

    name: Union[Unset, str] = UNSET
    offering: Union[None, Unset, str] = UNSET
    provider: Union[Unset, str] = UNSET
    portal: Union[Unset, str] = UNSET
    key: Union[None, Unset, str] = UNSET
    customer: Union[Unset, str] = UNSET
    shortname: Union[None, Unset, str] = UNSET
    offerings: Union[Unset, list[str]] = UNSET
    approval_limit: Union[None, Unset, str] = UNSET
    max_credit_limit: Union[None, Unset, str] = UNSET
    allocation_units_mapping: Union[Unset, Any] = UNSET
    role_mapping: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        offering: Union[None, Unset, str]
        if isinstance(self.offering, Unset):
            offering = UNSET
        else:
            offering = self.offering

        provider = self.provider

        portal = self.portal

        key: Union[None, Unset, str]
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        customer = self.customer

        shortname: Union[None, Unset, str]
        if isinstance(self.shortname, Unset):
            shortname = UNSET
        else:
            shortname = self.shortname

        offerings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = self.offerings

        approval_limit: Union[None, Unset, str]
        if isinstance(self.approval_limit, Unset):
            approval_limit = UNSET
        else:
            approval_limit = self.approval_limit

        max_credit_limit: Union[None, Unset, str]
        if isinstance(self.max_credit_limit, Unset):
            max_credit_limit = UNSET
        else:
            max_credit_limit = self.max_credit_limit

        allocation_units_mapping = self.allocation_units_mapping

        role_mapping = self.role_mapping

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if offering is not UNSET:
            field_dict["offering"] = offering
        if provider is not UNSET:
            field_dict["provider"] = provider
        if portal is not UNSET:
            field_dict["portal"] = portal
        if key is not UNSET:
            field_dict["key"] = key
        if customer is not UNSET:
            field_dict["customer"] = customer
        if shortname is not UNSET:
            field_dict["shortname"] = shortname
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if approval_limit is not UNSET:
            field_dict["approval_limit"] = approval_limit
        if max_credit_limit is not UNSET:
            field_dict["max_credit_limit"] = max_credit_limit
        if allocation_units_mapping is not UNSET:
            field_dict["allocation_units_mapping"] = allocation_units_mapping
        if role_mapping is not UNSET:
            field_dict["role_mapping"] = role_mapping

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        def _parse_offering(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        offering = _parse_offering(d.pop("offering", UNSET))

        provider = d.pop("provider", UNSET)

        portal = d.pop("portal", UNSET)

        def _parse_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        key = _parse_key(d.pop("key", UNSET))

        customer = d.pop("customer", UNSET)

        def _parse_shortname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        shortname = _parse_shortname(d.pop("shortname", UNSET))

        offerings = cast(list[str], d.pop("offerings", UNSET))

        def _parse_approval_limit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        approval_limit = _parse_approval_limit(d.pop("approval_limit", UNSET))

        def _parse_max_credit_limit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_credit_limit = _parse_max_credit_limit(d.pop("max_credit_limit", UNSET))

        allocation_units_mapping = d.pop("allocation_units_mapping", UNSET)

        role_mapping = d.pop("role_mapping", UNSET)

        patched_project_template_request = cls(
            name=name,
            offering=offering,
            provider=provider,
            portal=portal,
            key=key,
            customer=customer,
            shortname=shortname,
            offerings=offerings,
            approval_limit=approval_limit,
            max_credit_limit=max_credit_limit,
            allocation_units_mapping=allocation_units_mapping,
            role_mapping=role_mapping,
        )

        patched_project_template_request.additional_properties = d
        return patched_project_template_request

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
