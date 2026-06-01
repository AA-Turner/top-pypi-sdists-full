#!/usr/bin/env python3
"""Doc-vs-code drift checker.

Catches the class of bug the round-2 reviewer flagged: numeric claims
in prose ("344 passing", "60 indicators", "14 detectors") and command
references ("`efterlev detectors list`") that diverge from runtime
truth. The honesty-pass model is unsustainable — by the time the
maintainer notices a number went stale, the next one already has.
This script makes the check enforceable.

What's checked at this revision:
  1. Test count claims in prose match `pytest -q --collect-only -m "not e2e"`.
  2. Detector count claims match the runtime registry (the 16-of-30
     bug fixed 2026-04-25 is exactly this class).
  3. FRMR indicator count claims match the structural count of the
     vendored catalog.
  4. Source-file count claims match `find src -name "*.py" | wc -l`.
  5. Every `efterlev <verb>` reference in user-facing prose resolves
     to an actual CLI command.
  6. "First-detector" claims paired with a KSI-XXX-YYY identifier in
     prose are checked against the live `mapping.yaml` set — if the
     cited KSI is evidenced by more than one detector, the claim is
     wrong (the detector isn't "first" anymore). Catches the bug
     class fixed 2026-05-10 (PR #205 / #207 / v0.1.45 CHANGELOG
     claimed `aws.api_gateway_auth_required` was the library's
     first detector for KSI-CNA-EIS / KSI-CNA-DFP, but both were
     already covered by `aws.access_analyzer_enabled` and
     `aws.ec2_imdsv2_required` respectively).

Out of scope deliberately:
  - PyPI install honesty: README + LIMITATIONS already explicitly call
    out that pipx install is gated on launch. The grep-scrub script
    catches the inverse drift (post-launch references slipping in pre-
    launch). This script trusts that.
  - Internal-doc test counts (DECISIONS.md historical entries are
    snapshots-in-time and DO NOT need to match current).

Exit 0 = clean. Exit 1 = at least one drift; details on stdout.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# User-facing docs that should agree with runtime. Internal docs
# (CLAUDE.md, DECISIONS.md) deliberately carry dated "end state at
# <date>" snapshots — those are journal entries by design and should
# not be auto-updated. The reviewer's specific concern was the
# user-facing surface (README, LIMITATIONS, THREAT_MODEL, etc.); this
# checker scopes itself there.
USER_FACING_DOCS = [
    "README.md",
    "LIMITATIONS.md",
    "THREAT_MODEL.md",
    "CONTRIBUTING.md",
    "docs/architecture.md",
    "docs/quickstart.md",
    "docs/index.md",
    "docs/concepts/ksis-for-engineers.md",
    "docs/concepts/evidence-vs-claims.md",
    "docs/concepts/provenance.md",
    "docs/concepts/what-efterlev-is-not.md",
    "docs/reference/cli.md",
    "docs/reference/detectors.md",
    "docs/reference/primitives.md",
    "catalogs/README.md",
]

# Dated retrospectives, if any are reintroduced, are point-in-time and excluded.
EXCLUDE = re.compile(r"^docs/dogfood-\d{4}-\d{2}-\d{2}\.md$")

# A CLI reference that lives in a context where the prose explicitly
# names it as not-yet-implemented or planned doesn't count as a drift
# claim. These markers must appear in the SAME paragraph as the
# command reference (within ±200 chars of the match) for the
# exemption to apply.
ASPIRATIONAL_MARKERS = re.compile(
    r"(not yet implemented|not implemented|"
    r"planned for v|v1 command|v1\+|v1\.5\+|"
    r"v0\.1\.1[8-9]\+?|v0\.1\.2[0-9]\+?|v0\.2\.0\+?|"
    r"tracked as follow-up|follow-up|"
    r"deferred|aspirational|roadmap|"
    r"Tier 1\+?|Tier 2\+?|Tier 0\+?|"
    r"held until|queued for|new `efterlev|"
    r"\bTODO\b|\bFIXME\b)",
    re.IGNORECASE,
)


def runtime_test_count() -> int:
    """How many tests `pytest -m "not e2e"` collects right now.

    Counts `path::test_name` lines from `pytest --collect-only -q`. The
    summary-line approach is unreliable across pytest versions; the
    `path::test_name` shape is stable.
    """
    out = subprocess.check_output(
        ["uv", "run", "--extra", "dev", "pytest", "-m", "not e2e", "--collect-only", "-q"],
        cwd=REPO_ROOT,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return sum(1 for line in out.splitlines() if "::" in line and line.startswith("tests/"))


def runtime_detector_count() -> int:
    """How many detectors register on `import efterlev.detectors`."""
    out = subprocess.check_output(
        [
            "uv",
            "run",
            "python",
            "-c",
            "import efterlev.detectors; "
            "from efterlev.detectors.base import get_registry; "
            "print(len(get_registry()))",
        ],
        cwd=REPO_ROOT,
        text=True,
    )
    return int(out.strip())


def runtime_indicator_count() -> int:
    """How many KSIs the FRMR catalog declares structurally."""
    catalog = json.loads((REPO_ROOT / "catalogs" / "frmr" / "FRMR.documentation.json").read_text())
    return sum(len(theme.get("indicators", {})) for theme in catalog.get("KSI", {}).values())


def runtime_source_file_count() -> int:
    """Source-file count under `src/efterlev`. Used by README's lint stanza."""
    return sum(1 for _ in (REPO_ROOT / "src" / "efterlev").rglob("*.py"))


def runtime_ksi_detector_counts() -> dict[str, int]:
    """How many detectors evidence each KSI, by `id` from each detector's
    `mapping.yaml`. Used to validate "first-detector for KSI-X" prose
    claims — a KSI with count > 1 cannot legitimately be cited as the
    new detector's first coverage.

    `mapping.yaml`'s `ksis` field accepts two shapes (both seen in the
    library): a list of strings (`- KSI-CNA-MAT`) and a list of dicts
    with an `id` field (`- id: KSI-CNA-MAT`). Both are normalized.
    """
    import yaml  # lazy import — only this check needs it

    counts: dict[str, int] = {}
    for mapping_path in (REPO_ROOT / "src" / "efterlev" / "detectors").rglob("mapping.yaml"):
        with mapping_path.open(encoding="utf-8") as fp:
            data = yaml.safe_load(fp)
        if not isinstance(data, dict):
            continue
        ksis = data.get("ksis") or []
        for k in ksis:
            kid = k.get("id") if isinstance(k, dict) else k
            if isinstance(kid, str) and kid.startswith("KSI-"):
                counts[kid] = counts.get(kid, 0) + 1
    return counts


def runtime_cli_commands() -> set[str]:
    """Every command/verb the CLI exposes. Used to validate prose references.

    Captures top-level commands AND subcommand verbs (`agent gap`,
    `detectors list`, `provenance show`, etc.). Returned as the
    "<top> <sub>" or "<top>" string a doc would write.
    """
    out = subprocess.check_output(
        [
            "uv",
            "run",
            "python",
            "-c",
            "from efterlev.cli.main import app\n"
            "import typer\n"
            "from typer.main import get_command\n"
            "click_app = get_command(app)\n"
            "names = set()\n"
            "def walk(cmd, prefix=()):\n"
            "    for n, sub in getattr(cmd, 'commands', {}).items():\n"
            "        names.add(' '.join(prefix + (n,)))\n"
            "        walk(sub, prefix + (n,))\n"
            "walk(click_app)\n"
            "print('\\n'.join(sorted(names)))",
        ],
        cwd=REPO_ROOT,
        text=True,
    )
    return set(out.strip().splitlines())


# --- claim extractors ----------------------------------------------------------

# Patterns deliberately conservative — match must be unambiguous to
# count as a claim. Loose matches generate noise that desensitizes
# the maintainer to the real findings.

TEST_COUNT_RE = re.compile(r"\b(\d{2,4})\s+(?:tests?\s+(?:passing|pass)|passing)\b")
DETECTOR_COUNT_RE = re.compile(r"\b(\d{1,3})\s+detectors?\s+(?:register|registered|run|loaded)\b")
INDICATOR_COUNT_RE = re.compile(
    r"\b(\d{1,3})\s+(?:KSIs?|indicators?)\s+(?:in\s+FRMR|across\s+\d+\s+themes|in\s+the\s+baseline)"
)
SOURCE_FILES_RE = re.compile(r"\b(\d{1,4})\s+source\s+files?\b")
CLI_REFERENCE_RE = re.compile(r"`efterlev\s+([a-z][a-z\- ]*?[a-z])(?:\s+[<\-]|\s*`)")

# `.efterlev/reports/<name>/` shape claims must match the actual layout
# the CLI emits. Today only POA&M lives in a subdirectory; gap, scan,
# attestation, documentation reports are flat under `.efterlev/reports/`.
# When a new subdirectory is added in code, this allowlist must be
# updated in the same patch — the failure surfaces it.
REPORT_SUBDIR_RE = re.compile(r"\.efterlev/reports/([a-z][a-z\-]*)/")
ALLOWED_REPORT_SUBDIRS = {"poam"}

# "Current version" claims in user-facing docs. The bug class: each
# release ships a wheel where `__version__` advances, but README /
# docs/index.md / CLAUDE.md prose carrying "vX.Y.Z is current" or
# "vX.Y.Z current (date)" gets forgotten and rots silently. The v0.1.13
# triage caught two stale claims in docs/index.md (G1). This rule scans
# for the canonical phrasings and asserts the version matches the
# in-source `__version__`. Past-tense references ("v0.1.11 closed five
# findings", "since v0.1.0") deliberately don't match — those are
# historical, not current-state claims.
CURRENT_VERSION_CLAIM_RE = re.compile(
    r"\b(?:v|version\s+)(\d+\.\d+\.\d+)\b\s*(?:is\s+current|current\b)"
)


def check_doc(path: Path, expected: dict[str, int], cli_commands: set[str]) -> list[str]:
    """Return a list of finding strings (empty list = clean)."""
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(REPO_ROOT)

    # Numeric claims.
    for m in TEST_COUNT_RE.finditer(text):
        claimed = int(m.group(1))
        if claimed != expected["tests"]:
            line_no = text[: m.start()].count("\n") + 1
            findings.append(
                f"{rel}:{line_no}: claims '{claimed} passing' but actual is {expected['tests']}"
            )
    for m in DETECTOR_COUNT_RE.finditer(text):
        claimed = int(m.group(1))
        if claimed != expected["detectors"]:
            line_no = text[: m.start()].count("\n") + 1
            findings.append(
                f"{rel}:{line_no}: claims '{claimed} detectors' but registry has "
                f"{expected['detectors']}"
            )
    for m in INDICATOR_COUNT_RE.finditer(text):
        claimed = int(m.group(1))
        if claimed != expected["indicators"]:
            line_no = text[: m.start()].count("\n") + 1
            findings.append(
                f"{rel}:{line_no}: claims '{claimed} indicators' but FRMR catalog has "
                f"{expected['indicators']}"
            )
    for m in SOURCE_FILES_RE.finditer(text):
        claimed = int(m.group(1))
        if claimed != expected["source_files"]:
            line_no = text[: m.start()].count("\n") + 1
            findings.append(
                f"{rel}:{line_no}: claims '{claimed} source files' but actual is "
                f"{expected['source_files']}"
            )

    # CLI references. Keep the verb conservative — the regex picks up
    # only the form `efterlev <verb> [<verb>]` followed by a flag, an
    # arg placeholder, or backtick-close.
    for m in CLI_REFERENCE_RE.finditer(text):
        verb = m.group(1).strip()
        # Strip option-shaped suffixes that aren't real subcommands.
        verb = re.sub(r"\s+--?\w+.*$", "", verb)
        if not verb or verb in cli_commands:
            continue
        # Tolerate prefix matches: `agent` is a group; `agent gap` is the
        # actual command. A doc that says `efterlev agent` (with no sub)
        # is referring to the group root, which is legitimate.
        if any(c.startswith(verb + " ") for c in cli_commands):
            continue
        # Tolerate aspirational references: prose that names a not-yet-
        # implemented command in the same paragraph as a "planned for v1"
        # / "not yet implemented" marker is honest disclosure, not drift.
        nearby = text[max(0, m.start() - 200) : m.start() + 200]
        if ASPIRATIONAL_MARKERS.search(nearby):
            continue
        line_no = text[: m.start()].count("\n") + 1
        findings.append(
            f"{rel}:{line_no}: references `efterlev {verb}` but CLI has no such command"
        )

    return findings


def check_current_version_claims(path: Path, expected_version: str) -> list[str]:
    """Flag `vX.Y.Z is current` / `vX.Y.Z current` claims that disagree
    with `efterlev.__version__`.

    Catches the bug class the v0.1.13 triage surfaced (G1):
    docs/index.md said "v0.1.11 current" and "45 ship today (v0.1.11)"
    long after v0.1.13 had shipped. The check is per-doc, runs on every
    `.md` repo-wide, and uses the in-source `__version__` as truth.
    Past-tense references ("v0.1.11 closed five findings", "since
    v0.1.0") don't match the regex — those are historical.
    """
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(REPO_ROOT)
    for m in CURRENT_VERSION_CLAIM_RE.finditer(text):
        claimed = m.group(1)
        if claimed == expected_version:
            continue
        line_no = text[: m.start()].count("\n") + 1
        findings.append(
            f"{rel}:{line_no}: claims 'v{claimed} current' but __version__ is {expected_version}"
        )
    return findings


def runtime_version() -> str:
    """In-source `efterlev.__version__` — the single source of truth that
    pyproject.toml's hatch dynamic versioning reads."""
    out = subprocess.check_output(
        ["uv", "run", "python", "-c", "import efterlev; print(efterlev.__version__)"],
        cwd=REPO_ROOT,
        text=True,
    )
    return out.strip()


def check_report_paths(path: Path) -> list[str]:
    """Flag `.efterlev/reports/<subdir>/` references whose subdir is unknown.

    Catches bugs like:
      - `reports/gap/gap-<ts>.json` (gap reports are flat — no `gap/` subdir)
      - `reports/poam-<ts>.md` (POA&M is in a subdir — needs `poam/`)

    Runs on all `.md` files repo-wide because path-layout claims are
    facts independent of which doc carries them. Excludes test
    fixtures (which may carry deliberately-wrong paths).
    """
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(REPO_ROOT)
    for m in REPORT_SUBDIR_RE.finditer(text):
        subdir = m.group(1)
        if subdir in ALLOWED_REPORT_SUBDIRS:
            continue
        line_no = text[: m.start()].count("\n") + 1
        findings.append(
            f"{rel}:{line_no}: references `.efterlev/reports/{subdir}/` but only "
            f"{sorted(ALLOWED_REPORT_SUBDIRS)} are real subdirs (others are flat)"
        )
    return findings


# "First-detector" prose claims. The shape: `(library's )?first detector` /
# `first-detector coverage` followed (within ~200 chars) by one or more
# KSI-XXX-YYY identifiers. The check verifies each cited KSI is in fact
# evidenced by exactly one detector — claims paired with a KSI that
# has count > 1 are stale or wrong.
#
# Resource-type-side claims like "library's first `aws_lambda_function`-
# side detector" don't have a KSI in proximity and naturally don't
# trigger — they're a different (and verifiable elsewhere) class of
# claim about resource-type coverage, not KSI coverage.
#
# Catches the bug class fixed 2026-05-10: PR #205 / PR #207 / v0.1.45
# CHANGELOG all claimed `aws.api_gateway_auth_required` was the
# library's first detector for KSI-CNA-EIS / KSI-CNA-DFP, but both
# were already covered by `aws.access_analyzer_enabled` and
# `aws.ec2_imdsv2_required`.
# Match both ASCII apostrophe (U+0027) and U+2019 (right single
# quotation mark) -- docs in this repo use both; rich-text editors
# auto-substitute the curly form for the straight ASCII apostrophe.
# The U+2019 is written as a unicode escape so ruff RUF001 doesn't
# flag this string for an ambiguous literal character.
FIRST_DETECTOR_CLAIM_RE = re.compile(
    "(?:library(?:'|\u2019)s\\s+)?first[\\s\\-]detector"
    "|first[\\s\\-]detector\\s+(?:coverage|evidence)",
    re.IGNORECASE,
)
KSI_ID_RE = re.compile(r"\bKSI-[A-Z]{3}-[A-Z]{3}\b")
# Window after the "first-detector" phrase to look in for KSI references.
# 250 chars covers multi-clause sentences like "library's first detector
# evidencing X and Y -- both KSIs were previously uncovered" without
# pulling in unrelated KSI references from the next paragraph.
_KSI_LOOKAHEAD_CHARS = 250


def check_first_detector_claims(path: Path, ksi_counts: dict[str, int]) -> list[str]:
    """Flag "first-detector" claims about KSIs that already have multiple
    detectors. See FIRST_DETECTOR_CLAIM_RE block comment for the
    bug class this catches.

    DECISIONS.md is excluded — entries there are dated snapshots-in-time
    of what was thought at the time. Wrong claims are corrected via
    adjacent append-only correction entries (DECISIONS 2026-05-10
    "Correction: KSI-CNA-EIS / KSI-CNA-DFP …"), not edited retroactively.
    Auto-flagging the preserved-wrong text would fight the append-only
    contract.
    """
    findings: list[str] = []
    rel = path.relative_to(REPO_ROOT)
    if rel.name == "DECISIONS.md":
        return findings
    text = path.read_text(encoding="utf-8")
    for m in FIRST_DETECTOR_CLAIM_RE.finditer(text):
        window = text[m.start() : m.end() + _KSI_LOOKAHEAD_CHARS]
        cited = set(KSI_ID_RE.findall(window))
        for ksi in sorted(cited):
            count = ksi_counts.get(ksi, 0)
            if count > 1:
                line_no = text[: m.start()].count("\n") + 1
                findings.append(
                    f"{rel}:{line_no}: 'first-detector' claim cites {ksi}, "
                    f"but {ksi} is evidenced by {count} detectors in the "
                    f"library — claim is stale or wrong"
                )
    return findings


def all_markdown_files() -> list[Path]:
    """Markdown under the repo, minus test fixtures and build output."""
    skip_parts = {".git", "dist", "build", "site", "__pycache__", "node_modules", ".efterlev"}
    out: list[Path] = []
    for p in REPO_ROOT.rglob("*.md"):
        if any(part in skip_parts for part in p.relative_to(REPO_ROOT).parts):
            continue
        # Detector fixtures live under `src/efterlev/detectors/<id>/fixtures/`
        # — exclude them since they may carry deliberately-bad sample paths.
        if "fixtures" in p.parts:
            continue
        # `tests/` may carry sample paths a check shouldn't second-guess.
        if p.relative_to(REPO_ROOT).parts[0] == "tests":
            continue
        out.append(p)
    return out


def main() -> int:
    expected = {
        "tests": runtime_test_count(),
        "detectors": runtime_detector_count(),
        "indicators": runtime_indicator_count(),
        "source_files": runtime_source_file_count(),
    }
    cli_commands = runtime_cli_commands()

    ksi_counts = runtime_ksi_detector_counts()
    print(
        f"runtime: {expected['tests']} tests, "
        f"{expected['detectors']} detectors, "
        f"{expected['indicators']} indicators, "
        f"{expected['source_files']} source files, "
        f"{len(cli_commands)} CLI commands, "
        f"{len(ksi_counts)} KSIs covered by detectors"
    )

    all_findings: list[str] = []
    for rel in USER_FACING_DOCS:
        if EXCLUDE.match(rel):
            continue
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        all_findings.extend(check_doc(path, expected, cli_commands))

    # Path-layout claims are facts. Run repo-wide, not just on the
    # user-facing list — internal docs reference these paths too,
    # and a wrong layout claim there confuses contributors.
    for path in all_markdown_files():
        all_findings.extend(check_report_paths(path))

    # "Current version" claims are facts too. Run repo-wide so historical
    # snapshots in DECISIONS / past CHANGELOG entries don't drift either.
    # Past-tense references ("v0.1.11 closed five findings") don't trip
    # the regex — only "vX.Y.Z is current" / "vX.Y.Z current".
    expected_version = runtime_version()
    for path in all_markdown_files():
        all_findings.extend(check_current_version_claims(path, expected_version))

    # "First-detector" claims paired with KSI-XXX-YYY identifiers are
    # facts about the live mapping.yaml set. Run repo-wide; the check
    # function excludes DECISIONS.md per the append-only contract.
    for path in all_markdown_files():
        all_findings.extend(check_first_detector_claims(path, ksi_counts))

    if not all_findings:
        print("RESULT: clean. No doc-vs-code drift.")
        return 0

    print(f"\nRESULT: {len(all_findings)} drift finding(s):")
    for f in all_findings:
        print(f"  {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
