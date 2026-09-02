"""Tests for the pure ``specialize_expectations`` helper."""

from __future__ import annotations

import re
from types import MappingProxyType

import pytest

from agentic_devtools.cli.setup.expectations_specializer import (
    RepositoryConfiguration,
    specialize_expectations,
)

# A minimal synthetic document mirroring the managed structural markers of the
# real ``docs/setup-expectations/agdt-setup.md`` (phases + managed tables). Using
# a synthetic document gives precise, fast control over every prune/annotate path.
SYNTHETIC_DOC = """\
# agdt-setup — Expectations Document

Intro paragraph.

## Phases

The following phases execute in this order:

1. `version_check`
2. `certificate_prefetch`
3. `cli_installation`
4. `dependency_check`

## Parameters & State Keys

### CLI Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--system-only` | boolean | `false` | Skip managed installs. |
| `--issue-adapter` | choice | `null` | Override the issue-adapter axis. |
| `--npm` | boolean | `false` | Force npm work. |
| `--no-npm` | boolean | `false` | Skip npm work. |
| `--no-verify-ssl` | boolean | `false` | Disable SSL verification. |

### Environment Variables (Set During Execution)

| Variable | Condition |
|----------|-----------|
| `AGDT_NO_VERIFY_SSL` | Set when `--no-verify-ssl` is passed. |
| `NODE_EXTRA_CA_CERTS` | Pointed at the unified CA bundle. |
| `NPM_CONFIG_USERCONFIG` | Pointed at `~/.agdt/npmrc`. |
| `REQUESTS_CA_BUNDLE` | Pointed at `~/.agdt/certs/unified-ca-bundle.pem`. |

## Decision Points / Paths

| Decision | Condition | Path |
|----------|-----------|------|
| Version guard — block | Installed version < project pin | exit 3 |
| Version guard — force | Installed version < project pin but forced | continue |
| Version guard — allow | Installed version >= project pin | continue |
| `--system-only` | Flag set | Skip phases |

## Observable Side Effects

### File System (`~/.agdt/`)

| Path | Description |
|------|-------------|
| `~/.agdt/bin/` | Managed CLI binaries. |
| `~/.agdt/certs/` | Per-host PEM files. |
| `~/.agdt/npmrc` | npm configuration. |
| `~/.agdt/registry.json` | Append-only artifact reference index. |
| `~/.agdt/registry.json.lock` | Sidecar lock file for registry. |
| Shell profile (e.g., `~/.bashrc`) | PATH plus NODE_EXTRA_CA_CERTS and NPM_CONFIG_USERCONFIG. |

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | OK | Setup completed. |
| 3 | VERSION_BLOCKED | Version too old. |
| malformed |
"""


def _config(**overrides: object) -> RepositoryConfiguration:
    base = dict(
        repo="owner/repo",
        issue_adapter="github",
        has_npm=True,
        ssl_hosts=("a.internal",),
        system_only=False,
        version_pin="1.2.3",
        effective_flags=MappingProxyType({}),
    )
    base.update(overrides)
    return RepositoryConfiguration(**base)  # type: ignore[arg-type]


class TestStructuralValidation:
    """FR-006 / SC-003 structural-marker validation."""

    def test_missing_phases_raises_with_message(self) -> None:
        """A document without ``## Phases`` raises ``ValueError`` naming Phases."""
        with pytest.raises(ValueError, match="Phases"):
            specialize_expectations("# Title\n\nno phases here\n", _config())

    def test_empty_document_raises(self) -> None:
        """An empty document raises ``ValueError``."""
        with pytest.raises(ValueError, match="empty or whitespace"):
            specialize_expectations("", _config())

    def test_whitespace_only_document_raises(self) -> None:
        """A whitespace-only document raises ``ValueError``."""
        with pytest.raises(ValueError, match="empty or whitespace"):
            specialize_expectations("   \n\t\n", _config())

    @pytest.mark.parametrize("heading", ["## Phases notes", "## Phases-old"])
    def test_near_match_phases_heading_raises(self, heading: str) -> None:
        """Near-match Phases headings are rejected by structural validation."""
        with pytest.raises(ValueError, match="Phases"):
            specialize_expectations(f"# Title\n\n{heading}\n\n1. `version_check`\n", _config())


class TestNpmPruning:
    """SC-005 npm-off row pruning by key column."""

    def test_npm_off_prunes_npm_rows_retains_mixed(self) -> None:
        """npm-only rows are pruned; the mixed Shell profile row is retained."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(has_npm=False))
        assert "| `NODE_EXTRA_CA_CERTS` |" not in out
        assert "| `NPM_CONFIG_USERCONFIG` |" not in out
        assert "| `--npm` |" not in out
        assert "| `--no-npm` |" not in out
        assert "| `~/.agdt/npmrc` |" not in out
        assert "Shell profile (e.g., `~/.bashrc`)" in out

    def test_npm_on_retains_npm_rows(self) -> None:
        """With npm enabled, npm rows are retained."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(has_npm=True))
        assert "| `NODE_EXTRA_CA_CERTS` |" in out
        assert "| `--npm` |" in out
        assert "| `~/.agdt/npmrc` |" in out

    def test_system_only_with_npm_prunes_side_effect_rows_retains_flags(self) -> None:
        """In system-only mode, npm env/file-system side-effects are pruned; CLI flags kept.

        ``--system-only`` skips certificate prefetch and environment persistence,
        so the corresponding environment-variable and file-system rows cannot occur
        in this run. The ``--npm`` / ``--no-npm`` CLI flag rows are retained because
        they remain valid options for the caller to pass.
        """
        out = specialize_expectations(SYNTHETIC_DOC, _config(has_npm=True, system_only=True))
        assert "| `NODE_EXTRA_CA_CERTS` |" not in out
        assert "| `NPM_CONFIG_USERCONFIG` |" not in out
        assert "| `~/.agdt/npmrc` |" not in out
        # CLI flags must be retained.
        assert "| `--npm` |" in out
        assert "| `--no-npm` |" in out

    def test_system_only_without_npm_prunes_all_npm_rows(self) -> None:
        """With both system-only and no-npm, all npm rows are absent."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(has_npm=False, system_only=True))
        assert "| `NODE_EXTRA_CA_CERTS` |" not in out
        assert "| `NPM_CONFIG_USERCONFIG` |" not in out
        assert "| `~/.agdt/npmrc` |" not in out
        assert "| `--npm` |" not in out
        assert "| `--no-npm` |" not in out


class TestSystemOnlyPruning:
    """SC-002 / FR pruning of skipped-phase side-effect rows in ``--system-only`` mode."""

    def test_system_only_prunes_cert_and_cli_installation_rows(self) -> None:
        """cert-prefetch and CLI-installation outputs are pruned when system_only is True."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=True))
        assert "| `~/.agdt/bin/` |" not in out
        assert "| `~/.agdt/certs/` |" not in out
        assert "| `~/.agdt/registry.json` |" not in out
        assert "| `~/.agdt/registry.json.lock` |" not in out
        assert "| `REQUESTS_CA_BUNDLE` |" not in out

    def test_system_only_retains_non_phase_rows(self) -> None:
        """Rows unrelated to the skipped phases are retained in --system-only mode.

        The ``Shell profile`` row is pruned in ``--system-only`` mode because
        ``--system-only`` suppresses all profile writes (same effect as
        ``--no-persist-env``).
        """
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=True))
        assert "Shell profile (e.g., `~/.bashrc`)" not in out
        assert "| `AGDT_NO_VERIFY_SSL` |" in out
        assert "| `--system-only` |" in out

    def test_non_system_only_retains_cert_and_bin_rows(self) -> None:
        """cert-prefetch and CLI-installation rows are present when system_only is False."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=False))
        assert "| `~/.agdt/bin/` |" in out
        assert "| `~/.agdt/certs/` |" in out
        assert "| `~/.agdt/registry.json` |" in out
        assert "| `~/.agdt/registry.json.lock` |" in out
        assert "| `REQUESTS_CA_BUNDLE` |" in out


class TestNoPersistEnvPruning:
    """SC-006 shell-profile row pruning when ``--no-persist-env`` is effective."""

    def test_no_persist_env_prunes_shell_profile_row(self) -> None:
        """Shell profile row is pruned when ``--no-persist-env`` is True."""
        out = specialize_expectations(
            SYNTHETIC_DOC,
            _config(system_only=False, effective_flags=MappingProxyType({"--no-persist-env": True})),
        )
        assert "Shell profile (e.g., `~/.bashrc`)" not in out

    def test_persist_env_retains_shell_profile_row(self) -> None:
        """Shell profile row is retained when ``--no-persist-env`` is False."""
        out = specialize_expectations(
            SYNTHETIC_DOC,
            _config(system_only=False, effective_flags=MappingProxyType({"--no-persist-env": False})),
        )
        assert "Shell profile (e.g., `~/.bashrc`)" in out

    def test_system_only_prunes_shell_profile_independently_of_flag(self) -> None:
        """system_only always prunes the shell profile row regardless of effective_flags."""
        out = specialize_expectations(
            SYNTHETIC_DOC,
            _config(system_only=True, effective_flags=MappingProxyType({"--no-persist-env": False})),
        )
        assert "Shell profile (e.g., `~/.bashrc`)" not in out


class TestPhaseAnnotation:
    """SC-002 system-only phase annotation."""

    def test_system_only_annotates_gated_phases_without_removal(self) -> None:
        """Gated phases are annotated; total phase count is unchanged."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=True))
        assert "2. `certificate_prefetch` *(expected: skipped)*" in out
        assert "3. `cli_installation` *(expected: skipped)*" in out
        # Non-gated phases are untouched.
        assert "1. `version_check`\n" in out
        assert "4. `dependency_check`\n" in out
        assert _phase_count(out) == _phase_count(SYNTHETIC_DOC)

    def test_non_system_only_leaves_phases_unannotated(self) -> None:
        """Without system-only, no phase carries a skipped annotation."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=False))
        assert "*(expected: skipped)*" not in out


class TestVersionPin:
    """FR-002 / FR-003 version-guard pruning and annotation."""

    def test_pin_present_annotates_and_retains(self) -> None:
        """A pin annotates block/force rows and retains ``VERSION_BLOCKED``."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(version_pin="9.9.9"))
        assert "Version guard — block" in out
        assert "Version guard — force" in out
        assert "*(pin: 9.9.9)*" in out
        assert "| VERSION_BLOCKED |" in out
        assert "*(pin: 9.9.9)*" in out.split("VERSION_BLOCKED")[1]

    def test_no_pin_prunes_block_force_and_version_blocked(self) -> None:
        """No pin removes block/force rows and the ``VERSION_BLOCKED`` exit row."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(version_pin=None))
        assert "Version guard — block" not in out
        assert "Version guard — force" not in out
        assert "Version guard — allow" in out
        assert "| VERSION_BLOCKED |" not in out

    def test_empty_pin_treated_as_no_pin(self) -> None:
        """An empty-string pin is treated as unpinned."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(version_pin=""))
        assert "Version guard — block" not in out
        assert "version_pin: none" in out

    def test_malformed_version_guard_row_raises(self) -> None:
        """A one-cell version-guard row raises ``ValueError`` instead of ``IndexError``."""
        malformed_doc = SYNTHETIC_DOC.replace(
            "| Version guard — block | Installed version < project pin | exit 3 |",
            "| Version guard — block |",
        )
        with pytest.raises(ValueError, match="Malformed decision row"):
            specialize_expectations(malformed_doc, _config())


class TestIdentifierFillAndEscaping:
    """FR-003 identifier fill + context-specific escaping."""

    def test_metadata_block_filled(self) -> None:
        """The metadata block carries repo, adapter, hosts, pin, and flags."""
        out = specialize_expectations(
            SYNTHETIC_DOC,
            _config(
                repo="swai-factory/my-repo",
                ssl_hosts=("a.internal", "b.internal"),
                version_pin="1.0.0",
                effective_flags=MappingProxyType({"z": "1", "a": True, "m": None, "b": False}),
            ),
        )
        assert "<!-- agdt-setup-specialization" in out
        assert "repo: swai-factory/my-repo" in out
        assert "adapter: github" in out
        assert "ssl_hosts: a.internal,b.internal" in out
        assert "version_pin: 1.0.0" in out
        # effective_flags sorted by key; bool/None rendered deterministically.
        assert "effective_flags: a=true, b=false, m=none, z=1" in out

    def test_cli_flag_and_ssl_annotations(self) -> None:
        """CLI-flag cells receive effective-value annotations; ssl annotation absent in system-only."""
        out = specialize_expectations(
            SYNTHETIC_DOC, _config(issue_adapter="github", system_only=True, ssl_hosts=("h1", "h2"))
        )
        assert "*(effective adapter: github)*" in out
        assert "*(effective: true)*" in out
        # ~/.agdt/certs/ row is pruned in --system-only mode; inline annotation absent.
        assert "*(effective ssl_hosts: h1,h2)*" not in out

    def test_ssl_annotation_present_when_not_system_only(self) -> None:
        """SSL-host annotation appears in the file-system row when not in --system-only mode."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(system_only=False, ssl_hosts=("h1", "h2")))
        assert "*(effective ssl_hosts: h1,h2)*" in out

    def test_empty_ssl_hosts_render_none(self) -> None:
        """An empty SSL-host set renders ``none`` in metadata and annotation."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=()))
        assert "ssl_hosts: none" in out
        assert "*(effective ssl_hosts: none)*" in out

    def test_flag_value_double_dash_escaped_in_html_comment(self) -> None:
        """A ``--`` sequence in a flag value is escaped as ``- -`` in the metadata block."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=MappingProxyType({"k": "a-->b"})))
        assert "k=a- ->b" in out
        assert "a-->b" not in out

    def test_version_pin_pipe_escaped_in_table_cell(self) -> None:
        """A ``|`` in a version pin is escaped as ``\\|`` inside table cells."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(version_pin="1|2"))
        assert "*(pin: 1\\|2)*" in out

    def test_ssl_host_pipe_escaped_and_double_dash_in_metadata(self) -> None:
        """SSL hosts escape ``|`` in cells and ``--`` sequences in the metadata block."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=("a|b", "c-->d")))
        assert "*(effective ssl_hosts: a\\|b,c-->d)*" in out
        assert "ssl_hosts: a|b,c- ->d" in out

    def test_triple_hyphen_sequence_escaped_until_safe(self) -> None:
        """Three consecutive hyphens are repeatedly escaped to avoid ``-->`` in comments."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=MappingProxyType({"k": "--->"})))
        assert "k=--->" not in out
        assert "k=- -->" not in out
        assert "k=- - ->" in out


class TestAdapterHandling:
    """FR-003 adapter recognition and warning behavior."""

    def test_recognized_adapter_no_warning(self) -> None:
        """A recognized adapter emits no warning comment."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(issue_adapter="jira"))
        assert "WARNING: Unrecognized adapter" not in out

    def test_unrecognized_adapter_prepends_warning_and_retains(self) -> None:
        """An unrecognized adapter prepends a warning and retains all sections."""
        out = specialize_expectations(SYNTHETIC_DOC, _config(issue_adapter="gitlab"))
        assert out.startswith("<!-- WARNING: Unrecognized adapter type 'gitlab'; all adapter sections retained -->")
        # All adapter/CLI sections are still present (nothing pruned by adapter).
        assert "### CLI Flags" in out
        assert "## Exit Codes" in out


class TestHostileIdentifiers:
    """FR-003 identifier validation for hostile inputs."""

    def test_effective_flag_invalid_key_type_raises(self) -> None:
        """A non-string flag key raises ValueError."""
        with pytest.raises(ValueError, match="Invalid effective_flags key type: int"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags={123: "val"}))  # type: ignore

    def test_effective_flag_invalid_value_type_raises(self) -> None:
        """A flag value that is not str, bool, or None raises ValueError."""
        with pytest.raises(ValueError, match="Invalid effective_flags value type for 'key': int"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags={"key": 123}))  # type: ignore

    def test_version_pin_invalid_type_raises(self) -> None:
        """A version pin that is not str or None raises ValueError."""
        with pytest.raises(ValueError, match="Invalid version_pin type: int"):
            specialize_expectations(SYNTHETIC_DOC, _config(version_pin=123))  # type: ignore

    def test_has_npm_invalid_type_raises(self) -> None:
        """A non-boolean ``has_npm`` raises ``ValueError``."""
        with pytest.raises(ValueError, match="Invalid has_npm type: str"):
            specialize_expectations(SYNTHETIC_DOC, _config(has_npm="false"))  # type: ignore

    def test_system_only_invalid_type_raises(self) -> None:
        """A non-boolean ``system_only`` raises ``ValueError``."""
        with pytest.raises(ValueError, match="Invalid system_only type: str"):
            specialize_expectations(SYNTHETIC_DOC, _config(system_only="false"))  # type: ignore

    def test_effective_flags_invalid_outer_type_raises(self) -> None:
        """A non-mapping ``effective_flags`` raises ``ValueError``."""
        with pytest.raises(ValueError, match="Invalid effective_flags type: NoneType"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=None))  # type: ignore

    def test_ssl_hosts_invalid_outer_type_raises(self) -> None:
        """A non-tuple ``ssl_hosts`` raises ``ValueError``."""
        with pytest.raises(ValueError, match="Invalid ssl_hosts type: NoneType"):
            specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=None))  # type: ignore

    def test_ssl_hosts_invalid_type_raises(self) -> None:
        """An ssl_hosts entry that is not a string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid ssl_hosts entry type: int"):
            specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=(123,)))  # type: ignore

    def test_repo_slug_with_html_comment_close_raises(self) -> None:
        """A repo slug containing ``-->`` fails the slug regex."""
        with pytest.raises(ValueError, match="repo slug"):
            specialize_expectations(SYNTHETIC_DOC, _config(repo="a-->b/c"))

    def test_empty_adapter_raises(self) -> None:
        """An empty adapter string raises ``ValueError``."""
        with pytest.raises(ValueError, match="issue_adapter"):
            specialize_expectations(SYNTHETIC_DOC, _config(issue_adapter=""))

    def test_version_pin_newline_raises(self) -> None:
        """A newline in the version pin raises ``ValueError``."""
        with pytest.raises(ValueError, match="version_pin"):
            specialize_expectations(SYNTHETIC_DOC, _config(version_pin="1\n2"))

    def test_ssl_host_newline_raises(self) -> None:
        """A newline in an SSL host raises ``ValueError``."""
        with pytest.raises(ValueError, match="ssl_hosts"):
            specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=("a\nb",)))

    def test_ssl_host_empty_raises(self) -> None:
        """An empty SSL host raises ``ValueError``."""
        with pytest.raises(ValueError, match="ssl_hosts"):
            specialize_expectations(SYNTHETIC_DOC, _config(ssl_hosts=("",)))

    def test_effective_flag_invalid_key_raises(self) -> None:
        """An invalid effective_flags key raises ``ValueError``."""
        with pytest.raises(ValueError, match="effective_flags key"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=MappingProxyType({"bad key": "v"})))

    def test_effective_flag_key_with_newline_raises(self) -> None:
        """A newline in an effective_flags key raises ``ValueError``."""
        with pytest.raises(ValueError, match="effective_flags key"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=MappingProxyType({"flag\n": "v"})))

    def test_effective_flag_value_newline_raises(self) -> None:
        """A newline in an effective_flags string value raises ``ValueError``."""
        with pytest.raises(ValueError, match="must not contain newlines"):
            specialize_expectations(SYNTHETIC_DOC, _config(effective_flags=MappingProxyType({"k": "a\nb"})))


class TestStructuralNoOp:
    """Edge case / NFR-004: all-applicable output preserves structure."""

    def test_all_applicable_preserves_structure(self) -> None:
        """With no pruning triggers, structure is preserved (only annotations)."""
        # has_npm=True, pin present, not system-only, recognized adapter -> no row
        # removals, only cell annotations + metadata insertion.
        out = specialize_expectations(SYNTHETIC_DOC, _config())
        assert _heading_count(out) == _heading_count(SYNTHETIC_DOC)
        assert _phase_count(out) == _phase_count(SYNTHETIC_DOC)
        assert _separator_count(out) == _separator_count(SYNTHETIC_DOC)
        assert out.count("```") % 2 == 0

    def test_malformed_single_cell_exit_row_retained(self) -> None:
        """A malformed single-cell exit row is passed through unchanged."""
        out = specialize_expectations(SYNTHETIC_DOC, _config())
        assert "| malformed |" in out


def _phase_count(text: str) -> int:
    head = text.split("## Parameters")[0]
    return len(re.findall(r"(?m)^\d+\.\s+`\w+`", head))


def _heading_count(text: str) -> int:
    return len(re.findall(r"(?m)^##\s", text))


def _separator_count(text: str) -> int:
    return len(re.findall(r"(?m)^\|[-\s|:]+\|$", text))
