from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_gibson_existing_cut_sites_params_fragment_production_method import (
    AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyGibsonExistingCutSitesParams")


@attr.s(auto_attribs=True, repr=False)
class AssemblyGibsonExistingCutSitesParams:
    """  """

    _fragment_production_method: AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod
    _maximum_homology_and_binding_region_length: float
    _minimum_binding_region_melting_temperature: float
    _minimum_homology_and_binding_region_length: float

    def __repr__(self):
        fields = []
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        fields.append(
            "maximum_homology_and_binding_region_length={}".format(
                repr(self._maximum_homology_and_binding_region_length)
            )
        )
        fields.append(
            "minimum_binding_region_melting_temperature={}".format(
                repr(self._minimum_binding_region_melting_temperature)
            )
        )
        fields.append(
            "minimum_homology_and_binding_region_length={}".format(
                repr(self._minimum_homology_and_binding_region_length)
            )
        )
        return "AssemblyGibsonExistingCutSitesParams({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fragment_production_method = self._fragment_production_method.value

        maximum_homology_and_binding_region_length = self._maximum_homology_and_binding_region_length
        minimum_binding_region_melting_temperature = self._minimum_binding_region_melting_temperature
        minimum_homology_and_binding_region_length = self._minimum_homology_and_binding_region_length

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method
        if maximum_homology_and_binding_region_length is not UNSET:
            field_dict["maximumHomologyAndBindingRegionLength"] = maximum_homology_and_binding_region_length
        if minimum_binding_region_melting_temperature is not UNSET:
            field_dict["minimumBindingRegionMeltingTemperature"] = minimum_binding_region_melting_temperature
        if minimum_homology_and_binding_region_length is not UNSET:
            field_dict["minimumHomologyAndBindingRegionLength"] = minimum_homology_and_binding_region_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fragment_production_method() -> AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod:
            _fragment_production_method = d.pop("fragmentProductionMethod")
            try:
                fragment_production_method = AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod(
                    _fragment_production_method
                )
            except ValueError:
                fragment_production_method = (
                    AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod.of_unknown(
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
                AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod, UNSET
            )

        def get_maximum_homology_and_binding_region_length() -> float:
            maximum_homology_and_binding_region_length = d.pop("maximumHomologyAndBindingRegionLength")
            return maximum_homology_and_binding_region_length

        try:
            maximum_homology_and_binding_region_length = get_maximum_homology_and_binding_region_length()
        except KeyError:
            if strict:
                raise
            maximum_homology_and_binding_region_length = cast(float, UNSET)

        def get_minimum_binding_region_melting_temperature() -> float:
            minimum_binding_region_melting_temperature = d.pop("minimumBindingRegionMeltingTemperature")
            return minimum_binding_region_melting_temperature

        try:
            minimum_binding_region_melting_temperature = get_minimum_binding_region_melting_temperature()
        except KeyError:
            if strict:
                raise
            minimum_binding_region_melting_temperature = cast(float, UNSET)

        def get_minimum_homology_and_binding_region_length() -> float:
            minimum_homology_and_binding_region_length = d.pop("minimumHomologyAndBindingRegionLength")
            return minimum_homology_and_binding_region_length

        try:
            minimum_homology_and_binding_region_length = get_minimum_homology_and_binding_region_length()
        except KeyError:
            if strict:
                raise
            minimum_homology_and_binding_region_length = cast(float, UNSET)

        assembly_gibson_existing_cut_sites_params = cls(
            fragment_production_method=fragment_production_method,
            maximum_homology_and_binding_region_length=maximum_homology_and_binding_region_length,
            minimum_binding_region_melting_temperature=minimum_binding_region_melting_temperature,
            minimum_homology_and_binding_region_length=minimum_homology_and_binding_region_length,
        )

        return assembly_gibson_existing_cut_sites_params

    @property
    def fragment_production_method(self) -> AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: AssemblyGibsonExistingCutSitesParamsFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value

    @property
    def maximum_homology_and_binding_region_length(self) -> float:
        """ Maximum length, in base pairs, of the primer's binding/homology regions. """
        if isinstance(self._maximum_homology_and_binding_region_length, Unset):
            raise NotPresentError(self, "maximum_homology_and_binding_region_length")
        return self._maximum_homology_and_binding_region_length

    @maximum_homology_and_binding_region_length.setter
    def maximum_homology_and_binding_region_length(self, value: float) -> None:
        self._maximum_homology_and_binding_region_length = value

    @property
    def minimum_binding_region_melting_temperature(self) -> float:
        """ Minimum melting temperature of the primer binding region. """
        if isinstance(self._minimum_binding_region_melting_temperature, Unset):
            raise NotPresentError(self, "minimum_binding_region_melting_temperature")
        return self._minimum_binding_region_melting_temperature

    @minimum_binding_region_melting_temperature.setter
    def minimum_binding_region_melting_temperature(self, value: float) -> None:
        self._minimum_binding_region_melting_temperature = value

    @property
    def minimum_homology_and_binding_region_length(self) -> float:
        """ Minimum length, in base pairs, of the primer's binding/homology regions. """
        if isinstance(self._minimum_homology_and_binding_region_length, Unset):
            raise NotPresentError(self, "minimum_homology_and_binding_region_length")
        return self._minimum_homology_and_binding_region_length

    @minimum_homology_and_binding_region_length.setter
    def minimum_homology_and_binding_region_length(self, value: float) -> None:
        self._minimum_homology_and_binding_region_length = value
