import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.requested_offering_states import RequestedOfferingStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_public_plan import BasePublicPlan
    from ..models.offering_component import OfferingComponent
    from ..models.offering_options import OfferingOptions


T = TypeVar("T", bound="ProviderRequestedOffering")


@_attrs_define
class ProviderRequestedOffering:
    """
    Attributes:
        uuid (UUID):
        state (RequestedOfferingStates):
        offering (str):
        offering_name (str):
        offering_uuid (UUID):
        provider_name (str):
        category_uuid (UUID):
        category_name (str):
        call_managing_organisation (str):
        plan (Union[None, str]):
        plan_details (BasePublicPlan):
        options (OfferingOptions):
        components (list['OfferingComponent']):
        created (datetime.datetime):
        url (str):
        call_name (str):
        call (str):
        description (str):
        created_by_name (str):
        created_by_email (str):
        attributes (Union[Unset, Any]):
    """

    uuid: UUID
    state: RequestedOfferingStates
    offering: str
    offering_name: str
    offering_uuid: UUID
    provider_name: str
    category_uuid: UUID
    category_name: str
    call_managing_organisation: str
    plan: Union[None, str]
    plan_details: "BasePublicPlan"
    options: "OfferingOptions"
    components: list["OfferingComponent"]
    created: datetime.datetime
    url: str
    call_name: str
    call: str
    description: str
    created_by_name: str
    created_by_email: str
    attributes: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        state = self.state.value

        offering = self.offering

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        provider_name = self.provider_name

        category_uuid = str(self.category_uuid)

        category_name = self.category_name

        call_managing_organisation = self.call_managing_organisation

        plan: Union[None, str]
        plan = self.plan

        plan_details = self.plan_details.to_dict()

        options = self.options.to_dict()

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        created = self.created.isoformat()

        url = self.url

        call_name = self.call_name

        call = self.call

        description = self.description

        created_by_name = self.created_by_name

        created_by_email = self.created_by_email

        attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "state": state,
                "offering": offering,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "provider_name": provider_name,
                "category_uuid": category_uuid,
                "category_name": category_name,
                "call_managing_organisation": call_managing_organisation,
                "plan": plan,
                "plan_details": plan_details,
                "options": options,
                "components": components,
                "created": created,
                "url": url,
                "call_name": call_name,
                "call": call,
                "description": description,
                "created_by_name": created_by_name,
                "created_by_email": created_by_email,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_public_plan import BasePublicPlan
        from ..models.offering_component import OfferingComponent
        from ..models.offering_options import OfferingOptions

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        state = RequestedOfferingStates(d.pop("state"))

        offering = d.pop("offering")

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        provider_name = d.pop("provider_name")

        category_uuid = UUID(d.pop("category_uuid"))

        category_name = d.pop("category_name")

        call_managing_organisation = d.pop("call_managing_organisation")

        def _parse_plan(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        plan = _parse_plan(d.pop("plan"))

        plan_details = BasePublicPlan.from_dict(d.pop("plan_details"))

        options = OfferingOptions.from_dict(d.pop("options"))

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = OfferingComponent.from_dict(components_item_data)

            components.append(components_item)

        created = isoparse(d.pop("created"))

        url = d.pop("url")

        call_name = d.pop("call_name")

        call = d.pop("call")

        description = d.pop("description")

        created_by_name = d.pop("created_by_name")

        created_by_email = d.pop("created_by_email")

        attributes = d.pop("attributes", UNSET)

        provider_requested_offering = cls(
            uuid=uuid,
            state=state,
            offering=offering,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            provider_name=provider_name,
            category_uuid=category_uuid,
            category_name=category_name,
            call_managing_organisation=call_managing_organisation,
            plan=plan,
            plan_details=plan_details,
            options=options,
            components=components,
            created=created,
            url=url,
            call_name=call_name,
            call=call,
            description=description,
            created_by_name=created_by_name,
            created_by_email=created_by_email,
            attributes=attributes,
        )

        provider_requested_offering.additional_properties = d
        return provider_requested_offering

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
