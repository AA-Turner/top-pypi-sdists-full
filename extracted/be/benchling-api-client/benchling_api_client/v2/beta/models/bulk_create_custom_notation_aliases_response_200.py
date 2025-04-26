from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_notation_alias import CustomNotationAlias
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkCreateCustomNotationAliasesResponse_200")


@attr.s(auto_attribs=True, repr=False)
class BulkCreateCustomNotationAliasesResponse_200:
    """  """

    _aliases: Union[Unset, List[CustomNotationAlias]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BulkCreateCustomNotationAliasesResponse_200({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aliases, Unset):
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

        bulk_create_custom_notation_aliases_response_200 = cls(
            aliases=aliases,
        )

        bulk_create_custom_notation_aliases_response_200.additional_properties = d
        return bulk_create_custom_notation_aliases_response_200

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
