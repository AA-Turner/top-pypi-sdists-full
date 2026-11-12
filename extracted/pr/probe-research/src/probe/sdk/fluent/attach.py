"""attach to the run a launcher exported (PROBE_RUN_ID, per-run token), and read this process's global rank."""

from __future__ import annotations
import os
import uuid
import warnings
from typing import TYPE_CHECKING

from .. import errors
from ...foundation.process_rank import read_process_ranks
from ..client.client import Client
from ..client import FROM_ENV

if TYPE_CHECKING:

    from ..run.run import Run


#: Kwargs that CHOOSE where a run is. When PROBE_RUN_ID already chose one, they must
#: name that run's own home (D30, Codex O9: an agent-written script carries its slugs
#: and may be launched under `probe exec`); a different one is a contradiction, not a
#: refinement: silently preferring either side is how telemetry lands on a run nobody
#: was looking at. `project=probe.FROM_ENV` always agrees: the launcher chose.
_CHOOSING_KWARGS = ("experiment", "project", "slug")
#: Kwargs that DESCRIBE a run or experiment at creation: an attach has nothing to apply
#: them to, so they are named in the "ignored" warning (a matching name is not).
_DESCRIBING_KWARGS = ("name", "question", "hypothesis")
#: Every kwarg that names or describes a run (the integrations drop them under a launcher).
_IDENTITY_KWARGS = _CHOOSING_KWARGS + _DESCRIBING_KWARGS


#: The PROBE_RUN_ID this process exported from a per-run token, so a later
#: init() under another token never reads it as the user's choice.
_EXPORTED_RUN_ID: str | None = None


def _adopt_run_token(run_id: str, client: Client) -> str:
    """The run to attach to, given a per-run token (`probe_run_`).

    A per-run token records one run, so it names that run itself: a job given
    only PROBE_TOKEN attaches to it (and `_attach_from_env` exports the id once
    attached, for the CLI inside the job). A PROBE_RUN_ID naming another run is
    refused here rather than at the first write. Any other credential -- the
    client's own, which wins over the environment's -- leaves `run_id` as it was."""
    from ..settings.settings import run_token_run_id

    if run_id and run_id == _EXPORTED_RUN_ID:
        run_id = ""
    token = getattr(getattr(client, "settings", None), "token", None) or os.environ.get("PROBE_TOKEN")
    token_run = run_token_run_id(token)
    if token_run is None:
        return run_id
    if not run_id:
        return token_run
    try:
        same = uuid.UUID(run_id) == uuid.UUID(token_run)
    except ValueError:
        return run_id  # a slug: the server resolves it and refuses another run
    if not same:
        raise errors.ValidationError(
            f"PROBE_RUN_ID={run_id} but PROBE_TOKEN is a per-run token for run {token_run}, "
            "which records that run only. Unset PROBE_RUN_ID, or give this job the token "
            "`probe exec` printed for its own run."
        )
    return run_id


def _attach_from_env(client: Client, kw: dict) -> "Run | None":
    """Attach to the run named by PROBE_RUN_ID, or None if there is none.

    The epoch rides along when the launcher exported one: a run id names a ROW,
    not an execution attempt, and without the epoch a stale process holding an
    old id would attach to a row a newer attempt had already reopened and
    inherit its write authority.

    ``project=`` / ``experiment=`` / ``slug=`` naming the run's own home (or the run)
    are accepted, and so is ``project=probe.FROM_ENV`` (D30); a DIFFERENT one RAISES
    rather than being ignored or honoured. The environment has already chosen the
    run; a caller naming another either does not know that or is running the wrong
    script, and both deserve to find out at import rather than at read time.
    """
    global _EXPORTED_RUN_ID
    named = os.environ.get("PROBE_RUN_ID", "").strip()
    run_id = _adopt_run_token(named, client)
    if not run_id:
        return None
    from_token = run_id != named or (bool(named) and named == _EXPORTED_RUN_ID)
    if kw.get("project") is FROM_ENV:
        kw = {k: v for k, v in kw.items() if k != "project"}
    choosing = {k: kw[k] for k in _CHOOSING_KWARGS if kw.get(k) is not None}
    data, unchecked = None, []
    if choosing:
        data = client.get_run(run_id)
        verdicts = {k: _is_this_runs_home(client, data, k, str(ref)) for k, ref in choosing.items()}
        unchecked = sorted(k for k, agrees in verdicts.items() if agrees is None)
        conflicting = sorted(k for k, agrees in verdicts.items() if agrees is False)
    else:
        conflicting = []
    if conflicting and from_token:
        raise errors.ValidationError(
            f"probe.init() received {', '.join(conflicting)}, but PROBE_TOKEN is a per-run "
            f"token for run {run_id}: it records that run only, which a launcher opened for "
            "this job. Drop those arguments to join it."
        )
    if conflicting:
        raise errors.ValidationError(
            f"probe.init() received {', '.join(conflicting)} while PROBE_RUN_ID="
            f"{run_id} is set. The run is already chosen by the environment -- a "
            "launcher opened it and handed it to this process. Drop those "
            "arguments to join that run, or unset PROBE_RUN_ID to create a new "
            "one; doing both would write this job's telemetry onto whichever run "
            "happened to win."
        )
    # Everything else a caller passed is DROPPED -- attach_run has no use for
    # it. Silence there is its own failure: `probe.init(hw=True)` would stop
    # collecting hardware metrics with no sign, and tags/description would
    # simply not arrive. Name them. `config` is the exception (plan (c)): it
    # merges into the joined run below, from global rank 0 only.
    config = kw.get("config")
    agreed = set(choosing) - set(unchecked)
    name = kw.get("name")
    if name is not None and data is None:
        data = _read_run_quietly(client, run_id)  # whether the launcher's name is kept decides the next line
    # A name equal to the run's is not news. One the launcher left unkept (a minted or generated name) is
    # applied below, from global rank 0; a kept one is reported as ignored.
    same_name = data is not None and name == data.get("name")
    names_run = name is not None and not same_name and data is not None and not data.get("name_customized")
    dropped = sorted(
        k for k, v in kw.items()
        if v is not None and k != "config" and k not in agreed and not (k == "name" and (same_name or names_run))
        and not (k == "authored_by" and names_run)
    )
    if unchecked:
        warnings.warn(
            f"probe.init() could not check {', '.join(unchecked)} against PROBE_RUN_ID={run_id} "
            "(a per-run PROBE_TOKEN reads only its run): joining that run.",
            stacklevel=3,
        )
        dropped = [k for k in dropped if k not in unchecked]
    if dropped:
        warnings.warn(
            f"probe.init() ignored {', '.join(dropped)} while attaching to "
            f"PROBE_RUN_ID={run_id}: an attach joins a run that already exists, "
            "so creation-time arguments have nothing to apply to. Set them on "
            "the launcher that opened the run, or with run.set_* afterwards.",
            stacklevel=3,
        )
    raw_epoch = os.environ.get("PROBE_RUN_EPOCH", "").strip()
    try:
        write_epoch = int(raw_epoch) if raw_epoch else None
    except ValueError:
        # An unreadable epoch is not a reason to refuse the attach: the server
        # still fences on its own copy. Warn and attach unfenced.
        warnings.warn(
            f"PROBE_RUN_EPOCH={raw_epoch!r} is not an integer; attaching without "
            "the writer-epoch fence",
            stacklevel=3,
        )
        write_epoch = None
    run = client.attach_run(
        data if data is not None else run_id,
        heartbeat=True,
        # Beats from here say "the job itself is reporting", which is what
        # stamps attached_at. The launcher's own beats deliberately do not.
        attached=True,
        # A queued job can reach its run after the created-sweep already ended
        # it. Reopening is how a late start rejoins instead of beating into a
        # silent no-op for the rest of its life.
        reopen_if_dead=True,
        write_epoch=write_epoch,
    )
    # One line, because the alternative is a researcher wondering why their
    # curves are on a run they did not create.
    print(
        f"probe: attached to run {run.slug or run.id} via "
        + ("its per-run PROBE_TOKEN" if from_token else "PROBE_RUN_ID"),
        flush=True,
    )
    if from_token:
        # For the CLI inside the job (`probe artifact add` anchors to the run).
        _EXPORTED_RUN_ID = os.environ["PROBE_RUN_ID"] = str(run.id)
    if names_run and _nonzero_global_rank() is None:
        named = _apply_script_name(client, str(run.id), name, data.get("name"), kw.get("authored_by"))
        if named is not None:
            run._data = {**run._data, **named}  # the handle reads the name the run now has
    if config is not None and _nonzero_global_rank() is None:
        # Under `probe exec` the launcher created the run without the script's
        # config, so this is the only place it can arrive. One rank is enough:
        # every rank of a job passes the same config.
        run.update_config(config)
    return run

def _read_run_quietly(client: Client, run_id: str) -> dict | None:
    """The joined run's row, or None when it cannot be read (then nothing is applied to it)."""
    try:
        return client.get_run(run_id)
    except Exception:  # noqa: BLE001 -- naming never costs the job its attach
        return None


def _apply_script_name(client: Client, run_id: str, name: str, read_name: str | None,
                       authored_by: str | None) -> dict | None:
    """Name the launcher's run after the script's ``probe.init(name=...)``, once: a compare-and-set on the
    name read, so a rename meanwhile (409) stands. Declared as the script declared it, else undeclared and kept
    like a create-time name. The run's row as renamed, or None when it was not."""
    from ...foundation.safe_warn import safe_warn  # never raises, even under `-W error`

    try:
        row = client.update_run(run_id, name=name, expected_name=read_name or name, authored_by=authored_by)
        return row if isinstance(row, dict) and row.get("name") else None
    except errors.ConflictError:
        # Renamed, or its name kept, since it was read: theirs stands, and code finding the run by `name` must know.
        safe_warn.warn(f"probe: run {run_id} was renamed since it was read, or its name was chosen and is kept; "
                       f"it keeps that name, not {name!r}",
                       stacklevel=4)
    except Exception as exc:  # noqa: BLE001 -- naming never costs the job
        safe_warn.warn(f"probe: could not name run {run_id} {name!r} ({type(exc).__name__}); it keeps its name",
                       stacklevel=4)
    return None


def _is_this_runs_home(client: Client, run: dict, kind: str, ref: str) -> bool | None:
    """Whether `ref`, passed as `kind=` beside PROBE_RUN_ID, names the joined run (`slug`) or
    its project or experiment (D30). None when this credential cannot look a slug up (a
    per-run token reads only its run)."""
    from ..client.ids import _id_ref

    if kind == "slug":
        return ref in (run.get("slug"), str(run.get("id")))
    experiment_id = str(run.get("experiment_id") or "").lower()
    project_id = str(run.get("project_id") or "").lower()
    reads_only_its_run = _is_run_token(client)
    if _id_ref(ref):
        wanted = ref.removeprefix("id:").lower()
    elif reads_only_its_run:
        return None
    else:
        slug = ref.removeprefix("slug:")
        row = client.resolve_project(slug) if kind == "project" else client.resolve_experiment(slug)
        if row is None:
            return False
        wanted = str(row["id"]).lower()
    if kind == "experiment":
        return bool(experiment_id) and wanted == experiment_id
    if project_id and project_id != experiment_id:
        return wanted == project_id
    if not experiment_id:
        return False
    if reads_only_its_run:
        return None
    # The leaf shape names the experiment as the run's project: ask the experiment for its own.
    return str(client.get_experiment(experiment_id).get("project_id")).lower() == wanted


def _is_run_token(client: Client) -> bool:
    """This client's credential is a per-run token (`probe exec`'s hand-off)."""
    from ..settings.settings import run_token_run_id

    token = getattr(getattr(client, "settings", None), "token", None) or os.environ.get("PROBE_TOKEN")
    return run_token_run_id(token) is not None


def _nonzero_global_rank() -> int | None:
    """The global rank of this process when it is above 0, else None.

    ANY advertised rank above 0 counts: a worker is rank 0 only if every
    scheme that numbers it agrees. A rank whose own world size says the job is
    one process (``RANK=3 WORLD_SIZE=1``, a left-over export) does not count,
    and neither does a negative one (``RANK=-1``, "not distributed")."""
    for found in read_process_ranks(os.environ):
        if found.rank <= 0:
            continue
        if found.size is not None and found.size <= 1:
            continue
        return found.rank
    return None
