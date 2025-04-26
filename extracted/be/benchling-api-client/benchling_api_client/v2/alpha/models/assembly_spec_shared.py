from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_concatenation_method import AssemblyConcatenationMethod
from ..models.assembly_constant_bin import AssemblyConstantBin
from ..models.assembly_fragment_bin import AssemblyFragmentBin
from ..models.assembly_gibson_method import AssemblyGibsonMethod
from ..models.assembly_golden_gate_method import AssemblyGoldenGateMethod
from ..models.assembly_homology_method import AssemblyHomologyMethod
from ..models.assembly_spec_shared_constructs_item import AssemblySpecSharedConstructsItem
from ..models.assembly_spec_shared_fragments_item import AssemblySpecSharedFragmentsItem
from ..models.assembly_spec_shared_topology import AssemblySpecSharedTopology
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySpecShared")


@attr.s(auto_attribs=True, repr=False)
class AssemblySpecShared:
    """ Information required when validating or finalizing a bulk assembly. """

    _assembly_parameters: Union[
        AssemblyGoldenGateMethod,
        AssemblyGibsonMethod,
        AssemblyHomologyMethod,
        AssemblyConcatenationMethod,
        UnknownType,
    ]
    _bins: List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]
    _constructs: List[AssemblySpecSharedConstructsItem]
    _fragments: List[AssemblySpecSharedFragmentsItem]
    _topology: AssemblySpecSharedTopology
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assembly_parameters={}".format(repr(self._assembly_parameters)))
        fields.append("bins={}".format(repr(self._bins)))
        fields.append("constructs={}".format(repr(self._constructs)))
        fields.append("fragments={}".format(repr(self._fragments)))
        fields.append("topology={}".format(repr(self._topology)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblySpecShared({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self._assembly_parameters, UnknownType):
            assembly_parameters = self._assembly_parameters.value
        elif isinstance(self._assembly_parameters, AssemblyGoldenGateMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        elif isinstance(self._assembly_parameters, AssemblyGibsonMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        elif isinstance(self._assembly_parameters, AssemblyHomologyMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        else:
            assembly_parameters = self._assembly_parameters.to_dict()

        bins = []
        for bins_item_data in self._bins:
            if isinstance(bins_item_data, UnknownType):
                bins_item = bins_item_data.value
            elif isinstance(bins_item_data, AssemblyFragmentBin):
                bins_item = bins_item_data.to_dict()

            else:
                bins_item = bins_item_data.to_dict()

            bins.append(bins_item)

        constructs = []
        for constructs_item_data in self._constructs:
            constructs_item = constructs_item_data.to_dict()

            constructs.append(constructs_item)

        fragments = []
        for fragments_item_data in self._fragments:
            fragments_item = fragments_item_data.to_dict()

            fragments.append(fragments_item)

        topology = self._topology.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assembly_parameters is not UNSET:
            field_dict["assemblyParameters"] = assembly_parameters
        if bins is not UNSET:
            field_dict["bins"] = bins
        if constructs is not UNSET:
            field_dict["constructs"] = constructs
        if fragments is not UNSET:
            field_dict["fragments"] = fragments
        if topology is not UNSET:
            field_dict["topology"] = topology

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assembly_parameters() -> Union[
            AssemblyGoldenGateMethod,
            AssemblyGibsonMethod,
            AssemblyHomologyMethod,
            AssemblyConcatenationMethod,
            UnknownType,
        ]:
            assembly_parameters: Union[
                AssemblyGoldenGateMethod,
                AssemblyGibsonMethod,
                AssemblyHomologyMethod,
                AssemblyConcatenationMethod,
                UnknownType,
            ]
            _assembly_parameters = d.pop("assemblyParameters")

            if True:
                discriminator = _assembly_parameters["type"]
                if discriminator == "CONCATENATION":
                    assembly_parameters = AssemblyConcatenationMethod.from_dict(_assembly_parameters)
                elif discriminator == "GIBSON":
                    assembly_parameters = AssemblyGibsonMethod.from_dict(_assembly_parameters)
                elif discriminator == "GOLDEN_GATE":
                    assembly_parameters = AssemblyGoldenGateMethod.from_dict(_assembly_parameters)
                elif discriminator == "HOMOLOGY":
                    assembly_parameters = AssemblyHomologyMethod.from_dict(_assembly_parameters)
                else:
                    assembly_parameters = UnknownType(value=_assembly_parameters)

            return assembly_parameters

        try:
            assembly_parameters = get_assembly_parameters()
        except KeyError:
            if strict:
                raise
            assembly_parameters = cast(
                Union[
                    AssemblyGoldenGateMethod,
                    AssemblyGibsonMethod,
                    AssemblyHomologyMethod,
                    AssemblyConcatenationMethod,
                    UnknownType,
                ],
                UNSET,
            )

        def get_bins() -> List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]:
            bins = []
            _bins = d.pop("bins")
            for bins_item_data in _bins:

                def _parse_bins_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]:
                    bins_item: Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]
                    discriminator_value: str = cast(str, data.get("binType"))
                    if discriminator_value is not None:
                        if discriminator_value == "CONSTANT":
                            bins_item = AssemblyConstantBin.from_dict(data, strict=False)

                            return bins_item
                        if discriminator_value == "FRAGMENT":
                            bins_item = AssemblyFragmentBin.from_dict(data, strict=False)

                            return bins_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = AssemblyFragmentBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = AssemblyConstantBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                bins_item = _parse_bins_item(bins_item_data)

                bins.append(bins_item)

            return bins

        try:
            bins = get_bins()
        except KeyError:
            if strict:
                raise
            bins = cast(List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]], UNSET)

        def get_constructs() -> List[AssemblySpecSharedConstructsItem]:
            constructs = []
            _constructs = d.pop("constructs")
            for constructs_item_data in _constructs:
                constructs_item = AssemblySpecSharedConstructsItem.from_dict(
                    constructs_item_data, strict=False
                )

                constructs.append(constructs_item)

            return constructs

        try:
            constructs = get_constructs()
        except KeyError:
            if strict:
                raise
            constructs = cast(List[AssemblySpecSharedConstructsItem], UNSET)

        def get_fragments() -> List[AssemblySpecSharedFragmentsItem]:
            fragments = []
            _fragments = d.pop("fragments")
            for fragments_item_data in _fragments:
                fragments_item = AssemblySpecSharedFragmentsItem.from_dict(fragments_item_data, strict=False)

                fragments.append(fragments_item)

            return fragments

        try:
            fragments = get_fragments()
        except KeyError:
            if strict:
                raise
            fragments = cast(List[AssemblySpecSharedFragmentsItem], UNSET)

        def get_topology() -> AssemblySpecSharedTopology:
            _topology = d.pop("topology")
            try:
                topology = AssemblySpecSharedTopology(_topology)
            except ValueError:
                topology = AssemblySpecSharedTopology.of_unknown(_topology)

            return topology

        try:
            topology = get_topology()
        except KeyError:
            if strict:
                raise
            topology = cast(AssemblySpecSharedTopology, UNSET)

        assembly_spec_shared = cls(
            assembly_parameters=assembly_parameters,
            bins=bins,
            constructs=constructs,
            fragments=fragments,
            topology=topology,
        )

        assembly_spec_shared.additional_properties = d
        return assembly_spec_shared

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def assembly_parameters(
        self,
    ) -> Union[
        AssemblyGoldenGateMethod,
        AssemblyGibsonMethod,
        AssemblyHomologyMethod,
        AssemblyConcatenationMethod,
        UnknownType,
    ]:
        """ Assembly-wide parameters to describe requirements and procedures for the assembly. """
        if isinstance(self._assembly_parameters, Unset):
            raise NotPresentError(self, "assembly_parameters")
        return self._assembly_parameters

    @assembly_parameters.setter
    def assembly_parameters(
        self,
        value: Union[
            AssemblyGoldenGateMethod,
            AssemblyGibsonMethod,
            AssemblyHomologyMethod,
            AssemblyConcatenationMethod,
            UnknownType,
        ],
    ) -> None:
        self._assembly_parameters = value

    @property
    def bins(self) -> List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]:
        """Bins are used to group fragments according to their position in the output construct or add a spacer (i.e. constant) region."""
        if isinstance(self._bins, Unset):
            raise NotPresentError(self, "bins")
        return self._bins

    @bins.setter
    def bins(self, value: List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]) -> None:
        self._bins = value

    @property
    def constructs(self) -> List[AssemblySpecSharedConstructsItem]:
        """ Output constructs that should be created. """
        if isinstance(self._constructs, Unset):
            raise NotPresentError(self, "constructs")
        return self._constructs

    @constructs.setter
    def constructs(self, value: List[AssemblySpecSharedConstructsItem]) -> None:
        self._constructs = value

    @property
    def fragments(self) -> List[AssemblySpecSharedFragmentsItem]:
        """ Fragments to be used in the assembly. """
        if isinstance(self._fragments, Unset):
            raise NotPresentError(self, "fragments")
        return self._fragments

    @fragments.setter
    def fragments(self, value: List[AssemblySpecSharedFragmentsItem]) -> None:
        self._fragments = value

    @property
    def topology(self) -> AssemblySpecSharedTopology:
        """ Whether the created constructs should be circular or linear. """
        if isinstance(self._topology, Unset):
            raise NotPresentError(self, "topology")
        return self._topology

    @topology.setter
    def topology(self, value: AssemblySpecSharedTopology) -> None:
        self._topology = value
