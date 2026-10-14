import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.invoice_policy_enum import InvoicePolicyEnum
from ..models.offering_merge_state_enum import OfferingMergeStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_merge_attribute_key_mapping import OfferingMergeAttributeKeyMapping
    from ..models.offering_merge_component_mapping import OfferingMergeComponentMapping
    from ..models.offering_merge_offering import OfferingMergeOffering
    from ..models.offering_merge_plan_mapping import OfferingMergePlanMapping
    from ..models.offering_merge_preview import OfferingMergePreview
    from ..models.offering_merge_progress import OfferingMergeProgress
    from ..models.offering_merge_verification import OfferingMergeVerification


T = TypeVar("T", bound="OfferingMerge")


@_attrs_define
class OfferingMerge:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        state (OfferingMergeStateEnum):
        sources (list[UUID]): Offerings whose resources and history move to the target.
        target (UUID):
        source_offerings (list['OfferingMergeOffering']):
        target_offering (OfferingMergeOffering):
        created_by (Union[None, UUID]):
        created_by_full_name (Union[None, str]):
        preview (Union['OfferingMergePreview', None]):
        verification (Union['OfferingMergeVerification', None]):
        progress (Union['OfferingMergeProgress', None]):
        error_message (str):
        plan_mapping (Union[Unset, OfferingMergePlanMapping]): Source plan UUID to target plan UUID.
        component_mapping (Union[Unset, OfferingMergeComponentMapping]): Per source offering UUID: source component type
            to target component type.
        attribute_key_mapping (Union[Unset, OfferingMergeAttributeKeyMapping]): Order and resource answer key renames:
            old key to new key.
        invoice_policy (Union[Unset, InvoicePolicyEnum]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    state: OfferingMergeStateEnum
    sources: list[UUID]
    target: UUID
    source_offerings: list["OfferingMergeOffering"]
    target_offering: "OfferingMergeOffering"
    created_by: Union[None, UUID]
    created_by_full_name: Union[None, str]
    preview: Union["OfferingMergePreview", None]
    verification: Union["OfferingMergeVerification", None]
    progress: Union["OfferingMergeProgress", None]
    error_message: str
    plan_mapping: Union[Unset, "OfferingMergePlanMapping"] = UNSET
    component_mapping: Union[Unset, "OfferingMergeComponentMapping"] = UNSET
    attribute_key_mapping: Union[Unset, "OfferingMergeAttributeKeyMapping"] = UNSET
    invoice_policy: Union[Unset, InvoicePolicyEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.offering_merge_preview import OfferingMergePreview
        from ..models.offering_merge_progress import OfferingMergeProgress
        from ..models.offering_merge_verification import OfferingMergeVerification

        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        state = self.state.value

        sources = []
        for sources_item_data in self.sources:
            sources_item = str(sources_item_data)
            sources.append(sources_item)

        target = str(self.target)

        source_offerings = []
        for source_offerings_item_data in self.source_offerings:
            source_offerings_item = source_offerings_item_data.to_dict()
            source_offerings.append(source_offerings_item)

        target_offering = self.target_offering.to_dict()

        created_by: Union[None, str]
        if isinstance(self.created_by, UUID):
            created_by = str(self.created_by)
        else:
            created_by = self.created_by

        created_by_full_name: Union[None, str]
        created_by_full_name = self.created_by_full_name

        preview: Union[None, dict[str, Any]]
        if isinstance(self.preview, OfferingMergePreview):
            preview = self.preview.to_dict()
        else:
            preview = self.preview

        verification: Union[None, dict[str, Any]]
        if isinstance(self.verification, OfferingMergeVerification):
            verification = self.verification.to_dict()
        else:
            verification = self.verification

        progress: Union[None, dict[str, Any]]
        if isinstance(self.progress, OfferingMergeProgress):
            progress = self.progress.to_dict()
        else:
            progress = self.progress

        error_message = self.error_message

        plan_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan_mapping, Unset):
            plan_mapping = self.plan_mapping.to_dict()

        component_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.component_mapping, Unset):
            component_mapping = self.component_mapping.to_dict()

        attribute_key_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attribute_key_mapping, Unset):
            attribute_key_mapping = self.attribute_key_mapping.to_dict()

        invoice_policy: Union[Unset, str] = UNSET
        if not isinstance(self.invoice_policy, Unset):
            invoice_policy = self.invoice_policy.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "state": state,
                "sources": sources,
                "target": target,
                "source_offerings": source_offerings,
                "target_offering": target_offering,
                "created_by": created_by,
                "created_by_full_name": created_by_full_name,
                "preview": preview,
                "verification": verification,
                "progress": progress,
                "error_message": error_message,
            }
        )
        if plan_mapping is not UNSET:
            field_dict["plan_mapping"] = plan_mapping
        if component_mapping is not UNSET:
            field_dict["component_mapping"] = component_mapping
        if attribute_key_mapping is not UNSET:
            field_dict["attribute_key_mapping"] = attribute_key_mapping
        if invoice_policy is not UNSET:
            field_dict["invoice_policy"] = invoice_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_attribute_key_mapping import OfferingMergeAttributeKeyMapping
        from ..models.offering_merge_component_mapping import OfferingMergeComponentMapping
        from ..models.offering_merge_offering import OfferingMergeOffering
        from ..models.offering_merge_plan_mapping import OfferingMergePlanMapping
        from ..models.offering_merge_preview import OfferingMergePreview
        from ..models.offering_merge_progress import OfferingMergeProgress
        from ..models.offering_merge_verification import OfferingMergeVerification

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        state = OfferingMergeStateEnum(d.pop("state"))

        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = UUID(sources_item_data)

            sources.append(sources_item)

        target = UUID(d.pop("target"))

        source_offerings = []
        _source_offerings = d.pop("source_offerings")
        for source_offerings_item_data in _source_offerings:
            source_offerings_item = OfferingMergeOffering.from_dict(source_offerings_item_data)

            source_offerings.append(source_offerings_item)

        target_offering = OfferingMergeOffering.from_dict(d.pop("target_offering"))

        def _parse_created_by(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_type_0 = UUID(data)

                return created_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        created_by = _parse_created_by(d.pop("created_by"))

        def _parse_created_by_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by_full_name = _parse_created_by_full_name(d.pop("created_by_full_name"))

        def _parse_preview(data: object) -> Union["OfferingMergePreview", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preview_type_1 = OfferingMergePreview.from_dict(data)

                return preview_type_1
            except:  # noqa: E722
                pass
            return cast(Union["OfferingMergePreview", None], data)

        preview = _parse_preview(d.pop("preview"))

        def _parse_verification(data: object) -> Union["OfferingMergeVerification", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1 = OfferingMergeVerification.from_dict(data)

                return verification_type_1
            except:  # noqa: E722
                pass
            return cast(Union["OfferingMergeVerification", None], data)

        verification = _parse_verification(d.pop("verification"))

        def _parse_progress(data: object) -> Union["OfferingMergeProgress", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                progress_type_1 = OfferingMergeProgress.from_dict(data)

                return progress_type_1
            except:  # noqa: E722
                pass
            return cast(Union["OfferingMergeProgress", None], data)

        progress = _parse_progress(d.pop("progress"))

        error_message = d.pop("error_message")

        _plan_mapping = d.pop("plan_mapping", UNSET)
        plan_mapping: Union[Unset, OfferingMergePlanMapping]
        if isinstance(_plan_mapping, Unset):
            plan_mapping = UNSET
        else:
            plan_mapping = OfferingMergePlanMapping.from_dict(_plan_mapping)

        _component_mapping = d.pop("component_mapping", UNSET)
        component_mapping: Union[Unset, OfferingMergeComponentMapping]
        if isinstance(_component_mapping, Unset):
            component_mapping = UNSET
        else:
            component_mapping = OfferingMergeComponentMapping.from_dict(_component_mapping)

        _attribute_key_mapping = d.pop("attribute_key_mapping", UNSET)
        attribute_key_mapping: Union[Unset, OfferingMergeAttributeKeyMapping]
        if isinstance(_attribute_key_mapping, Unset):
            attribute_key_mapping = UNSET
        else:
            attribute_key_mapping = OfferingMergeAttributeKeyMapping.from_dict(_attribute_key_mapping)

        _invoice_policy = d.pop("invoice_policy", UNSET)
        invoice_policy: Union[Unset, InvoicePolicyEnum]
        if isinstance(_invoice_policy, Unset):
            invoice_policy = UNSET
        else:
            invoice_policy = InvoicePolicyEnum(_invoice_policy)

        offering_merge = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            state=state,
            sources=sources,
            target=target,
            source_offerings=source_offerings,
            target_offering=target_offering,
            created_by=created_by,
            created_by_full_name=created_by_full_name,
            preview=preview,
            verification=verification,
            progress=progress,
            error_message=error_message,
            plan_mapping=plan_mapping,
            component_mapping=component_mapping,
            attribute_key_mapping=attribute_key_mapping,
            invoice_policy=invoice_policy,
        )

        offering_merge.additional_properties = d
        return offering_merge

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
