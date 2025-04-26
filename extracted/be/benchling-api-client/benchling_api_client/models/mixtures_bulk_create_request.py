from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.mixture_create import MixtureCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="MixturesBulkCreateRequest")


@attr.s(auto_attribs=True, repr=False)
class MixturesBulkCreateRequest:
    """  """

    _mixtures: List[MixtureCreate]

    def __repr__(self):
        fields = []
        fields.append("mixtures={}".format(repr(self._mixtures)))
        return "MixturesBulkCreateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        mixtures = []
        for mixtures_item_data in self._mixtures:
            mixtures_item = mixtures_item_data.to_dict()

            mixtures.append(mixtures_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if mixtures is not UNSET:
            field_dict["mixtures"] = mixtures

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_mixtures() -> List[MixtureCreate]:
            mixtures = []
            _mixtures = d.pop("mixtures")
            for mixtures_item_data in _mixtures:
                mixtures_item = MixtureCreate.from_dict(mixtures_item_data, strict=False)

                mixtures.append(mixtures_item)

            return mixtures

        try:
            mixtures = get_mixtures()
        except KeyError:
            if strict:
                raise
            mixtures = cast(List[MixtureCreate], UNSET)

        mixtures_bulk_create_request = cls(
            mixtures=mixtures,
        )

        return mixtures_bulk_create_request

    @property
    def mixtures(self) -> List[MixtureCreate]:
        if isinstance(self._mixtures, Unset):
            raise NotPresentError(self, "mixtures")
        return self._mixtures

    @mixtures.setter
    def mixtures(self, value: List[MixtureCreate]) -> None:
        self._mixtures = value
