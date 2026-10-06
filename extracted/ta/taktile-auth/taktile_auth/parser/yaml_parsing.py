import pathlib
import typing as t

import yaml

from taktile_auth.entities import (
    PermissionDefinition,
    ResourceDefinition,
    RoleDefinition,
)
from taktile_auth.entities.permission import PermissionArgs
from taktile_auth.parser.utils import parse_body

_YamlLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def parse_role(
    role_signature: str,
    role_yaml: t.Dict[str, t.Any],
    resources: t.Dict[str, ResourceDefinition],
    role_cache: t.Optional[t.Dict[str, RoleDefinition]] = None,
) -> RoleDefinition:
    if role_cache is None:
        role_cache = {}
    if role_signature in role_cache:
        return role_cache[role_signature]
    perm_definitions = []
    sub_role_definitions = []

    role_entry = role_yaml.get(role_signature)
    if role_entry is None:
        raise KeyError(f"Role {role_signature} not found in role definitions")

    role_name = role_signature.split("/")[0]
    role_args = role_entry["role_args"]
    role_body = role_entry["role_body"]
    clauses = parse_body(role_body)

    for clause in clauses:
        if clause["type"] == "permission":
            perm_args = PermissionArgs({})
            if "args" in clause:
                perm_args = clause["args"]

            resource_definition = resources[clause["resource_name"]]
            resource_definition.assert_actions_allowed(clause["actions"])

            perm_definitions.append(
                (
                    set(clause["actions"]),
                    PermissionDefinition(
                        resource_definition=resource_definition,
                    ),
                    perm_args,
                )
            )
        else:
            # For sub-roles, we need to find the full signature
            sub_role_name = clause["sub_role_name"]
            matching_signatures = [sig for sig in role_yaml.keys() if sig.split("/")[0] == sub_role_name.split("/")[0]]
            if not matching_signatures:
                raise KeyError(f"Sub-role {sub_role_name} not found in role definitions")

            sub_role_definitions.append(parse_role(matching_signatures[0], role_yaml, resources, role_cache))

    role_cache[role_signature] = RoleDefinition(
        name=role_name,
        permission_definitions=perm_definitions,
        args=role_args,
        sub_role_definitions=sub_role_definitions,
    )
    return role_cache[role_signature]


def parse_resource_yaml(path: pathlib.Path) -> t.Dict[str, ResourceDefinition]:
    with open(path, "r") as f:
        resources_yaml = yaml.load(f, Loader=_YamlLoader)
    resources: t.Dict[str, ResourceDefinition] = {}
    for resource_name, body in resources_yaml.items():
        args = dict(filter(lambda entry: entry[0] != "additional_actions", body.items()))
        resources[resource_name] = ResourceDefinition(
            resource_name=resource_name,
            args=args,
            additional_actions=body.get("additional_actions", []),
        )
    return resources


def parse_role_yaml(role_path: pathlib.Path, resources: t.Dict[str, ResourceDefinition]) -> t.Dict[str, RoleDefinition]:
    with open(role_path, "r") as f:
        roles_raw: t.Dict[str, t.Any] = yaml.load(f, Loader=_YamlLoader)

    role_yaml = {}
    for role_signature, role_body in roles_raw.items():
        if isinstance(role_body, list):
            _, _, role_args_str = role_signature.partition("/")
            role_args = role_args_str.split(",") if role_args_str else []
            role_yaml[role_signature] = {
                "role_args": role_args,
                "role_body": role_body,
            }

    role_cache: t.Dict[str, RoleDefinition] = {}
    return {
        role_signature.split("/")[0]: parse_role(role_signature, role_yaml, resources, role_cache)
        for role_signature in role_yaml.keys()
    }
