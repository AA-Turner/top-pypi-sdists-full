"""Boundary regression test: no shared/default Teamspace fallback on direct-ingress writes.

Enforces the contract defined in
``kitty-specs/tracker-direct-ingress-teamspace-boundary-audit-01KQH08N/contracts/private-teamspace-ingress.md``
(§4 Test Assertions T-1..T-4).

Two complementary mechanisms keep this test load-bearing — even when the
audit's "no risky path" branch is the live state:

1. **Audit-driven parametric assertions (T-1, T-2)** iterate over every
   ``bucket=DIRECT_INGRESS_WRITE`` row enumerated by WP01 in
   ``research/audit-findings.md``. Each row asserts that the surface either
   raises ``MissingPrivateTeamspaceError`` (if WP04 shipped the fail-closed
   error) **or** rejects missing identity at the type level (Python
   ``TypeError`` / ``ConnectorConfigError``). Both outcomes prove no
   shared-team fallback can fire.
2. **Static source guard (T008)** scans ``src/spec_kitty_tracker/`` for known
   fallback signatures (``teams[0]``, ``default_team``, ``team_id or X``,
   etc.) and fails on any match not on the explicit allowlist
   (``tests/_no_shared_team_fallback_allowlist.txt``).

The audit-findings parser hard-fails (no ``pytest.skip``) when the file is
missing or malformed: a missing audit is itself a regression of WP01.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from spec_kitty_tracker.connectors.azure_devops import (
    AzureDevOpsConnector,
    AzureDevOpsConnectorConfig,
)
from spec_kitty_tracker.connectors.github import GitHubConnector, GitHubConnectorConfig
from spec_kitty_tracker.connectors.gitlab import GitLabConnector, GitLabConnectorConfig
from spec_kitty_tracker.connectors.in_memory import InMemoryConnector
from spec_kitty_tracker.connectors.jira import JiraConnector, JiraConnectorConfig
from spec_kitty_tracker.connectors.linear import LinearConnector, LinearConnectorConfig
from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.hosted import (
    GitHubHostedParams,
    GitLabHostedParams,
    JiraHostedParams,
    LinearHostedParams,
)
from spec_kitty_tracker.models import ExternalRef

# T005: Guarded import for WP04 conditional types. Per WP01 audit findings,
# WP04 closes as not-applied (0 DIRECT_INGRESS_WRITE rows with
# fallback_risk: yes), so these symbols are not expected to exist. The
# guarded import is retained so that, if a future mission ships WP04, this
# test transparently switches to the fail-closed-error assertion branch.
if TYPE_CHECKING:
    _CONDITIONAL_TYPES_AVAILABLE: bool
try:
    from spec_kitty_tracker.errors import (
        MissingPrivateTeamspaceError,  # type: ignore[attr-defined]  # noqa: F401
    )
    from spec_kitty_tracker.protocols import (
        NonIngressContext,  # type: ignore[attr-defined]  # noqa: F401
    )

    _CONDITIONAL_TYPES_AVAILABLE = True
except ImportError:
    _CONDITIONAL_TYPES_AVAILABLE = False


# ---------------------------------------------------------------------------
# Audit-findings parser (T005)
# ---------------------------------------------------------------------------


AUDIT_FINDINGS_PATH = (
    Path(__file__).parents[1]
    / "kitty-specs"
    / "tracker-direct-ingress-teamspace-boundary-audit-01KQH08N"
    / "research"
    / "audit-findings.md"
)

PASS_2_HEADING = "## Pass 2 — Classification Table"

# WP01 outcome line that justifies T-3 being skipped (the contract document
# stands as a future-work boundary; the conditional fail-closed error path
# is not implemented in this mission).
WP01_NO_RISKY_PATH_OUTCOME = (
    "Count of `DIRECT_INGRESS_WRITE` rows with `fallback_risk: yes`: **0**."
)


@dataclass(frozen=True)
class AuditRow:
    """One row of the Pass-2 classification table in audit-findings.md."""

    file_path: str
    line: int
    symbol: str
    bucket: str
    fallback_risk: str
    notes: str

    @property
    def row_id(self) -> str:
        """Stable identifier used in pytest parametrize ids."""
        return f"{self.file_path}:{self.line}"


def _load_audit_findings() -> list[AuditRow]:
    """Parse the Pass-2 classification table from audit-findings.md.

    Hard-fails (raises ``AssertionError``) if the file is missing or does
    not contain the expected ``## Pass 2 — Classification Table`` heading.
    A missing or malformed audit is a regression of WP01 and must be loud,
    never silently skipped.
    """
    assert AUDIT_FINDINGS_PATH.is_file(), (
        f"Expected audit-findings.md at {AUDIT_FINDINGS_PATH} but the file is "
        f"missing. WP01 must populate the audit before WP02 can run."
    )
    text = AUDIT_FINDINGS_PATH.read_text(encoding="utf-8")
    assert PASS_2_HEADING in text, (
        f"audit-findings.md is malformed: missing required heading "
        f"{PASS_2_HEADING!r}. Re-run WP01 to regenerate the classification table."
    )

    rows: list[AuditRow] = []
    in_table = False
    saw_header = False
    pass2_section = text.split(PASS_2_HEADING, 1)[1]
    # Stop at the next H2 heading to avoid spilling into later sections.
    pass2_section = re.split(r"\n## ", pass2_section, maxsplit=1)[0]

    for raw_line in pass2_section.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        # Markdown table: header row, separator row (|---|---|...|), then data.
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        # Detect header row by presence of "bucket" cell.
        if not saw_header:
            if "bucket" in (c.lower() for c in cells):
                saw_header = True
                in_table = True
            continue
        # Skip separator row (all dashes).
        if all(set(c) <= set("-:") for c in cells if c):
            continue
        if not in_table:
            continue
        # Expect 6 columns: #, file:line, symbol, bucket, fallback_risk, notes.
        if len(cells) < 6:
            continue
        _row_num, file_line, symbol, bucket, fallback_risk, notes = cells[:6]
        # file_line is "<path>:<line>"; split on the LAST colon.
        if ":" not in file_line:
            continue
        path_part, _, line_part = file_line.rpartition(":")
        try:
            line_no = int(line_part)
        except ValueError:
            continue
        rows.append(
            AuditRow(
                file_path=path_part,
                line=line_no,
                symbol=symbol,
                bucket=bucket,
                fallback_risk=fallback_risk,
                notes=notes,
            )
        )

    assert rows, (
        "Parsed zero rows from the Pass-2 classification table in "
        f"{AUDIT_FINDINGS_PATH}. The table is empty or unparseable; this is a "
        "regression of WP01 (the audit must enumerate at least the public "
        "write surfaces)."
    )
    return rows


def _direct_ingress_rows() -> list[AuditRow]:
    """Return only rows with ``bucket == DIRECT_INGRESS_WRITE``."""
    return [r for r in _load_audit_findings() if r.bucket == "DIRECT_INGRESS_WRITE"]


def _wp01_outcome_justifies_zero_rows() -> bool:
    """Check whether WP01's outcome line explicitly justifies a zero-rows result."""
    if not AUDIT_FINDINGS_PATH.is_file():
        return False
    return WP01_NO_RISKY_PATH_OUTCOME in AUDIT_FINDINGS_PATH.read_text(encoding="utf-8")


# Module-level fixture caching (cheap to recompute, but parametrize needs the
# list at collection time, so we evaluate eagerly and gate on a clear error).
_DIRECT_INGRESS_ROWS: list[AuditRow] = _direct_ingress_rows()
if not _DIRECT_INGRESS_ROWS:
    # The audit produced zero direct-ingress rows. Per WP01 outcome contract,
    # this is only acceptable if explicitly justified. Otherwise we fail loudly.
    assert _wp01_outcome_justifies_zero_rows(), (
        "audit-findings.md has zero DIRECT_INGRESS_WRITE rows AND no WP01 "
        "outcome line justifies the empty result. This indicates a missed "
        "audit or a parser regression."
    )


# ---------------------------------------------------------------------------
# Per-row identity guards: how to invoke each surface without identity, and
# how to invoke it WITH a sentinel identity for T-2 round-tripping.
#
# For DIRECT_INGRESS_WRITE rows that are connector method definitions, the
# load-bearing fail-closed enforcement lives at construction (the connector
# refuses to instantiate without identity). Exercising the constructor's
# guard for each connector-family is sufficient to prove the post-condition
# for every method on that connector.
#
# For Protocol method definitions, in-memory write surfaces, and orchestrator
# methods, identity rides on ``ExternalRef.workspace`` (model attribute);
# the load-bearing fail-closed enforcement lives in ``ExternalRef.__post_init__``
# (raises ValueError on empty workspace, see audit row #6).
# ---------------------------------------------------------------------------

SENTINEL_TEAMSPACE = "PRIV_TEAMSPACE_42_BFLZ"


def _assert_t1_for_row(row: AuditRow) -> None:
    """T-1: surface rejects missing identity. Raises pytest.fail on unknown row."""
    path = row.file_path
    if path.endswith("connectors/linear.py"):
        # All Linear DIRECT_INGRESS_WRITE rows: fail-closed via constructor
        # guard at linear.py:56-57.
        with pytest.raises((TypeError, ConnectorConfigError)):
            LinearConnector(LinearConnectorConfig(api_key="k", team_id=""))
        return
    if path.endswith("connectors/jira.py"):
        with pytest.raises((TypeError, ConnectorConfigError)):
            JiraConnector(
                JiraConnectorConfig(
                    base_url="https://example.atlassian.net",
                    email="e",
                    api_token="t",
                    project_key="",
                )
            )
        return
    if path.endswith("connectors/github.py"):
        with pytest.raises((TypeError, ConnectorConfigError)):
            GitHubConnector(GitHubConnectorConfig(owner="", repo="r", token="t"))
        return
    if path.endswith("connectors/gitlab.py"):
        with pytest.raises((TypeError, ConnectorConfigError)):
            GitLabConnector(GitLabConnectorConfig(project_id="", token="t"))
        return
    if path.endswith("connectors/azure_devops.py"):
        with pytest.raises((TypeError, ConnectorConfigError)):
            AzureDevOpsConnector(
                AzureDevOpsConnectorConfig(organization="", project="p", personal_access_token="t")
            )
        return
    if path.endswith("connectors/in_memory.py"):
        # InMemoryConnector requires `workspace` kwarg at type level; identity
        # also flows through ExternalRef.workspace which validates non-empty.
        with pytest.raises(TypeError):
            InMemoryConnector(name="mem")  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            ExternalRef(system="mem", workspace="", id="X")
        return
    if path.endswith("connectors/fp.py") or path.endswith("connectors/beads.py"):
        # Local-CLI connectors with no Teamspace concept; identity travels on
        # ExternalRef.workspace which is validated non-empty.
        with pytest.raises(ValueError):
            ExternalRef(system="local", workspace="", id="X")
        return
    if path.endswith("nango.py"):
        # NangoProxyAdapter delegates to a wrapped connector. The wrapped
        # connector's construction guard is the load-bearing enforcement;
        # also ExternalRef.workspace cannot be empty.
        with pytest.raises((TypeError, ConnectorConfigError)):
            LinearConnector(LinearConnectorConfig(api_key="k", team_id=""))
        with pytest.raises(ValueError):
            ExternalRef(system="linear", workspace="", id="X")
        return
    if path.endswith("protocols.py"):
        # Protocol method definition: identity rides on the model attribute
        # (CanonicalIssue.ref.workspace / ExternalRef.workspace), validated
        # non-empty in ExternalRef.__post_init__.
        with pytest.raises(ValueError):
            ExternalRef(system="any", workspace="", id="X")
        return
    if path.endswith("mission_sync.py") or path.endswith("sync.py"):
        # Orchestrator: identity flows through CanonicalIssue.ref / ExternalRef
        # supplied by the caller; the model layer guards empty workspace.
        with pytest.raises(ValueError):
            ExternalRef(system="any", workspace="", id="X")
        return
    pytest.fail(
        f"No T-1 guard recipe for direct-ingress row {row.row_id} ({row.symbol}). "
        f"Update _assert_t1_for_row to handle file_path={path!r}."
    )


def _assert_t2_for_row(row: AuditRow) -> None:
    """T-2: caller-supplied identity is preserved verbatim. Per-family check."""
    path = row.file_path
    if path.endswith("connectors/linear.py"):
        linear_cfg = LinearConnectorConfig(api_key="k", team_id=SENTINEL_TEAMSPACE)
        linear_conn = LinearConnector(linear_cfg)
        assert linear_conn.config.team_id == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/jira.py"):
        jira_cfg = JiraConnectorConfig(
            base_url="https://example.atlassian.net",
            email="e",
            api_token="t",
            project_key=SENTINEL_TEAMSPACE,
        )
        jira_conn = JiraConnector(jira_cfg)
        assert jira_conn.config.project_key == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/github.py"):
        github_cfg = GitHubConnectorConfig(owner=SENTINEL_TEAMSPACE, repo="r", token="t")
        github_conn = GitHubConnector(github_cfg)
        assert github_conn.config.owner == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/gitlab.py"):
        gitlab_cfg = GitLabConnectorConfig(project_id=SENTINEL_TEAMSPACE, token="t")
        gitlab_conn = GitLabConnector(gitlab_cfg)
        assert gitlab_conn.config.project_id == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/azure_devops.py"):
        ado_cfg = AzureDevOpsConnectorConfig(
            organization=SENTINEL_TEAMSPACE,
            project="p",
            personal_access_token="t",
        )
        ado_conn = AzureDevOpsConnector(ado_cfg)
        assert ado_conn.config.organization == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/in_memory.py"):
        mem_conn = InMemoryConnector(name="mem", workspace=SENTINEL_TEAMSPACE)
        assert mem_conn.workspace == SENTINEL_TEAMSPACE
        mem_ref = ExternalRef(system="mem", workspace=SENTINEL_TEAMSPACE, id="X")
        assert mem_ref.workspace == SENTINEL_TEAMSPACE
        return
    if path.endswith("connectors/fp.py") or path.endswith("connectors/beads.py"):
        local_ref = ExternalRef(system="local", workspace=SENTINEL_TEAMSPACE, id="X")
        assert local_ref.workspace == SENTINEL_TEAMSPACE
        return
    if path.endswith("nango.py"):
        nango_cfg = LinearConnectorConfig(api_key="k", team_id=SENTINEL_TEAMSPACE)
        nango_conn = LinearConnector(nango_cfg)
        assert nango_conn.config.team_id == SENTINEL_TEAMSPACE
        return
    if (
        path.endswith("protocols.py")
        or path.endswith("mission_sync.py")
        or path.endswith("sync.py")
    ):
        ref = ExternalRef(system="any", workspace=SENTINEL_TEAMSPACE, id="X")
        assert ref.workspace == SENTINEL_TEAMSPACE
        return
    pytest.fail(
        f"No T-2 round-trip recipe for direct-ingress row {row.row_id} ({row.symbol}). "
        f"Update _assert_t2_for_row to handle file_path={path!r}."
    )


# ---------------------------------------------------------------------------
# T006: Parametric T-1 (fail-closed) over every direct-ingress row
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "row",
    _DIRECT_INGRESS_ROWS,
    ids=[r.row_id for r in _DIRECT_INGRESS_ROWS],
)
def test_t1_fail_closed_per_audit_row(row: AuditRow) -> None:
    """T-1 (contract §4): direct-ingress write surfaces refuse missing identity.

    Because WP01's audit identified zero rows with ``fallback_risk: yes`` and
    WP04 closes as not-applied (no ``MissingPrivateTeamspaceError`` ships in
    this mission), every parametrized case here exercises the type-level /
    construction-guard enforcement: the connector refuses to instantiate (or
    the model layer refuses to construct an ``ExternalRef`` with an empty
    workspace), which structurally precludes any shared/default fallback.
    """
    _assert_t1_for_row(row)


# ---------------------------------------------------------------------------
# T007: Parametric T-2 (identity preservation) over every direct-ingress row
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "row",
    _DIRECT_INGRESS_ROWS,
    ids=[r.row_id for r in _DIRECT_INGRESS_ROWS],
)
def test_t2_identity_preserved_per_audit_row(row: AuditRow) -> None:
    """T-2 (contract §4): a caller-supplied identifier is preserved unchanged.

    Uses a high-entropy sentinel (``PRIV_TEAMSPACE_42_BFLZ``) that no
    reasonable default would produce, so any substitution would be visible.
    """
    _assert_t2_for_row(row)


def test_t2_dataclass_guard_always_runs() -> None:
    """T-2 belt-and-braces: even on the empty-rows branch the sentinel survives.

    Constructs ``LinearHostedParams`` with the sentinel and confirms the
    dataclass round-trips it verbatim. This guarantees the test file is
    never vacuously empty under any audit outcome.
    """
    params = LinearHostedParams(team_id=SENTINEL_TEAMSPACE)
    assert params.team_id == SENTINEL_TEAMSPACE


# ---------------------------------------------------------------------------
# T-3: legacy parameter without NonIngressContext must not select a Teamspace.
# Skipped when WP04 is not applied (the ``MissingPrivateTeamspaceError`` /
# ``NonIngressContext`` types do not exist), per WP01 outcome.
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _CONDITIONAL_TYPES_AVAILABLE,
    reason=(
        "WP04 closes as not-applied per WP01 audit outcome "
        f"({WP01_NO_RISKY_PATH_OUTCOME!r}); MissingPrivateTeamspaceError and "
        "NonIngressContext do not ship in this mission. T-3 will activate "
        "automatically if a future mission introduces those symbols."
    ),
)
def test_t3_legacy_parameter_without_marker_fails_closed() -> None:
    """T-3 (contract §4): legacy team identifier alone does not select a Teamspace."""
    # Only reachable when WP04 has shipped the conditional types.
    assert _CONDITIONAL_TYPES_AVAILABLE  # tautology; satisfies type checker
    pytest.fail(
        "WP04 conditional types are present, but T-3 has not been "
        "implemented for this branch. Update test_no_shared_team_fallback.py "
        "to exercise the dual-accept compatibility shim defined by Rules R-2 / R-5."
    )


# ---------------------------------------------------------------------------
# T009: T-4 — workspace="linear" regression guard
# ---------------------------------------------------------------------------


def test_t4_linear_workspace_default_is_workspace_family_selector() -> None:
    """Regression guard: workspace='linear' is the workspace family selector,
    not a team identity default. See plan Phase 0 §4."""
    # 1. Default literal is "linear".
    params = LinearHostedParams(team_id="X")
    assert params.workspace == "linear"
    # 2. The default is a workspace selector — caller can override.
    custom = LinearHostedParams(team_id="X", workspace="custom-workspace")
    assert custom.workspace == "custom-workspace"
    # 3. team_id has no default — constructing without it is a TypeError.
    with pytest.raises(TypeError):
        LinearHostedParams()  # type: ignore[call-arg]


def test_other_hosted_params_require_identity_at_type_level() -> None:
    """Companion to T-4: every hosted-params dataclass requires identity (no defaults)."""
    with pytest.raises(TypeError):
        JiraHostedParams()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        GitHubHostedParams()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        GitLabHostedParams()  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# T008: Static source guard for known fallback patterns
# ---------------------------------------------------------------------------

TRACKER_SRC = Path(__file__).parents[1] / "src" / "spec_kitty_tracker"
ALLOWLIST_PATH = Path(__file__).parent / "_no_shared_team_fallback_allowlist.txt"
REPO_ROOT = Path(__file__).parents[1]

# Each entry: (compiled regex, pattern id, description). All patterns are
# narrow on purpose to avoid false positives; a true fallback regression will
# almost certainly trip one of these.
FALLBACK_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    # P-1: indexing into a teams iterable (e.g., teams[0])
    (re.compile(r"\bteams\s*\[\s*0\s*\]"), "P-1", "teams[0] index access"),
    # P-2: first/default/primary team identifier
    (
        re.compile(r"\b(first|default|primary)_team\w*\b"),
        "P-2",
        "first/default/primary_team* identifier",
    ),
    # P-3: .first() on a teams iterable
    (re.compile(r"\bteam[_s]?\.first\(\)"), "P-3", "team(s).first() call"),
    # P-4: team_id falsy-fallback (excluding `team_id or None`)
    (
        re.compile(r"\bteam_id\s+or\s+(?!None\b)\w+"),
        "P-4",
        "team_id falsy-fallback ('team_id or X')",
    ),
    # P-5: workspace falsy-fallback (excluding `workspace or None`)
    (
        re.compile(r"\bworkspace\s+or\s+(?!None\b)\w+"),
        "P-5",
        "workspace falsy-fallback ('workspace or X')",
    ),
]


def _load_allowlist() -> set[str]:
    """Load `<rel_path>:<line>` keys from the allowlist file."""
    if not ALLOWLIST_PATH.is_file():
        return set()
    keys: set[str] = set()
    for raw in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Format: "<rel_path>:<line> | <rationale>"
        key = line.split("|", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def test_static_source_guard() -> None:
    """Scan src/spec_kitty_tracker/ for fallback signatures; fail on un-allowlisted matches."""
    assert TRACKER_SRC.is_dir(), (
        f"Expected tracker source at {TRACKER_SRC} but the directory does not exist."
    )

    allowlist = _load_allowlist()
    violations: list[str] = []
    py_files = sorted(TRACKER_SRC.rglob("*.py"))
    assert py_files, f"No .py files found under {TRACKER_SRC} — package layout is broken"

    for py_file in py_files:
        rel = py_file.relative_to(REPO_ROOT).as_posix()
        content = py_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            for pattern, pat_id, description in FALLBACK_PATTERNS:
                if pattern.search(line):
                    key = f"{rel}:{line_num}"
                    if key in allowlist:
                        continue
                    violations.append(f"  {key} [{pat_id}: {description}]\n      {line.strip()}")

    assert not violations, (
        "Fallback-pattern matches found in tracker source:\n"
        + "\n".join(violations)
        + "\n\nEither (a) fix the source to remove the shared-team fallback, or "
        "(b) add an allowlist entry to "
        f"{ALLOWLIST_PATH.relative_to(REPO_ROOT).as_posix()} of the form\n"
        "    <rel_path>:<line> | <audit-findings row id or rationale>\n"
        "referencing the audit-findings row (with fallback_risk: no) that "
        "justifies why this match is NOT a shared-team fallback."
    )
