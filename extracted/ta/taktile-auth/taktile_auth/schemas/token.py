import typing as t

from pydantic import UUID4, BaseModel, parse_obj_as

from taktile_auth.entities import Permission, Role
from taktile_auth.exceptions import InsufficientRightsException
from taktile_auth.parser import RESOURCES, ROLES
from taktile_auth.parser.utils import parse_permission


class TaktileIdToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: int
    iat: int
    roles: t.List[str]
    actor_name: str | None = None

    @classmethod
    def build_role(cls, role_signature: str) -> Role:
        role_name, _, role_args_str = role_signature.partition("/")
        role_args = role_args_str.split(",") if role_args_str else []
        role_def = ROLES[role_name]
        return ROLES[role_name].build(**dict(zip(role_def.args, role_args)))

    @classmethod
    def build_permission(cls, permission_str: str) -> Permission:
        permission = parse_permission(permission_str)
        resource_vals = {}

        # First, get the resource arguments from the path
        resource_args = permission.get("resource_args", [])
        for i, key in enumerate(
            RESOURCES[permission["resource_name"]].args.keys()
        ):
            if i < len(resource_args):
                resource_vals[key] = resource_args[i]

        # Then, update with any explicit arguments from the permission string
        resource_vals.update(permission.get("args", {}))

        return Permission(
            actions=set(permission["actions"]),
            resource=RESOURCES[permission["resource_name"]].get_resource()(
                **resource_vals
            ),
            resource_name=permission["resource_name"],
        )

    def _is_allowed(
        self, permission_str: str, roles: t.Generator[Role, None, None]
    ) -> None:
        permission = self.build_permission(permission_str)
        if not any(permission in role for role in roles):
            raise InsufficientRightsException

    @property
    def auth_roles(self) -> t.List[Role]:
        return [self.build_role(role) for role in self.roles]

    @property
    def user_id(self) -> UUID4:
        return parse_obj_as(UUID4, self.sub.split(":")[-1])

    def assert_access(self, permission: t.Union[str, t.Sequence[str]]) -> None:
        if isinstance(permission, str):
            permission = [permission]

        for p in permission:
            self._is_allowed(p, (self.build_role(role) for role in self.roles))
