import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.call_states import CallStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_document import CallDocument
    from ..models.call_resource_template import CallResourceTemplate
    from ..models.nested_requested_offering import NestedRequestedOffering
    from ..models.nested_round import NestedRound


T = TypeVar("T", bound="PublicCall")


@_attrs_define
class PublicCall:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        state (Union[Unset, CallStates]):
        manager (Union[Unset, str]):
        manager_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        offerings (Union[Unset, list['NestedRequestedOffering']]):
        rounds (Union[Unset, list['NestedRound']]):
        documents (Union[Unset, list['CallDocument']]):
        resource_templates (Union[Unset, list['CallResourceTemplate']]):
        fixed_duration_in_days (Union[None, Unset, int]): Fixed duration in days that applies to all proposals in this
            call
        backend_id (Union[Unset, str]):
        external_url (Union[None, Unset, str]):
        reviewer_identity_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see reviewer
            identities. If False, reviewers appear as 'Reviewer 1', 'Reviewer 2', etc.
        reviews_visible_to_submitters (Union[Unset, bool]): Whether proposal applicants can see review comments and
            scores. If False, applicants only see final approval/rejection status.
        has_eligibility_restrictions (Union[Unset, bool]): Check if call has any eligibility restrictions configured.
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    slug: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, CallStates] = UNSET
    manager: Union[Unset, str] = UNSET
    manager_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    offerings: Union[Unset, list["NestedRequestedOffering"]] = UNSET
    rounds: Union[Unset, list["NestedRound"]] = UNSET
    documents: Union[Unset, list["CallDocument"]] = UNSET
    resource_templates: Union[Unset, list["CallResourceTemplate"]] = UNSET
    fixed_duration_in_days: Union[None, Unset, int] = UNSET
    backend_id: Union[Unset, str] = UNSET
    external_url: Union[None, Unset, str] = UNSET
    reviewer_identity_visible_to_submitters: Union[Unset, bool] = UNSET
    reviews_visible_to_submitters: Union[Unset, bool] = UNSET
    has_eligibility_restrictions: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        slug = self.slug

        name = self.name

        description = self.description

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        manager = self.manager

        manager_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.manager_uuid, Unset):
            manager_uuid = str(self.manager_uuid)

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        offerings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = offerings_item_data.to_dict()
                offerings.append(offerings_item)

        rounds: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rounds, Unset):
            rounds = []
            for rounds_item_data in self.rounds:
                rounds_item = rounds_item_data.to_dict()
                rounds.append(rounds_item)

        documents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()
                documents.append(documents_item)

        resource_templates: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.resource_templates, Unset):
            resource_templates = []
            for resource_templates_item_data in self.resource_templates:
                resource_templates_item = resource_templates_item_data.to_dict()
                resource_templates.append(resource_templates_item)

        fixed_duration_in_days: Union[None, Unset, int]
        if isinstance(self.fixed_duration_in_days, Unset):
            fixed_duration_in_days = UNSET
        else:
            fixed_duration_in_days = self.fixed_duration_in_days

        backend_id = self.backend_id

        external_url: Union[None, Unset, str]
        if isinstance(self.external_url, Unset):
            external_url = UNSET
        else:
            external_url = self.external_url

        reviewer_identity_visible_to_submitters = self.reviewer_identity_visible_to_submitters

        reviews_visible_to_submitters = self.reviews_visible_to_submitters

        has_eligibility_restrictions = self.has_eligibility_restrictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if slug is not UNSET:
            field_dict["slug"] = slug
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if manager is not UNSET:
            field_dict["manager"] = manager
        if manager_uuid is not UNSET:
            field_dict["manager_uuid"] = manager_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if rounds is not UNSET:
            field_dict["rounds"] = rounds
        if documents is not UNSET:
            field_dict["documents"] = documents
        if resource_templates is not UNSET:
            field_dict["resource_templates"] = resource_templates
        if fixed_duration_in_days is not UNSET:
            field_dict["fixed_duration_in_days"] = fixed_duration_in_days
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if external_url is not UNSET:
            field_dict["external_url"] = external_url
        if reviewer_identity_visible_to_submitters is not UNSET:
            field_dict["reviewer_identity_visible_to_submitters"] = reviewer_identity_visible_to_submitters
        if reviews_visible_to_submitters is not UNSET:
            field_dict["reviews_visible_to_submitters"] = reviews_visible_to_submitters
        if has_eligibility_restrictions is not UNSET:
            field_dict["has_eligibility_restrictions"] = has_eligibility_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_document import CallDocument
        from ..models.call_resource_template import CallResourceTemplate
        from ..models.nested_requested_offering import NestedRequestedOffering
        from ..models.nested_round import NestedRound

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        slug = d.pop("slug", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, CallStates]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = CallStates(_state)

        manager = d.pop("manager", UNSET)

        _manager_uuid = d.pop("manager_uuid", UNSET)
        manager_uuid: Union[Unset, UUID]
        if isinstance(_manager_uuid, Unset):
            manager_uuid = UNSET
        else:
            manager_uuid = UUID(_manager_uuid)

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = NestedRequestedOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        rounds = []
        _rounds = d.pop("rounds", UNSET)
        for rounds_item_data in _rounds or []:
            rounds_item = NestedRound.from_dict(rounds_item_data)

            rounds.append(rounds_item)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = CallDocument.from_dict(documents_item_data)

            documents.append(documents_item)

        resource_templates = []
        _resource_templates = d.pop("resource_templates", UNSET)
        for resource_templates_item_data in _resource_templates or []:
            resource_templates_item = CallResourceTemplate.from_dict(resource_templates_item_data)

            resource_templates.append(resource_templates_item)

        def _parse_fixed_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        fixed_duration_in_days = _parse_fixed_duration_in_days(d.pop("fixed_duration_in_days", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        def _parse_external_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_url = _parse_external_url(d.pop("external_url", UNSET))

        reviewer_identity_visible_to_submitters = d.pop("reviewer_identity_visible_to_submitters", UNSET)

        reviews_visible_to_submitters = d.pop("reviews_visible_to_submitters", UNSET)

        has_eligibility_restrictions = d.pop("has_eligibility_restrictions", UNSET)

        public_call = cls(
            url=url,
            uuid=uuid,
            created=created,
            start_date=start_date,
            end_date=end_date,
            slug=slug,
            name=name,
            description=description,
            state=state,
            manager=manager,
            manager_uuid=manager_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            offerings=offerings,
            rounds=rounds,
            documents=documents,
            resource_templates=resource_templates,
            fixed_duration_in_days=fixed_duration_in_days,
            backend_id=backend_id,
            external_url=external_url,
            reviewer_identity_visible_to_submitters=reviewer_identity_visible_to_submitters,
            reviews_visible_to_submitters=reviews_visible_to_submitters,
            has_eligibility_restrictions=has_eligibility_restrictions,
        )

        public_call.additional_properties = d
        return public_call

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
