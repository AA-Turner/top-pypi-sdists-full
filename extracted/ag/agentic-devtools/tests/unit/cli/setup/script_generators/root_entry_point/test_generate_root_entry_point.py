"""Tests for generate_root_entry_point."""

from agentic_devtools.cli.setup.script_generators.constants import (
    COMPLETE_SETUP_FILENAME,
    ORCHESTRATOR_MARKER,
    REPO_SPECIFIC_FILENAME,
)
from agentic_devtools.cli.setup.script_generators.root_entry_point import generate_root_entry_point


class TestGenerateRootEntryPoint:
    """Tests for generate_root_entry_point."""

    def test_contains_marker(self):
        """Script contains the AGDT-MANAGED-ORCHESTRATOR marker."""
        script = generate_root_entry_point()
        assert ORCHESTRATOR_MARKER in script

    def test_references_complete_setup(self):
        """Script references the complete-setup filename."""
        script = generate_root_entry_point()
        assert COMPLETE_SETUP_FILENAME in script

    def test_references_repo_specific(self):
        """Script references the repo-specific filename."""
        script = generate_root_entry_point()
        assert REPO_SPECIFIC_FILENAME in script

    def test_fail_fast(self):
        """Script exits on failure."""
        script = generate_root_entry_point()
        assert "returncode != 0" in script
        assert "sys.exit" in script

    def test_skips_repo_specific_on_failure(self):
        """Script mentions skipping repo-specific on failure."""
        script = generate_root_entry_point()
        assert "skipping repo-specific" in script.lower()

    def test_missing_agdt_dir_error(self):
        """Script detects missing .agdt/ directory."""
        script = generate_root_entry_point()
        assert ".agdt/" in script
        assert "agdt-setup" in script
        assert "agdt_dir.is_dir()" in script

    def test_stdlib_only(self):
        """Script does not import agentic_devtools."""
        script = generate_root_entry_point()
        assert "import agentic_devtools" not in script

    def test_foreground_flag(self):
        """Script supports --foreground flag."""
        script = generate_root_entry_point()
        assert "--foreground" in script
        assert 'action="store_true"' in script

    def test_foreground_propagated_to_subprocess(self):
        """Script propagates --foreground to subprocess calls."""
        script = generate_root_entry_point()
        assert "foreground_args" in script

    def test_subprocess_uses_cwd(self):
        """subprocess.run calls use cwd=str(repo_root) for location independence."""
        script = generate_root_entry_point()
        assert "cwd=str(repo_root)" in script

    def test_supports_target_repo_root_override(self):
        """Script supports AGDT_SETUP_TARGET_REPO_ROOT for explicit branch-created autorun."""
        script = generate_root_entry_point()
        assert 'os.environ.get("AGDT_SETUP_TARGET_REPO_ROOT")' in script
        assert "script_root = Path(__file__).resolve().parent" in script
        assert 'agdt_dir = script_root / ".agdt"' in script
        assert "repo_root = Path(_AGDT_TARGET_REPO_ROOT).resolve() if _AGDT_TARGET_REPO_ROOT else script_root" in script

    def test_uses_pathlib(self):
        """Script uses pathlib.Path for cross-platform paths."""
        script = generate_root_entry_point()
        assert "from pathlib import Path" in script

    def test_repo_specific_resolved_from_repo_root(self):
        """Repo-specific script is resolved from repo_root for stable __file__ semantics."""
        script = generate_root_entry_point()
        assert "repo_root / " in script
        # Must NOT resolve repo_specific from script_root
        lines = [ln.strip() for ln in script.splitlines()]
        for line in lines:
            if "repo_specific" in line and "=" in line and "/" in line:
                assert "repo_root" in line, f"repo_specific must be resolved from repo_root, got: {line!r}"
                assert "script_root" not in line, f"repo_specific must not be resolved from script_root, got: {line!r}"


class TestGenerateRootEntryPointAutorunGuard:
    """Tests for the autorun recursion guard in the generated script."""

    def test_contains_autorun_guard_marker_comment(self):
        """Script contains the AGDT-SETUP-AUTORUN-GUARD marker comment."""
        script = generate_root_entry_point()
        assert "# AGDT-SETUP-AUTORUN-GUARD" in script

    def test_contains_environ_get_check(self):
        """Script contains the os.environ.get check for the marker."""
        script = generate_root_entry_point()
        assert 'os.environ.get("AGDT_SETUP_AUTORUN")' in script

    def test_normal_delegation_unchanged(self):
        """Normal managed delegation is unchanged when the marker is present."""
        script = generate_root_entry_point()
        # The delegation to complete-setup and repo-specific scripts must still be present
        assert COMPLETE_SETUP_FILENAME in script
        assert REPO_SPECIFIC_FILENAME in script
        # The guard does NOT add any sys.exit or return that would skip delegation
        assert "_AGDT_AUTORUN_ACTIVE" in script
        # Ensure there's no early return/exit tied to the guard
        lines = script.split("\n")
        guard_line_idx = None
        for i, line in enumerate(lines):
            if "_AGDT_AUTORUN_ACTIVE = os.environ.get" in line:
                guard_line_idx = i
                break
        assert guard_line_idx is not None
        # Next non-empty, non-comment line after guard should NOT be sys.exit or return
        for line in lines[guard_line_idx + 1 : guard_line_idx + 5]:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                assert not stripped.startswith("sys.exit")
                assert not stripped.startswith("return")
                break
