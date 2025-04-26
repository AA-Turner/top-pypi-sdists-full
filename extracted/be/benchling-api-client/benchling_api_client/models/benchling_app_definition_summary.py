from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppDefinitionSummary")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppDefinitionSummary:
    """  """

    _id: Union[Unset, str] = UNSET
    _version_number: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("version_number={}".format(repr(self._version_number)))
        return "BenchlingAppDefinitionSummary({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        version_number = self._version_number

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if version_number is not UNSET:
            field_dict["versionNumber"] = version_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_version_number() -> Union[Unset, str]:
            version_number = d.pop("versionNumber")
            return version_number

        try:
            version_number = get_version_number()
        except KeyError:
            if strict:
                raise
            version_number = cast(Union[Unset, str], UNSET)

        benchling_app_definition_summary = cls(
            id=id,
            version_number=version_number,
        )

        return benchling_app_definition_summary

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def version_number(self) -> str:
        if isinstance(self._version_number, Unset):
            raise NotPresentError(self, "version_number")
        return self._version_number

    @version_number.setter
    def version_number(self, value: str) -> None:
        self._version_number = value

    @version_number.deleter
    def version_number(self) -> None:
        self._version_number = UNSET
