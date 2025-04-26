from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_postgres_trigger_json_body_publication import UpdatePostgresTriggerJsonBodyPublication


T = TypeVar("T", bound="UpdatePostgresTriggerJsonBody")


@_attrs_define
class UpdatePostgresTriggerJsonBody:
    """
    Attributes:
        replication_slot_name (str):
        publication_name (str):
        path (str):
        script_path (str):
        is_flow (bool):
        enabled (bool):
        postgres_resource_path (str):
        publication (Union[Unset, UpdatePostgresTriggerJsonBodyPublication]):
    """

    replication_slot_name: str
    publication_name: str
    path: str
    script_path: str
    is_flow: bool
    enabled: bool
    postgres_resource_path: str
    publication: Union[Unset, "UpdatePostgresTriggerJsonBodyPublication"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        replication_slot_name = self.replication_slot_name
        publication_name = self.publication_name
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        enabled = self.enabled
        postgres_resource_path = self.postgres_resource_path
        publication: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.publication, Unset):
            publication = self.publication.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "replication_slot_name": replication_slot_name,
                "publication_name": publication_name,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "enabled": enabled,
                "postgres_resource_path": postgres_resource_path,
            }
        )
        if publication is not UNSET:
            field_dict["publication"] = publication

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_postgres_trigger_json_body_publication import UpdatePostgresTriggerJsonBodyPublication

        d = src_dict.copy()
        replication_slot_name = d.pop("replication_slot_name")

        publication_name = d.pop("publication_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        enabled = d.pop("enabled")

        postgres_resource_path = d.pop("postgres_resource_path")

        _publication = d.pop("publication", UNSET)
        publication: Union[Unset, UpdatePostgresTriggerJsonBodyPublication]
        if isinstance(_publication, Unset):
            publication = UNSET
        else:
            publication = UpdatePostgresTriggerJsonBodyPublication.from_dict(_publication)

        update_postgres_trigger_json_body = cls(
            replication_slot_name=replication_slot_name,
            publication_name=publication_name,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            enabled=enabled,
            postgres_resource_path=postgres_resource_path,
            publication=publication,
        )

        update_postgres_trigger_json_body.additional_properties = d
        return update_postgres_trigger_json_body

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
