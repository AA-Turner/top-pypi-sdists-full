from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySpecSharedConstructsItem")


@attr.s(auto_attribs=True, repr=False)
class AssemblySpecSharedConstructsItem:
    """  """

    _fragments: List[str]
    _id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("fragments={}".format(repr(self._fragments)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblySpecSharedConstructsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fragments = self._fragments

        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fragments is not UNSET:
            field_dict["fragments"] = fragments
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fragments() -> List[str]:
            fragments = cast(List[str], d.pop("fragments"))

            return fragments

        try:
            fragments = get_fragments()
        except KeyError:
            if strict:
                raise
            fragments = cast(List[str], UNSET)

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        assembly_spec_shared_constructs_item = cls(
            fragments=fragments,
            id=id,
        )

        assembly_spec_shared_constructs_item.additional_properties = d
        return assembly_spec_shared_constructs_item

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
    def fragments(self) -> List[str]:
        """ Ordered list of fragment IDs to use in creating the construct, or a special option (SKIP) to indicate a bin should be skipped. """
        if isinstance(self._fragments, Unset):
            raise NotPresentError(self, "fragments")
        return self._fragments

    @fragments.setter
    def fragments(self, value: List[str]) -> None:
        self._fragments = value

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value
