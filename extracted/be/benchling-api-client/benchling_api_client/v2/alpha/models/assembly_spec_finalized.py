from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_spec_finalized_output_location import AssemblySpecFinalizedOutputLocation
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySpecFinalized")


@attr.s(auto_attribs=True, repr=False)
class AssemblySpecFinalized:
    """ Additional information required when creating and finalizing a bulk assembly. """

    _folder_id: str
    _name: str
    _output_location: AssemblySpecFinalizedOutputLocation
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("output_location={}".format(repr(self._output_location)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblySpecFinalized({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self._folder_id
        name = self._name
        output_location = self._output_location.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if output_location is not UNSET:
            field_dict["outputLocation"] = output_location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_folder_id() -> str:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_output_location() -> AssemblySpecFinalizedOutputLocation:
            output_location = AssemblySpecFinalizedOutputLocation.from_dict(
                d.pop("outputLocation"), strict=False
            )

            return output_location

        try:
            output_location = get_output_location()
        except KeyError:
            if strict:
                raise
            output_location = cast(AssemblySpecFinalizedOutputLocation, UNSET)

        assembly_spec_finalized = cls(
            folder_id=folder_id,
            name=name,
            output_location=output_location,
        )

        assembly_spec_finalized.additional_properties = d
        return assembly_spec_finalized

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
    def folder_id(self) -> str:
        """ API identifier of the folder in which the assembly should be created. """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @property
    def name(self) -> str:
        """ Name of the bulk assembly. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def output_location(self) -> AssemblySpecFinalizedOutputLocation:
        if isinstance(self._output_location, Unset):
            raise NotPresentError(self, "output_location")
        return self._output_location

    @output_location.setter
    def output_location(self, value: AssemblySpecFinalizedOutputLocation) -> None:
        self._output_location = value
