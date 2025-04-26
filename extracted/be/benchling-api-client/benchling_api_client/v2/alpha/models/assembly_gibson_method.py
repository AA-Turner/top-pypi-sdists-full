from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_gibson_existing_cut_sites_params import AssemblyGibsonExistingCutSitesParams
from ..models.assembly_gibson_existing_homology_regions_params import (
    AssemblyGibsonExistingHomologyRegionsParams,
)
from ..models.assembly_gibson_method_type import AssemblyGibsonMethodType
from ..models.assembly_gibson_primer_pair_params import AssemblyGibsonPrimerPairParams
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyGibsonMethod")


@attr.s(auto_attribs=True, repr=False)
class AssemblyGibsonMethod:
    """  """

    _parameters: Union[
        AssemblyGibsonExistingHomologyRegionsParams,
        AssemblyGibsonExistingCutSitesParams,
        AssemblyGibsonPrimerPairParams,
        UnknownType,
    ]
    _type: AssemblyGibsonMethodType

    def __repr__(self):
        fields = []
        fields.append("parameters={}".format(repr(self._parameters)))
        fields.append("type={}".format(repr(self._type)))
        return "AssemblyGibsonMethod({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self._parameters, UnknownType):
            parameters = self._parameters.value
        elif isinstance(self._parameters, AssemblyGibsonExistingHomologyRegionsParams):
            parameters = self._parameters.to_dict()

        elif isinstance(self._parameters, AssemblyGibsonExistingCutSitesParams):
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
            AssemblyGibsonExistingHomologyRegionsParams,
            AssemblyGibsonExistingCutSitesParams,
            AssemblyGibsonPrimerPairParams,
            UnknownType,
        ]:
            parameters: Union[
                AssemblyGibsonExistingHomologyRegionsParams,
                AssemblyGibsonExistingCutSitesParams,
                AssemblyGibsonPrimerPairParams,
                UnknownType,
            ]
            _parameters = d.pop("parameters")

            if True:
                discriminator = _parameters["fragmentProductionMethod"]
                if discriminator == "EXISTING_CUT_SITES":
                    parameters = AssemblyGibsonExistingCutSitesParams.from_dict(_parameters)
                elif discriminator == "EXISTING_HOMOLOGY_REGIONS":
                    parameters = AssemblyGibsonExistingHomologyRegionsParams.from_dict(_parameters)
                elif discriminator == "PRIMER_PAIR":
                    parameters = AssemblyGibsonPrimerPairParams.from_dict(_parameters)
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
                    AssemblyGibsonExistingHomologyRegionsParams,
                    AssemblyGibsonExistingCutSitesParams,
                    AssemblyGibsonPrimerPairParams,
                    UnknownType,
                ],
                UNSET,
            )

        def get_type() -> AssemblyGibsonMethodType:
            _type = d.pop("type")
            try:
                type = AssemblyGibsonMethodType(_type)
            except ValueError:
                type = AssemblyGibsonMethodType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(AssemblyGibsonMethodType, UNSET)

        assembly_gibson_method = cls(
            parameters=parameters,
            type=type,
        )

        return assembly_gibson_method

    @property
    def parameters(
        self,
    ) -> Union[
        AssemblyGibsonExistingHomologyRegionsParams,
        AssemblyGibsonExistingCutSitesParams,
        AssemblyGibsonPrimerPairParams,
        UnknownType,
    ]:
        if isinstance(self._parameters, Unset):
            raise NotPresentError(self, "parameters")
        return self._parameters

    @parameters.setter
    def parameters(
        self,
        value: Union[
            AssemblyGibsonExistingHomologyRegionsParams,
            AssemblyGibsonExistingCutSitesParams,
            AssemblyGibsonPrimerPairParams,
            UnknownType,
        ],
    ) -> None:
        self._parameters = value

    @property
    def type(self) -> AssemblyGibsonMethodType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyGibsonMethodType) -> None:
        self._type = value
