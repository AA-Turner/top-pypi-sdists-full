"""Routing layer for the ``agdt-create-epic`` command (issue #2117).

This module owns the *front door* of the repurposed ``agdt-create-epic``
command: it parses the optional positional JSON plan path plus the
``--dry-run``, ``--start-from``, and ``--provider`` flags, decides between the
new *tree mode* and the preserved *legacy single-epic mode*, and dispatches to
the correct execution path.

Behavioral contract (see ``specs/2117-cli-entry-argument-parsing/spec.md``):

* A ``--help`` request short-circuits all routing and validation, prints usage
  to stdout, and exits ``0`` (handled natively by :mod:`argparse`).
* When a positional file path is supplied the command selects tree mode and
  forwards the invocation to
  :func:`agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree`. The
  router never opens, reads, or validates the file (FR-011).
* When no file is supplied, deterministic validation precedence is applied
  (``unsupported_provider`` → ``start_from_requires_file`` →
  ``provider_requires_file`` → ``missing_input``); a rejected invocation emits a
  single NDJSON validation record to stderr and exits ``2`` (FR-012, NFR-002).
* When no file is supplied and any legacy ``jira.*`` single-epic input state key
  is present, the command dispatches to the unchanged legacy creation path
  (FR-004, NFR-004).

Routing decisions for dispatched invocations are emitted as single-line JSON
routing records from inside the spawned background task so they are captured by
the command's background-task log (FR-009). New pre-spawn validation failures
emit their structured record to the foreground process's stderr (NFR-003).
"""

from __future__ import annotations

import argparse
import json
import sys

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import get_value, load_state
from agentic_devtools.task_state import print_task_tracking_info

# --- Structured record schema constants (FR-009, NFR-003) --------------------

ROUTING_EVENT = "create_epic.routing"
VALIDATION_EVENT = "create_epic.validation_error"

MODE_TREE = "tree"
MODE_LEGACY = "legacy"

BASIS_FILE_PRESENT = "file_present"
BASIS_FILE_OVERRIDES_LEGACY = "file_overrides_legacy_state"
BASIS_LEGACY_PRESENT = "legacy_state_present"

REASON_UNSUPPORTED_PROVIDER = "unsupported_provider"
REASON_START_FROM_REQUIRES_FILE = "start_from_requires_file"
REASON_PROVIDER_REQUIRES_FILE = "provider_requires_file"
REASON_MISSING_INPUT = "missing_input"

# Providers recognized by the no-file rejection layer. Tree-mode provider
# compatibility (including diagnostic values such as ``markdown``) is owned by
# the downstream provider-resolution/factory path, not this router (FR-007).
SUPPORTED_PROVIDERS = ("github", "jira")

# Legacy single-epic input state sub-keys within the ``jira`` namespace (FR-004).
# Presence of *any* of these keys (regardless of value, including empty string,
# null, or false) selects legacy mode when no file is supplied.
LEGACY_STATE_SUBKEYS = (
    "project_key",
    "summary",
    "epic_name",
    "role",
    "desired_outcome",
    "benefit",
    "acceptance_criteria",
    "additional_information",
    "description",
    "labels",
    "dry_run",
)

_ROUTER_MODULE = "agentic_devtools.cli.jira.create_epic_router"
_EXIT_VALIDATION_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for ``agdt-create-epic`` (FR-001, FR-002, FR-008)."""
    parser = argparse.ArgumentParser(
        prog="agdt-create-epic",
        description=(
            "Create an epic. With a JSON plan file, route to tree mode "
            "(reserved handoff — tree pipeline available in #2118; currently "
            "no-op); with no file and legacy jira.* state, "
            "create a single Jira epic (legacy mode)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Modes:\n"
            "  Tree mode   agdt-create-epic plan.json [--start-from REF] "
            "[--provider github|jira] [--dry-run]\n"
            "  Legacy mode agdt-create-epic [--provider jira] [--dry-run]\n"
            "              (requires legacy jira.* state; see agdt-set jira.*)\n"
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Optional path to a JSON epic-tree plan file. When present, selects tree mode.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without creating issues (valid in both tree and legacy mode).",
    )
    parser.add_argument(
        "--start-from",
        default=None,
        metavar="REFERENCE",
        help="Named node reference to resume tree creation from (requires a file argument).",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Issue provider to target: github or jira (github requires a file argument).",
    )
    return parser


def normalize_provider(provider: str | None) -> str | None:
    """Normalize a provider value by trimming whitespace and lowercasing (FR-012).

    Returns ``None`` unchanged when no provider was supplied.
    """
    if provider is None:
        return None
    return provider.strip().lower()


def legacy_state_present() -> bool:
    """Return True when any legacy single-epic ``jira.*`` input key exists in state.

    Presence is determined by key existence, not truthiness, so an empty
    string, ``null``, or ``false`` value still selects legacy mode (FR-004).
    """
    state = load_state()
    if not isinstance(state, dict):
        return False
    jira_ns = state.get("jira")
    if not isinstance(jira_ns, dict):
        return False
    return any(subkey in jira_ns for subkey in LEGACY_STATE_SUBKEYS)


def _serialize_record(record: dict[str, object]) -> str:
    """Serialize a record as a single-line NDJSON string terminated by one newline."""
    return json.dumps(record, ensure_ascii=False) + "\n"


def emit_routing_record(mode: str, basis: str, *, file_path: str | None = None) -> None:
    """Write a single-line routing record to stdout (captured by the task log, FR-009)."""
    record: dict[str, object] = {"event": ROUTING_EVENT, "mode": mode, "basis": basis}
    if file_path is not None:
        record["file_path"] = file_path
    sys.stdout.write(_serialize_record(record))


def _reject(reason: str, message: str, *, provider: str | None = None, start_from: str | None = None) -> None:
    """Emit one NDJSON validation record plus a human-readable message and exit 2.

    Args:
        reason: Stable machine-readable reason code from the FR-012 precedence list.
        message: Distinct, actionable human-readable message written to stderr.
        provider: Normalized provider value to include when present and unambiguous.
        start_from: Supplied ``--start-from`` value to include when it explains
            the rejection.
    """
    record: dict[str, object] = {"event": VALIDATION_EVENT, "reason": reason}
    if provider is not None:
        record["provider"] = provider
    if start_from is not None:
        record["start_from"] = start_from
    sys.stderr.write(f"{message}\n")
    sys.stderr.write(_serialize_record(record))
    sys.exit(_EXIT_VALIDATION_ERROR)


def run_tree_mode(
    file_path: str,
    *,
    start_from: str | None = None,
    provider: str | None = None,
    dry_run: bool = False,
    basis: str = BASIS_FILE_PRESENT,
) -> None:
    """Spawned tree-mode task target: log the routing decision then forward to #2118.

    This runs inside the background task process so the routing record lands in
    the command's background-task log (FR-009). It forwards the parsed inputs
    unchanged to the reserved ``create_epic_tree`` handoff contract (FR-003,
    FR-006, FR-011).
    """
    from .tree_mode_commands import create_epic_tree

    emit_routing_record(MODE_TREE, basis, file_path=file_path)
    create_epic_tree(file_path, start_from=start_from, provider=provider, dry_run=dry_run)


def run_legacy_mode(*, dry_run_override: bool = False) -> None:
    """Spawned legacy-mode task target: log the routing decision then run legacy creation.

    Runs inside the background task process (FR-009). Delegates to the unchanged
    legacy epic-creation path, passing the invocation-scoped dry-run override
    without mutating persistent state (FR-004, NFR-004).
    """
    from .create_commands import create_epic

    emit_routing_record(MODE_LEGACY, BASIS_LEGACY_PRESENT)
    create_epic(dry_run_override=dry_run_override)


def _dispatch_tree(
    file_path: str,
    *,
    start_from: str | None,
    provider: str | None,
    dry_run: bool,
    legacy_present: bool,
) -> None:
    """Select tree mode and spawn the tree-mode background task (FR-003, FR-010)."""
    basis = BASIS_FILE_OVERRIDES_LEGACY if legacy_present else BASIS_FILE_PRESENT
    task = run_function_in_background(
        _ROUTER_MODULE,
        "run_tree_mode",
        command_display_name="agdt-create-epic",
        func_kwargs={
            "file_path": file_path,
            "start_from": start_from,
            "provider": provider,
            "dry_run": dry_run,
            "basis": basis,
        },
    )
    print_task_tracking_info(task, "Creating epic tree")


def _require_legacy_value(subkey: str, error_example: str) -> None:
    """Preserve the legacy async wrapper's pre-spawn required-field validation.

    Missing ``jira.project_key``, ``jira.summary``, or ``jira.epic_name`` fails
    here before any background task is spawned, exactly as the pre-takeover
    legacy command did (FR-004, US2 scenario 3). No routing record is emitted on
    this path because no background task exists (FR-009).
    """
    if not get_value(f"jira.{subkey}"):
        print(f"Error: jira.{subkey} is required. Use: {error_example}", file=sys.stderr)
        sys.exit(1)


def _dispatch_legacy(dry_run_flag: bool) -> None:
    """Select legacy mode and spawn the unchanged legacy creation path (FR-004)."""
    _require_legacy_value("project_key", "agdt-set jira.project_key PROJECT")
    _require_legacy_value("summary", 'agdt-set jira.summary "Epic Title"')
    _require_legacy_value("epic_name", 'agdt-set jira.epic_name "Epic Name"')

    task = run_function_in_background(
        _ROUTER_MODULE,
        "run_legacy_mode",
        command_display_name="agdt-create-epic",
        func_kwargs={"dry_run_override": dry_run_flag},
    )
    print_task_tracking_info(task, "Creating epic")


def route_create_epic(argv: list[str] | None = None) -> None:
    """Parse arguments and route ``agdt-create-epic`` to tree or legacy mode.

    Args:
        argv: Optional argument vector (defaults to ``sys.argv[1:]`` via argparse).

    A ``--help`` request exits 0 (argparse). No-file validation rejections exit
    2. Successful routing to tree or legacy mode returns after spawning the
    background task; any later non-zero status originates downstream (NFR-002).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    file_path: str | None = args.file
    start_from: str | None = args.start_from
    provider = normalize_provider(args.provider)
    dry_run_flag = bool(args.dry_run)

    legacy_present = legacy_state_present()

    # Tree mode: an explicit file always wins, even over legacy state (FR-010).
    if file_path is not None:
        _dispatch_tree(
            file_path,
            start_from=start_from,
            provider=provider,
            dry_run=dry_run_flag,
            legacy_present=legacy_present,
        )
        return

    # No-file deterministic rejection precedence (FR-012).
    if provider is not None and provider not in SUPPORTED_PROVIDERS:
        _reject(
            REASON_UNSUPPORTED_PROVIDER,
            f"Error: Unsupported provider '{provider}'. Supported providers are: github, jira.",
            provider=provider,
        )

    if start_from is not None:
        _reject(
            REASON_START_FROM_REQUIRES_FILE,
            "Error: --start-from requires a JSON plan file argument (tree mode).",
            provider=provider,
            start_from=start_from,
        )

    if provider == "github":
        _reject(
            REASON_PROVIDER_REQUIRES_FILE,
            "Error: --provider github requires a JSON plan file argument. "
            "Legacy mode supports only the default provider or --provider jira.",
            provider=provider,
        )

    if not legacy_present:
        _reject(
            REASON_MISSING_INPUT,
            "Error: No input provided. Supply a JSON plan file (tree mode) or set "
            "legacy jira.* state (legacy mode). See agdt-create-epic --help.",
            provider=provider,
        )

    # Legacy mode (FR-004): no file, legacy state present, no higher-precedence rejection.
    _dispatch_legacy(dry_run_flag)
