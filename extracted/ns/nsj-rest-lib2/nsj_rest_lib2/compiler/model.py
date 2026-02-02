import uuid

from typing import Any


class RelationDependency:
    def __init__(self):
        self.tenant: int | None = None
        self.grupo_empresarial: uuid.UUID | None = None
        self.entity_resource: str | None = None
        self.entity_scope: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "tenant": self.tenant,
            "grupo_empresarial": (
                str(self.grupo_empresarial) if self.grupo_empresarial else None
            ),
            "entity_resource": self.entity_resource,
            "entity_scope": self.entity_scope,
        }

    def from_dict(self, data: dict[str, Any]) -> "RelationDependency":
        self.tenant = data.get("tenant")
        self.grupo_empresarial = (
            uuid.UUID(data["grupo_empresarial"])
            if data.get("grupo_empresarial")
            else None
        )
        self.entity_resource = data.get("entity_resource")
        self.entity_scope = data.get("entity_scope")

        return self


class CompilerResult:
    def __init__(self):
        self.dto_class_name: str | None = None
        self.dto_code: str | None = None
        self.entity_class_name: str | None = None
        self.entity_code: str | None = None
        self.api_expose: bool | None = None
        self.api_resource: str | None = None
        self.api_verbs: list[str] | None = None
        self.service_account: str | None = None
        self.relations_dependencies: list[RelationDependency] | None = None
        self.insert_function_class_name: str | None = None
        self.insert_function_name: str | None = None
        self.source_insert_function: str | None = None
        self.update_function_class_name: str | None = None
        self.update_function_name: str | None = None
        self.source_update_function: str | None = None
        self.get_function_name: str | None = None
        self.list_function_name: str | None = None
        self.delete_function_name: str | None = None
        self.get_function_type_class_name: str | None = None
        self.list_function_type_class_name: str | None = None
        self.delete_function_type_class_name: str | None = None
        self.source_get_function_type: str | None = None
        self.source_list_function_type: str | None = None
        self.source_delete_function_type: str | None = None
        self.retrieve_after_insert: bool | None = None
        self.retrieve_after_update: bool | None = None
        self.retrieve_after_partial_update: bool | None = None
        self.post_response_dto_class_name: str | None = None
        self.put_response_dto_class_name: str | None = None
        self.patch_response_dto_class_name: str | None = None
        self.custom_json_post_response: bool | None = None
        self.custom_json_put_response: bool | None = None
        self.custom_json_patch_response: bool | None = None
        self.custom_json_get_response: bool | None = None
        self.custom_json_list_response: bool | None = None
        self.custom_json_delete_response: bool | None = None
