from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_price_estimate import NestedPriceEstimate
    from ..models.payment_profile import PaymentProfile
    from ..models.provider_project import ProviderProject
    from ..models.provider_user import ProviderUser


T = TypeVar("T", bound="MarketplaceProviderCustomer")


@_attrs_define
class MarketplaceProviderCustomer:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        slug (Union[Unset, str]):
        abbreviation (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        email (Union[Unset, str]):
        payment_profiles (Union[Unset, list['PaymentProfile']]):
        billing_price_estimate (Union[Unset, NestedPriceEstimate]):
        projects_count (Union[Unset, int]):
        users_count (Union[Unset, int]):
        projects (Union[Unset, list['ProviderProject']]):
        users (Union[Unset, list['ProviderUser']]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    abbreviation: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    payment_profiles: Union[Unset, list["PaymentProfile"]] = UNSET
    billing_price_estimate: Union[Unset, "NestedPriceEstimate"] = UNSET
    projects_count: Union[Unset, int] = UNSET
    users_count: Union[Unset, int] = UNSET
    projects: Union[Unset, list["ProviderProject"]] = UNSET
    users: Union[Unset, list["ProviderUser"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        slug = self.slug

        abbreviation = self.abbreviation

        phone_number = self.phone_number

        email = self.email

        payment_profiles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.payment_profiles, Unset):
            payment_profiles = []
            for payment_profiles_item_data in self.payment_profiles:
                payment_profiles_item = payment_profiles_item_data.to_dict()
                payment_profiles.append(payment_profiles_item)

        billing_price_estimate: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.billing_price_estimate, Unset):
            billing_price_estimate = self.billing_price_estimate.to_dict()

        projects_count = self.projects_count

        users_count = self.users_count

        projects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()
                projects.append(projects_item)

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if email is not UNSET:
            field_dict["email"] = email
        if payment_profiles is not UNSET:
            field_dict["payment_profiles"] = payment_profiles
        if billing_price_estimate is not UNSET:
            field_dict["billing_price_estimate"] = billing_price_estimate
        if projects_count is not UNSET:
            field_dict["projects_count"] = projects_count
        if users_count is not UNSET:
            field_dict["users_count"] = users_count
        if projects is not UNSET:
            field_dict["projects"] = projects
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_price_estimate import NestedPriceEstimate
        from ..models.payment_profile import PaymentProfile
        from ..models.provider_project import ProviderProject
        from ..models.provider_user import ProviderUser

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        abbreviation = d.pop("abbreviation", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        email = d.pop("email", UNSET)

        payment_profiles = []
        _payment_profiles = d.pop("payment_profiles", UNSET)
        for payment_profiles_item_data in _payment_profiles or []:
            payment_profiles_item = PaymentProfile.from_dict(payment_profiles_item_data)

            payment_profiles.append(payment_profiles_item)

        _billing_price_estimate = d.pop("billing_price_estimate", UNSET)
        billing_price_estimate: Union[Unset, NestedPriceEstimate]
        if isinstance(_billing_price_estimate, Unset):
            billing_price_estimate = UNSET
        else:
            billing_price_estimate = NestedPriceEstimate.from_dict(_billing_price_estimate)

        projects_count = d.pop("projects_count", UNSET)

        users_count = d.pop("users_count", UNSET)

        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = ProviderProject.from_dict(projects_item_data)

            projects.append(projects_item)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = ProviderUser.from_dict(users_item_data)

            users.append(users_item)

        marketplace_provider_customer = cls(
            uuid=uuid,
            name=name,
            slug=slug,
            abbreviation=abbreviation,
            phone_number=phone_number,
            email=email,
            payment_profiles=payment_profiles,
            billing_price_estimate=billing_price_estimate,
            projects_count=projects_count,
            users_count=users_count,
            projects=projects,
            users=users,
        )

        marketplace_provider_customer.additional_properties = d
        return marketplace_provider_customer

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
