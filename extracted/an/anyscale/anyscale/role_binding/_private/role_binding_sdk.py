from typing import List, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import (
    PolicyPrincipal as ApiPolicyPrincipal,
    PolicyRole as ApiPolicyRole,
    RoleBindingPolicy as ApiRoleBindingPolicy,
)
from anyscale.role_binding.models import (
    AppliedResultUnreadable,
    PolicyApplyResult,
    PolicyChange,
    PolicyPrincipals,
    PolicyRole,
    RoleBindingPolicy,
)


_USER = "user"
_USER_GROUP = "user_group"


class PrivateRoleBindingSDK(BaseSDK):
    """A resource's access list, read and written as one document.

    Roles and principals are identified by id, in and out. Nothing here
    resolves a name, so nothing here reads an organization wide listing: a
    caller whose authority reaches one resource needs no more than that.
    `anyscale role list` and `anyscale user-group list` are how a name becomes
    an id.
    """

    def generate_policy(
        self,
        resource_type: str,
        resource_id: Optional[str] = None,
    ) -> RoleBindingPolicy:
        """The resource's permission state, in the shape an apply accepts."""
        resource_id = self._resource_id(resource_type, resource_id)
        api_policy = self.client.generate_role_binding_policy(
            resource_type=resource_type,
            resource_id=resource_id,
        )
        return RoleBindingPolicy(
            roles=[
                PolicyRole(
                    role_id=api_role.role_id,
                    principals=PolicyPrincipals(
                        user_id=[
                            p.principal_id
                            for p in api_role.principals
                            if p.principal_type == _USER
                        ]
                        or None,
                        group_id=[
                            p.principal_id
                            for p in api_role.principals
                            if p.principal_type == _USER_GROUP
                        ]
                        or None,
                    ),
                )
                for api_role in api_policy.roles
            ]
        )

    def apply_policy(
        self,
        resource_type: str,
        policy: RoleBindingPolicy,
        resource_id: Optional[str] = None,
        dry_run: bool = False,
    ) -> PolicyApplyResult:
        """
        Make the resource hold the role bindings the policy states, and only those.

        A revoked binding comes back with what it granted and to whom, so the
        result names every change the apply made without a second read.
        """
        resource_id = self._resource_id(resource_type, resource_id)
        api_policy = ApiRoleBindingPolicy(
            roles=[
                ApiPolicyRole(
                    role_id=role.role_id,
                    principals=[
                        ApiPolicyPrincipal(
                            principal_type=principal_type,
                            principal_id=principal_id,
                        )
                        for principal_type, principal_id in role.principals.flattened()
                    ],
                )
                for role in policy.roles
            ]
        )

        result = self.client.apply_role_binding_policy(
            resource_type=resource_type,
            resource_id=resource_id,
            policy=api_policy,
            dry_run=dry_run,
        )

        try:
            return self._result(result, dry_run)
        except (TypeError, ValueError) as e:
            if dry_run:
                raise
            raise AppliedResultUnreadable(str(e)) from None

    @staticmethod
    def _result(result, dry_run: bool) -> PolicyApplyResult:
        """
        What the apply changed.

        Read after the write has landed, so a failure here is reported as a
        result that could not be read rather than as an apply that did not
        happen.
        """
        granted = [
            PolicyChange(
                role_id=added.role_id,
                principal_id=added.principal_id,
                principal_type=added.principal_type,
            )
            for added in result.added
        ]
        revoked = [
            PolicyChange(
                role_id=removed.role_id,
                principal_id=removed.principal_id,
                principal_type=removed.principal_type,
            )
            for removed in result.removed
        ]
        return PolicyApplyResult(granted=granted, revoked=revoked, dry_run=dry_run)

    def _resource_id(self, resource_type: str, resource_id: Optional[str]) -> str:
        """
        The resource to act on. The API requires an organization to be named
        explicitly and refuses another organization's rather than answering for
        a different one, so filling the caller's own in belongs here, where the
        caller's identity is already known. Only an absent id is filled in: a
        blank one is a value that was meant to say something and did not.
        """
        if resource_id is not None:
            if not resource_id.strip():
                raise ValueError(
                    f"A resource id is required for resource type '{resource_type}', "
                    "and the one given is blank."
                )
            return resource_id
        if resource_type != "organization":
            raise ValueError(f"A resource id is required for resource type '{resource_type}'.")
        organizations: List = self.client.get_user_info().organizations or []
        if not organizations:
            raise ValueError("Could not resolve your organization. Name it explicitly instead.")
        return organizations[0].id
