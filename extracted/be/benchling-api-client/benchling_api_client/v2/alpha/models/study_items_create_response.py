from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.study_item import StudyItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyItemsCreateResponse")


@attr.s(auto_attribs=True, repr=False)
class StudyItemsCreateResponse:
    """  """

    _items: Union[Unset, List[StudyItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("items={}".format(repr(self._items)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StudyItemsCreateResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        items: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._items, Unset):
            items = []
            for items_item_data in self._items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_items() -> Union[Unset, List[StudyItem]]:
            items = []
            _items = d.pop("items")
            for items_item_data in _items or []:
                items_item = StudyItem.from_dict(items_item_data, strict=False)

                items.append(items_item)

            return items

        try:
            items = get_items()
        except KeyError:
            if strict:
                raise
            items = cast(Union[Unset, List[StudyItem]], UNSET)

        study_items_create_response = cls(
            items=items,
        )

        study_items_create_response.additional_properties = d
        return study_items_create_response

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
    def items(self) -> List[StudyItem]:
        """ The created study items """
        if isinstance(self._items, Unset):
            raise NotPresentError(self, "items")
        return self._items

    @items.setter
    def items(self, value: List[StudyItem]) -> None:
        self._items = value

    @items.deleter
    def items(self) -> None:
        self._items = UNSET
