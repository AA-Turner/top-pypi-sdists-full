import typing as t
from collections import defaultdict

import pydantic

from taktile_auth.entities.permission import (
    Permission,
    PermissionArgs,
    PermissionDefinition,
)
from taktile_auth.entities.resource import Resource
from taktile_auth.enums import Action


class Role(pydantic.BaseModel):
    name: str
    args: t.Dict[str, str]
    arg_list: t.List[str]
    permissions: t.List[Permission]
    sub_roles: t.List["Role"]

    def __contains__(self, query: Permission) -> bool:
        for permission in self.permissions:
            if query in permission:
                return True
        return False

    def get_all_permissions(self) -> t.Set[Permission]:
        """Return all permissions this role has

        Parameters
        ----------

        Returns
        -------
        t.Set[Permission]

        """
        direct_perms = {perm for perm in self.permissions}
        indirect_perms = {
            perm
            for role in self.sub_roles
            for perm in role.get_all_permissions()
        }
        all_perms = direct_perms.union(indirect_perms)

        deduplicate_dict: t.Dict[t.Tuple[str, Resource], t.Set[Action]] = (
            defaultdict(set)
        )
        for perm in all_perms:
            deduplicate_dict[(perm.resource_name, perm.resource)] = (
                deduplicate_dict[(perm.resource_name, perm.resource)].union(
                    perm.actions
                )
            )

        return {
            Permission(actions=actions, resource=res, resource_name=name)
            for (name, res), actions in deduplicate_dict.items()
        }

    def __repr__(self) -> str:
        return self.name + "/" + ",".join(self.args[x] for x in self.arg_list)

    class Config:
        arbitrary_types_allowed = True


Role.update_forward_refs()


class RoleDefinition(pydantic.BaseModel):
    name: str
    permission_definitions: t.List[
        t.Tuple[t.Set[Action], PermissionDefinition, PermissionArgs]
    ]
    args: t.List[str]
    sub_role_definitions: t.List["RoleDefinition"]

    def build(self, **kwargs: str) -> Role:
        assert set(self.args).issubset(set(kwargs.keys()))
        # Flattening Permissions to include those from sub_role
        perm_map: t.Dict[Resource, t.Set[Action]] = defaultdict(set)
        for (
            actions,
            permission_definition,
            perm_args,
        ) in self.permission_definitions:
            # Merge role kwargs with permission args,
            # permission args take precedence
            merged_args = {**kwargs, **perm_args}
            perm = permission_definition.build(actions=actions, **merged_args)
            perm_map[perm.resource] = perm_map[perm.resource].union(
                perm.actions
            )
        sub_roles = []
        for sub_role_definition in self.sub_role_definitions:
            extra_args = {
                arg: "*"
                for arg in set(sub_role_definition.args).difference(self.args)
            }
            sub_role = sub_role_definition.build(**kwargs, **extra_args)
            sub_roles.append(sub_role)
            for perm in sub_role.permissions:
                perm_map[perm.resource] = perm_map[perm.resource].union(
                    perm.actions
                )
        permissions = []
        for resource, actions in perm_map.items():
            permissions.append(
                Permission(
                    actions=actions,
                    resource=resource,
                    resource_name=type(resource).__name__,
                )
            )
        return Role(
            name=self.name,
            arg_list=self.args,
            args=kwargs,
            permissions=permissions,
            sub_roles=sub_roles,
        )

    class Config:
        arbitrary_types_allowed = True


RoleDefinition.update_forward_refs()
