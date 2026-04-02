"""Tests for permissions type definitions."""

import pytest
from pydantic import ValidationError

from pydantic_ai_backends.permissions.types import (
    OperationPermissions,
    PermissionRule,
    PermissionRuleset,
)


class TestPermissionRule:
    """Tests for PermissionRule."""

    def test_create_rule(self):
        """Test creating a permission rule."""
        rule = PermissionRule(
            pattern="**/.env",
            action="deny",
            description="Protect environment files",
        )
        assert rule.pattern == "**/.env"
        assert rule.action == "deny"
        assert rule.description == "Protect environment files"

    def test_rule_default_description(self):
        """Test that description defaults to empty string."""
        rule = PermissionRule(pattern="*.txt", action="allow")
        assert rule.description == ""

    def test_rule_action_validation(self):
        """Test that invalid actions are rejected."""
        with pytest.raises(ValidationError):
            PermissionRule(pattern="*", action="invalid")  # type: ignore[arg-type]

    def test_rule_serialization(self):
        """Test rule serialization to dict."""
        rule = PermissionRule(
            pattern="**/secret*",
            action="ask",
            description="Ask for secrets",
        )
        data = rule.model_dump()
        assert data["pattern"] == "**/secret*"
        assert data["action"] == "ask"
        assert data["description"] == "Ask for secrets"


class TestOperationPermissions:
    """Tests for OperationPermissions."""

    def test_create_with_defaults(self):
        """Test creating operation permissions with defaults."""
        perms = OperationPermissions()
        assert perms.default == "allow"
        assert perms.rules == []

    def test_create_with_custom_default(self):
        """Test creating with custom default action."""
        perms = OperationPermissions(default="deny")
        assert perms.default == "deny"

    def test_create_with_rules(self):
        """Test creating with rules."""
        rules = [
            PermissionRule(pattern="**/.env", action="deny"),
            PermissionRule(pattern="**/temp/*", action="allow"),
        ]
        perms = OperationPermissions(default="ask", rules=rules)
        assert perms.default == "ask"
        assert len(perms.rules) == 2
        assert perms.rules[0].pattern == "**/.env"

    def test_default_action_validation(self):
        """Test that invalid default actions are rejected."""
        with pytest.raises(ValidationError):
            OperationPermissions(default="invalid")  # type: ignore[arg-type]


class TestPermissionRuleset:
    """Tests for PermissionRuleset."""

    def test_create_with_defaults(self):
        """Test creating ruleset with defaults."""
        ruleset = PermissionRuleset()
        assert ruleset.default == "ask"
        assert ruleset.read is None
        assert ruleset.write is None
        assert ruleset.execute is None

    def test_create_with_operations(self):
        """Test creating ruleset with operation-specific permissions."""
        ruleset = PermissionRuleset(
            default="deny",
            read=OperationPermissions(default="allow"),
            write=OperationPermissions(default="ask"),
        )
        assert ruleset.default == "deny"
        assert ruleset.read is not None
        assert ruleset.read.default == "allow"
        assert ruleset.write is not None
        assert ruleset.write.default == "ask"
        assert ruleset.execute is None

    def test_get_operation_permissions_with_config(self):
        """Test getting operation permissions when configured."""
        read_perms = OperationPermissions(
            default="allow",
            rules=[PermissionRule(pattern="**/.env", action="deny")],
        )
        ruleset = PermissionRuleset(read=read_perms)

        result = ruleset.get_operation_permissions("read")
        assert result is read_perms
        assert result.default == "allow"
        assert len(result.rules) == 1

    def test_get_operation_permissions_without_config(self):
        """Test getting operation permissions when not configured."""
        ruleset = PermissionRuleset(default="deny")

        result = ruleset.get_operation_permissions("write")
        assert result.default == "deny"
        assert result.rules == []

    def test_get_all_operations(self):
        """Test getting permissions for all operation types."""
        ruleset = PermissionRuleset(
            default="ask",
            read=OperationPermissions(default="allow"),
            write=OperationPermissions(default="ask"),
            edit=OperationPermissions(default="ask"),
            execute=OperationPermissions(default="deny"),
            glob=OperationPermissions(default="allow"),
            grep=OperationPermissions(default="allow"),
            ls=OperationPermissions(default="allow"),
        )

        assert ruleset.get_operation_permissions("read").default == "allow"
        assert ruleset.get_operation_permissions("write").default == "ask"
        assert ruleset.get_operation_permissions("edit").default == "ask"
        assert ruleset.get_operation_permissions("execute").default == "deny"
        assert ruleset.get_operation_permissions("glob").default == "allow"
        assert ruleset.get_operation_permissions("grep").default == "allow"
        assert ruleset.get_operation_permissions("ls").default == "allow"

    def test_ruleset_serialization(self):
        """Test ruleset serialization."""
        ruleset = PermissionRuleset(
            default="deny",
            read=OperationPermissions(default="allow"),
        )
        data = ruleset.model_dump()
        assert data["default"] == "deny"
        assert data["read"]["default"] == "allow"
        assert data["write"] is None

    def test_ruleset_json_roundtrip(self):
        """Test JSON serialization and deserialization."""
        original = PermissionRuleset(
            default="ask",
            read=OperationPermissions(
                default="allow",
                rules=[PermissionRule(pattern="**/.env", action="deny")],
            ),
        )

        json_str = original.model_dump_json()
        restored = PermissionRuleset.model_validate_json(json_str)

        assert restored.default == original.default
        assert restored.read is not None
        assert restored.read.default == original.read.default
        assert len(restored.read.rules) == 1
        assert restored.read.rules[0].pattern == "**/.env"
