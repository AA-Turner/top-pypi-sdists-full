"""Pre-configured permission rulesets for common use cases."""

from __future__ import annotations

from pydantic_ai_backends.permissions.types import (
    OperationPermissions,
    PermissionRule,
    PermissionRuleset,
)

# Common patterns for sensitive files
SECRETS_PATTERNS = [
    "**/.env",
    "**/.env.*",
    "**/*.pem",
    "**/*.key",
    "**/*.crt",
    "**/credentials*",
    "**/secrets*",
    "**/*secret*",
    "**/*password*",
    "**/.aws/**",
    "**/.ssh/**",
    "**/.gnupg/**",
]

# Common patterns for system files
SYSTEM_PATTERNS = [
    "/etc/**",
    "/var/**",
    "/usr/**",
    "/bin/**",
    "/sbin/**",
    "/boot/**",
    "/sys/**",
    "/proc/**",
]

# Dangerous command patterns
DANGEROUS_COMMANDS = [
    "rm -rf /*",
    "rm -rf /",
    ":(){:|:&};:",  # Fork bomb
    "dd if=*of=/dev/*",
    "mkfs*",
    "> /dev/sda",
    "chmod -R 777 /",
]


def _create_deny_rules(patterns: list[str], description: str) -> list[PermissionRule]:
    """Create deny rules for a list of patterns."""
    return [PermissionRule(pattern=p, action="deny", description=description) for p in patterns]


# =============================================================================
# DEFAULT_RULESET
# =============================================================================
# Safe defaults: allow reads (except secrets), ask for writes/executes

DEFAULT_RULESET = PermissionRuleset(
    default="ask",
    read=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    write=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    edit=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    execute=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(DANGEROUS_COMMANDS, "Block dangerous commands"),
    ),
    glob=OperationPermissions(default="allow"),
    grep=OperationPermissions(default="allow"),
    ls=OperationPermissions(default="allow"),
)


# =============================================================================
# PERMISSIVE_RULESET
# =============================================================================
# Allow most operations, deny only dangerous ones

PERMISSIVE_RULESET = PermissionRuleset(
    default="allow",
    read=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    write=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(
            SECRETS_PATTERNS + SYSTEM_PATTERNS, "Protect sensitive and system files"
        ),
    ),
    edit=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(
            SECRETS_PATTERNS + SYSTEM_PATTERNS, "Protect sensitive and system files"
        ),
    ),
    execute=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(DANGEROUS_COMMANDS, "Block dangerous commands"),
    ),
    glob=OperationPermissions(default="allow"),
    grep=OperationPermissions(default="allow"),
    ls=OperationPermissions(default="allow"),
)


# =============================================================================
# READONLY_RULESET
# =============================================================================
# Allow read operations only, deny writes and executes

READONLY_RULESET = PermissionRuleset(
    default="deny",
    read=OperationPermissions(
        default="allow",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    write=OperationPermissions(default="deny"),
    edit=OperationPermissions(default="deny"),
    execute=OperationPermissions(default="deny"),
    glob=OperationPermissions(default="allow"),
    grep=OperationPermissions(default="allow"),
    ls=OperationPermissions(default="allow"),
)


# =============================================================================
# STRICT_RULESET
# =============================================================================
# Everything requires explicit approval

STRICT_RULESET = PermissionRuleset(
    default="ask",
    read=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    write=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    edit=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files"),
    ),
    execute=OperationPermissions(
        default="ask",
        rules=_create_deny_rules(DANGEROUS_COMMANDS, "Block dangerous commands"),
    ),
    glob=OperationPermissions(default="ask"),
    grep=OperationPermissions(default="ask"),
    ls=OperationPermissions(default="ask"),
)


# =============================================================================
# Factory functions for custom rulesets
# =============================================================================


def create_ruleset(
    *,
    default: str = "ask",
    allow_read: bool = True,
    allow_write: bool = False,
    allow_edit: bool = False,
    allow_execute: bool = False,
    allow_glob: bool = True,
    allow_grep: bool = True,
    allow_ls: bool = True,
    deny_secrets: bool = True,
) -> PermissionRuleset:
    """Create a custom permission ruleset.

    A convenience factory for creating rulesets with common configurations.

    Args:
        default: Global default action ("allow", "deny", or "ask").
        allow_read: Whether to allow read operations by default.
        allow_write: Whether to allow write operations by default.
        allow_edit: Whether to allow edit operations by default.
        allow_execute: Whether to allow execute operations by default.
        allow_glob: Whether to allow glob operations by default.
        allow_grep: Whether to allow grep operations by default.
        allow_ls: Whether to allow ls operations by default.
        deny_secrets: Whether to deny access to sensitive file patterns.

    Returns:
        A configured PermissionRuleset.

    Example:
        ```python
        # Create a ruleset that allows reads and writes but asks for execute
        ruleset = create_ruleset(
            allow_read=True,
            allow_write=True,
            allow_execute=False,
        )
        ```
    """

    def _action(allowed: bool) -> str:
        return "allow" if allowed else "ask"

    secret_rules = (
        _create_deny_rules(SECRETS_PATTERNS, "Protect sensitive files") if deny_secrets else []
    )

    return PermissionRuleset(
        default=default,  # type: ignore[arg-type]
        read=OperationPermissions(default=_action(allow_read), rules=secret_rules),  # type: ignore[arg-type]
        write=OperationPermissions(default=_action(allow_write), rules=secret_rules),  # type: ignore[arg-type]
        edit=OperationPermissions(default=_action(allow_edit), rules=secret_rules),  # type: ignore[arg-type]
        execute=OperationPermissions(default=_action(allow_execute)),  # type: ignore[arg-type]
        glob=OperationPermissions(default=_action(allow_glob)),  # type: ignore[arg-type]
        grep=OperationPermissions(default=_action(allow_grep)),  # type: ignore[arg-type]
        ls=OperationPermissions(default=_action(allow_ls)),  # type: ignore[arg-type]
    )
