from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.export_item_request_format import ExportItemRequestFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportItemRequest")


@attr.s(auto_attribs=True, repr=False)
class ExportItemRequest:
    """  """

    _id: str
    _format: Union[Unset, ExportItemRequestFormat] = ExportItemRequestFormat.PDF

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("format={}".format(repr(self._format)))
        return "ExportItemRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        format: Union[Unset, int] = UNSET
        if not isinstance(self._format, Unset):
            format = self._format.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if format is not UNSET:
            field_dict["format"] = format

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

        def get_format() -> Union[Unset, ExportItemRequestFormat]:
            format = UNSET
            _format = d.pop("format")
            if _format is not None and _format is not UNSET:
                try:
                    format = ExportItemRequestFormat(_format)
                except ValueError:
                    format = ExportItemRequestFormat.of_unknown(_format)

            return format

        try:
            format = get_format()
        except KeyError:
            if strict:
                raise
            format = cast(Union[Unset, ExportItemRequestFormat], UNSET)

        export_item_request = cls(
            id=id,
            format=format,
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

    @property
    def format(self) -> ExportItemRequestFormat:
        """ The export format for the item. Defaults to pdf if not specified. """
        if isinstance(self._format, Unset):
            raise NotPresentError(self, "format")
        return self._format

    @format.setter
    def format(self, value: ExportItemRequestFormat) -> None:
        self._format = value

    @format.deleter
    def format(self) -> None:
        self._format = UNSET
