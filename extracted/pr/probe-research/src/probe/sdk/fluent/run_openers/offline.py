"""Bind a run recorded with no network (PROBE_MODE=offline, or the fallback)."""

from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any

from ... import errors

if TYPE_CHECKING:

    from ...run.run import Run


def _init_offline(
    kw: dict,
    *,
    sent: dict | None = None,
    fallback: bool = False,
    settings: Any = None,
    reinit_mode: str = "default",
    capture: dict | None = None,
) -> "Run":
    """``PROBE_MODE=offline`` (or the init fallback): bind a run recorded with
    no network (unbound under ``reinit="create_new"``, as online). See
    :mod:`probe.sdk.delivery.offline`. The exit hooks close it (a queued close, no
    waiting). What the run reads and writes is recorded as online (F6) and
    queued with its other writes at the close, for ``probe sync`` to deliver;
    ``capture_reads`` / ``capture_outputs`` / ``ignore`` (popped from ``kw``, or
    handed over by the fallback in ``capture``) shape it. The crash breadcrumb
    is skipped: it needs the server."""
    from ...settings.settings import env_run_id

    if os.environ.get("PROBE_RUN_ID", "").strip():
        raise errors.ValidationError(
            "PROBE_MODE=offline cannot attach to PROBE_RUN_ID: that run exists only on "
            "the server. Unset PROBE_RUN_ID to record a new run offline."
        )
    if env_run_id():
        raise errors.ValidationError(
            "PROBE_MODE=offline cannot record with a per-run PROBE_TOKEN: it records only "
            "the run `probe exec` opened, which exists only on the server."
        )
    from ...delivery.offline.offline import open_offline_run

    capture = dict(capture or {})
    for name in ("capture_reads", "capture_outputs", "ignore"):
        if name in kw:
            capture[name] = kw.pop(name)
    ignore = capture.get("ignore")
    if ignore is not None:
        from ...recording_rules import ignore as _ignore

        try:
            ignore = _ignore.normalize(ignore)
        except ValueError as exc:
            raise errors.ValidationError(str(exc)) from None
    run = open_offline_run(kw, sent=sent, fallback=fallback, settings=settings)
    _bind_new(_Binding(run=run, close_client=run._client), reinit_mode)
    _install_exit_hooks()
    _install_sigterm_flush()
    # Never a gate, as online. No recovery from here: an offline client has
    # no server to send other runs' leftovers to.
    try:
        from ...capture import lineage as _inputs

        run._set_ignore(ignore)
        if _inputs.start(
            run.id,
            capture_reads=capture.get("capture_reads"),
            capture_outputs=capture.get("capture_outputs"),
            client=run._client,
            ignore=run._ignore_rules(),
            offline_dir=run.offline_dir,
        ):
            _inputs.bind_workers(run.id)
    except Exception:  # noqa: BLE001
        pass
    return run
from probe.sdk.fluent.bindings import _Binding, _bind_new  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.exit import _install_exit_hooks, _install_sigterm_flush  # noqa: E402 -- pieces need each other; the front door loads this one first
