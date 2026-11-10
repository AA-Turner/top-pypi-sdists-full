"""Bind a run recorded with no network (PROBE_MODE=offline, or the fallback)."""

from __future__ import annotations
import os
import warnings
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
    from ...delivery.offline.offline import LOCAL_PREFIX

    capture = dict(capture or {})
    for name in ("capture_reads", "capture_outputs", "ignore"):
        if name in kw:
            capture[name] = kw.pop(name)
    named = os.environ.get("PROBE_RUN_ID", "").strip()
    if named.startswith(LOCAL_PREFIX) and not fallback:
        return _attach_offline(named, kw, reinit_mode=reinit_mode, capture=capture)
    if named:
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

    ignore = _normalized_ignore(capture.get("ignore"))
    run = open_offline_run(kw, sent=sent, fallback=fallback, settings=settings)
    _bind_new(_Binding(run=run, close_client=run._client), reinit_mode)
    _install_exit_hooks()
    _install_sigterm_flush()
    _start_offline_lineage(run, capture, ignore)
    _start_offline_log(run, capture)
    return run


def _attach_offline(named: str, kw: dict, *, reinit_mode: str, capture: dict) -> "Run":
    """Join the offline run an offline `execute()` handed this process (``PROBE_RUN_ID=local:<key>``),
    as an online child joins its launcher's run: `project=FROM_ENV` accepted, other identity
    arguments refused (no server to check them against), the rest named."""
    from ...client import FROM_ENV
    from ...delivery.offline.offline import attach_offline_run
    from ..attach import _IDENTITY_KWARGS, _nonzero_global_rank

    if kw.get("project") is FROM_ENV:
        kw = {k: v for k, v in kw.items() if k != "project"}
    conflicting = sorted(k for k in _IDENTITY_KWARGS if kw.get(k) is not None)
    if conflicting:
        raise errors.ValidationError(
            f"probe.init() received {', '.join(conflicting)} while PROBE_RUN_ID={named} is set. "
            "The run is already chosen by the environment -- an offline launcher opened it "
            "and handed it to this process. Drop those arguments to join that run, or unset "
            "PROBE_RUN_ID to create a new one."
        )
    config = kw.pop("config", None)
    dropped = sorted(k for k, v in kw.items() if v is not None)
    if dropped:
        warnings.warn(
            f"probe.init() ignored {', '.join(dropped)} while attaching to PROBE_RUN_ID={named}: "
            "an attach joins a run that already exists, so creation-time arguments have "
            "nothing to apply to.",
            stacklevel=4,
        )
    ignore = _normalized_ignore(capture.get("ignore"))
    run = attach_offline_run(named)
    run._set_ignore(ignore)  # before the hand-off below reads it
    # The launcher on this host collects our reads and sweeps our folder with ITS rules.
    run._hand_ignore_to_launcher()
    if _nonzero_global_rank() is not None:
        run._sends_terminal_status = False  # rank 0 and the launcher own the verdict, as online
    _bind_new(_Binding(run=run, close_client=run._client, attached=True), reinit_mode)
    _install_exit_hooks()
    _install_sigterm_flush()
    if config is not None and _nonzero_global_rank() is None:
        run.update_config(config)
    _start_offline_lineage(run, capture, ignore)
    _start_offline_log(run, capture)
    return run


def _normalized_ignore(ignore: Any) -> Any:
    if ignore is None:
        return None
    from ...recording_rules import recording_rules as _ignore

    try:
        return _ignore.normalize(ignore)
    except ValueError as exc:
        raise errors.ValidationError(str(exc)) from None


def _start_offline_log(run: "Run", capture: dict) -> None:
    """What the run prints, kept as its log in its queue for `probe sync` (T18): the log only, output files
    stay online-only. A no-op when a launcher on this host (an offline `execute()`) tees this process."""
    try:
        run._start_capture(capture_outputs=capture.get("capture_outputs"), should_keep_files=False)
    except Exception:  # noqa: BLE001 -- the log is never a reason for a run not to open
        pass


def _start_offline_lineage(run: "Run", capture: dict, ignore: Any) -> None:
    """Record what the run reads and writes into its queue. Never a gate, as online. No
    recovery from here: an offline client has no server to send other runs' leftovers to."""
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
from probe.sdk.fluent.bindings import _Binding, _bind_new  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.exit import _install_exit_hooks, _install_sigterm_flush  # noqa: E402 -- pieces need each other; the front door loads this one first
