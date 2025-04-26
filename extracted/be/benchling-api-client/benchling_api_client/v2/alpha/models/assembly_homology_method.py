from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_homology_method_parameters import AssemblyHomologyMethodParameters
from ..models.assembly_homology_method_type import AssemblyHomologyMethodType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyHomologyMethod")


@attr.s(auto_attribs=True, repr=False)
class AssemblyHomologyMethod:
    """  """

    _parameters: AssemblyHomologyMethodParameters
    _type: AssemblyHomologyMethodType

    def __repr__(self):
        fields = []
        fields.append("parameters={}".format(repr(self._parameters)))
        fields.append("type={}".format(repr(self._type)))
        return "AssemblyHomologyMethod({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        parameters = self._parameters.to_dict()

        type = self._type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_parameters() -> AssemblyHomologyMethodParameters:
            parameters = AssemblyHomologyMethodParameters.from_dict(d.pop("parameters"), strict=False)

            return parameters

        try:
            parameters = get_parameters()
        except KeyError:
            if strict:
                raise
            parameters = cast(AssemblyHomologyMethodParameters, UNSET)

        def get_type() -> AssemblyHomologyMethodType:
            _type = d.pop("type")
            try:
                type = AssemblyHomologyMethodType(_type)
            except ValueError:
                type = AssemblyHomologyMethodType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(AssemblyHomologyMethodType, UNSET)

        assembly_homology_method = cls(
            parameters=parameters,
            type=type,
        )

        return assembly_homology_method

    @property
    def parameters(self) -> AssemblyHomologyMethodParameters:
        if isinstance(self._parameters, Unset):
            raise NotPresentError(self, "parameters")
        return self._parameters

    @parameters.setter
    def parameters(self, value: AssemblyHomologyMethodParameters) -> None:
        self._parameters = value

    @property
    def type(self) -> AssemblyHomologyMethodType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyHomologyMethodType) -> None:
        self._type = value
