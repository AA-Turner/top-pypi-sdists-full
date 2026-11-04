from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.role_binding._private.role_binding_sdk import PrivateRoleBindingSDK
from anyscale.role_binding.models import PolicyApplyResult, RoleBindingPolicy


_ROLE_BINDING_SDK_SINGLETON_KEY = "role_binding_sdk"

_GENERATE_EXAMPLE = """
import anyscale

# Generate the policy of a cloud, every role and principal by id
policy = anyscale.role_binding.generate_policy(
    resource_type="cloud", resource_id="cld_abc123",
)
for role in policy.roles:
    for principal_type, principal_id in role.principals.flattened():
        print(role.role_id, principal_id, principal_type)
"""

_GENERATE_ARG_DOCSTRINGS = {
    "resource_type": "Resource type ('cloud', 'project', or 'organization').",
    "resource_id": "Resource ID (e.g., cld_abc123, prj_xyz789). Your own organization when the type is 'organization' and none is given.",
}

_APPLY_EXAMPLE = """
import anyscale
from anyscale.role_binding.models import PolicyPrincipals, PolicyRole, RoleBindingPolicy

policy = RoleBindingPolicy(
    roles=[
        PolicyRole(
            role_id="rol_abc123",
            principals=PolicyPrincipals(user_id=["usr_abc123"], group_id=["ug_abc123"]),
        ),
    ]
)

# See what would change before committing to it
preview = anyscale.role_binding.apply_policy(
    resource_type="cloud", resource_id="cld_abc123", policy=policy, dry_run=True,
)
print(len(preview.granted), "granted,", len(preview.revoked), "revoked")

# Then make the resource match
anyscale.role_binding.apply_policy(
    resource_type="cloud", resource_id="cld_abc123", policy=policy,
)
"""

_APPLY_ARG_DOCSTRINGS = {
    "resource_type": "Resource type ('cloud', 'project', or 'organization').",
    "resource_id": "Resource ID (e.g., cld_abc123, prj_xyz789). Your own organization when the type is 'organization' and none is given.",
    "policy": "The permission state wanted for the resource.",
    "dry_run": "Report what the apply would change, and change nothing.",
}


@sdk_command(
    _ROLE_BINDING_SDK_SINGLETON_KEY,
    PrivateRoleBindingSDK,
    doc_py_example=_GENERATE_EXAMPLE,
    arg_docstrings=_GENERATE_ARG_DOCSTRINGS,
)
def generate_policy(
    resource_type: str,
    resource_id: Optional[str] = None,
    *,
    _private_sdk: PrivateRoleBindingSDK,
) -> RoleBindingPolicy:
    """Generate the role bindings a resource holds, in the shape an apply accepts."""
    return _private_sdk.generate_policy(resource_type=resource_type, resource_id=resource_id)


@sdk_command(
    _ROLE_BINDING_SDK_SINGLETON_KEY,
    PrivateRoleBindingSDK,
    doc_py_example=_APPLY_EXAMPLE,
    arg_docstrings=_APPLY_ARG_DOCSTRINGS,
)
def apply_policy(
    resource_type: str,
    policy: RoleBindingPolicy,
    resource_id: Optional[str] = None,
    dry_run: bool = False,
    *,
    _private_sdk: PrivateRoleBindingSDK,
) -> PolicyApplyResult:
    """Make a resource hold the role bindings a policy states, and only those."""
    return _private_sdk.apply_policy(
        resource_type=resource_type,
        policy=policy,
        resource_id=resource_id,
        dry_run=dry_run,
    )
