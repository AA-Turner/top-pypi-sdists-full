"""Tests for ``is_checkable_path_reference()``."""

import pytest

from agentic_devtools.cli.speckit.verify_artifacts import is_checkable_path_reference


class TestIsCheckablePathReference:
    """Deciding whether a reference names a concrete repository path."""

    @pytest.mark.parametrize(
        "text",
        [
            "agentic_devtools/cli/runner.py",
            "scripts/targeted-checks.sh",
            ".github/workflows/ci.yml",
            "config/pyproject.toml",
            "docs/notes.txt",
            "src/app.ts",
        ],
    )
    def test_accepts_concrete_paths(self, text: str) -> None:
        assert is_checkable_path_reference(text) is True

    def test_accepts_bare_spec_artifact_filename(self) -> None:
        assert is_checkable_path_reference("spec.md") is True

    def test_accepts_bare_filename_at_repo_root(self) -> None:
        assert is_checkable_path_reference("runner.py") is True

    def test_accepts_bare_filename_with_multi_suffix(self) -> None:
        assert is_checkable_path_reference("default.md.j2") is True

    def test_accepts_requirements_in_root_filename(self) -> None:
        assert is_checkable_path_reference("requirements.in") is True

    def test_accepts_bare_lockfile(self) -> None:
        assert is_checkable_path_reference("yarn.lock") is True

    def test_accepts_bare_filename_with_unknown_extension(self) -> None:
        assert is_checkable_path_reference("README.rst") is True

    def test_rejects_empty_text(self) -> None:
        assert is_checkable_path_reference("") is False

    def test_rejects_text_containing_whitespace(self) -> None:
        assert is_checkable_path_reference("some dir/file.py") is False

    @pytest.mark.parametrize(
        "text",
        [
            "src/<name>.py",
            "src/{module}.py",
            "src/$VAR.py",
            "src/*.py",
            "src/a?.py",
            "a|b/c.py",
            'src/"q".py',
            "src/'q'.py",
            "src/`q`.py",
            "src/(a).py",
            "src/[a].py",
            "src/a!.py",
        ],
    )
    def test_rejects_template_and_glob_fragments(self, text: str) -> None:
        assert is_checkable_path_reference(text) is False

    def test_rejects_urls(self) -> None:
        assert is_checkable_path_reference("https://example.com/a.md") is False

    def test_rejects_bare_hostname_tokens(self) -> None:
        assert is_checkable_path_reference("example.com") is False

    def test_rejects_absolute_paths(self) -> None:
        assert is_checkable_path_reference("/etc/config.yml") is False

    def test_rejects_home_relative_paths(self) -> None:
        assert is_checkable_path_reference("~/.agdt/report.json") is False

    def test_rejects_parent_traversal(self) -> None:
        assert is_checkable_path_reference("../other/file.py") is False

    def test_accepts_unknown_extension_when_path_is_concrete(self) -> None:
        assert is_checkable_path_reference("dir/file.bin") is True

    def test_rejects_slashed_text_without_extension(self) -> None:
        assert is_checkable_path_reference("P1/P2/P3") is False

    def test_accepts_bare_conventional_extensionless_filename(self) -> None:
        assert is_checkable_path_reference("Makefile") is True

    def test_accepts_slashed_path_with_conventional_extensionless_basename(self) -> None:
        assert is_checkable_path_reference("deploy/Dockerfile") is True

    @pytest.mark.parametrize(
        "text",
        [
            "Makefile",
            "Dockerfile",
            "Vagrantfile",
            "Procfile",
            "Jenkinsfile",
            "Brewfile",
            "Gemfile",
            "Pipfile",
            "Rakefile",
            "CMakeLists",
        ],
    )
    def test_accepts_each_conventional_extensionless_filename(self, text: str) -> None:
        assert is_checkable_path_reference(text) is True

    def test_rejects_bare_version_string(self) -> None:
        assert is_checkable_path_reference("3.12") is False

    def test_rejects_semver_string(self) -> None:
        assert is_checkable_path_reference("v1.2.3") is False

    def test_rejects_two_part_numeric_version(self) -> None:
        assert is_checkable_path_reference("1.0") is False

    def test_rejects_three_part_numeric_version(self) -> None:
        assert is_checkable_path_reference("3.12.5") is False

    def test_accepts_slashed_path_with_version_like_basename(self) -> None:
        """A path segment is not a bare token, so it is not auto-rejected."""
        assert is_checkable_path_reference("releases/3.12") is True

    def test_accepts_slashed_path_ending_in_makefile(self) -> None:
        assert is_checkable_path_reference("docker/Makefile") is True

    @pytest.mark.parametrize(
        "text",
        [
            "HierarchyLevel.FEATURE",
            "HierarchyLevel.EPIC",
            "HierarchyLevel.SUBTASK",
            "ReferenceKind.FILE_PATH",
            "MyClass.MY_CONSTANT",
        ],
    )
    def test_rejects_python_class_attribute_expressions(self, text: str) -> None:
        """Python class-attribute access like ``HierarchyLevel.FEATURE`` is a symbol, not a path."""
        assert is_checkable_path_reference(text) is False

    @pytest.mark.parametrize(
        "text",
        [
            "agentic_devtools.cli.workflows.orchestrator_commands",
            "project.scripts",
        ],
    )
    def test_rejects_dotted_module_or_config_identifiers(self, text: str) -> None:
        assert is_checkable_path_reference(text) is False

    @pytest.mark.parametrize(
        "text",
        [
            "pyproject.toml",
            "default.md.j2",
        ],
    )
    def test_accepts_multi_dot_filenames_with_known_extensions(self, text: str) -> None:
        assert is_checkable_path_reference(text) is True

    @pytest.mark.parametrize("text", ["schema.proto", "notebook.ipynb"])
    def test_accepts_root_files_with_extensions_not_used_by_python_modules(self, text: str) -> None:
        assert is_checkable_path_reference(text) is True

    @pytest.mark.parametrize("text", ["schema.sql", "styles.css"])
    def test_accepts_root_files_with_passthrough_extensions(self, text: str) -> None:
        assert is_checkable_path_reference(text) is True

    def test_rejects_python_module_path_expression(self) -> None:
        """Dotted lowercase identifiers like ``os.path`` are Python module paths, not files."""
        assert is_checkable_path_reference("os.path") is False

    def test_rejects_python_method_expression_with_lowercase_name(self) -> None:
        assert is_checkable_path_reference("Path.name") is False
