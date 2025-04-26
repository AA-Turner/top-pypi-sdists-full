from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assembly_transient_primer_type import AssemblyTransientPrimerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyTransientPrimer")


@attr.s(auto_attribs=True, repr=False)
class AssemblyTransientPrimer:
    """  """

    _bases: Union[Unset, str] = UNSET
    _binding_position: Union[Unset, str] = UNSET
    _type: Union[Unset, AssemblyTransientPrimerType] = UNSET

    def __repr__(self):
        fields = []
        fields.append("bases={}".format(repr(self._bases)))
        fields.append("binding_position={}".format(repr(self._binding_position)))
        fields.append("type={}".format(repr(self._type)))
        return "AssemblyTransientPrimer({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bases = self._bases
        binding_position = self._binding_position
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bases is not UNSET:
            field_dict["bases"] = bases
        if binding_position is not UNSET:
            field_dict["bindingPosition"] = binding_position
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bases() -> Union[Unset, str]:
            bases = d.pop("bases")
            return bases

        try:
            bases = get_bases()
        except KeyError:
            if strict:
                raise
            bases = cast(Union[Unset, str], UNSET)

        def get_binding_position() -> Union[Unset, str]:
            binding_position = d.pop("bindingPosition")
            return binding_position

        try:
            binding_position = get_binding_position()
        except KeyError:
            if strict:
                raise
            binding_position = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, AssemblyTransientPrimerType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AssemblyTransientPrimerType(_type)
                except ValueError:
                    type = AssemblyTransientPrimerType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, AssemblyTransientPrimerType], UNSET)

        assembly_transient_primer = cls(
            bases=bases,
            binding_position=binding_position,
            type=type,
        )

        return assembly_transient_primer

    @property
    def bases(self) -> str:
        """ Bases of the primer. """
        if isinstance(self._bases, Unset):
            raise NotPresentError(self, "bases")
        return self._bases

    @bases.setter
    def bases(self, value: str) -> None:
        self._bases = value

    @bases.deleter
    def bases(self) -> None:
        self._bases = UNSET

    @property
    def binding_position(self) -> str:
        """ Binding position of the primer on the construct. """
        if isinstance(self._binding_position, Unset):
            raise NotPresentError(self, "binding_position")
        return self._binding_position

    @binding_position.setter
    def binding_position(self, value: str) -> None:
        self._binding_position = value

    @binding_position.deleter
    def binding_position(self) -> None:
        self._binding_position = UNSET

    @property
    def type(self) -> AssemblyTransientPrimerType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyTransientPrimerType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
