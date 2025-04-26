from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assembly_fragment_bin_bin_type import AssemblyFragmentBinBinType
from ..models.assembly_fragment_bin_fragment_production_method import (
    AssemblyFragmentBinFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyFragmentBin")


@attr.s(auto_attribs=True, repr=False)
class AssemblyFragmentBin:
    """  """

    _bin_type: AssemblyFragmentBinBinType
    _id: str
    _name: str
    _fragment_production_method: Union[Unset, AssemblyFragmentBinFragmentProductionMethod] = UNSET

    def __repr__(self):
        fields = []
        fields.append("bin_type={}".format(repr(self._bin_type)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        return "AssemblyFragmentBin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bin_type = self._bin_type.value

        id = self._id
        name = self._name
        fragment_production_method: Union[Unset, int] = UNSET
        if not isinstance(self._fragment_production_method, Unset):
            fragment_production_method = self._fragment_production_method.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bin_type is not UNSET:
            field_dict["binType"] = bin_type
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bin_type() -> AssemblyFragmentBinBinType:
            _bin_type = d.pop("binType")
            try:
                bin_type = AssemblyFragmentBinBinType(_bin_type)
            except ValueError:
                bin_type = AssemblyFragmentBinBinType.of_unknown(_bin_type)

            return bin_type

        try:
            bin_type = get_bin_type()
        except KeyError:
            if strict:
                raise
            bin_type = cast(AssemblyFragmentBinBinType, UNSET)

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_fragment_production_method() -> Union[Unset, AssemblyFragmentBinFragmentProductionMethod]:
            fragment_production_method = UNSET
            _fragment_production_method = d.pop("fragmentProductionMethod")
            if _fragment_production_method is not None and _fragment_production_method is not UNSET:
                try:
                    fragment_production_method = AssemblyFragmentBinFragmentProductionMethod(
                        _fragment_production_method
                    )
                except ValueError:
                    fragment_production_method = AssemblyFragmentBinFragmentProductionMethod.of_unknown(
                        _fragment_production_method
                    )

            return fragment_production_method

        try:
            fragment_production_method = get_fragment_production_method()
        except KeyError:
            if strict:
                raise
            fragment_production_method = cast(
                Union[Unset, AssemblyFragmentBinFragmentProductionMethod], UNSET
            )

        assembly_fragment_bin = cls(
            bin_type=bin_type,
            id=id,
            name=name,
            fragment_production_method=fragment_production_method,
        )

        return assembly_fragment_bin

    @property
    def bin_type(self) -> AssemblyFragmentBinBinType:
        if isinstance(self._bin_type, Unset):
            raise NotPresentError(self, "bin_type")
        return self._bin_type

    @bin_type.setter
    def bin_type(self, value: AssemblyFragmentBinBinType) -> None:
        self._bin_type = value

    @property
    def id(self) -> str:
        """ Unique identifier for the bin. """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def fragment_production_method(self) -> AssemblyFragmentBinFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(self, value: AssemblyFragmentBinFragmentProductionMethod) -> None:
        self._fragment_production_method = value

    @fragment_production_method.deleter
    def fragment_production_method(self) -> None:
        self._fragment_production_method = UNSET
