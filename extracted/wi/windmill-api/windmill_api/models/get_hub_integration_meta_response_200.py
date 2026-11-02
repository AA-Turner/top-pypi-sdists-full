from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_hub_integration_meta_response_200_metadata_source import (
    GetHubIntegrationMetaResponse200MetadataSource,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_hub_integration_meta_response_200_derived import GetHubIntegrationMetaResponse200Derived
    from ..models.get_hub_integration_meta_response_200_meta import GetHubIntegrationMetaResponse200Meta
    from ..models.get_hub_integration_meta_response_200_resource_types_item import (
        GetHubIntegrationMetaResponse200ResourceTypesItem,
    )


T = TypeVar("T", bound="GetHubIntegrationMetaResponse200")


@_attrs_define
class GetHubIntegrationMetaResponse200:
    """
    Attributes:
        app (str):
        display_name (str):
        description (Union[Unset, None, str]):
        docs_url (Union[Unset, None, str]):
        curated (Union[Unset, None, bool]): whether the script set was pruned to idiomatic actions rather than generated
            one per endpoint; null when nobody has assessed it, which is distinct from a stated false
        metadata_source (Union[Unset, GetHubIntegrationMetaResponse200MetadataSource]): whether the provider knowledge
            was authored (curated) or inferred from the shipped scripts (derived)
        meta (Union[Unset, None, GetHubIntegrationMetaResponse200Meta]): the integration's authored meta.json verbatim;
            the content repo owns its schema, so it is passed through unvalidated
        meta_updated_at (Union[Unset, None, str]):
        derived (Union[Unset, GetHubIntegrationMetaResponse200Derived]): facts computed from the integration's shipped
            scripts
        resource_types (Union[Unset, List['GetHubIntegrationMetaResponse200ResourceTypesItem']]):
    """

    app: str
    display_name: str
    description: Union[Unset, None, str] = UNSET
    docs_url: Union[Unset, None, str] = UNSET
    curated: Union[Unset, None, bool] = UNSET
    metadata_source: Union[Unset, GetHubIntegrationMetaResponse200MetadataSource] = UNSET
    meta: Union[Unset, None, "GetHubIntegrationMetaResponse200Meta"] = UNSET
    meta_updated_at: Union[Unset, None, str] = UNSET
    derived: Union[Unset, "GetHubIntegrationMetaResponse200Derived"] = UNSET
    resource_types: Union[Unset, List["GetHubIntegrationMetaResponse200ResourceTypesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app = self.app
        display_name = self.display_name
        description = self.description
        docs_url = self.docs_url
        curated = self.curated
        metadata_source: Union[Unset, str] = UNSET
        if not isinstance(self.metadata_source, Unset):
            metadata_source = self.metadata_source.value

        meta: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict() if self.meta else None

        meta_updated_at = self.meta_updated_at
        derived: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.derived, Unset):
            derived = self.derived.to_dict()

        resource_types: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resource_types, Unset):
            resource_types = []
            for resource_types_item_data in self.resource_types:
                resource_types_item = resource_types_item_data.to_dict()

                resource_types.append(resource_types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "app": app,
                "display_name": display_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if docs_url is not UNSET:
            field_dict["docs_url"] = docs_url
        if curated is not UNSET:
            field_dict["curated"] = curated
        if metadata_source is not UNSET:
            field_dict["metadata_source"] = metadata_source
        if meta is not UNSET:
            field_dict["meta"] = meta
        if meta_updated_at is not UNSET:
            field_dict["meta_updated_at"] = meta_updated_at
        if derived is not UNSET:
            field_dict["derived"] = derived
        if resource_types is not UNSET:
            field_dict["resource_types"] = resource_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_hub_integration_meta_response_200_derived import GetHubIntegrationMetaResponse200Derived
        from ..models.get_hub_integration_meta_response_200_meta import GetHubIntegrationMetaResponse200Meta
        from ..models.get_hub_integration_meta_response_200_resource_types_item import (
            GetHubIntegrationMetaResponse200ResourceTypesItem,
        )

        d = src_dict.copy()
        app = d.pop("app")

        display_name = d.pop("display_name")

        description = d.pop("description", UNSET)

        docs_url = d.pop("docs_url", UNSET)

        curated = d.pop("curated", UNSET)

        _metadata_source = d.pop("metadata_source", UNSET)
        metadata_source: Union[Unset, GetHubIntegrationMetaResponse200MetadataSource]
        if isinstance(_metadata_source, Unset):
            metadata_source = UNSET
        else:
            metadata_source = GetHubIntegrationMetaResponse200MetadataSource(_metadata_source)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, None, GetHubIntegrationMetaResponse200Meta]
        if _meta is None:
            meta = None
        elif isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = GetHubIntegrationMetaResponse200Meta.from_dict(_meta)

        meta_updated_at = d.pop("meta_updated_at", UNSET)

        _derived = d.pop("derived", UNSET)
        derived: Union[Unset, GetHubIntegrationMetaResponse200Derived]
        if isinstance(_derived, Unset):
            derived = UNSET
        else:
            derived = GetHubIntegrationMetaResponse200Derived.from_dict(_derived)

        resource_types = []
        _resource_types = d.pop("resource_types", UNSET)
        for resource_types_item_data in _resource_types or []:
            resource_types_item = GetHubIntegrationMetaResponse200ResourceTypesItem.from_dict(resource_types_item_data)

            resource_types.append(resource_types_item)

        get_hub_integration_meta_response_200 = cls(
            app=app,
            display_name=display_name,
            description=description,
            docs_url=docs_url,
            curated=curated,
            metadata_source=metadata_source,
            meta=meta,
            meta_updated_at=meta_updated_at,
            derived=derived,
            resource_types=resource_types,
        )

        get_hub_integration_meta_response_200.additional_properties = d
        return get_hub_integration_meta_response_200

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
