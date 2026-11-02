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
    List,
    Union,
    cast,
)

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.upsert_entity_relationships_item import UpsertEntityRelationshipsItem
    from ..models.upsert_entity_base import UpsertEntityBase


T = TypeVar("T", bound="UpsertEntity")


@attr.s(auto_attribs=True)
class UpsertEntity:
    """
    ### Attributes:
    * `entity (Union[Unset, UpsertEntityBase])`:
    * `relationships (Union[Unset, List['UpsertEntityRelationshipsItem']])`: None
    """

    entity: Union[Unset, "UpsertEntityBase"] = UNSET
    relationships: Union[Unset, List["UpsertEntityRelationshipsItem"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.upsert_entity_relationships_item import (
            UpsertEntityRelationshipsItem,
        )
        from ..models.upsert_entity_base import UpsertEntityBase

        entity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity, Unset):
            entity = self.entity.to_dict()

        relationships: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = []
            for relationships_item_data in self.relationships:
                relationships_item = relationships_item_data.to_dict()

                relationships.append(relationships_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entity is not UNSET:
            field_dict["entity"] = entity
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.upsert_entity_relationships_item import (
            UpsertEntityRelationshipsItem,
        )
        from ..models.upsert_entity_base import UpsertEntityBase

        d = src_dict.copy()
        _entity = d.pop("entity", UNSET)
        entity: Union[Unset, UpsertEntityBase]
        if isinstance(_entity, Unset):
            entity = UNSET
        else:
            entity = UpsertEntityBase.from_dict(_entity)

        relationships = []
        _relationships = d.pop("relationships", UNSET)
        for relationships_item_data in _relationships or []:
            relationships_item = UpsertEntityRelationshipsItem.from_dict(
                relationships_item_data
            )

            relationships.append(relationships_item)

        upsert_entity = cls(
            entity=entity,
            relationships=relationships,
        )

        upsert_entity.additional_properties = d
        return upsert_entity

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
