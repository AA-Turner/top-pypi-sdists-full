import contextlib
import warnings
from dataclasses import dataclass, field

from django.db.backends.base.base import BaseDatabaseWrapper

from django_pg_utils.set._identifier import validate_guc_name
from django_pg_utils.set._result import SettingResult
from django_pg_utils.set._settings import DEFAULT_SETTINGS, HushSetting


@dataclass
class PgRestoreState:
    """State needed to restore PG settings on scope exit."""

    used_set_local: bool
    changed_settings: list[tuple[str, str]] = field(default_factory=list)
    # Each entry is (setting_name, original_value)


def _in_transaction(connection: BaseDatabaseWrapper) -> bool:
    """Check if the Django connection is inside an atomic block."""
    return connection.in_atomic_block


def _emit_notice(connection: BaseDatabaseWrapper, message: str) -> None:
    """Emit a RAISE NOTICE on the given connection.

    PL/pgSQL DO blocks can't take protocol bind parameters, so the message is
    interpolated into the SQL text. Two hardening choices make that safe for the
    file:line caller locations we pass:

    - The message is the *argument* to ``RAISE NOTICE '%', ...`` rather than the
      format string itself, so a literal ``%`` in a path is data, not a
      placeholder (which would otherwise raise "too few parameters").
    - Both the DO body and the message literal are dollar-quoted with tagged
      delimiters (``$hush$`` / ``$hushmsg$``), so embedded quotes or ``$$`` can't
      break out the way ``'...'`` / ``$$...$$`` would.

    # ponytail: relies on a file path never containing the literal `$hushmsg$`
    # tag; a sanitizer is the upgrade path if arbitrary text is ever passed.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            f"DO $hush$ BEGIN RAISE NOTICE '%', $hushmsg${message}$hushmsg$; "
            f"END $hush$;"
        )


def _resolve_settings(
    requested: list[str] | None,
    registry: tuple[HushSetting, ...] | None = None,
) -> list[HushSetting]:
    """Map requested setting names to HushSetting objects, or return all."""
    if registry is None:
        registry = DEFAULT_SETTINGS
    if requested is None:
        return list(registry)
    by_name = {s.name: s for s in registry}
    result = []
    for name in requested:
        if name in by_name:
            result.append(by_name[name])
        else:
            result.append(HushSetting(name=name, hush_value=""))
    return result


def suppress_pg(
    connection: BaseDatabaseWrapper,
    alias: str,
    requested_settings: list[str] | None,
    caller_location: str = "",
    registry: tuple[HushSetting, ...] | None = None,
) -> tuple[list[SettingResult], PgRestoreState]:
    """Suppress PG logging settings on one connection.

    Returns (results, restore_state).
    """
    settings = _resolve_settings(requested_settings, registry)
    use_local = _in_transaction(connection)
    set_keyword = "LOCAL" if use_local else "SESSION"
    state = PgRestoreState(used_set_local=use_local)
    results: list[SettingResult] = []

    # Emit audit notice before suppression
    if caller_location:
        _emit_notice(connection, f"pg_hush: logging disabled at {caller_location}")

    for setting in settings:
        try:
            # Validate before interpolating the name into SQL. A bad name is
            # recorded as a failed SettingResult (below), not bubbled, matching
            # the per-setting graceful-failure contract.
            validate_guc_name(setting.name)
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW {setting.name}")
                original_value = cursor.fetchone()[0]
                cursor.execute(
                    f"SET {set_keyword} {setting.name} = %s", [setting.hush_value]
                )
            state.changed_settings.append((setting.name, original_value))
            results.append(
                SettingResult(
                    name=setting.name,
                    connection=alias,
                    suppressed=True,
                    original_value=original_value,
                    error=None,
                )
            )
        except Exception as exc:
            results.append(
                SettingResult(
                    name=setting.name,
                    connection=alias,
                    suppressed=False,
                    original_value=None,
                    error=str(exc),
                )
            )

    return results, state


def restore_pg(
    connection: BaseDatabaseWrapper,
    state: PgRestoreState,
    caller_location: str = "",
) -> None:
    """Restore PG settings from saved state. Best-effort, never raises."""
    if state.used_set_local:
        # SET LOCAL is undone automatically by transaction end
        pass
    else:
        for name, original_value in state.changed_settings:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SET SESSION {name} = %s", [original_value])
            except Exception as exc:
                warnings.warn(
                    f"pg_hush: failed to restore {name}: {exc}",
                    RuntimeWarning,
                    stacklevel=2,
                )

    # Emit audit notice after restoration
    if caller_location:
        with contextlib.suppress(Exception):
            _emit_notice(
                connection,
                f"pg_hush: logging re-enabled at {caller_location}",
            )
