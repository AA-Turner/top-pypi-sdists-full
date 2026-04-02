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


T = TypeVar("T", bound="NestedRequestedOffering")


@_attrs_define
class NestedRequestedOffering:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        state (Union[Unset, RequestedOfferingStates]):
        offering (Union[Unset, str]):
        offering_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        provider_name (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        category_name (Union[Unset, str]):
        call_managing_organisation (Union[Unset, str]):
        attributes (Union[Unset, Any]):
        plan (Union[None, Unset, str]):
        plan_details (Union[Unset, BasePublicPlan]):
        options (Union[Unset, OfferingOptions]):
        components (Union[Unset, list['OfferingComponent']]):
        created (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, UUID] = UNSET
    state: Union[Unset, RequestedOfferingStates] = UNSET
    offering: Union[Unset, str] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    provider_name: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, UUID] = UNSET
    category_name: Union[Unset, str] = UNSET
    call_managing_organisation: Union[Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    plan: Union[None, Unset, str] = UNSET
    plan_details: Union[Unset, "BasePublicPlan"] = UNSET
    options: Union[Unset, "OfferingOptions"] = UNSET
    components: Union[Unset, list["OfferingComponent"]] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        offering = self.offering

        offering_name = self.offering_name

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        provider_name = self.provider_name

        category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.category_uuid, Unset):
            category_uuid = str(self.category_uuid)

        category_name = self.category_name

        call_managing_organisation = self.call_managing_organisation

        attributes = self.attributes

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        else:
            plan = self.plan

        plan_details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan_details, Unset):
            plan_details = self.plan_details.to_dict()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if state is not UNSET:
            field_dict["state"] = state
        if offering is not UNSET:
            field_dict["offering"] = offering
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if provider_name is not UNSET:
            field_dict["provider_name"] = provider_name
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if category_name is not UNSET:
            field_dict["category_name"] = category_name
        if call_managing_organisation is not UNSET:
            field_dict["call_managing_organisation"] = call_managing_organisation
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if plan is not UNSET:
            field_dict["plan"] = plan
        if plan_details is not UNSET:
            field_dict["plan_details"] = plan_details
        if options is not UNSET:
            field_dict["options"] = options
        if components is not UNSET:
            field_dict["components"] = components
        if created is not UNSET:
            field_dict["created"] = created

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_public_plan import BasePublicPlan
        from ..models.offering_component import OfferingComponent
        from ..models.offering_options import OfferingOptions

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _state = d.pop("state", UNSET)
        state: Union[Unset, RequestedOfferingStates]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = RequestedOfferingStates(_state)

        offering = d.pop("offering", UNSET)

        offering_name = d.pop("offering_name", UNSET)

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        provider_name = d.pop("provider_name", UNSET)

        _category_uuid = d.pop("category_uuid", UNSET)
        category_uuid: Union[Unset, UUID]
        if isinstance(_category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = UUID(_category_uuid)

        category_name = d.pop("category_name", UNSET)

        call_managing_organisation = d.pop("call_managing_organisation", UNSET)

        attributes = d.pop("attributes", UNSET)

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _plan_details = d.pop("plan_details", UNSET)
        plan_details: Union[Unset, BasePublicPlan]
        if isinstance(_plan_details, Unset):
            plan_details = UNSET
        else:
            plan_details = BasePublicPlan.from_dict(_plan_details)

        _options = d.pop("options", UNSET)
        options: Union[Unset, OfferingOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = OfferingOptions.from_dict(_options)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = OfferingComponent.from_dict(components_item_data)

            components.append(components_item)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        nested_requested_offering = cls(
            uuid=uuid,
            state=state,
            offering=offering,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            provider_name=provider_name,
            category_uuid=category_uuid,
            category_name=category_name,
            call_managing_organisation=call_managing_organisation,
            attributes=attributes,
            plan=plan,
            plan_details=plan_details,
            options=options,
            components=components,
            created=created,
        )

        nested_requested_offering.additional_properties = d
        return nested_requested_offering

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
