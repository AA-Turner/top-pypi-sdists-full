from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.custom_notation_alias_create import CustomNotationAliasCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationAliasBulkCreate")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationAliasBulkCreate:
    """  """

    _aliases: List[CustomNotationAliasCreate]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationAliasBulkCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aliases = []
        for aliases_item_data in self._aliases:
            aliases_item = aliases_item_data.to_dict()

            aliases.append(aliases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aliases() -> List[CustomNotationAliasCreate]:
            aliases = []
            _aliases = d.pop("aliases")
            for aliases_item_data in _aliases:
                aliases_item = CustomNotationAliasCreate.from_dict(aliases_item_data, strict=False)

                aliases.append(aliases_item)

            return aliases

        try:
            aliases = get_aliases()
        except KeyError:
            if strict:
                raise
            aliases = cast(List[CustomNotationAliasCreate], UNSET)

        custom_notation_alias_bulk_create = cls(
            aliases=aliases,
        )

        custom_notation_alias_bulk_create.additional_properties = d
        return custom_notation_alias_bulk_create

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
    def aliases(self) -> List[CustomNotationAliasCreate]:
        if isinstance(self._aliases, Unset):
            raise NotPresentError(self, "aliases")
        return self._aliases

    @aliases.setter
    def aliases(self, value: List[CustomNotationAliasCreate]) -> None:
        self._aliases = value
