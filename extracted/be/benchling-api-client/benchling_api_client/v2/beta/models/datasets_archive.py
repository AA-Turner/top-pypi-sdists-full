from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.datasets_archive_reason import DatasetsArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetsArchive")


@attr.s(auto_attribs=True, repr=False)
class DatasetsArchive:
    """The request body for archiving Datasets."""

    _dataset_ids: List[str]
    _reason: DatasetsArchiveReason

    def __repr__(self):
        fields = []
        fields.append("dataset_ids={}".format(repr(self._dataset_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "DatasetsArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dataset_ids = self._dataset_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dataset_ids is not UNSET:
            field_dict["datasetIds"] = dataset_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dataset_ids() -> List[str]:
            dataset_ids = cast(List[str], d.pop("datasetIds"))

            return dataset_ids

        try:
            dataset_ids = get_dataset_ids()
        except KeyError:
            if strict:
                raise
            dataset_ids = cast(List[str], UNSET)

        def get_reason() -> DatasetsArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = DatasetsArchiveReason(_reason)
            except ValueError:
                reason = DatasetsArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(DatasetsArchiveReason, UNSET)

        datasets_archive = cls(
            dataset_ids=dataset_ids,
            reason=reason,
        )

        return datasets_archive

    @property
    def dataset_ids(self) -> List[str]:
        if isinstance(self._dataset_ids, Unset):
            raise NotPresentError(self, "dataset_ids")
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, value: List[str]) -> None:
        self._dataset_ids = value

    @property
    def reason(self) -> DatasetsArchiveReason:
        """The reason for archiving the provided Datasets. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: DatasetsArchiveReason) -> None:
        self._reason = value
