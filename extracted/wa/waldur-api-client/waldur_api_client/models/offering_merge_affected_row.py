from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingMergeAffectedRow")


@_attrs_define
class OfferingMergeAffectedRow:
    """
    Attributes:
        id (int): Primary key of the row.
        uuid (Union[None, str]): The object's UUID, when it has one.
        model (str): Model label of the row.
        field (str): Column the merge writes.
        description (str): The object described in names rather than primary keys.
        old_value (Union[None, str]): The current value, resolved to a name.
        new_value (Union[None, str]): The value after the merge; null when the row does not change.
        kept_on_source (bool): Whether the row stays with the archived source instead of moving.
    """

    id: int
    uuid: Union[None, str]
    model: str
    field: str
    description: str
    old_value: Union[None, str]
    new_value: Union[None, str]
    kept_on_source: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid: Union[None, str]
        uuid = self.uuid

        model = self.model

        field = self.field

        description = self.description

        old_value: Union[None, str]
        old_value = self.old_value

        new_value: Union[None, str]
        new_value = self.new_value

        kept_on_source = self.kept_on_source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "model": model,
                "field": field,
                "description": description,
                "old_value": old_value,
                "new_value": new_value,
                "kept_on_source": kept_on_source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        uuid = _parse_uuid(d.pop("uuid"))

        model = d.pop("model")

        field = d.pop("field")

        description = d.pop("description")

        def _parse_old_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        old_value = _parse_old_value(d.pop("old_value"))

        def _parse_new_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        new_value = _parse_new_value(d.pop("new_value"))

        kept_on_source = d.pop("kept_on_source")

        offering_merge_affected_row = cls(
            id=id,
            uuid=uuid,
            model=model,
            field=field,
            description=description,
            old_value=old_value,
            new_value=new_value,
            kept_on_source=kept_on_source,
        )

        offering_merge_affected_row.additional_properties = d
        return offering_merge_affected_row

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
