from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_concatenation_method_parameters_fragment_production_method import (
    AssemblyConcatenationMethodParametersFragmentProductionMethod,
)
from ..models.assembly_concatenation_method_parameters_polymer_type import (
    AssemblyConcatenationMethodParametersPolymerType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyConcatenationMethodParameters")


@attr.s(auto_attribs=True, repr=False)
class AssemblyConcatenationMethodParameters:
    """  """

    _fragment_production_method: AssemblyConcatenationMethodParametersFragmentProductionMethod
    _polymer_type: AssemblyConcatenationMethodParametersPolymerType

    def __repr__(self):
        fields = []
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        fields.append("polymer_type={}".format(repr(self._polymer_type)))
        return "AssemblyConcatenationMethodParameters({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fragment_production_method = self._fragment_production_method.value

        polymer_type = self._polymer_type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method
        if polymer_type is not UNSET:
            field_dict["polymerType"] = polymer_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fragment_production_method() -> AssemblyConcatenationMethodParametersFragmentProductionMethod:
            _fragment_production_method = d.pop("fragmentProductionMethod")
            try:
                fragment_production_method = AssemblyConcatenationMethodParametersFragmentProductionMethod(
                    _fragment_production_method
                )
            except ValueError:
                fragment_production_method = (
                    AssemblyConcatenationMethodParametersFragmentProductionMethod.of_unknown(
                        _fragment_production_method
                    )
                )

            return fragment_production_method

        try:
            fragment_production_method = get_fragment_production_method()
        except KeyError:
            if strict:
                raise
            fragment_production_method = cast(
                AssemblyConcatenationMethodParametersFragmentProductionMethod, UNSET
            )

        def get_polymer_type() -> AssemblyConcatenationMethodParametersPolymerType:
            _polymer_type = d.pop("polymerType")
            try:
                polymer_type = AssemblyConcatenationMethodParametersPolymerType(_polymer_type)
            except ValueError:
                polymer_type = AssemblyConcatenationMethodParametersPolymerType.of_unknown(_polymer_type)

            return polymer_type

        try:
            polymer_type = get_polymer_type()
        except KeyError:
            if strict:
                raise
            polymer_type = cast(AssemblyConcatenationMethodParametersPolymerType, UNSET)

        assembly_concatenation_method_parameters = cls(
            fragment_production_method=fragment_production_method,
            polymer_type=polymer_type,
        )

        return assembly_concatenation_method_parameters

    @property
    def fragment_production_method(self) -> AssemblyConcatenationMethodParametersFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: AssemblyConcatenationMethodParametersFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value

    @property
    def polymer_type(self) -> AssemblyConcatenationMethodParametersPolymerType:
        if isinstance(self._polymer_type, Unset):
            raise NotPresentError(self, "polymer_type")
        return self._polymer_type

    @polymer_type.setter
    def polymer_type(self, value: AssemblyConcatenationMethodParametersPolymerType) -> None:
        self._polymer_type = value
