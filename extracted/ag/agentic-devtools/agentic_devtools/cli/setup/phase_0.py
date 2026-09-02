"""Phase 0 configuration prompts for ``agdt-setup``.

Provides interactive prompts for enabling Phase 0 issue normalization
and configuring sync-back behavior. Skippable with ``--defaults``.
"""

import sys
from pathlib import Path
from typing import cast


def _parse_yes_no(answer: str, default: bool) -> bool:
    """Parse a yes/no answer string, returning *default* for empty or unrecognised input.

    Handles ``y``, ``yes``, ``n``, ``no`` (case-insensitive). Empty string
    returns *default* silently. Unrecognised input prints a warning and
    returns *default* (no retry loop per FR-008).
    """
    stripped = answer.strip().lower()
    if stripped == "":
        return default
    if stripped in {"y", "yes"}:
        return True
    if stripped in {"n", "no"}:
        return False
    print(
        f"  ⚠ Unrecognised input '{answer.strip()}'; using default ({'yes' if default else 'no'}).",
        file=sys.stderr,
    )
    return default


def _prompt_phase_0_config(*, force_prompt: bool = False, use_defaults: bool = False) -> None:
    """Prompt for Phase 0 configuration or apply safe defaults.

    Called during ``agdt-setup`` after platform detection/config save.

    Args:
        force_prompt: When ``True``, re-prompt even if already configured
            (``--reconfigure``).
        use_defaults: When ``True``, skip prompts and write safe defaults
            if absent or preserve existing valid config (``--defaults``).
    """
    from agentic_devtools.config import (
        PHASE_0_DEFAULT_ENABLED,
        PHASE_0_DEFAULT_SYNC_BACK_FIELDS,
        PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE,
        VALID_SYNC_BACK_FIELDS,
        load_repo_config,
        validate_phase_0_config,
    )
    from agentic_devtools.state import _get_git_repo_root

    git_root = _get_git_repo_root()
    if git_root is None:
        print("  ⚠ Cannot determine git root; skipping Phase 0 configuration.", file=sys.stderr)
        return

    git_root_str = str(git_root)

    # Load raw config for presence detection (load_platform_config always injects defaults)
    raw_config = load_repo_config(git_root_str)
    raw_platform = raw_config.get("platform")
    has_phase_0 = isinstance(raw_platform, dict) and isinstance(raw_platform.get("phase_0"), dict)

    # ── Defaults path (--defaults) ──
    if use_defaults:
        if has_phase_0:
            # Validate existing; on failure fall back to safe defaults
            try:
                phase_0 = validate_phase_0_config(raw_platform["phase_0"])  # type: ignore[index]
            except ValueError:
                print(
                    "  ⚠ Existing Phase 0 config invalid; applying safe defaults.",
                    file=sys.stderr,
                )
                phase_0 = validate_phase_0_config({})
        else:
            phase_0 = validate_phase_0_config({})
        _persist(git_root, phase_0)
        return

    # ── Idempotent re-run (already configured, not forcing) ──
    if has_phase_0 and not force_prompt:
        # Normalize and mirror to project.json without modification
        try:
            phase_0 = validate_phase_0_config(raw_platform["phase_0"])  # type: ignore[index]
        except ValueError:
            print(
                "  ⚠ Existing Phase 0 config invalid; skipping mirror.",
                file=sys.stderr,
            )
            return
        _mirror_to_project_json(git_root, phase_0)
        return

    # ── Interactive path ──
    print()
    print("─── Phase 0 Configuration ──────────────────────────────────")
    print("  Configure Phase 0 issue normalization & sync-back.")
    print()

    # Determine current values for bracket defaults (--reconfigure)
    current_enabled = PHASE_0_DEFAULT_ENABLED
    current_sync_back = PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE
    current_sync_back_fields: list[str] = list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS)
    if force_prompt and has_phase_0:
        try:
            existing = validate_phase_0_config(raw_platform["phase_0"])  # type: ignore[index]
            current_enabled = bool(existing.get("enabled", PHASE_0_DEFAULT_ENABLED))
            current_sync_back = bool(existing.get("sync_back_on_merge", PHASE_0_DEFAULT_SYNC_BACK_ON_MERGE))
            current_sync_back_fields = list(cast(list[str], existing["sync_back_fields"]))
        except ValueError:
            pass  # Use defaults for brackets

    # Prompt: enabled
    enabled_bracket = "[Y/n]" if current_enabled else "[y/N]"
    answer = input(f"  Enable Phase 0 issue normalization? {enabled_bracket}: ")
    enabled = _parse_yes_no(answer, current_enabled)

    # Prompt: sync_back_on_merge (only if enabled)
    sync_back_on_merge = False
    if enabled:
        sync_bracket = "[Y/n]" if current_sync_back else "[y/N]"
        answer = input(f"  Enable sync-back on merge? {sync_bracket}: ")
        sync_back_on_merge = _parse_yes_no(answer, current_sync_back)
    elif force_prompt and current_enabled:
        # Disabling resets sync_back_on_merge per FR-002
        sync_back_on_merge = False

    # When enabling sync-back, sanitize sync_back_fields against the allowed set.
    # Fields loaded from an existing config may have been saved while sync_back_on_merge
    # was false (unknown fields are silently accepted in that state); if any are invalid
    # now that both gates will be active, reset to defaults so _persist() won't raise.
    if sync_back_on_merge:
        _valid = frozenset(VALID_SYNC_BACK_FIELDS)
        if any(f not in _valid for f in current_sync_back_fields):
            print(
                "  ⚠ sync_back_fields contained invalid entries; resetting to defaults.",
                file=sys.stderr,
            )
            current_sync_back_fields = list(PHASE_0_DEFAULT_SYNC_BACK_FIELDS)

    phase_0_result: dict[str, object] = {
        "enabled": enabled,
        "sync_back_on_merge": sync_back_on_merge,
        "sync_back_fields": current_sync_back_fields,
    }
    if _persist(git_root, phase_0_result):
        print("  ✓ Phase 0 configuration saved")


def _persist(git_root: Path, phase_0: dict[str, object]) -> bool:
    """Validate and persist phase_0 to both config files."""
    from agentic_devtools.config import (
        load_platform_config,
        save_platform_config,
        validate_phase_0_config,
    )

    phase_0 = validate_phase_0_config(phase_0)

    # Save to .github/agdt-config.json
    git_root_str = str(git_root)
    platform_config = load_platform_config(git_root_str)
    platform_config["phase_0"] = phase_0
    platform_saved = save_platform_config(git_root_str, platform_config)
    if not platform_saved:
        print(
            "  ⚠ Failed to save Phase 0 to platform config — check directory permissions.",
            file=sys.stderr,
        )

    # Save to .agdt/config/project.json
    project_saved = _mirror_to_project_json(git_root, phase_0)
    return platform_saved and project_saved


def _mirror_to_project_json(git_root: Path, phase_0: dict[str, object]) -> bool:
    """Mirror phase_0 dict to project.json."""
    from agentic_devtools.cli.config.project_config import (
        load_project_config,
        save_project_config,
    )

    try:
        project_cfg = load_project_config(git_root=git_root)
        project_cfg["phase_0"] = phase_0
        save_project_config(project_cfg, git_root=git_root)
        return True
    except (RuntimeError, OSError) as exc:
        print(
            f"  ⚠ Failed to save Phase 0 to project.json ({exc}) — skipping.",
            file=sys.stderr,
        )
        return False
