import re
import time
import typing as t

from pydantic import UUID4, BaseModel, parse_obj_as

from taktile_auth._logging import get_logger
from taktile_auth._metrics import emit_metric
from taktile_auth.entities import Permission, Role
from taktile_auth.entities.role import RoleDefinition
from taktile_auth.exceptions import InsufficientRightsException
from taktile_auth.parser import RESOURCES, ROLES
from taktile_auth.parser.utils import parse_permission

logger = get_logger()


def _arg_matches(role_value: str, filter_value: str) -> bool:
    """Check if a role argument value matches the filter value.

    Uses regex matching consistent with resource containment logic.
    A role value of "*" becomes ".*" matching anything.
    """
    return bool(re.fullmatch(role_value.replace("*", ".*"), filter_value))


class TaktileIdToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: int
    iat: int
    roles: t.List[str]
    actor_name: str | None = None
    workspace_id: str | None = None
    org_id: str | None = None

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

        if permission["resource_name"] not in RESOURCES:
            # by default we deny access to non-existing resources
            raise InsufficientRightsException

        # First, get the resource arguments from the path
        resource_args = permission.get("resource_args", [])
        for i, key in enumerate(RESOURCES[permission["resource_name"]].args.keys()):
            if i < len(resource_args):
                resource_vals[key] = resource_args[i]

        # Then, update with any explicit arguments from the permission string
        resource_vals.update(permission.get("args", {}))

        return Permission(
            actions=set(permission["actions"]),
            resource=RESOURCES[permission["resource_name"]].get_resource()(**resource_vals),
            resource_name=permission["resource_name"],
        )

    def _is_allowed(self, permission_str: str, roles: t.Generator[Role, None, None]) -> None:
        permission = self.build_permission(permission_str)
        if not any(permission in role for role in roles):
            raise InsufficientRightsException

    @property
    def auth_roles(self) -> t.List[Role]:
        # only filter roles that are defined in the ROLES dict
        return [self.build_role(role) for role in self.roles if role.split("/")[0] in ROLES]

    @property
    def user_id(self) -> UUID4:
        return parse_obj_as(UUID4, self.sub.split(":")[-1])

    _SCOPE_DIMS: t.ClassVar[t.Tuple[str, ...]] = ("org_id", "ws_id")

    @classmethod
    def _filter_one_role(
        cls,
        role_def: RoleDefinition,
        role_args: t.Dict[str, str],
        filters: t.Dict[str, str],
        target_roles: t.Optional[t.FrozenSet[str]] = None,
    ) -> t.List[t.Tuple[RoleDefinition, t.Dict[str, str]]]:
        """Filter one role against (org_id, ws_id) constraints.

        - Role declares a scope dim: narrow each declared dim against
          the filter; drop on concrete mismatch. Dims not declared are
          left alone.
        - Role declares no scope dim: walk sub_role_definitions and
          recurse. A role with non-scope args and no sub-roles is
          dropped — fail-closed default for future roles that don't
          opt into scope-awareness.

        With ``target_roles`` set, the stop condition changes: walk
        every non-matching role's sub-role tree (even through scoped
        roles) until a requested role is found, then narrow it as
        above. A non-matching leaf is dropped, so the token can never
        reach a role that is not in (or below) what it already holds.
        """
        declared_scope = set(role_def.args) & set(cls._SCOPE_DIMS)

        if target_roles is None:
            stop_and_narrow = bool(declared_scope)
        else:
            stop_and_narrow = role_def.name in target_roles

        if stop_and_narrow:
            narrowed = dict(role_args)
            for dim in declared_scope:
                target = filters.get(dim)
                if target is None:
                    continue
                if not _arg_matches(role_args.get(dim, ""), target):
                    return []
                narrowed[dim] = target
            return [(role_def, narrowed)]

        results: t.List[t.Tuple[RoleDefinition, t.Dict[str, str]]] = []
        for sub_def in role_def.sub_role_definitions:
            sub_args = dict(role_args)
            for arg in sub_def.args:
                if arg not in sub_args:
                    sub_args[arg] = "*"
            results.extend(cls._filter_one_role(sub_def, sub_args, filters, target_roles))
        return results

    def filter_roles(
        self,
        *,
        org_id: t.Optional[str] = None,
        ws_id: t.Optional[str] = None,
        role_names: t.Optional[t.Sequence[str]] = None,
    ) -> t.List[Role]:
        """Filter token roles by org_id, ws_id and/or role names in a
        single pass.

        ``role_names`` subsets to the named roles: each token role is
        expanded down its sub-role inheritance tree until a requested
        role is found, which is then narrowed against ``org_id`` /
        ``ws_id``. Roles whose subtree contains none of the requested
        names are dropped (fail-closed), so this can only ever narrow
        — never escalate — the token's authority. An empty sequence
        matches nothing; unknown names raise ``ValueError``.
        """
        if role_names is not None:
            unknown = [name for name in role_names if name not in ROLES]
            if unknown:
                raise ValueError(f"Unknown role names: {sorted(unknown)}")

        filters: t.Dict[str, str] = {}
        if org_id is not None:
            filters["org_id"] = org_id
        if ws_id is not None:
            filters["ws_id"] = ws_id

        if not filters and role_names is None:
            return self.auth_roles

        candidates: t.List[t.Tuple[RoleDefinition, t.Dict[str, str]]] = []
        for role_str in self.roles:
            role_name = role_str.split("/")[0]
            if role_name not in ROLES:
                continue
            role_def = ROLES[role_name]
            role_args_str = role_str.partition("/")[2]
            role_args_list = role_args_str.split(",") if role_args_str else []
            candidates.append((role_def, dict(zip(role_def.args, role_args_list))))

        target_roles = frozenset(role_names) if role_names is not None else None
        expanded: t.List[t.Tuple[RoleDefinition, t.Dict[str, str]]] = []
        for role_def, role_kwargs in candidates:
            expanded.extend(self._filter_one_role(role_def, role_kwargs, filters, target_roles))
        candidates = expanded

        seen: t.Set[str] = set()
        results: t.List[Role] = []
        for role_def, role_kwargs in candidates:
            key = role_def.name + "/" + ",".join(role_kwargs.get(a, "*") for a in role_def.args)
            if key not in seen:
                seen.add(key)
                results.append(role_def.build(**role_kwargs))

        return results

    def assert_access(self, permission: t.Union[str, t.Sequence[str]]) -> None:
        t0 = time.perf_counter()
        if isinstance(permission, str):
            permission = [permission]

        allowed = True
        try:
            for p in permission:
                self._is_allowed(
                    p,
                    (self.build_role(role) for role in self.roles if role.split("/")[0] in ROLES),
                )
        except InsufficientRightsException:
            allowed = False
            raise
        finally:
            duration_ms = (time.perf_counter() - t0) * 1000
            emit_metric(
                "AssertAccessDuration",
                duration_ms,
                {"Allowed": str(allowed)},
            )

    def has_access(self, permission: t.Union[str, t.Sequence[str]]) -> bool:
        """Like ``assert_access``, but returns a boolean instead of raising."""
        try:
            self.assert_access(permission)
        except InsufficientRightsException:
            return False
        return True

    def assert_access_with_fallback(
        self,
        permission: t.Union[str, t.Sequence[str]],
        *,
        fallback_permission: t.Union[str, t.Sequence[str], None] = None,
    ) -> None:
        """Assert access against a new permission with an optional fallback.

        Access is granted if either the new permission or the fallback
        (old) permission allows it. Any disagreement between the two is
        logged as a warning so rule divergences can be found before the
        new rules are enforced exclusively. Without a fallback, this is
        equivalent to ``assert_access``.
        """
        if fallback_permission is None:
            self.assert_access(permission)
            return

        allowed = self.has_access(permission)
        fallback_allowed = self.has_access(fallback_permission)

        if allowed != fallback_allowed:
            logger.warning(
                "authz-discrepancy: permission and fallback disagree",
                extra={
                    "permission": permission,
                    "fallback_permission": fallback_permission,
                    "permission_allowed": allowed,
                    "fallback_allowed": fallback_allowed,
                    "sub": self.sub,
                    "roles": self.roles,
                },
            )

        if not allowed and not fallback_allowed:
            raise InsufficientRightsException
