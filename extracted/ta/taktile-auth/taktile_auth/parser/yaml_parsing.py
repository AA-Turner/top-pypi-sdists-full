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


def parse_role(
    role_signature: str,
    role_yaml: t.Dict[str, t.Any],
    resources: t.Dict[str, ResourceDefinition],
) -> RoleDefinition:
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

            perm_definitions.append(
                (
                    set(clause["actions"]),
                    PermissionDefinition(
                        resource_definition=resources[clause["resource_name"]],
                    ),
                    perm_args,
                )
            )
        else:
            # For sub-roles, we need to find the full signature
            sub_role_name = clause["sub_role_name"]
            matching_signatures = [
                sig
                for sig in role_yaml.keys()
                if sig.split("/")[0] == sub_role_name.split("/")[0]
            ]
            if not matching_signatures:
                raise KeyError(
                    f"Sub-role {sub_role_name} not found in role definitions"
                )

            sub_role_definitions.append(
                parse_role(matching_signatures[0], role_yaml, resources)
            )

    return RoleDefinition(
        name=role_name,
        permission_definitions=perm_definitions,
        args=role_args,
        sub_role_definitions=sub_role_definitions,
    )


def parse_resource_yaml(path: pathlib.Path) -> t.Dict[str, ResourceDefinition]:
    with open(path, "r") as f:
        resources_yaml = yaml.safe_load(f)
    resources: t.Dict[str, ResourceDefinition] = {}
    for resource_name, args in resources_yaml.items():
        resources[resource_name] = ResourceDefinition(
            resource_name=resource_name, args=args
        )
    return resources


def parse_role_yaml(
    role_path: pathlib.Path, resource_path: pathlib.Path
) -> t.Dict[str, RoleDefinition]:
    resources = parse_resource_yaml(resource_path)
    with open(role_path, "r") as f:
        roles_raw: t.Dict[str, t.Any] = yaml.safe_load(f)

    role_yaml = {}
    for role_signature, role_body in roles_raw.items():
        if isinstance(role_body, list):
            _, _, role_args_str = role_signature.partition("/")
            role_args = role_args_str.split(",") if role_args_str else []
            role_yaml[role_signature] = {
                "role_args": role_args,
                "role_body": role_body,
            }

    return {
        role_signature.split("/")[0]: parse_role(
            role_signature, role_yaml, resources
        )
        for role_signature in role_yaml.keys()
    }
