from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.role_binding._private.role_binding_sdk import PrivateRoleBindingSDK
from anyscale.role_binding.commands import (
    _APPLY_ARG_DOCSTRINGS,
    _APPLY_EXAMPLE,
    _GENERATE_ARG_DOCSTRINGS,
    _GENERATE_EXAMPLE,
    apply_policy as apply_policy,
    generate_policy as generate_policy,
)
from anyscale.role_binding.models import PolicyApplyResult, RoleBindingPolicy


class RoleBindingSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateRoleBindingSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_GENERATE_EXAMPLE,
        arg_docstrings=_GENERATE_ARG_DOCSTRINGS,
    )
    def generate_policy(  # noqa: F811
        self,
        resource_type: str,
        resource_id: Optional[str] = None,
    ) -> RoleBindingPolicy:
        """Generate the role bindings a resource holds, in the shape an apply accepts."""
        return self._private_sdk.generate_policy(
            resource_type=resource_type, resource_id=resource_id
        )

    @sdk_docs(
        doc_py_example=_APPLY_EXAMPLE,
        arg_docstrings=_APPLY_ARG_DOCSTRINGS,
    )
    def apply_policy(  # noqa: F811
        self,
        resource_type: str,
        policy: RoleBindingPolicy,
        resource_id: Optional[str] = None,
        dry_run: bool = False,
    ) -> PolicyApplyResult:
        """Make a resource hold the role bindings a policy states, and only those."""
        return self._private_sdk.apply_policy(
            resource_type=resource_type,
            policy=policy,
            resource_id=resource_id,
            dry_run=dry_run,
        )
