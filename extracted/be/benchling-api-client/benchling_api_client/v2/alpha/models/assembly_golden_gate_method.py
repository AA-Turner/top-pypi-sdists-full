from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_golden_gate_existing_cut_sites_params import AssemblyGoldenGateExistingCutSitesParams
from ..models.assembly_golden_gate_method_type import AssemblyGoldenGateMethodType
from ..models.assembly_golden_gate_primer_pair_params import AssemblyGoldenGatePrimerPairParams
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyGoldenGateMethod")


@attr.s(auto_attribs=True, repr=False)
class AssemblyGoldenGateMethod:
    """  """

    _parameters: Union[
        AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType
    ]
    _type: AssemblyGoldenGateMethodType

    def __repr__(self):
        fields = []
        fields.append("parameters={}".format(repr(self._parameters)))
        fields.append("type={}".format(repr(self._type)))
        return "AssemblyGoldenGateMethod({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self._parameters, UnknownType):
            parameters = self._parameters.value
        elif isinstance(self._parameters, AssemblyGoldenGateExistingCutSitesParams):
            parameters = self._parameters.to_dict()

        else:
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

        def get_parameters() -> Union[
            AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType
        ]:
            parameters: Union[
                AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType
            ]
            _parameters = d.pop("parameters")

            if True:
                discriminator = _parameters["fragmentProductionMethod"]
                if discriminator == "EXISTING_CUT_SITES":
                    parameters = AssemblyGoldenGateExistingCutSitesParams.from_dict(_parameters)
                elif discriminator == "PRIMER_PAIR":
                    parameters = AssemblyGoldenGatePrimerPairParams.from_dict(_parameters)
                else:
                    parameters = UnknownType(value=_parameters)

            return parameters

        try:
            parameters = get_parameters()
        except KeyError:
            if strict:
                raise
            parameters = cast(
                Union[
                    AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType
                ],
                UNSET,
            )

        def get_type() -> AssemblyGoldenGateMethodType:
            _type = d.pop("type")
            try:
                type = AssemblyGoldenGateMethodType(_type)
            except ValueError:
                type = AssemblyGoldenGateMethodType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(AssemblyGoldenGateMethodType, UNSET)

        assembly_golden_gate_method = cls(
            parameters=parameters,
            type=type,
        )

        return assembly_golden_gate_method

    @property
    def parameters(
        self,
    ) -> Union[AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType]:
        if isinstance(self._parameters, Unset):
            raise NotPresentError(self, "parameters")
        return self._parameters

    @parameters.setter
    def parameters(
        self,
        value: Union[
            AssemblyGoldenGateExistingCutSitesParams, AssemblyGoldenGatePrimerPairParams, UnknownType
        ],
    ) -> None:
        self._parameters = value

    @property
    def type(self) -> AssemblyGoldenGateMethodType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyGoldenGateMethodType) -> None:
        self._type = value
