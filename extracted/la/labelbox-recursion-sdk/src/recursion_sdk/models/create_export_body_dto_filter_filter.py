from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_export_body_dto_filter_filter_avg_score_metric import CreateExportBodyDtoFilterFilterAvgScoreMetric
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.create_export_body_dto_filter_filter_enrichment_filters import CreateExportBodyDtoFilterFilterEnrichmentFilters





T = TypeVar("T", bound="CreateExportBodyDtoFilterFilter")



@_attrs_define
class CreateExportBodyDtoFilterFilter:
    """ Filter describing which problems to include, resolved server-side at job-start.

        Attributes:
            enrichment_filters (CreateExportBodyDtoFilterFilterEnrichmentFilters): JSON-encoded enrichment-dimension filters
                applied uniformly across list items, stats, analytics, and exports.
            search (str | Unset): Free-text search filter applied across problem title and external id.
            models (list[str] | Unset): Comma-separated list of model identifiers; matches problems with at least one run on
                any listed model.
            avg_score_metric (CreateExportBodyDtoFilterFilterAvgScoreMetric | Unset): Which aggregate (avg, min, or max) the
                score bounds apply to. Defaults to the average.
            avg_score_min (float | Unset): Inclusive lower bound on the selected score metric, expressed as a 0–100
                percentage. Example: 25.
            avg_score_max (float | Unset): Inclusive upper bound on the selected score metric, expressed as a 0–100
                percentage. Example: 75.
            created_at_from (datetime.date | Unset): Inclusive lower bound on problem creation date, in YYYY-MM-DD form (UTC
                calendar day).
            created_at_to (datetime.date | Unset): Inclusive upper bound on problem creation date, in YYYY-MM-DD form (UTC
                calendar day).
     """

    enrichment_filters: CreateExportBodyDtoFilterFilterEnrichmentFilters
    search: str | Unset = UNSET
    models: list[str] | Unset = UNSET
    avg_score_metric: CreateExportBodyDtoFilterFilterAvgScoreMetric | Unset = UNSET
    avg_score_min: float | Unset = UNSET
    avg_score_max: float | Unset = UNSET
    created_at_from: datetime.date | Unset = UNSET
    created_at_to: datetime.date | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_export_body_dto_filter_filter_enrichment_filters import CreateExportBodyDtoFilterFilterEnrichmentFilters # noqa: PLC0415
        enrichment_filters = self.enrichment_filters.to_dict()

        search = self.search

        models: list[str] | Unset = UNSET
        if not isinstance(self.models, Unset):
            models = self.models



        avg_score_metric: str | Unset = UNSET
        if not isinstance(self.avg_score_metric, Unset):
            avg_score_metric = self.avg_score_metric.value


        avg_score_min = self.avg_score_min

        avg_score_max = self.avg_score_max

        created_at_from: str | Unset = UNSET
        if not isinstance(self.created_at_from, Unset):
            created_at_from = self.created_at_from.isoformat()

        created_at_to: str | Unset = UNSET
        if not isinstance(self.created_at_to, Unset):
            created_at_to = self.created_at_to.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "enrichmentFilters": enrichment_filters,
        })
        if search is not UNSET:
            field_dict["search"] = search
        if models is not UNSET:
            field_dict["models"] = models
        if avg_score_metric is not UNSET:
            field_dict["avgScoreMetric"] = avg_score_metric
        if avg_score_min is not UNSET:
            field_dict["avgScoreMin"] = avg_score_min
        if avg_score_max is not UNSET:
            field_dict["avgScoreMax"] = avg_score_max
        if created_at_from is not UNSET:
            field_dict["createdAtFrom"] = created_at_from
        if created_at_to is not UNSET:
            field_dict["createdAtTo"] = created_at_to

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_export_body_dto_filter_filter_enrichment_filters import CreateExportBodyDtoFilterFilterEnrichmentFilters # noqa: PLC0415
        d = dict(src_dict)
        enrichment_filters = CreateExportBodyDtoFilterFilterEnrichmentFilters.from_dict(d.pop("enrichmentFilters"))




        search = d.pop("search", UNSET)

        models = cast(list[str], d.pop("models", UNSET))


        _avg_score_metric = d.pop("avgScoreMetric", UNSET)
        avg_score_metric: CreateExportBodyDtoFilterFilterAvgScoreMetric | Unset
        if isinstance(_avg_score_metric,  Unset):
            avg_score_metric = UNSET
        else:
            avg_score_metric = CreateExportBodyDtoFilterFilterAvgScoreMetric(_avg_score_metric)




        avg_score_min = d.pop("avgScoreMin", UNSET)

        avg_score_max = d.pop("avgScoreMax", UNSET)

        _created_at_from = d.pop("createdAtFrom", UNSET)
        created_at_from: datetime.date | Unset
        if isinstance(_created_at_from,  Unset):
            created_at_from = UNSET
        else:
            created_at_from = datetime.date.fromisoformat(_created_at_from)




        _created_at_to = d.pop("createdAtTo", UNSET)
        created_at_to: datetime.date | Unset
        if isinstance(_created_at_to,  Unset):
            created_at_to = UNSET
        else:
            created_at_to = datetime.date.fromisoformat(_created_at_to)




        create_export_body_dto_filter_filter = cls(
            enrichment_filters=enrichment_filters,
            search=search,
            models=models,
            avg_score_metric=avg_score_metric,
            avg_score_min=avg_score_min,
            avg_score_max=avg_score_max,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
        )


        create_export_body_dto_filter_filter.additional_properties = d
        return create_export_body_dto_filter_filter

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
