from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.dataset import Dataset
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class DatasetsPaginatedList:
    """  """

    _datasets: Union[Unset, List[Dataset]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("datasets={}".format(repr(self._datasets)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DatasetsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        datasets: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._datasets, Unset):
            datasets = []
            for datasets_item_data in self._datasets:
                datasets_item = datasets_item_data.to_dict()

                datasets.append(datasets_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if datasets is not UNSET:
            field_dict["datasets"] = datasets
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_datasets() -> Union[Unset, List[Dataset]]:
            datasets = []
            _datasets = d.pop("datasets")
            for datasets_item_data in _datasets or []:
                datasets_item = Dataset.from_dict(datasets_item_data, strict=False)

                datasets.append(datasets_item)

            return datasets

        try:
            datasets = get_datasets()
        except KeyError:
            if strict:
                raise
            datasets = cast(Union[Unset, List[Dataset]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        datasets_paginated_list = cls(
            datasets=datasets,
            next_token=next_token,
        )

        datasets_paginated_list.additional_properties = d
        return datasets_paginated_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def datasets(self) -> List[Dataset]:
        if isinstance(self._datasets, Unset):
            raise NotPresentError(self, "datasets")
        return self._datasets

    @datasets.setter
    def datasets(self, value: List[Dataset]) -> None:
        self._datasets = value

    @datasets.deleter
    def datasets(self) -> None:
        self._datasets = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
