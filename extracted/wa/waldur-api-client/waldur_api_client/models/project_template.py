from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer import Customer
    from ..models.project_template_role_mapping_data import ProjectTemplateRoleMappingData
    from ..models.provider_offering_details import ProviderOfferingDetails


T = TypeVar("T", bound="ProjectTemplate")


@_attrs_define
class ProjectTemplate:
    """
    Attributes:
        uuid (UUID):
        name (str):
        provider (str):
        provider_data (Customer):
        portal (str):
        customer (str):
        customer_data (Customer):
        offerings (list[str]):
        offerings_data (list['ProviderOfferingDetails']):
        role_mapping_data (ProjectTemplateRoleMappingData): Serialize the role mapping dictionary returned by
            get_role_mapping()
        offering (Union[None, Unset, str]): The offering for which this template applies.
        key (Union[None, Unset, str]): The key that is used to authenticate requests for this class.
        shortname (Union[None, Unset, str]):
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

    uuid: UUID
    name: str
    provider: str
    provider_data: "Customer"
    portal: str
    customer: str
    customer_data: "Customer"
    offerings: list[str]
    offerings_data: list["ProviderOfferingDetails"]
    role_mapping_data: "ProjectTemplateRoleMappingData"
    offering: Union[None, Unset, str] = UNSET
    key: Union[None, Unset, str] = UNSET
    shortname: Union[None, Unset, str] = UNSET
    approval_limit: Union[None, Unset, str] = UNSET
    max_credit_limit: Union[None, Unset, str] = UNSET
    allocation_units_mapping: Union[Unset, Any] = UNSET
    role_mapping: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        provider = self.provider

        provider_data = self.provider_data.to_dict()

        portal = self.portal

        customer = self.customer

        customer_data = self.customer_data.to_dict()

        offerings = self.offerings

        offerings_data = []
        for offerings_data_item_data in self.offerings_data:
            offerings_data_item = offerings_data_item_data.to_dict()
            offerings_data.append(offerings_data_item)

        role_mapping_data = self.role_mapping_data.to_dict()

        offering: Union[None, Unset, str]
        if isinstance(self.offering, Unset):
            offering = UNSET
        else:
            offering = self.offering

        key: Union[None, Unset, str]
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        shortname: Union[None, Unset, str]
        if isinstance(self.shortname, Unset):
            shortname = UNSET
        else:
            shortname = self.shortname

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
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "provider": provider,
                "provider_data": provider_data,
                "portal": portal,
                "customer": customer,
                "customer_data": customer_data,
                "offerings": offerings,
                "offerings_data": offerings_data,
                "role_mapping_data": role_mapping_data,
            }
        )
        if offering is not UNSET:
            field_dict["offering"] = offering
        if key is not UNSET:
            field_dict["key"] = key
        if shortname is not UNSET:
            field_dict["shortname"] = shortname
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
        from ..models.customer import Customer
        from ..models.project_template_role_mapping_data import ProjectTemplateRoleMappingData
        from ..models.provider_offering_details import ProviderOfferingDetails

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        provider = d.pop("provider")

        provider_data = Customer.from_dict(d.pop("provider_data"))

        portal = d.pop("portal")

        customer = d.pop("customer")

        customer_data = Customer.from_dict(d.pop("customer_data"))

        offerings = cast(list[str], d.pop("offerings"))

        offerings_data = []
        _offerings_data = d.pop("offerings_data")
        for offerings_data_item_data in _offerings_data:
            offerings_data_item = ProviderOfferingDetails.from_dict(offerings_data_item_data)

            offerings_data.append(offerings_data_item)

        role_mapping_data = ProjectTemplateRoleMappingData.from_dict(d.pop("role_mapping_data"))

        def _parse_offering(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        offering = _parse_offering(d.pop("offering", UNSET))

        def _parse_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_shortname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        shortname = _parse_shortname(d.pop("shortname", UNSET))

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

        project_template = cls(
            uuid=uuid,
            name=name,
            provider=provider,
            provider_data=provider_data,
            portal=portal,
            customer=customer,
            customer_data=customer_data,
            offerings=offerings,
            offerings_data=offerings_data,
            role_mapping_data=role_mapping_data,
            offering=offering,
            key=key,
            shortname=shortname,
            approval_limit=approval_limit,
            max_credit_limit=max_credit_limit,
            allocation_units_mapping=allocation_units_mapping,
            role_mapping=role_mapping,
        )

        project_template.additional_properties = d
        return project_template

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
