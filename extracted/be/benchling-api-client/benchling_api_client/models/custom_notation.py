from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_notation_alias import CustomNotationAlias
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotation")


@attr.s(auto_attribs=True, repr=False)
class CustomNotation:
    """  """

    _aliases: Union[Unset, List[CustomNotationAlias]] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotation({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aliases, Unset):
            aliases = []
            for aliases_item_data in self._aliases:
                aliases_item = aliases_item_data.to_dict()

                aliases.append(aliases_item)

        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aliases() -> Union[Unset, List[CustomNotationAlias]]:
            aliases = []
            _aliases = d.pop("aliases")
            for aliases_item_data in _aliases or []:
                aliases_item = CustomNotationAlias.from_dict(aliases_item_data, strict=False)

                aliases.append(aliases_item)

            return aliases

        try:
            aliases = get_aliases()
        except KeyError:
            if strict:
                raise
            aliases = cast(Union[Unset, List[CustomNotationAlias]], UNSET)

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

        custom_notation = cls(
            aliases=aliases,
            id=id,
            name=name,
        )

        custom_notation.additional_properties = d
        return custom_notation

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
    def aliases(self) -> List[CustomNotationAlias]:
        if isinstance(self._aliases, Unset):
            raise NotPresentError(self, "aliases")
        return self._aliases

    @aliases.setter
    def aliases(self, value: List[CustomNotationAlias]) -> None:
        self._aliases = value

    @aliases.deleter
    def aliases(self) -> None:
        self._aliases = UNSET

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
