"""the one confirm-then-delete flow every irreversible delete verb goes through (resolve, show, confirm, delete by id)."""

from __future__ import annotations
from typing import Any

import typer


#: How long a run, group, experiment or project stays restorable in the
#: server's trash (`app/teams/deletion_policy.py::TRASH_DAYS`; kept equal by
#: tests/unit/accounts/teams/lifecycle/test_trash_days_parity.py). The prompt promises it before the
#: delete; the server's answer then names the exact date.
TRASH_DAYS = 21


def _confirm_delete(
    yes: bool, subject: str, *, cascade: str | None = None, trash: bool = False
) -> None:
    """The one confirmation path for every irreversible delete verb.

    This was spelled by hand in four places and forgotten entirely in a fifth:
    ``artifact delete`` took no ``--yes`` and prompted for nothing, so the flag
    that guards the *cascading* deletes was rejected by the one that deletes
    silently. Passing ``--yes`` there — the habit every other delete teaches —
    failed the whole batch, which is the good outcome; had it been accepted and
    ignored, the artifacts would have been gone before anyone read them.

    A verb that forgets to prompt is indistinguishable from one that decided not
    to, so the decision belongs here rather than being re-made per verb.

    ``cascade`` names what else goes; omit it when nothing else does.

    ``subject`` is the RESOLVED entity (name, handle and id), never the string the
    operator typed. Echoing the ref back asks them to approve their own typo, and
    in the id/slug collision that string is exactly the one that does not say
    which entity is about to go.
    """
    if yes:
        return
    if trash:
        # 0261: a run, experiment or project delete MOVES it to the trash.
        question = f"move {subject} to the trash?"
        if cascade:
            question += f" {cascade}."
        question += (
            f" Probe support can restore it for {TRASH_DAYS} days; "
            "after that it is deleted for good"
        )
        typer.confirm(question, abort=True)
        return
    question = f"permanently delete {subject}?"
    if cascade:
        question += f" {cascade}, and this cannot be undone"
    typer.confirm(question, abort=True)


def _confirmed_delete(
    kind: str,
    ref: str,
    *,
    yes: bool,
    cascade: str | None = None,
    delete_kwargs: dict[str, Any] | None = None,
    trash: bool = False,
    dry_run: bool = False,
) -> None:
    """The whole shape of a delete: resolve, show, confirm, delete by id.

    Every delete verb goes through here so they cannot drift apart on the three
    things that decide whether the right thing dies: which ref forms are accepted,
    what the prompt names, and whether the id or the typed string reaches the
    endpoint. ``run delete`` accepting a petname while ``project delete`` accepted
    a slug and ``experiment delete`` accepted neither is how an operator learns a
    habit from one verb that silently misfires in the next.

    Resolution happens BEFORE the prompt, which is the ordering the confirmation
    is worth anything under.

    ``dry_run`` resolves the same way, asks the same route with
    ``?dry_run=true`` and prints its answer: what would go, whose it is and when
    it last changed, with nothing moved and no prompt. Only a trash delete has
    one (0261).
    """
    with _client() as c:
        target = _ref(c, kind, ref)
        # Promise the trash only where the server has one: before 0261 the
        # same DELETE is permanent, and the prompt must say so.
        trash = trash and c.supports_feature("trash")
        kwargs = dict(delete_kwargs or {})
        if kind == "experiment" and _filed_under(target):
            kwargs.setdefault("project_id", _filed_under(target))  # saves a lookup
        if dry_run:
            if not trash:
                raise typer.BadParameter("this Probe server has no trash, so a delete has no dry run")
            _print_json(getattr(c, f"delete_{kind}")(target.id, dry_run=True, **kwargs))
            return
        _confirm_delete(yes, target.label, cascade=cascade, trash=trash)
        answer = getattr(c, f"delete_{kind}")(target.id, **kwargs)
    until = answer.get("restorable_until") if trash and isinstance(answer, dict) else None
    if until:
        print(
            f"{target.label} moved to the trash; Probe support can restore it "
            f"until {str(until)[:10]}"
        )
        return
    print(f"{target.label} deleted")
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _filed_under, _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
