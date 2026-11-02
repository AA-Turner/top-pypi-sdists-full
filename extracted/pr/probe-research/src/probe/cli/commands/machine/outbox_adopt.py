"""probe outbox adopt: send the writes another credential queued with your login."""

from __future__ import annotations
import re

import typer
from ....sdk.settings.settings import current_context_name
from ....sdk import session_marker
from ....shared.reads import reads
from probe.cli.commands.machine.outbox import outbox_app


#: Context ``name``'s stored login alone, as Settings (`reads.stored_login`).
_stored_login = reads.stored_login


#: How long `outbox adopt` waits for another drain's pass, per queue.
_ADOPT_LOCK_TIMEOUT_S = 10.0


@outbox_app.command("adopt")
def outbox_adopt(
    credential: str = typer.Option(
        ...,
        "--credential",
        help="the credential fingerprint `probe outbox status` or `drain` names",
    ),
) -> None:
    """Send the writes another credential queued with YOUR login.

    For a job that ran with its own `PROBE_TOKEN` (or a token in code) and is
    gone, or whose token was revoked: nothing else can ever send what it
    queued. Allowed only when that credential was your own account -- the
    same team and user as the login stored here, checked with the server --
    and never for `/ingest` writes. Recorded for good (a later sign-in does
    not undo it), then delivered now, in the foreground."""
    from ....sdk.delivery import outbox as outbox_worker
    from ....sdk.settings.settings import current_context_name
    from ....foundation.durable.durable import now_iso, write_text_atomic
    from ....sdk.delivery.journal.journal import Journal
    from ....sdk.delivery.outbox.drain.adoption import (
        NotAdoptable,
        adopt_credential,
        adoption_account)
    from ....sdk.delivery.outbox.drain.credentials import (
        credential_fingerprint,
        op_credential)
    from ....sdk.delivery.ops.ops import queued_ops

    fp = credential.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{16}", fp):
        raise typer.BadParameter(
            "a credential fingerprint is 16 hex characters, as `probe outbox status` prints it"
        )
    if fp in outbox_worker.env_fingerprints():
        typer.echo(
            f"this shell holds credential {fp} (PROBE_TOKEN): `probe outbox drain` here sends "
            "its writes with it",
            err=True,
        )
        raise typer.Exit(1)
    name = current_context_name() or None
    login = _stored_login(name)
    if login is None:
        typer.echo(
            f"no login is stored here to send them with; {session_marker.WIZARD_HINT}", err=True
        )
        raise typer.Exit(1)
    if credential_fingerprint(login.token, None) == fp:
        typer.echo(
            f"credential {fp} is the login stored here: its writes go out with it already",
            err=True,
        )
        raise typer.Exit(1)
    queues: set = set()
    ops: list = []
    for root in _outbox_journals():
        for queue in root.namespaces():
            for _path, op in queued_ops(queue):
                stamp = (op.get("context") or {}).get("principal")
                if isinstance(stamp, dict) and stamp.get("fingerprint") == fp:
                    ops.append(op)
                    queues.add(queue.dir)
    writes = len(ops)
    if not writes:
        typer.echo(f"nothing is queued with credential {fp}", err=True)
        raise typer.Exit(1)
    account, why, context_name = adoption_account(fp, ops)
    label = context_name or "<default>"
    refusals = {
        NotAdoptable.UNKNOWN_ACCOUNT: (
            f"the account credential {fp} belongs to was never recorded on this machine, so "
            "it cannot be matched to your login and its writes cannot be sent with it. "
            f"`probe outbox discard --held --credential {fp}` drops them."
        ),
        NotAdoptable.NO_LOGIN: (
            f"context {label} stores no login to send them with; sign in to it first"
        ),
        NotAdoptable.OTHER_SERVER: (
            f"credential {fp}'s writes are for another server than the login stored for "
            f"context {label}; sign in to that server in that context first"
        ),
        NotAdoptable.UNCONFIRMED: (
            f"could not confirm the account of context {label}'s login with the server; "
            "nothing was changed, try again"
        ),
        NotAdoptable.OTHER_ACCOUNT: (
            f"credential {fp} queued its writes as another account than the one logged in "
            f"to context {label}; sign in as that account, or "
            f"`probe outbox discard --held --credential {fp}` drops them"
        ),
        NotAdoptable.SCOPE: (
            f"credential {fp} may not do what its writes ask (Probe refused them for scope, "
            "or its recorded scopes lack it); your login may, and must not do it in its place. "
            f"`probe outbox discard --held --credential {fp}` drops them"
        ),
    }
    if why is not None or account is None:
        typer.echo(refusals.get(why, refusals[NotAdoptable.OTHER_ACCOUNT]), err=True)
        raise typer.Exit(1)
    adopt_credential(fp, account)
    for directory in queues:
        try:  # a worker sleeping on held runs looks again now
            write_text_atomic(directory / ".wake", now_iso() + "\n", mode=0o600)
        except OSError:
            pass
    typer.echo(
        f"adopted credential {fp}: its {writes} queued write(s), and any it queues later, go "
        f"out with your login (team {account[0]})"
    )
    delivered, _dead, _remaining, busy = outbox_worker.drain_adopted(
        queues, lock_timeout=_ADOPT_LOCK_TIMEOUT_S
    )
    left = [
        op
        for directory in queues
        for _, op in queued_ops(Journal(directory))
        if ((op.get("context") or {}).get("principal") or {}).get("fingerprint") == fp
    ]
    typer.echo(f"delivered {delivered}; {len(left)} of credential {fp} left")
    if not left:
        return
    ingest = sum(1 for op in left if op_credential(op)[1])
    if ingest:
        typer.echo(
            f"  {ingest} of them are /ingest writes, which go out only with their own ingest "
            "token: adoption never sends those",
            err=True,
        )
    try:
        import probe as _probe

        ours = str(getattr(_probe, "__version__", "") or "")
    except Exception:  # noqa: BLE001
        ours = ""
    for directory in sorted(queues):
        holder = outbox_worker.worker_holder(Journal(directory))
        if holder is None:
            continue
        pid, version = holder
        if version and version == ours:
            typer.echo(
                f"  a worker (pid {pid}) of this release is delivering {directory} now", err=True
            )
            continue
        typer.echo(
            f"  an older Probe worker (pid {pid or '?'}, release {version or 'unknown'}) holds "
            f"delivery of {directory} and cannot send adopted writes. Restart the job that "
            "started it (or stop that pid), then run `probe outbox drain`.",
            err=True,
        )
    if busy:
        typer.echo(
            "  another drain held a queue's lock; `probe outbox drain` tries again", err=True
        )
    raise typer.Exit(2)
from probe.cli.commands.account.account import login  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _outbox_journals  # noqa: E402 -- pieces need each other; the front door loads this one first
