from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AffinityMatrixEntry")


@_attrs_define
class AffinityMatrixEntry:
    """
    Attributes:
        uuid (UUID):
        reviewer_uuid (UUID):
        reviewer_name (str):
        proposal_uuid (UUID):
        proposal_name (str):
        affinity_score (float):
        keyword_score (Union[None, float]):
        text_score (Union[None, float]):
        has_conflict (bool):
        coi_type (Union[None, str]):
        coi_severity (Union[None, str]):
        coi_status (Union[None, str]):
        source (str):
    """

    uuid: UUID
    reviewer_uuid: UUID
    reviewer_name: str
    proposal_uuid: UUID
    proposal_name: str
    affinity_score: float
    keyword_score: Union[None, float]
    text_score: Union[None, float]
    has_conflict: bool
    coi_type: Union[None, str]
    coi_severity: Union[None, str]
    coi_status: Union[None, str]
    source: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        affinity_score = self.affinity_score

        keyword_score: Union[None, float]
        keyword_score = self.keyword_score

        text_score: Union[None, float]
        text_score = self.text_score

        has_conflict = self.has_conflict

        coi_type: Union[None, str]
        coi_type = self.coi_type

        coi_severity: Union[None, str]
        coi_severity = self.coi_severity

        coi_status: Union[None, str]
        coi_status = self.coi_status

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "affinity_score": affinity_score,
                "keyword_score": keyword_score,
                "text_score": text_score,
                "has_conflict": has_conflict,
                "coi_type": coi_type,
                "coi_severity": coi_severity,
                "coi_status": coi_status,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        affinity_score = d.pop("affinity_score")

        def _parse_keyword_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        keyword_score = _parse_keyword_score(d.pop("keyword_score"))

        def _parse_text_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        text_score = _parse_text_score(d.pop("text_score"))

        has_conflict = d.pop("has_conflict")

        def _parse_coi_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        coi_type = _parse_coi_type(d.pop("coi_type"))

        def _parse_coi_severity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        coi_severity = _parse_coi_severity(d.pop("coi_severity"))

        def _parse_coi_status(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        coi_status = _parse_coi_status(d.pop("coi_status"))

        source = d.pop("source")

        affinity_matrix_entry = cls(
            uuid=uuid,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            affinity_score=affinity_score,
            keyword_score=keyword_score,
            text_score=text_score,
            has_conflict=has_conflict,
            coi_type=coi_type,
            coi_severity=coi_severity,
            coi_status=coi_status,
            source=source,
        )

        affinity_matrix_entry.additional_properties = d
        return affinity_matrix_entry

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
