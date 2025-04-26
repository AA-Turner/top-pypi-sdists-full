from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetsArchivalChange")


@attr.s(auto_attribs=True, repr=False)
class DatasetsArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type."""

    _dataset_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("dataset_ids={}".format(repr(self._dataset_ids)))
        return "DatasetsArchivalChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dataset_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._dataset_ids, Unset):
            dataset_ids = self._dataset_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dataset_ids is not UNSET:
            field_dict["datasetIds"] = dataset_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dataset_ids() -> Union[Unset, List[str]]:
            dataset_ids = cast(List[str], d.pop("datasetIds"))

            return dataset_ids

        try:
            dataset_ids = get_dataset_ids()
        except KeyError:
            if strict:
                raise
            dataset_ids = cast(Union[Unset, List[str]], UNSET)

        datasets_archival_change = cls(
            dataset_ids=dataset_ids,
        )

        return datasets_archival_change

    @property
    def dataset_ids(self) -> List[str]:
        if isinstance(self._dataset_ids, Unset):
            raise NotPresentError(self, "dataset_ids")
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, value: List[str]) -> None:
        self._dataset_ids = value

    @dataset_ids.deleter
    def dataset_ids(self) -> None:
        self._dataset_ids = UNSET
