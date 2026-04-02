"""Type definitions for the permissions system."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# Permission actions that can be taken
PermissionAction = Literal["allow", "deny", "ask"]

# Operations that can be controlled by permissions
PermissionOperation = Literal["read", "write", "edit", "execute", "glob", "grep", "ls"]


class PermissionRule(BaseModel):
    """A rule that matches paths/commands and specifies an action.

    Rules are evaluated in order - first matching rule wins.
    Patterns use fnmatch-style matching with support for `**` (recursive).

    Example:
        ```python
        # Deny access to .env files
        PermissionRule(
            pattern="**/.env*",
            action="deny",
            description="Protect environment files",
        )

        # Ask before writing to config files
        PermissionRule(
            pattern="**/config/**",
            action="ask",
            description="Confirm config changes",
        )
        ```
    """

    pattern: str
    """Glob pattern to match against paths or commands.

    Supports fnmatch patterns:
    - `*` matches any characters except `/`
    - `**` matches any characters including `/` (recursive)
    - `?` matches any single character
    - `[seq]` matches any character in seq
    """

    action: PermissionAction
    """Action to take when pattern matches: "allow", "deny", or "ask"."""

    description: str = ""
    """Human-readable description of why this rule exists."""


class OperationPermissions(BaseModel):
    """Permissions configuration for a single operation type.

    Contains a default action and a list of rules that override
    the default for specific patterns.

    Example:
        ```python
        OperationPermissions(
            default="allow",
            rules=[
                PermissionRule(pattern="**/.env*", action="deny"),
                PermissionRule(pattern="**/secrets/**", action="deny"),
            ],
        )
        ```
    """

    default: PermissionAction = "allow"
    """Default action when no rule matches."""

    rules: list[PermissionRule] = Field(default_factory=list)
    """Rules evaluated in order - first match wins."""


class PermissionRuleset(BaseModel):
    """Complete permissions configuration for all operations.

    Defines default behavior and per-operation permissions.
    Each operation can have its own default and rules.

    Example:
        ```python
        ruleset = PermissionRuleset(
            default="deny",  # Default deny everything
            read=OperationPermissions(default="allow"),  # But allow reads
            write=OperationPermissions(
                default="ask",  # Ask before writing
                rules=[
                    PermissionRule(pattern="**/temp/**", action="allow"),
                ],
            ),
        )
        ```
    """

    default: PermissionAction = "ask"
    """Global default action when operation has no specific config."""

    read: OperationPermissions | None = None
    """Permissions for read operations."""

    write: OperationPermissions | None = None
    """Permissions for write operations."""

    edit: OperationPermissions | None = None
    """Permissions for edit operations."""

    execute: OperationPermissions | None = None
    """Permissions for execute operations (shell commands)."""

    glob: OperationPermissions | None = None
    """Permissions for glob operations."""

    grep: OperationPermissions | None = None
    """Permissions for grep operations."""

    ls: OperationPermissions | None = None
    """Permissions for ls operations."""

    def get_operation_permissions(self, operation: PermissionOperation) -> OperationPermissions:
        """Get permissions for a specific operation.

        Returns the operation-specific permissions if defined,
        otherwise creates default permissions using the global default.

        Args:
            operation: The operation type to get permissions for.

        Returns:
            OperationPermissions for the specified operation.
        """
        op_perms: OperationPermissions | None = getattr(self, operation, None)
        if op_perms is not None:
            return op_perms
        return OperationPermissions(default=self.default)
