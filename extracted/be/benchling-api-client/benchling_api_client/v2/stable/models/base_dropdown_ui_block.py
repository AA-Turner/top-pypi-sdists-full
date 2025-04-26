from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseDropdownUIBlock")


@attr.s(auto_attribs=True, repr=False)
class BaseDropdownUIBlock:
    """  """

    _dropdown_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("dropdown_id={}".format(repr(self._dropdown_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BaseDropdownUIBlock({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dropdown_id = self._dropdown_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dropdown_id is not UNSET:
            field_dict["dropdownId"] = dropdown_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dropdown_id() -> str:
            dropdown_id = d.pop("dropdownId")
            return dropdown_id

        try:
            dropdown_id = get_dropdown_id()
        except KeyError:
            if strict:
                raise
            dropdown_id = cast(str, UNSET)

        base_dropdown_ui_block = cls(
            dropdown_id=dropdown_id,
        )

        base_dropdown_ui_block.additional_properties = d
        return base_dropdown_ui_block

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
    def dropdown_id(self) -> str:
        if isinstance(self._dropdown_id, Unset):
            raise NotPresentError(self, "dropdown_id")
        return self._dropdown_id

    @dropdown_id.setter
    def dropdown_id(self, value: str) -> None:
        self._dropdown_id = value
