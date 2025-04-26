from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_homology_method_parameters_ambiguous_construct_preference import (
    AssemblyHomologyMethodParametersAmbiguousConstructPreference,
)
from ..models.assembly_homology_method_parameters_fragment_production_method import (
    AssemblyHomologyMethodParametersFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyHomologyMethodParameters")


@attr.s(auto_attribs=True, repr=False)
class AssemblyHomologyMethodParameters:
    """  """

    _ambiguous_construct_preference: AssemblyHomologyMethodParametersAmbiguousConstructPreference
    _fragment_production_method: AssemblyHomologyMethodParametersFragmentProductionMethod

    def __repr__(self):
        fields = []
        fields.append("ambiguous_construct_preference={}".format(repr(self._ambiguous_construct_preference)))
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        return "AssemblyHomologyMethodParameters({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        ambiguous_construct_preference = self._ambiguous_construct_preference.value

        fragment_production_method = self._fragment_production_method.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if ambiguous_construct_preference is not UNSET:
            field_dict["ambiguousConstructPreference"] = ambiguous_construct_preference
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_ambiguous_construct_preference() -> AssemblyHomologyMethodParametersAmbiguousConstructPreference:
            _ambiguous_construct_preference = d.pop("ambiguousConstructPreference")
            try:
                ambiguous_construct_preference = AssemblyHomologyMethodParametersAmbiguousConstructPreference(
                    _ambiguous_construct_preference
                )
            except ValueError:
                ambiguous_construct_preference = (
                    AssemblyHomologyMethodParametersAmbiguousConstructPreference.of_unknown(
                        _ambiguous_construct_preference
                    )
                )

            return ambiguous_construct_preference

        try:
            ambiguous_construct_preference = get_ambiguous_construct_preference()
        except KeyError:
            if strict:
                raise
            ambiguous_construct_preference = cast(
                AssemblyHomologyMethodParametersAmbiguousConstructPreference, UNSET
            )

        def get_fragment_production_method() -> AssemblyHomologyMethodParametersFragmentProductionMethod:
            _fragment_production_method = d.pop("fragmentProductionMethod")
            try:
                fragment_production_method = AssemblyHomologyMethodParametersFragmentProductionMethod(
                    _fragment_production_method
                )
            except ValueError:
                fragment_production_method = (
                    AssemblyHomologyMethodParametersFragmentProductionMethod.of_unknown(
                        _fragment_production_method
                    )
                )

            return fragment_production_method

        try:
            fragment_production_method = get_fragment_production_method()
        except KeyError:
            if strict:
                raise
            fragment_production_method = cast(AssemblyHomologyMethodParametersFragmentProductionMethod, UNSET)

        assembly_homology_method_parameters = cls(
            ambiguous_construct_preference=ambiguous_construct_preference,
            fragment_production_method=fragment_production_method,
        )

        return assembly_homology_method_parameters

    @property
    def ambiguous_construct_preference(self) -> AssemblyHomologyMethodParametersAmbiguousConstructPreference:
        if isinstance(self._ambiguous_construct_preference, Unset):
            raise NotPresentError(self, "ambiguous_construct_preference")
        return self._ambiguous_construct_preference

    @ambiguous_construct_preference.setter
    def ambiguous_construct_preference(
        self, value: AssemblyHomologyMethodParametersAmbiguousConstructPreference
    ) -> None:
        self._ambiguous_construct_preference = value

    @property
    def fragment_production_method(self) -> AssemblyHomologyMethodParametersFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: AssemblyHomologyMethodParametersFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value
