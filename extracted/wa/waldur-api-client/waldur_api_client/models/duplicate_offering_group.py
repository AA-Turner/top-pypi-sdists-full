from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.duplicate_offering_candidate import DuplicateOfferingCandidate


T = TypeVar("T", bound="DuplicateOfferingGroup")


@_attrs_define
class DuplicateOfferingGroup:
    """
    Attributes:
        tenant_id (int):
        tenant_uuid (Union[None, UUID]):
        tenant_name (Union[None, str]):
        customer_name (Union[None, str]):
        customer_uuid (Union[None, UUID]):
        offering_type (str):
        recommended_keeper_id (int):
        orphan_count (int):
        candidates (list['DuplicateOfferingCandidate']):
    """

    tenant_id: int
    tenant_uuid: Union[None, UUID]
    tenant_name: Union[None, str]
    customer_name: Union[None, str]
    customer_uuid: Union[None, UUID]
    offering_type: str
    recommended_keeper_id: int
    orphan_count: int
    candidates: list["DuplicateOfferingCandidate"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        tenant_uuid: Union[None, str]
        if isinstance(self.tenant_uuid, UUID):
            tenant_uuid = str(self.tenant_uuid)
        else:
            tenant_uuid = self.tenant_uuid

        tenant_name: Union[None, str]
        tenant_name = self.tenant_name

        customer_name: Union[None, str]
        customer_name = self.customer_name

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        offering_type = self.offering_type

        recommended_keeper_id = self.recommended_keeper_id

        orphan_count = self.orphan_count

        candidates = []
        for candidates_item_data in self.candidates:
            candidates_item = candidates_item_data.to_dict()
            candidates.append(candidates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant_id": tenant_id,
                "tenant_uuid": tenant_uuid,
                "tenant_name": tenant_name,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "offering_type": offering_type,
                "recommended_keeper_id": recommended_keeper_id,
                "orphan_count": orphan_count,
                "candidates": candidates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.duplicate_offering_candidate import DuplicateOfferingCandidate

        d = dict(src_dict)
        tenant_id = d.pop("tenant_id")

        def _parse_tenant_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                tenant_uuid_type_0 = UUID(data)

                return tenant_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        tenant_uuid = _parse_tenant_uuid(d.pop("tenant_uuid"))

        def _parse_tenant_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tenant_name = _parse_tenant_name(d.pop("tenant_name"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        offering_type = d.pop("offering_type")

        recommended_keeper_id = d.pop("recommended_keeper_id")

        orphan_count = d.pop("orphan_count")

        candidates = []
        _candidates = d.pop("candidates")
        for candidates_item_data in _candidates:
            candidates_item = DuplicateOfferingCandidate.from_dict(candidates_item_data)

            candidates.append(candidates_item)

        duplicate_offering_group = cls(
            tenant_id=tenant_id,
            tenant_uuid=tenant_uuid,
            tenant_name=tenant_name,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            offering_type=offering_type,
            recommended_keeper_id=recommended_keeper_id,
            orphan_count=orphan_count,
            candidates=candidates,
        )

        duplicate_offering_group.additional_properties = d
        return duplicate_offering_group

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
