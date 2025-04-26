import typing as t

from taktile_auth.entities import ResourceDefinition, RoleDefinition
from taktile_auth.parser.yaml_parsing import (
    parse_resource_yaml,
    parse_role_yaml,
)
from taktile_auth.settings import settings

RESOURCES: t.Dict[str, ResourceDefinition] = parse_resource_yaml(
    settings.RESOURCE_PATH
)
ROLES: t.Dict[str, RoleDefinition] = parse_role_yaml(
    settings.ROLE_PATH, settings.RESOURCE_PATH
)
