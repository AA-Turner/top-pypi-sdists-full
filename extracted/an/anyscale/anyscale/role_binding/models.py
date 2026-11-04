from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from anyscale._private.models import ModelBase


_FIND_ROLES = "Find a role's id with 'anyscale role list'."
_FIND_USERS = "Find a user's id with 'anyscale user list'."
_FIND_GROUPS = "Find a group's id with 'anyscale user-group list'."


class AppliedResultUnreadable(Exception):
    """
    The apply was committed and its result could not be read.

    A type of its own rather than a builtin, so nothing raised by the client,
    the HTTP layer or the interpreter can be mistaken for it and report a write
    that never happened.
    """


def require_id(value: str, what: str, how: str) -> str:
    """
    An id, or a refusal that says where to find one.

    Only the shape of the value is judged here. Whether the id names anything
    is the platform's to answer, and it answers it precisely, naming the
    element and whether the role, the user or the group is the one it cannot
    find.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{what}' must be a non-empty string. {how}")
    return value.strip()


def _id_block(ids: Optional[List[str]], what: str, how: str, block: str) -> Optional[List[str]]:
    """
    One block of principal ids, or a refusal naming the block it was in.

    A block says what its ids are, and so does every prefix inside it, so the
    two can disagree. The block wins the argument and the id is refused, since
    putting a group under 'user_id' is a mistake rather than a shorthand.
    """
    if ids is None:
        return None
    if not isinstance(ids, list):
        raise TypeError(f"'{block}' must be a list of ids.")
    built = [require_id(value, what, f"It is under '{block}'. {how}") for value in ids]
    if len(set(built)) != len(built):
        raise ValueError(f"'{block}' names the same {what} more than once.")
    return built


@dataclass(frozen=True)
class PolicyPrincipals(ModelBase):
    """Who holds a role, as one block of user ids and one of user group ids."""

    __doc_py_example__ = """\
from anyscale.role_binding.models import PolicyPrincipals

principals = PolicyPrincipals(user_id=["usr_abc123"], group_id=["ug_abc123"])
"""

    user_id: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "The ids of the users to hold this role. Absent grants it to no user."
        },
    )
    group_id: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "The ids of the user groups to hold this role. Absent grants it to no group."
        },
    )

    def _validate_user_id(self, user_id: Optional[List[str]]) -> Optional[List[str]]:
        return _id_block(user_id, "user", _FIND_USERS, "user_id")

    def _validate_group_id(self, group_id: Optional[List[str]]) -> Optional[List[str]]:
        return _id_block(group_id, "user group", _FIND_GROUPS, "group_id")

    def flattened(self) -> List[Tuple[str, str]]:
        """Every principal as a (type, id) pair, users first."""
        return [("user", value) for value in self.user_id or []] + [
            ("user_group", value) for value in self.group_id or []
        ]


@dataclass(frozen=True)
class PolicyRole(ModelBase):
    """One role and every principal that is to hold it on the resource."""

    __doc_py_example__ = """\
from anyscale.role_binding.models import PolicyPrincipals, PolicyRole

role = PolicyRole(
    role_id="rol_abc123",
    principals=PolicyPrincipals(user_id=["usr_abc123"], group_id=["ug_abc123"]),
)
"""

    role_id: str = field(metadata={"docstring": "The id of a role your organization may assign."})
    principals: PolicyPrincipals = field(
        default_factory=PolicyPrincipals,
        metadata={
            "docstring": "The users and user groups to hold this role, in a block each. Both absent grants it to nobody."
        },
    )

    def _validate_role_id(self, role_id: str) -> str:
        return require_id(role_id, "role", _FIND_ROLES)

    def _validate_principals(self, principals: PolicyPrincipals) -> PolicyPrincipals:
        if isinstance(principals, dict):
            return PolicyPrincipals.from_dict(principals)
        if not isinstance(principals, PolicyPrincipals):
            raise TypeError("'principals' must be a PolicyPrincipals object.")
        return principals


@dataclass(frozen=True)
class RoleBindingPolicy(ModelBase):
    """The permission state of one resource: every role held on it and who holds it.

    Sent to an apply as the state wanted, returned by a generate as the state
    there now, so a generated policy can be applied unchanged.
    """

    __doc_py_example__ = """\
from anyscale.role_binding.models import PolicyPrincipals, PolicyRole, RoleBindingPolicy

policy = RoleBindingPolicy(
    roles=[
        PolicyRole(
            role_id="rol_abc123",
            principals=PolicyPrincipals(user_id=["usr_abc123"], group_id=["ug_abc123"]),
        )
    ]
)
"""

    roles: List[PolicyRole] = field(
        metadata={
            "docstring": (
                "Every role held on the resource. An empty list revokes every role "
                "binding on it, so it has to be sent deliberately: the field is "
                "required, and leaving it out is an error rather than an empty list."
            )
        },
    )

    def _validate_roles(self, roles: List[PolicyRole]) -> List[PolicyRole]:
        if not isinstance(roles, list):
            raise TypeError("'roles' must be a list.")
        built = [PolicyRole.from_dict(role) if isinstance(role, dict) else role for role in roles]
        for role in built:
            if not isinstance(role, PolicyRole):
                raise TypeError("'roles' must hold PolicyRole objects.")
        named = [role.role_id for role in built]
        if len(set(named)) != len(named):
            raise ValueError("'roles' names the same role more than once.")
        return built


@dataclass(frozen=True)
class PolicyChange(ModelBase):
    """One binding an apply created or revoked."""

    __doc_py_example__ = """\
from anyscale.role_binding.models import PolicyChange

change = PolicyChange(role_id="rol_abc123", principal_id="usr_abc123", principal_type="user")
"""

    role_id: str = field(metadata={"docstring": "The id of the role the binding grants."})
    principal_id: str = field(
        metadata={"docstring": "The id of the user or user group holding it."}
    )
    principal_type: str = field(
        metadata={"docstring": "Whether the principal is a 'user' or a 'user_group'."}
    )

    def _validate_role_id(self, role_id: str):
        if not isinstance(role_id, str):
            raise TypeError("'role_id' must be a string.")

    def _validate_principal_id(self, principal_id: str):
        if not isinstance(principal_id, str):
            raise TypeError("'principal_id' must be a string.")

    def _validate_principal_type(self, principal_type: str):
        if principal_type not in ("user", "user_group"):
            raise ValueError("'principal_type' must be 'user' or 'user_group'.")


@dataclass(frozen=True)
class PolicyApplyResult(ModelBase):
    """What an apply changed, or what a dry run would change.

    Both lists empty means the resource already matched the policy.
    """

    __doc_py_example__ = """\
from anyscale.role_binding.models import PolicyApplyResult

result = PolicyApplyResult(granted=[], revoked=[], dry_run=True)
"""

    granted: List[PolicyChange] = field(
        default_factory=list,
        metadata={"docstring": "The bindings the apply created, or would create."},
    )
    revoked: List[PolicyChange] = field(
        default_factory=list,
        metadata={"docstring": "The bindings the apply revoked, or would revoke."},
    )
    dry_run: bool = field(
        default=False,
        metadata={"docstring": "Whether the apply reported without writing anything."},
    )

    def _validate_granted(self, granted: List[PolicyChange]):
        if not isinstance(granted, list):
            raise TypeError("'granted' must be a list.")

    def _validate_revoked(self, revoked: List[PolicyChange]):
        if not isinstance(revoked, list):
            raise TypeError("'revoked' must be a list.")

    def _validate_dry_run(self, dry_run: bool):
        if not isinstance(dry_run, bool):
            raise TypeError("'dry_run' must be a bool.")
