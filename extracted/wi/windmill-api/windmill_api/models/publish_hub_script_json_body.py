from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_hub_script_json_body_schema import PublishHubScriptJsonBodySchema


T = TypeVar("T", bound="PublishHubScriptJsonBody")


@_attrs_define
class PublishHubScriptJsonBody:
    """
    Attributes:
        summary (str):
        app (str):
        content (str):
        language (str):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
        description (Union[Unset, str]):
        kind (Union[Unset, str]):
        schema (Union[Unset, PublishHubScriptJsonBodySchema]):
        lockfile (Union[Unset, str]):
        path (Union[Unset, str]):
        source_path (Union[Unset, str]):
    """

    summary: str
    app: str
    content: str
    language: str
    project_slug: str
    description: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    schema: Union[Unset, "PublishHubScriptJsonBodySchema"] = UNSET
    lockfile: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    source_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        app = self.app
        content = self.content
        language = self.language
        project_slug = self.project_slug
        description = self.description
        kind = self.kind
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        lockfile = self.lockfile
        path = self.path
        source_path = self.source_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "app": app,
                "content": content,
                "language": language,
                "project_slug": project_slug,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if kind is not UNSET:
            field_dict["kind"] = kind
        if schema is not UNSET:
            field_dict["schema"] = schema
        if lockfile is not UNSET:
            field_dict["lockfile"] = lockfile
        if path is not UNSET:
            field_dict["path"] = path
        if source_path is not UNSET:
            field_dict["source_path"] = source_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_hub_script_json_body_schema import PublishHubScriptJsonBodySchema

        d = src_dict.copy()
        summary = d.pop("summary")

        app = d.pop("app")

        content = d.pop("content")

        language = d.pop("language")

        project_slug = d.pop("project_slug")

        description = d.pop("description", UNSET)

        kind = d.pop("kind", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, PublishHubScriptJsonBodySchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = PublishHubScriptJsonBodySchema.from_dict(_schema)

        lockfile = d.pop("lockfile", UNSET)

        path = d.pop("path", UNSET)

        source_path = d.pop("source_path", UNSET)

        publish_hub_script_json_body = cls(
            summary=summary,
            app=app,
            content=content,
            language=language,
            project_slug=project_slug,
            description=description,
            kind=kind,
            schema=schema,
            lockfile=lockfile,
            path=path,
            source_path=source_path,
        )

        publish_hub_script_json_body.additional_properties = d
        return publish_hub_script_json_body

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
