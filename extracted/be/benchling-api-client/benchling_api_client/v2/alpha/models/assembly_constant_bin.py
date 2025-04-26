from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_constant_bin_bin_type import AssemblyConstantBinBinType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyConstantBin")


@attr.s(auto_attribs=True, repr=False)
class AssemblyConstantBin:
    """  """

    _bin_type: AssemblyConstantBinBinType
    _id: str
    _name: str
    _residues: str

    def __repr__(self):
        fields = []
        fields.append("bin_type={}".format(repr(self._bin_type)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("residues={}".format(repr(self._residues)))
        return "AssemblyConstantBin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bin_type = self._bin_type.value

        id = self._id
        name = self._name
        residues = self._residues

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bin_type is not UNSET:
            field_dict["binType"] = bin_type
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if residues is not UNSET:
            field_dict["residues"] = residues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bin_type() -> AssemblyConstantBinBinType:
            _bin_type = d.pop("binType")
            try:
                bin_type = AssemblyConstantBinBinType(_bin_type)
            except ValueError:
                bin_type = AssemblyConstantBinBinType.of_unknown(_bin_type)

            return bin_type

        try:
            bin_type = get_bin_type()
        except KeyError:
            if strict:
                raise
            bin_type = cast(AssemblyConstantBinBinType, UNSET)

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

        def get_residues() -> str:
            residues = d.pop("residues")
            return residues

        try:
            residues = get_residues()
        except KeyError:
            if strict:
                raise
            residues = cast(str, UNSET)

        assembly_constant_bin = cls(
            bin_type=bin_type,
            id=id,
            name=name,
            residues=residues,
        )

        return assembly_constant_bin

    @property
    def bin_type(self) -> AssemblyConstantBinBinType:
        if isinstance(self._bin_type, Unset):
            raise NotPresentError(self, "bin_type")
        return self._bin_type

    @bin_type.setter
    def bin_type(self, value: AssemblyConstantBinBinType) -> None:
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
    def residues(self) -> str:
        """ Base pairs or amino acid residues for the spacer/constant. """
        if isinstance(self._residues, Unset):
            raise NotPresentError(self, "residues")
        return self._residues

    @residues.setter
    def residues(self, value: str) -> None:
        self._residues = value
