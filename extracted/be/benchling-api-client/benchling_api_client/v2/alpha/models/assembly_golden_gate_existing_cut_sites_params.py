from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_golden_gate_existing_cut_sites_params_fragment_production_method import (
    AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyGoldenGateExistingCutSitesParams")


@attr.s(auto_attribs=True, repr=False)
class AssemblyGoldenGateExistingCutSitesParams:
    """  """

    _fragment_production_method: AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod
    _type2_s_restriction_enzyme_id: str

    def __repr__(self):
        fields = []
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        fields.append("type2_s_restriction_enzyme_id={}".format(repr(self._type2_s_restriction_enzyme_id)))
        return "AssemblyGoldenGateExistingCutSitesParams({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fragment_production_method = self._fragment_production_method.value

        type2_s_restriction_enzyme_id = self._type2_s_restriction_enzyme_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method
        if type2_s_restriction_enzyme_id is not UNSET:
            field_dict["type2SRestrictionEnzymeId"] = type2_s_restriction_enzyme_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fragment_production_method() -> AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod:
            _fragment_production_method = d.pop("fragmentProductionMethod")
            try:
                fragment_production_method = AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod(
                    _fragment_production_method
                )
            except ValueError:
                fragment_production_method = (
                    AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod.of_unknown(
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
                AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod, UNSET
            )

        def get_type2_s_restriction_enzyme_id() -> str:
            type2_s_restriction_enzyme_id = d.pop("type2SRestrictionEnzymeId")
            return type2_s_restriction_enzyme_id

        try:
            type2_s_restriction_enzyme_id = get_type2_s_restriction_enzyme_id()
        except KeyError:
            if strict:
                raise
            type2_s_restriction_enzyme_id = cast(str, UNSET)

        assembly_golden_gate_existing_cut_sites_params = cls(
            fragment_production_method=fragment_production_method,
            type2_s_restriction_enzyme_id=type2_s_restriction_enzyme_id,
        )

        return assembly_golden_gate_existing_cut_sites_params

    @property
    def fragment_production_method(self) -> AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: AssemblyGoldenGateExistingCutSitesParamsFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value

    @property
    def type2_s_restriction_enzyme_id(self) -> str:
        if isinstance(self._type2_s_restriction_enzyme_id, Unset):
            raise NotPresentError(self, "type2_s_restriction_enzyme_id")
        return self._type2_s_restriction_enzyme_id

    @type2_s_restriction_enzyme_id.setter
    def type2_s_restriction_enzyme_id(self, value: str) -> None:
        self._type2_s_restriction_enzyme_id = value
