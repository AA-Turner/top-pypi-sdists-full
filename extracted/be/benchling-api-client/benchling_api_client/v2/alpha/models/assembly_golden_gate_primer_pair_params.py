from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_golden_gate_primer_pair_params_fragment_production_method import (
    AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyGoldenGatePrimerPairParams")


@attr.s(auto_attribs=True, repr=False)
class AssemblyGoldenGatePrimerPairParams:
    """  """

    _fragment_production_method: AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod
    _maximum_primer_pair_melting_temperature_difference: float
    _minimum_binding_region_length: float
    _minimum_binding_region_melting_temperature: float
    _pre_recognition_site_bases: str
    _pre_recognition_site_length: float
    _type2_s_restriction_enzyme_id: str

    def __repr__(self):
        fields = []
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        fields.append(
            "maximum_primer_pair_melting_temperature_difference={}".format(
                repr(self._maximum_primer_pair_melting_temperature_difference)
            )
        )
        fields.append("minimum_binding_region_length={}".format(repr(self._minimum_binding_region_length)))
        fields.append(
            "minimum_binding_region_melting_temperature={}".format(
                repr(self._minimum_binding_region_melting_temperature)
            )
        )
        fields.append("pre_recognition_site_bases={}".format(repr(self._pre_recognition_site_bases)))
        fields.append("pre_recognition_site_length={}".format(repr(self._pre_recognition_site_length)))
        fields.append("type2_s_restriction_enzyme_id={}".format(repr(self._type2_s_restriction_enzyme_id)))
        return "AssemblyGoldenGatePrimerPairParams({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fragment_production_method = self._fragment_production_method.value

        maximum_primer_pair_melting_temperature_difference = (
            self._maximum_primer_pair_melting_temperature_difference
        )
        minimum_binding_region_length = self._minimum_binding_region_length
        minimum_binding_region_melting_temperature = self._minimum_binding_region_melting_temperature
        pre_recognition_site_bases = self._pre_recognition_site_bases
        pre_recognition_site_length = self._pre_recognition_site_length
        type2_s_restriction_enzyme_id = self._type2_s_restriction_enzyme_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method
        if maximum_primer_pair_melting_temperature_difference is not UNSET:
            field_dict[
                "maximumPrimerPairMeltingTemperatureDifference"
            ] = maximum_primer_pair_melting_temperature_difference
        if minimum_binding_region_length is not UNSET:
            field_dict["minimumBindingRegionLength"] = minimum_binding_region_length
        if minimum_binding_region_melting_temperature is not UNSET:
            field_dict["minimumBindingRegionMeltingTemperature"] = minimum_binding_region_melting_temperature
        if pre_recognition_site_bases is not UNSET:
            field_dict["preRecognitionSiteBases"] = pre_recognition_site_bases
        if pre_recognition_site_length is not UNSET:
            field_dict["preRecognitionSiteLength"] = pre_recognition_site_length
        if type2_s_restriction_enzyme_id is not UNSET:
            field_dict["type2SRestrictionEnzymeId"] = type2_s_restriction_enzyme_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fragment_production_method() -> AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod:
            _fragment_production_method = d.pop("fragmentProductionMethod")
            try:
                fragment_production_method = AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod(
                    _fragment_production_method
                )
            except ValueError:
                fragment_production_method = (
                    AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod.of_unknown(
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
                AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod, UNSET
            )

        def get_maximum_primer_pair_melting_temperature_difference() -> float:
            maximum_primer_pair_melting_temperature_difference = d.pop(
                "maximumPrimerPairMeltingTemperatureDifference"
            )
            return maximum_primer_pair_melting_temperature_difference

        try:
            maximum_primer_pair_melting_temperature_difference = (
                get_maximum_primer_pair_melting_temperature_difference()
            )
        except KeyError:
            if strict:
                raise
            maximum_primer_pair_melting_temperature_difference = cast(float, UNSET)

        def get_minimum_binding_region_length() -> float:
            minimum_binding_region_length = d.pop("minimumBindingRegionLength")
            return minimum_binding_region_length

        try:
            minimum_binding_region_length = get_minimum_binding_region_length()
        except KeyError:
            if strict:
                raise
            minimum_binding_region_length = cast(float, UNSET)

        def get_minimum_binding_region_melting_temperature() -> float:
            minimum_binding_region_melting_temperature = d.pop("minimumBindingRegionMeltingTemperature")
            return minimum_binding_region_melting_temperature

        try:
            minimum_binding_region_melting_temperature = get_minimum_binding_region_melting_temperature()
        except KeyError:
            if strict:
                raise
            minimum_binding_region_melting_temperature = cast(float, UNSET)

        def get_pre_recognition_site_bases() -> str:
            pre_recognition_site_bases = d.pop("preRecognitionSiteBases")
            return pre_recognition_site_bases

        try:
            pre_recognition_site_bases = get_pre_recognition_site_bases()
        except KeyError:
            if strict:
                raise
            pre_recognition_site_bases = cast(str, UNSET)

        def get_pre_recognition_site_length() -> float:
            pre_recognition_site_length = d.pop("preRecognitionSiteLength")
            return pre_recognition_site_length

        try:
            pre_recognition_site_length = get_pre_recognition_site_length()
        except KeyError:
            if strict:
                raise
            pre_recognition_site_length = cast(float, UNSET)

        def get_type2_s_restriction_enzyme_id() -> str:
            type2_s_restriction_enzyme_id = d.pop("type2SRestrictionEnzymeId")
            return type2_s_restriction_enzyme_id

        try:
            type2_s_restriction_enzyme_id = get_type2_s_restriction_enzyme_id()
        except KeyError:
            if strict:
                raise
            type2_s_restriction_enzyme_id = cast(str, UNSET)

        assembly_golden_gate_primer_pair_params = cls(
            fragment_production_method=fragment_production_method,
            maximum_primer_pair_melting_temperature_difference=maximum_primer_pair_melting_temperature_difference,
            minimum_binding_region_length=minimum_binding_region_length,
            minimum_binding_region_melting_temperature=minimum_binding_region_melting_temperature,
            pre_recognition_site_bases=pre_recognition_site_bases,
            pre_recognition_site_length=pre_recognition_site_length,
            type2_s_restriction_enzyme_id=type2_s_restriction_enzyme_id,
        )

        return assembly_golden_gate_primer_pair_params

    @property
    def fragment_production_method(self) -> AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: AssemblyGoldenGatePrimerPairParamsFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value

    @property
    def maximum_primer_pair_melting_temperature_difference(self) -> float:
        """ Maximum difference of melting temperature between both primers in a pair. """
        if isinstance(self._maximum_primer_pair_melting_temperature_difference, Unset):
            raise NotPresentError(self, "maximum_primer_pair_melting_temperature_difference")
        return self._maximum_primer_pair_melting_temperature_difference

    @maximum_primer_pair_melting_temperature_difference.setter
    def maximum_primer_pair_melting_temperature_difference(self, value: float) -> None:
        self._maximum_primer_pair_melting_temperature_difference = value

    @property
    def minimum_binding_region_length(self) -> float:
        """ Minimum length of the primer binding region. """
        if isinstance(self._minimum_binding_region_length, Unset):
            raise NotPresentError(self, "minimum_binding_region_length")
        return self._minimum_binding_region_length

    @minimum_binding_region_length.setter
    def minimum_binding_region_length(self, value: float) -> None:
        self._minimum_binding_region_length = value

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
    def pre_recognition_site_bases(self) -> str:
        """ Specific base pairs to insert before the type IIS enzyme recognition site. """
        if isinstance(self._pre_recognition_site_bases, Unset):
            raise NotPresentError(self, "pre_recognition_site_bases")
        return self._pre_recognition_site_bases

    @pre_recognition_site_bases.setter
    def pre_recognition_site_bases(self, value: str) -> None:
        self._pre_recognition_site_bases = value

    @property
    def pre_recognition_site_length(self) -> float:
        """ Number of base pairs to insert before the type IIS enzyme recognition site. """
        if isinstance(self._pre_recognition_site_length, Unset):
            raise NotPresentError(self, "pre_recognition_site_length")
        return self._pre_recognition_site_length

    @pre_recognition_site_length.setter
    def pre_recognition_site_length(self, value: float) -> None:
        self._pre_recognition_site_length = value

    @property
    def type2_s_restriction_enzyme_id(self) -> str:
        if isinstance(self._type2_s_restriction_enzyme_id, Unset):
            raise NotPresentError(self, "type2_s_restriction_enzyme_id")
        return self._type2_s_restriction_enzyme_id

    @type2_s_restriction_enzyme_id.setter
    def type2_s_restriction_enzyme_id(self, value: str) -> None:
        self._type2_s_restriction_enzyme_id = value
