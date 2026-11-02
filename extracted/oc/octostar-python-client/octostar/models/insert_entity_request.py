from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import cast, List
from typing import Dict
from typing import cast

if TYPE_CHECKING:
    from ..models.insert_entity import InsertEntity


T = TypeVar("T", bound="InsertEntityRequest")


@attr.s(auto_attribs=True)
class InsertEntityRequest:
    """Entities to insert.

    ### Attributes:
    * `entities (List['InsertEntity'])`: None
    """

    entities: List["InsertEntity"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.insert_entity import InsertEntity

        entities = []
        for entities_item_data in self.entities:
            entities_item = entities_item_data.to_dict()

            entities.append(entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entities": entities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.insert_entity import InsertEntity

        d = src_dict.copy()
        entities = []
        _entities = d.pop("entities")
        for entities_item_data in _entities:
            entities_item = InsertEntity.from_dict(entities_item_data)

            entities.append(entities_item)

        insert_entity_request = cls(
            entities=entities,
        )

        insert_entity_request.additional_properties = d
        return insert_entity_request

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
