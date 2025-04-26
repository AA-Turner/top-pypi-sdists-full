import typing as t

import pydantic

from taktile_auth.entities.resource import Resource, ResourceDefinition
from taktile_auth.enums import Action

PermissionArgs = t.NewType("PermissionArgs", t.Dict[str, str])


class Permission(pydantic.BaseModel):
    actions: t.Set[Action]
    resource: Resource
    resource_name: str

    def __contains__(self, query: "Permission") -> bool:
        if not query.actions.issubset(self.actions):
            return False
        if query.resource_name != self.resource_name:
            return False
        return query.resource in self.resource

    def __repr__(self) -> str:
        actions = "+".join(sorted(self.actions))
        vals = ",".join(self.resource.dict().values())
        return f"{actions}:{self.resource_name}/{vals}"

    def __hash__(self) -> int:
        return hash(
            (
                tuple(sorted(list(self.actions))),
                self.resource_name,
                self.resource,
            )
        )

    class Config:
        arbitrary_types_allowed = True


Permission.update_forward_refs()


class PermissionDefinition(pydantic.BaseModel):
    resource_definition: ResourceDefinition

    def build(self, *, actions: t.Set[Action], **kwargs: str) -> Permission:
        extra_args = {
            arg: "*"
            for arg in set(self.resource_definition.args.keys()).difference(
                kwargs
            )
        }

        return Permission(
            actions=actions,
            resource=self.resource_definition.get_resource()(
                **kwargs, **extra_args
            ),
            resource_name=self.resource_definition.resource_name,
        )

    class Config:
        arbitrary_types_allowed = True
