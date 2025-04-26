from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assembly_shared_assembly_type import AssemblySharedAssemblyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyShared")


@attr.s(auto_attribs=True, repr=False)
class AssemblyShared:
    """  """

    _assembly_type: Union[Unset, AssemblySharedAssemblyType] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("assembly_type={}".format(repr(self._assembly_type)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblyShared({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assembly_type: Union[Unset, int] = UNSET
        if not isinstance(self._assembly_type, Unset):
            assembly_type = self._assembly_type.value

        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assembly_type is not UNSET:
            field_dict["assemblyType"] = assembly_type
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assembly_type() -> Union[Unset, AssemblySharedAssemblyType]:
            assembly_type = UNSET
            _assembly_type = d.pop("assemblyType")
            if _assembly_type is not None and _assembly_type is not UNSET:
                try:
                    assembly_type = AssemblySharedAssemblyType(_assembly_type)
                except ValueError:
                    assembly_type = AssemblySharedAssemblyType.of_unknown(_assembly_type)

            return assembly_type

        try:
            assembly_type = get_assembly_type()
        except KeyError:
            if strict:
                raise
            assembly_type = cast(Union[Unset, AssemblySharedAssemblyType], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        assembly_shared = cls(
            assembly_type=assembly_type,
            id=id,
            name=name,
        )

        assembly_shared.additional_properties = d
        return assembly_shared

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
    def assembly_type(self) -> AssemblySharedAssemblyType:
        if isinstance(self._assembly_type, Unset):
            raise NotPresentError(self, "assembly_type")
        return self._assembly_type

    @assembly_type.setter
    def assembly_type(self, value: AssemblySharedAssemblyType) -> None:
        self._assembly_type = value

    @assembly_type.deleter
    def assembly_type(self) -> None:
        self._assembly_type = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
