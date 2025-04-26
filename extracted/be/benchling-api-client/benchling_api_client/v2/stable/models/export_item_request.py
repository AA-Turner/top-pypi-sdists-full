from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportItemRequest")


@attr.s(auto_attribs=True, repr=False)
class ExportItemRequest:
    """  """

    _id: str

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        return "ExportItemRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        export_item_request = cls(
            id=id,
        )

        return export_item_request

    @property
    def id(self) -> str:
        """ ID of the item to export """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value
