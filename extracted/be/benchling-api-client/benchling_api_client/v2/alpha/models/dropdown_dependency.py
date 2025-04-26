from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.base_manifest_config import BaseManifestConfig
from ..models.dropdown_dependency_types import DropdownDependencyTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownDependency")


@attr.s(auto_attribs=True, repr=False)
class DropdownDependency:
    """  """

    _type: DropdownDependencyTypes
    _name: str
    _options: Union[Unset, List[BaseManifestConfig]] = UNSET
    _description: Union[Unset, None, str] = UNSET
    _required_config: Union[Unset, bool] = False

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("options={}".format(repr(self._options)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        return "DropdownDependency({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        name = self._name
        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._options, Unset):
            options = []
            for options_item_data in self._options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        description = self._description
        required_config = self._required_config

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if options is not UNSET:
            field_dict["options"] = options
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> DropdownDependencyTypes:
            _type = d.pop("type")
            try:
                type = DropdownDependencyTypes(_type)
            except ValueError:
                type = DropdownDependencyTypes.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(DropdownDependencyTypes, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_options() -> Union[Unset, List[BaseManifestConfig]]:
            options = []
            _options = d.pop("options")
            for options_item_data in _options or []:
                options_item = BaseManifestConfig.from_dict(options_item_data, strict=False)

                options.append(options_item)

            return options

        try:
            options = get_options()
        except KeyError:
            if strict:
                raise
            options = cast(Union[Unset, List[BaseManifestConfig]], UNSET)

        def get_description() -> Union[Unset, None, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, None, str], UNSET)

        def get_required_config() -> Union[Unset, bool]:
            required_config = d.pop("requiredConfig")
            return required_config

        try:
            required_config = get_required_config()
        except KeyError:
            if strict:
                raise
            required_config = cast(Union[Unset, bool], UNSET)

        dropdown_dependency = cls(
            type=type,
            name=name,
            options=options,
            description=description,
            required_config=required_config,
        )

        return dropdown_dependency

    @property
    def type(self) -> DropdownDependencyTypes:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: DropdownDependencyTypes) -> None:
        self._type = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def options(self) -> List[BaseManifestConfig]:
        if isinstance(self._options, Unset):
            raise NotPresentError(self, "options")
        return self._options

    @options.setter
    def options(self, value: List[BaseManifestConfig]) -> None:
        self._options = value

    @options.deleter
    def options(self) -> None:
        self._options = UNSET

    @property
    def description(self) -> Optional[str]:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def required_config(self) -> bool:
        if isinstance(self._required_config, Unset):
            raise NotPresentError(self, "required_config")
        return self._required_config

    @required_config.setter
    def required_config(self, value: bool) -> None:
        self._required_config = value

    @required_config.deleter
    def required_config(self) -> None:
        self._required_config = UNSET
