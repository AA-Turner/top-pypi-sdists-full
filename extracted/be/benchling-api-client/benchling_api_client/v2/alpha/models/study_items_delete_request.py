from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyItemsDeleteRequest")


@attr.s(auto_attribs=True, repr=False)
class StudyItemsDeleteRequest:
    """  """

    _item_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("item_ids={}".format(repr(self._item_ids)))
        return "StudyItemsDeleteRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        item_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._item_ids, Unset):
            item_ids = self._item_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if item_ids is not UNSET:
            field_dict["itemIds"] = item_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_item_ids() -> Union[Unset, List[str]]:
            item_ids = cast(List[str], d.pop("itemIds"))

            return item_ids

        try:
            item_ids = get_item_ids()
        except KeyError:
            if strict:
                raise
            item_ids = cast(Union[Unset, List[str]], UNSET)

        study_items_delete_request = cls(
            item_ids=item_ids,
        )

        return study_items_delete_request

    @property
    def item_ids(self) -> List[str]:
        if isinstance(self._item_ids, Unset):
            raise NotPresentError(self, "item_ids")
        return self._item_ids

    @item_ids.setter
    def item_ids(self, value: List[str]) -> None:
        self._item_ids = value

    @item_ids.deleter
    def item_ids(self) -> None:
        self._item_ids = UNSET
