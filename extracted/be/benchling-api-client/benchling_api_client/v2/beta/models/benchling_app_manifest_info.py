from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppManifestInfo")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppManifestInfo:
    """  """

    _description: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _version: Union[Unset, str] = "0.0.1"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("description={}".format(repr(self._description)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("version={}".format(repr(self._version)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BenchlingAppManifestInfo({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        description = self._description
        name = self._name
        version = self._version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_version() -> Union[Unset, str]:
            version = d.pop("version")
            return version

        try:
            version = get_version()
        except KeyError:
            if strict:
                raise
            version = cast(Union[Unset, str], UNSET)

        benchling_app_manifest_info = cls(
            description=description,
            name=name,
            version=version,
        )

        benchling_app_manifest_info.additional_properties = d
        return benchling_app_manifest_info

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
    def description(self) -> str:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

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

    @property
    def version(self) -> str:
        """ A semver string for the version of the benchling app described by this manifest. """
        if isinstance(self._version, Unset):
            raise NotPresentError(self, "version")
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._version = value

    @version.deleter
    def version(self) -> None:
        self._version = UNSET
