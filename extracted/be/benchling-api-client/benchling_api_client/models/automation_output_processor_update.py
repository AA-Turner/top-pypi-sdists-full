from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessorUpdate")


@attr.s(auto_attribs=True, repr=False)
class AutomationOutputProcessorUpdate:
    """  """

    _file_id: str

    def __repr__(self):
        fields = []
        fields.append("file_id={}".format(repr(self._file_id)))
        return "AutomationOutputProcessorUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_id = self._file_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_id is not UNSET:
            field_dict["fileId"] = file_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_file_id() -> str:
            file_id = d.pop("fileId")
            return file_id

        try:
            file_id = get_file_id()
        except KeyError:
            if strict:
                raise
            file_id = cast(str, UNSET)

        automation_output_processor_update = cls(
            file_id=file_id,
        )

        return automation_output_processor_update

    @property
    def file_id(self) -> str:
        """ The ID of a blob link or the API ID of a file to process. """
        if isinstance(self._file_id, Unset):
            raise NotPresentError(self, "file_id")
        return self._file_id

    @file_id.setter
    def file_id(self, value: str) -> None:
        self._file_id = value
