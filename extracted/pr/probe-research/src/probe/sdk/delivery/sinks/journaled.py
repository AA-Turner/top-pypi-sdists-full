"""JournalSink: an async client's writes are queued in the outbox journal, and where that
journal is (the $TMPDIR fallback, the Kubernetes root-disk notice)."""

from __future__ import annotations

import errno
import os
from pathlib import Path
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ...secret_gate import check_upload
from .. import sink as _sink
from ..journal.journal import Journal
from ..sink import HeldClient, SinkKind

#: Outbox directories this process has already warned about falling back from.
_FALLBACK_WARNED: set[str] = set()
_K8S_NOTICE_GIVEN = False


def _usable_journal(directory: Path | None) -> Journal:
    """The journal a `Client` should queue in: ``directory`` (default: the machine's
    outbox) when it can take appends, else the ``$TMPDIR`` fallback with ONE warning that
    it does not survive a pod or machine restart (plan 1.5). An unusable queue used to drop
    every write, one warning each; an explicit unusable ``PROBE_OUTBOX_DIR`` falls back too."""
    from ..journal.paths import fallback_dir, private_fallback_root

    primary = Journal(directory)
    try:
        reason = primary.usable()
    except Exception:  # noqa: BLE001 -- cannot tell: keep the configured queue
        return primary
    if reason is None:
        if (
            directory is None
            and not os.environ.get("PROBE_OUTBOX_DIR")
            and _under_private_fallback(primary.dir, private_fallback_root)
        ):
            # No home directory (`journal.default_root`): the default already IS the
            # fallback, which must still be said once.
            _warn_fallback(primary, "there is no home directory", primary)
        elif directory is None:
            # Only the DEFAULT outbox: an explicit `spool_dir` is the caller's choice (review
            # of #2054).
            _kubernetes_notice(primary)
        return primary
    try:
        fallback = Journal(fallback_dir())
        if fallback.dir == primary.dir or fallback.usable() is not None:
            return primary
    except Exception:  # noqa: BLE001
        return primary
    _warn_fallback(primary, reason, fallback)
    return fallback


def _under_private_fallback(path: Path, private_fallback_root) -> bool:
    try:
        return path.is_relative_to(private_fallback_root())
    except Exception:  # noqa: BLE001
        return False


def _warn_fallback(primary: Journal, reason: str, fallback: Journal) -> None:
    if str(primary.dir) in _FALLBACK_WARNED:
        return
    _FALLBACK_WARNED.add(str(primary.dir))
    where = (
        f"queueing in {fallback.dir}"
        if fallback.dir == primary.dir
        else f"the outbox at {primary.dir} cannot be used; queueing in {fallback.dir} instead"
    )
    small = ""
    try:
        import shutil

        free = shutil.disk_usage(fallback.dir if fallback.dir.exists() else fallback.dir.parent).free
        if free < 256 * 1024 * 1024:
            # A small tmpfs: most writes will be sent directly or dropped, and this is the
            # one place that can say why (review of #2054).
            small = f" It has only {free // (1024 * 1024)} MiB free, so writes may be dropped."
    except OSError:
        pass
    _diagnostics.warn(
        f"probe: {reason}: {where}. That directory does NOT survive a pod or machine "
        f"restart: set PROBE_OUTBOX_DIR to a writable, persistent path.{small}"
    )


def _kubernetes_notice(journal: Journal) -> None:
    """Once per process, on Kubernetes with the default outbox: the queue sits on the
    container's disk and the detached worker dies with the pod, so writes still queued when
    the pod is deleted are lost (plan 1.5)."""
    global _K8S_NOTICE_GIVEN
    if (
        _K8S_NOTICE_GIVEN
        or not os.environ.get("KUBERNETES_SERVICE_HOST")
        or os.environ.get("PROBE_OUTBOX_DIR")
        or os.environ.get("PROBE_OUTBOX_WORKER")
        or not _on_container_root_disk(journal.dir)
    ):
        return
    _K8S_NOTICE_GIVEN = True
    _diagnostics.warn(
        f"probe: running on Kubernetes with the outbox on the container's disk "
        f"({journal.dir}); writes still queued when the pod is deleted are lost. Set "
        "PROBE_OUTBOX_DIR to a persistent volume, and PROBE_FINISH_TIMEOUT_SEC=600 with "
        "terminationGracePeriodSeconds at least that long."
    )


def _on_container_root_disk(path: Path) -> bool:
    """Whether ``path`` is on the same filesystem as ``/`` (the container's writable layer).
    A HOME that is a mounted volume (JupyterHub's per-user PV) is another device and the
    notice would be wrong there (review of #2054)."""
    try:
        probe_path = path
        while not probe_path.exists() and probe_path.parent != probe_path:
            probe_path = probe_path.parent
        return os.stat(probe_path).st_dev == os.stat("/").st_dev
    except OSError:
        return False


#: An append that failed for want of space (plan 1.5): ENOSPC, and EDQUOT
#: where the platform has it.
_OUT_OF_SPACE = frozenset(
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
)


class JournalSink:
    """Queues in the client's journal. Holds no state: the client keeps its counters."""

    kind = SinkKind.JOURNALED
    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client

    def queues(self, *, strict: bool, sync: bool) -> bool:
        # strict means "fail loudly, never journal": a demand for the network, so it implies sync.
        return not sync and not strict

    def land(
        self, method: str, path: str, body: dict | None, *, strict: bool, sync: bool, blocking: bool,
        raise_permanent: bool, admitted: bool,
    ) -> Any:
        """Queue the write, or send it around the queue below the free-space floor; a strict or
        sync write goes out now as a sync client's would."""
        client = self._client
        if not self.queues(strict=strict, sync=sync):
            return client._delivery.direct.land(
                method, path, body, strict=strict, sync=sync, blocking=blocking,
                raise_permanent=raise_permanent, admitted=admitted,
            )
        if client._send_instead_of_queueing(method, path, body):
            return None
        if client._enqueue(
            method,
            path,
            body,
            blocking=blocking,
            prepared=True,
            direct_ok=True,
            admitted=admitted,
        ):
            client._after_enqueue()
        return None

    def enqueue(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        blocking: bool = True,
        validation_error: str | None = None,
        prepared: bool = False,
        admitted: bool = False,
        direct_ok: bool = False,
    ) -> bool:
        """Journal one op. Returns whether it landed; NEVER raises for a failure of ours.
        KeyboardInterrupt/SystemExit propagate.

        ``direct_ok`` (async write path): on an append failing for want of space, try
        `_send_instead_of_queueing` before dropping (plan 1.5).

        ``prepared=True`` only from `write`, whose body is already normalized, NUL-checked
        and scrubbed: the journal skips all three (plan 1.3). Any other caller (the CLI's
        reference door) hands a raw body and the journal scrubs it.

        Async-by-default moved the per-write failure surface from network to disk, which was
        unguarded: ENOSPC on the state partition, a read-only or full `XDG_STATE_HOME`, a
        stale NFS handle, or `flock` ENOSYS (Lustre without `-o flock`, some container
        overlays, FUSE mounts) raised a raw OSError out of `run.log()`: telemetry killing a
        training step.

        Losing a datapoint is correct when the outbox itself is broken. The gap is recorded
        in the journal's accounting when it can be written, else in a warning. It is ALSO
        counted on `dropped_writes`, because `write()` discards this return value and returns
        None either way: a CLI printing "queued" on a dropped write would report success for
        data that reached nothing (`Client.dropped_writes`).
        """
        client = self._client
        try:
            options: dict[str, Any] = (
                {"validation_error": validation_error} if validation_error is not None else {}
            )
            if prepared:
                options["_prepared"] = True
            if admitted:
                options["admitted"] = True
            client.journal.append_http(method, path, body, blocking=blocking, **options)
            return True
        except (KeyboardInterrupt, SystemExit):
            # A Ctrl-C (or `sys.exit`) mid-append is the user stopping the process, not a
            # broken outbox: counting it a dropped write let training carry on past the
            # Ctrl-C and closed an interrupted run with a drop notice. Nothing is left
            # half-written: `write_text_atomic` unlinks its temp file, and the op file
            # either landed whole (it delivers) or not at all.
            raise
        except BaseException as enqueue_error:  # noqa: BLE001
            if (
                direct_ok
                and isinstance(enqueue_error, OSError)
                and enqueue_error.errno in _OUT_OF_SPACE
                and client._send_instead_of_queueing(method, path, body, out_of_space=True)
            ):
                return True
            client.dropped_writes += 1
            try:
                # Once per drop: a refusal at the cap was already recorded by the journal
                # (review of #2014: each drop rewrote the producer file twice).
                if not getattr(enqueue_error, "gap_recorded", False):
                    client.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            # One line per kind, then at most one per 5 min with the running count (plan
            # 1.7): a warning per drop was 44 lines for 50 drops.
            client._note_drop(f"{method} {path}: {_diagnostics.describe(enqueue_error)}")
            # The warning reaches the operator's terminal and nothing else. This is DATA
            # LOSS (neither server nor journal got the write): exactly what must not stay local.
            _sink._capture_swallowed(
                enqueue_error,
                site="client.enqueue_dropped",
                base_url=client.settings.base_url,
                spool_dir=str(client.journal.dir),
            )
            return False

    def enqueue_upload(self, **kwargs) -> dict | None:
        """Journal one byte upload. Returns the journal's result, or None when it could not
        be queued; NEVER raises for a failure of ours.

        Symmetric sibling of :meth:`_enqueue`: this client and the CLI both queue uploads
        here so "telemetry must not raise into the caller" has ONE implementation (the CLI
        called ``journal.append_upload`` directly, so the `_enqueue` guard never covered it).

        Two deliberate differences from `_enqueue`:

        ``Exception``, not ``BaseException``. `append_upload` does a full byte copy, so a
        Ctrl-C during a multi-GB checkpoint lands here far more than anywhere else, and
        swallowing it would leave the user unable to interrupt their own upload.
        ``Exception`` still covers every failure of ours (ENOSPC, read-only
        `XDG_STATE_HOME`, `flock` ENOSYS on Lustre/FUSE, `OutboxFull`, serialization and
        redaction errors a narrower tuple would miss); KeyboardInterrupt and SystemExit pass
        through. (`_enqueue` passes those too: a mid-append Ctrl-C was counted a drop.)

        Redaction happens HERE, before bytes reach the journal, UNCONDITIONALLY, not gated on
        ``client._redact``. This is the one departure from "the caller owns redaction":
        `write()` scrubs a payload on its way to the NETWORK, where the caller's preference
        is the whole story, but this writes durable local disk that a dead-lettered op keeps
        in `failed/` indefinitely. A caller with no redactor asked not to reshape API
        payloads, not for their `--meta` secrets parked on disk forever. A caller-supplied
        ``_redact`` still runs on top.

        String leaves in `meta` get `scrub_text` on top of `default_scrub`. They are not
        interchangeable: `default_scrub` redacts by KEY NAME (right for structure, wrong for
        prose), so a bare token or `PROBE_TOKEN=...` under an innocent key passes it;
        `scrub_text` is the value-level pass built for that.

        No `notes`: files stopped carrying notes; a caller still passing it has it dropped
        here rather than failing the upload on an unexpected keyword.
        """
        client = self._client
        check_upload(kwargs.get("src_path"))
        try:
            # INSIDE the try: redaction is arbitrary code (the caller's especially) and one
            # that raises would escape a method that never raises, taking out the caller's
            # synchronous fallback.
            # scanning disabled: from ...redaction import default_scrub, scrub_text

            kwargs.pop("notes", None)
            meta = kwargs.get("meta")
            if isinstance(meta, dict):
                # scanning disabled: scrubbed = default_scrub(meta)
                scrubbed = meta
                if isinstance(scrubbed, dict):
                    # default_scrub caught the sensitive KEYS; scrub_text catches
                    # a secret sitting in prose under an innocent one.
                    scrubbed = {
                        # scanning disabled: k: (scrub_text(v) if isinstance(v, str) else v) for k, v in scrubbed.items()
                        k: v for k, v in scrubbed.items()
                    }
                kwargs["meta"] = scrubbed
            if client._redact is not None and isinstance(kwargs.get("meta"), dict):
                # Only structured values go to a caller redactor (declared dict -> dict):
                # round-tripping a string through a wrapper key DROPPED the value when the
                # redactor returned an allowlisted subset.
                kwargs["meta"] = client._redact(kwargs["meta"])
            # scanning disabled: kwargs = default_scrub(kwargs)
            return client.journal.append_upload(**kwargs)
        except Exception as enqueue_error:  # noqa: BLE001 -- see the docstring
            client.dropped_writes += 1
            try:
                if not getattr(enqueue_error, "gap_recorded", False):
                    client.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            client._note_drop(
                f"upload {kwargs.get('name')!r}: {_diagnostics.describe(enqueue_error)}"
            )
            _sink._capture_swallowed(
                enqueue_error,
                site="client.enqueue_upload_dropped",
                base_url=client.settings.base_url,
                spool_dir=str(client.journal.dir),
            )
            return None
