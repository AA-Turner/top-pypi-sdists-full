from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_concatenation_method import AssemblyConcatenationMethod
from ..models.assembly_constant_bin import AssemblyConstantBin
from ..models.assembly_construct import AssemblyConstruct
from ..models.assembly_fragment_bin import AssemblyFragmentBin
from ..models.assembly_fragment_shared import AssemblyFragmentShared
from ..models.assembly_gibson_method import AssemblyGibsonMethod
from ..models.assembly_golden_gate_method import AssemblyGoldenGateMethod
from ..models.assembly_homology_method import AssemblyHomologyMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinalizedAssembly")


@attr.s(auto_attribs=True, repr=False)
class FinalizedAssembly:
    """  """

    _bins: Union[Unset, List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]] = UNSET
    _constructs: Union[Unset, List[AssemblyConstruct]] = UNSET
    _fragments: Union[Unset, List[AssemblyFragmentShared]] = UNSET
    _method: Union[
        Unset,
        AssemblyGoldenGateMethod,
        AssemblyGibsonMethod,
        AssemblyHomologyMethod,
        AssemblyConcatenationMethod,
        UnknownType,
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("bins={}".format(repr(self._bins)))
        fields.append("constructs={}".format(repr(self._constructs)))
        fields.append("fragments={}".format(repr(self._fragments)))
        fields.append("method={}".format(repr(self._method)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FinalizedAssembly({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bins: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._bins, Unset):
            bins = []
            for bins_item_data in self._bins:
                if isinstance(bins_item_data, UnknownType):
                    bins_item = bins_item_data.value
                elif isinstance(bins_item_data, AssemblyFragmentBin):
                    bins_item = bins_item_data.to_dict()

                else:
                    bins_item = bins_item_data.to_dict()

                bins.append(bins_item)

        constructs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._constructs, Unset):
            constructs = []
            for constructs_item_data in self._constructs:
                constructs_item = constructs_item_data.to_dict()

                constructs.append(constructs_item)

        fragments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._fragments, Unset):
            fragments = []
            for fragments_item_data in self._fragments:
                fragments_item = fragments_item_data.to_dict()

                fragments.append(fragments_item)

        method: Union[Unset, Dict[str, Any]]
        if isinstance(self._method, Unset):
            method = UNSET
        elif isinstance(self._method, UnknownType):
            method = self._method.value
        elif isinstance(self._method, AssemblyGoldenGateMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        elif isinstance(self._method, AssemblyGibsonMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        elif isinstance(self._method, AssemblyHomologyMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        else:
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bins is not UNSET:
            field_dict["bins"] = bins
        if constructs is not UNSET:
            field_dict["constructs"] = constructs
        if fragments is not UNSET:
            field_dict["fragments"] = fragments
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bins() -> Union[Unset, List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]]:
            bins = []
            _bins = d.pop("bins")
            for bins_item_data in _bins or []:

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
            bins = cast(
                Union[Unset, List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]], UNSET
            )

        def get_constructs() -> Union[Unset, List[AssemblyConstruct]]:
            constructs = []
            _constructs = d.pop("constructs")
            for constructs_item_data in _constructs or []:
                constructs_item = AssemblyConstruct.from_dict(constructs_item_data, strict=False)

                constructs.append(constructs_item)

            return constructs

        try:
            constructs = get_constructs()
        except KeyError:
            if strict:
                raise
            constructs = cast(Union[Unset, List[AssemblyConstruct]], UNSET)

        def get_fragments() -> Union[Unset, List[AssemblyFragmentShared]]:
            fragments = []
            _fragments = d.pop("fragments")
            for fragments_item_data in _fragments or []:
                fragments_item = AssemblyFragmentShared.from_dict(fragments_item_data, strict=False)

                fragments.append(fragments_item)

            return fragments

        try:
            fragments = get_fragments()
        except KeyError:
            if strict:
                raise
            fragments = cast(Union[Unset, List[AssemblyFragmentShared]], UNSET)

        def get_method() -> Union[
            Unset,
            AssemblyGoldenGateMethod,
            AssemblyGibsonMethod,
            AssemblyHomologyMethod,
            AssemblyConcatenationMethod,
            UnknownType,
        ]:
            method: Union[
                Unset,
                AssemblyGoldenGateMethod,
                AssemblyGibsonMethod,
                AssemblyHomologyMethod,
                AssemblyConcatenationMethod,
                UnknownType,
            ]
            _method = d.pop("method")

            if not isinstance(_method, Unset):
                discriminator = _method["type"]
                if discriminator == "CONCATENATION":
                    method = AssemblyConcatenationMethod.from_dict(_method)
                elif discriminator == "GIBSON":
                    method = AssemblyGibsonMethod.from_dict(_method)
                elif discriminator == "GOLDEN_GATE":
                    method = AssemblyGoldenGateMethod.from_dict(_method)
                elif discriminator == "HOMOLOGY":
                    method = AssemblyHomologyMethod.from_dict(_method)
                else:
                    method = UnknownType(value=_method)

            return method

        try:
            method = get_method()
        except KeyError:
            if strict:
                raise
            method = cast(
                Union[
                    Unset,
                    AssemblyGoldenGateMethod,
                    AssemblyGibsonMethod,
                    AssemblyHomologyMethod,
                    AssemblyConcatenationMethod,
                    UnknownType,
                ],
                UNSET,
            )

        finalized_assembly = cls(
            bins=bins,
            constructs=constructs,
            fragments=fragments,
            method=method,
        )

        finalized_assembly.additional_properties = d
        return finalized_assembly

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
    def bins(self) -> List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]:
        if isinstance(self._bins, Unset):
            raise NotPresentError(self, "bins")
        return self._bins

    @bins.setter
    def bins(self, value: List[Union[AssemblyFragmentBin, AssemblyConstantBin, UnknownType]]) -> None:
        self._bins = value

    @bins.deleter
    def bins(self) -> None:
        self._bins = UNSET

    @property
    def constructs(self) -> List[AssemblyConstruct]:
        if isinstance(self._constructs, Unset):
            raise NotPresentError(self, "constructs")
        return self._constructs

    @constructs.setter
    def constructs(self, value: List[AssemblyConstruct]) -> None:
        self._constructs = value

    @constructs.deleter
    def constructs(self) -> None:
        self._constructs = UNSET

    @property
    def fragments(self) -> List[AssemblyFragmentShared]:
        if isinstance(self._fragments, Unset):
            raise NotPresentError(self, "fragments")
        return self._fragments

    @fragments.setter
    def fragments(self, value: List[AssemblyFragmentShared]) -> None:
        self._fragments = value

    @fragments.deleter
    def fragments(self) -> None:
        self._fragments = UNSET

    @property
    def method(
        self,
    ) -> Union[
        AssemblyGoldenGateMethod,
        AssemblyGibsonMethod,
        AssemblyHomologyMethod,
        AssemblyConcatenationMethod,
        UnknownType,
    ]:
        if isinstance(self._method, Unset):
            raise NotPresentError(self, "method")
        return self._method

    @method.setter
    def method(
        self,
        value: Union[
            AssemblyGoldenGateMethod,
            AssemblyGibsonMethod,
            AssemblyHomologyMethod,
            AssemblyConcatenationMethod,
            UnknownType,
        ],
    ) -> None:
        self._method = value

    @method.deleter
    def method(self) -> None:
        self._method = UNSET
