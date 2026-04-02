"""Tests for permission presets."""

from pydantic_ai_backends.permissions.checker import PermissionChecker
from pydantic_ai_backends.permissions.presets import (
    DEFAULT_RULESET,
    PERMISSIVE_RULESET,
    READONLY_RULESET,
    SECRETS_PATTERNS,
    STRICT_RULESET,
    SYSTEM_PATTERNS,
    create_ruleset,
)


class TestSecretsPatterns:
    """Tests for secrets patterns."""

    def test_env_files_matched(self):
        """Test that .env files are matched by secrets patterns."""
        checker = PermissionChecker(DEFAULT_RULESET)

        # These should all be denied for read
        assert checker.is_denied("read", "/home/user/.env")
        assert checker.is_denied("read", "/project/.env.local")
        assert checker.is_denied("read", ".env.production")

    def test_key_files_matched(self):
        """Test that key files are matched."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_denied("read", "/home/.ssh/id_rsa.pem")
        assert checker.is_denied("read", "/ssl/server.key")
        assert checker.is_denied("read", "/certs/ca.crt")

    def test_credentials_matched(self):
        """Test that credentials files are matched."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_denied("read", "/home/.aws/credentials")
        assert checker.is_denied("read", "/app/credentials.json")

    def test_secrets_patterns_list(self):
        """Test that SECRETS_PATTERNS is a non-empty list."""
        assert isinstance(SECRETS_PATTERNS, list)
        assert len(SECRETS_PATTERNS) > 0
        assert "**/.env" in SECRETS_PATTERNS


class TestSystemPatterns:
    """Tests for system patterns."""

    def test_system_patterns_list(self):
        """Test that SYSTEM_PATTERNS is a non-empty list."""
        assert isinstance(SYSTEM_PATTERNS, list)
        assert len(SYSTEM_PATTERNS) > 0
        assert "/etc/**" in SYSTEM_PATTERNS


class TestDefaultRuleset:
    """Tests for DEFAULT_RULESET behavior."""

    def test_read_allowed_for_regular_files(self):
        """Test that reads are allowed for regular files."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_allowed("read", "/project/src/main.py")
        assert checker.is_allowed("read", "/home/user/document.txt")

    def test_read_denied_for_secrets(self):
        """Test that reads are denied for secret files."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_denied("read", "/project/.env")

    def test_write_requires_approval(self):
        """Test that writes require approval."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.requires_approval("write", "/project/file.txt")

    def test_execute_requires_approval(self):
        """Test that execute requires approval."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.requires_approval("execute", "ls -la")

    def test_glob_allowed(self):
        """Test that glob is allowed."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_allowed("glob", "**/*.py")

    def test_grep_allowed(self):
        """Test that grep is allowed."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_allowed("grep", "TODO")

    def test_ls_allowed(self):
        """Test that ls is allowed."""
        checker = PermissionChecker(DEFAULT_RULESET)

        assert checker.is_allowed("ls", "/project")


class TestPermissiveRuleset:
    """Tests for PERMISSIVE_RULESET behavior."""

    def test_read_allowed(self):
        """Test that reads are generally allowed."""
        checker = PermissionChecker(PERMISSIVE_RULESET)

        assert checker.is_allowed("read", "/project/file.txt")

    def test_write_allowed(self):
        """Test that writes are generally allowed."""
        checker = PermissionChecker(PERMISSIVE_RULESET)

        assert checker.is_allowed("write", "/project/file.txt")

    def test_write_denied_for_secrets(self):
        """Test that writes to secrets are denied."""
        checker = PermissionChecker(PERMISSIVE_RULESET)

        assert checker.is_denied("write", "/project/.env")

    def test_execute_allowed(self):
        """Test that execute is generally allowed."""
        checker = PermissionChecker(PERMISSIVE_RULESET)

        assert checker.is_allowed("execute", "npm test")


class TestReadonlyRuleset:
    """Tests for READONLY_RULESET behavior."""

    def test_read_allowed(self):
        """Test that reads are allowed."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_allowed("read", "/project/file.txt")

    def test_read_denied_for_secrets(self):
        """Test that secret reads are still denied."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_denied("read", "/project/.env")

    def test_write_denied(self):
        """Test that writes are denied."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_denied("write", "/project/file.txt")

    def test_edit_denied(self):
        """Test that edits are denied."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_denied("edit", "/project/file.txt")

    def test_execute_denied(self):
        """Test that execute is denied."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_denied("execute", "rm file.txt")

    def test_glob_allowed(self):
        """Test that glob is allowed."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_allowed("glob", "**/*.py")

    def test_grep_allowed(self):
        """Test that grep is allowed."""
        checker = PermissionChecker(READONLY_RULESET)

        assert checker.is_allowed("grep", "pattern")


class TestStrictRuleset:
    """Tests for STRICT_RULESET behavior."""

    def test_read_requires_approval(self):
        """Test that reads require approval."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.requires_approval("read", "/project/file.txt")

    def test_read_denied_for_secrets(self):
        """Test that secret reads are denied (not just ask)."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.is_denied("read", "/project/.env")

    def test_write_requires_approval(self):
        """Test that writes require approval."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.requires_approval("write", "/project/file.txt")

    def test_execute_requires_approval(self):
        """Test that execute requires approval."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.requires_approval("execute", "echo hello")

    def test_glob_requires_approval(self):
        """Test that glob requires approval."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.requires_approval("glob", "**/*.py")

    def test_ls_requires_approval(self):
        """Test that ls requires approval."""
        checker = PermissionChecker(STRICT_RULESET)

        assert checker.requires_approval("ls", "/project")


class TestCreateRuleset:
    """Tests for create_ruleset factory function."""

    def test_default_values(self):
        """Test that default values are correct."""
        ruleset = create_ruleset()

        checker = PermissionChecker(ruleset)

        # Default allows reads
        assert checker.is_allowed("read", "/file.txt")
        # Default asks for writes
        assert checker.requires_approval("write", "/file.txt")

    def test_allow_write(self):
        """Test creating ruleset that allows writes."""
        ruleset = create_ruleset(allow_write=True)

        checker = PermissionChecker(ruleset)
        assert checker.is_allowed("write", "/file.txt")

    def test_deny_read(self):
        """Test creating ruleset that asks for reads."""
        ruleset = create_ruleset(allow_read=False)

        checker = PermissionChecker(ruleset)
        assert checker.requires_approval("read", "/file.txt")

    def test_allow_execute(self):
        """Test creating ruleset that allows execute."""
        ruleset = create_ruleset(allow_execute=True)

        checker = PermissionChecker(ruleset)
        assert checker.is_allowed("execute", "ls")

    def test_deny_secrets_false(self):
        """Test creating ruleset without secret protection."""
        ruleset = create_ruleset(deny_secrets=False)

        checker = PermissionChecker(ruleset)
        # Should be allowed since no secret rules
        assert checker.is_allowed("read", "/project/.env")

    def test_all_operations(self):
        """Test creating ruleset with all operations configured."""
        ruleset = create_ruleset(
            allow_read=True,
            allow_write=True,
            allow_edit=True,
            allow_execute=True,
            allow_glob=True,
            allow_grep=True,
            allow_ls=True,
            deny_secrets=False,
        )

        checker = PermissionChecker(ruleset)

        assert checker.is_allowed("read", "/file.txt")
        assert checker.is_allowed("write", "/file.txt")
        assert checker.is_allowed("edit", "/file.txt")
        assert checker.is_allowed("execute", "ls")
        assert checker.is_allowed("glob", "*.py")
        assert checker.is_allowed("grep", "pattern")
        assert checker.is_allowed("ls", "/")
