from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorklistItemCreate")


@attr.s(auto_attribs=True, repr=False)
class WorklistItemCreate:
    """  """

    _item_id: str

    def __repr__(self):
        fields = []
        fields.append("item_id={}".format(repr(self._item_id)))
        return "WorklistItemCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        item_id = self._item_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if item_id is not UNSET:
            field_dict["itemId"] = item_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_item_id() -> str:
            item_id = d.pop("itemId")
            return item_id

        try:
            item_id = get_item_id()
        except KeyError:
            if strict:
                raise
            item_id = cast(str, UNSET)

        worklist_item_create = cls(
            item_id=item_id,
        )

        return worklist_item_create

    @property
    def item_id(self) -> str:
        """ The ID of the item to add to the worklist. """
        if isinstance(self._item_id, Unset):
            raise NotPresentError(self, "item_id")
        return self._item_id

    @item_id.setter
    def item_id(self, value: str) -> None:
        self._item_id = value
