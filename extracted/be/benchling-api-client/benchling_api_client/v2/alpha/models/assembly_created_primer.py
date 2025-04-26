from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assembly_created_primer_type import AssemblyCreatedPrimerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyCreatedPrimer")


@attr.s(auto_attribs=True, repr=False)
class AssemblyCreatedPrimer:
    """  """

    _created_oligo_id: Union[Unset, str] = UNSET
    _type: Union[Unset, AssemblyCreatedPrimerType] = UNSET

    def __repr__(self):
        fields = []
        fields.append("created_oligo_id={}".format(repr(self._created_oligo_id)))
        fields.append("type={}".format(repr(self._type)))
        return "AssemblyCreatedPrimer({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_oligo_id = self._created_oligo_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_oligo_id is not UNSET:
            field_dict["createdOligoId"] = created_oligo_id
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_created_oligo_id() -> Union[Unset, str]:
            created_oligo_id = d.pop("createdOligoId")
            return created_oligo_id

        try:
            created_oligo_id = get_created_oligo_id()
        except KeyError:
            if strict:
                raise
            created_oligo_id = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, AssemblyCreatedPrimerType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AssemblyCreatedPrimerType(_type)
                except ValueError:
                    type = AssemblyCreatedPrimerType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, AssemblyCreatedPrimerType], UNSET)

        assembly_created_primer = cls(
            created_oligo_id=created_oligo_id,
            type=type,
        )

        return assembly_created_primer

    @property
    def created_oligo_id(self) -> str:
        """ API identifier of the Benchling oligo created by the assembly. """
        if isinstance(self._created_oligo_id, Unset):
            raise NotPresentError(self, "created_oligo_id")
        return self._created_oligo_id

    @created_oligo_id.setter
    def created_oligo_id(self, value: str) -> None:
        self._created_oligo_id = value

    @created_oligo_id.deleter
    def created_oligo_id(self) -> None:
        self._created_oligo_id = UNSET

    @property
    def type(self) -> AssemblyCreatedPrimerType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyCreatedPrimerType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
