"""The owner side of an RL adapter's run (RL plan §6.7): open it (or resume it with a rewind), run every hook
fail-open, and close it with the terminal manifest and the producers' close barrier. Why: integrations/art/DESIGN.md."""

from __future__ import annotations

import atexit
import json
import logging
import os
import re
import tempfile
import uuid
import weakref
from collections.abc import Callable, Mapping
from typing import Any

from probe.generated.records import RunType
from probe.sdk import errors
from probe.foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.agent_session import ComposedName
from probe.sdk.settings.settings import env_run_id as _env_run_id


logger = logging.getLogger(__name__)

#: A per-run token's prefix (`app/accounts/auth/tokens/run_tokens.py`).
RUN_TOKEN_PREFIX = "probe_run_"
#: Runs an RL adapter opened in this process: another adapter's tracker never adopts one.
OPENED_RUNS: set[str] = set()
#: Under a launcher (`PROBE_RUN_ID`) these choose nothing: the launcher already chose the run.
_LAUNCHER_DROPPED = ("project", "experiment", "slug", "name", "question", "hypothesis", "external_id", "on_conflict")
#: `PROBE_*` names never copied into a Ray runtime env (Ray's dashboard shows it): its only credential is the run's.
SECRET_WORDS = ("TOKEN", "SECRET", "PASSWORD", "KEY")


class HookGuard:
    """Fail open: a hook body that raises warns once per hook, is counted, and never reaches training."""

    def __init__(self, adapter: str, *, what_continues: str = "training") -> None:
        self.adapter = adapter
        #: What a warning promises keeps running: training, or a Harbor eval job.
        self.what_continues = what_continues
        self.failures = 0
        self._warned: set[str] = set()

    def call(self, what: str, function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except errors.ProjectRequired:
            raise  # a setup mistake, not an outage: stop before the GPU hours
        except Exception as exc:  # noqa: BLE001 -- fail open: a Probe error never stops training
            self.record_failure(what, exc)
            return None

    async def call_async(self, what: str, function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            return await function(*args, **kwargs)
        except errors.ProjectRequired:
            raise
        except Exception as exc:  # noqa: BLE001 -- fail open
            self.record_failure(what, exc)
            return None

    def record_failure(self, what: str, exc: BaseException) -> None:
        self.failures += 1
        if what in self._warned:
            return
        self._warned.add(what)
        _diagnostics.warn(
            f"probe: the {self.adapter} adapter could not record {what} ({type(exc).__name__}: {exc}); "
            f"{self.what_continues} continues, and the run's capture will answer 'no'. Later failures here are "
            "counted, not shown."
        )


def open_run(
    *,
    name: str | None,
    external_id: str | None,
    rewind_step: int | None,
    config: Mapping[str, Any] | None,
    init_kwargs: Mapping[str, Any],
    resume_from: str | None = None,
    should_stamp_checkpoints: bool = False,
) -> tuple[Any, bool]:
    """The run an adapter writes to and whether it opened it (so finishes it). A run the script opened
    with `probe.init()` is adopted; a launcher's (`PROBE_RUN_ID`) is joined. Otherwise a new run, keyed
    by ``external_id`` so a relaunch finds it: a resume reopens it with `Rewind(step=rewind_step)`
    (the run continues from that step), a fresh start retries it from scratch (`supersede`).

    ``should_stamp_checkpoints``: the adapter stamps each checkpoint with its attempt (`stamp_checkpoint`; verl,
    SkyRL), and ``resume_from`` is the checkpoint folder a resume loads, so the resume reopens exactly the attempt
    that wrote it. A checkpoint with no stamp of this job (an older CLI's) is found by name, as before. A job
    whose sent name and adapter name are both none or a library default (a ComposedName) gets a key nobody else
    has, so it is never filed as a retry of someone else's run. TRL keys its runs itself (`trl/run_key.py`) and opts out."""
    import probe

    active = probe.active_run()
    if active is not None and getattr(active, "_closed_status", None) is not None:
        active = None  # finished, but still bound in this scope: never written to again
    if active is not None and str(active.id) not in OPENED_RUNS:
        return active, False
    kwargs: dict[str, Any] = {"name": name, **dict(init_kwargs)}
    if _env_run_id():
        for key in _LAUNCHER_DROPPED:
            kwargs.pop(key, None)
        run = probe.init(**{key: value for key, value in kwargs.items() if value is not None})
        if config is not None:
            send_missing_config(run, config)
        return run, False
    if config is not None:
        kwargs.setdefault("config", dict(config))
    owns_key = should_stamp_checkpoints and external_id is not None and "external_id" not in init_kwargs
    is_minted = False
    stamped = read_checkpoint_attempt(resume_from, external_id) if owns_key and rewind_step is not None and resume_from else None
    if stamped is not None:
        external_id = stamped
    elif owns_key and _is_unchosen(kwargs.get("name")) and _is_unchosen(name):
        # Neither the name sent (init kwargs win) nor the adapter's names the job: none (verl's empty experiment,
        # SkyRL's empty run_name) or a library default.
        # A library default names nobody's run: a key nobody else has. A resume whose checkpoint names no attempt
        # of this job continues in a new run rather than rewind the team-wide name's (someone else's points).
        if rewind_step is not None:
            _diagnostics.warn(
                f"probe: the checkpoint this job resumes from records no run of {external_id!r} (saved by an older "
                "CLI, or not written); it continues in a new run."
            )
            rewind_step = None  # a key nobody has: nothing to rewind (and offline refuses a Rewind)
        external_id, is_minted = make_unique_key(external_id), True
    if external_id is not None:
        kwargs.setdefault("external_id", external_id)
        kwargs.setdefault("on_conflict", probe.Rewind(step=rewind_step) if rewind_step is not None else "supersede")
    if kwargs.get("project") is None and kwargs.get("experiment") is None:
        kwargs["project"] = probe.FROM_ENV
    if active is not None:
        kwargs.setdefault("reinit", "create_new")  # another adapter's open run stays open and bound
    # Only a run this adapter creates is born `rl`; an adopted or joined one is someone's choice to keep
    # (the server marks it `rl` on its first sample batch when nobody declared a type).
    kwargs.setdefault("run_type", RunType.RL.value)
    run = probe.init(**{key: value for key, value in kwargs.items() if value is not None})
    OPENED_RUNS.add(str(run.id))
    if is_minted:
        # An offline run's handle carries no external_id. A minted key cannot collide when `probe sync` delivers
        # it, so it is the attempt's; a chosen name may become `-r2` there, so it is never stamped from here.
        OPENED_KEYS[str(run.id)] = external_id
    return run, True


def send_missing_config(run: Any, config: Mapping[str, Any]) -> None:
    """A joined run (`PROBE_RUN_ID`) gets the trainer's config keys it lacks; a key already on the run (a person's,
    or another process's) is kept: the server's merge is new-wins, so those are never sent."""
    try:
        stored = getattr(run, "config", None) or {}
        missing = {key: value for key, value in dict(config).items() if key not in stored}
        if missing:
            run.update_config(missing, allow_val_change=True)
    except Exception as exc:  # noqa: BLE001 -- fail open: a config Probe cannot send never costs the run
        logger.warning("Probe could not add the trainer config to the joined run (%s: %s)", type(exc).__name__, exc)


def close_run(
    run: Any,
    samples: Any,
    *,
    final_step: int | None,
    should_finish: bool,
    status: str | None,
    wait_seconds: float | None = None,
    flush_timeout: float | None = None,
) -> None:
    """The owner's close: the terminal manifest, this producer's held parts journaled, the barrier that
    waits (``wait_seconds``, default `PROBE_SAMPLES_CLOSE_WAIT`; 0 skips it) for every declared producer's last
    seal, then the run's own finish when this adapter opened it (its delivery bounded by ``flush_timeout``)."""
    manifest: dict[str, Any] = {"is_closed": True}
    if final_step is not None:
        manifest["final_step"] = final_step
    samples.plan(**manifest)
    samples.close()
    if wait_seconds is None or wait_seconds > 0:
        samples.wait_for_producers(timeout=wait_seconds)
    if should_finish:
        import probe
        from probe.sdk import fluent

        args = () if status is None else (status,)
        kwargs = {} if flush_timeout is None else {"flush_timeout": flush_timeout}
        if probe.active_run() is run:
            fluent.finish(*args, **kwargs)  # also unbinds it, so the next `probe.init()` opens a new run
        else:
            run.finish(*args, **kwargs)
        OPENED_RUNS.discard(str(run.id))


def close_at_exit(tracker: Any) -> None:
    """At interpreter exit, ``tracker.close_at_exit()`` once: registered after the run opened, so it runs
    before `probe.init()`'s own exit hooks, which then give the run its exit status."""
    ref = weakref.ref(tracker)

    def _close() -> None:
        found = ref()
        if found is not None:
            try:
                found.close_at_exit()
            except Exception:  # noqa: BLE001 -- nothing raises at exit
                pass

    atexit.register(_close)


def get_worker_settings(environ: Mapping[str, str]) -> dict[str, str]:
    """This driver's `PROBE_*` settings a Ray worker may see: never a credential (`SECRET_WORDS`)."""
    return {name: value for name, value in environ.items()
            if name.startswith("PROBE_") and not any(word in name for word in SECRET_WORDS)}


def build_worker_env(run: Any, environ: Mapping[str, str], *, worker_token_env: str) -> dict[str, str]:
    """What a launcher's Ray workers need to join ``run`` as producers: its id and epoch, the server, and a
    credential that can write this one run only (``worker_token_env`` when set, the launcher's own when it is
    already a run token, else a minted one). A Ray runtime env shows in Ray's dashboard, so the researcher's own
    token never goes there: no run token, no worker credential (workers then warn and record nothing)."""
    run_id = getattr(run, "id", None)
    if not run_id or getattr(run, "disabled", False):
        return {}
    client = getattr(run, "_client", None)
    env = {"PROBE_RUN_ID": str(run_id)}
    if epoch := getattr(run, "write_epoch", None):
        env["PROBE_RUN_EPOCH"] = str(epoch)
    base_url = getattr(getattr(client, "settings", None), "base_url", None)
    if base_url:
        env["PROBE_BASE_URL"] = str(base_url)
    token = (environ.get(worker_token_env) or _get_run_scoped_token(environ)
             or _mint_run_token(client, str(run_id), worker_token_env))
    if token:
        env["PROBE_TOKEN"] = token
    return env


def _get_run_scoped_token(environ: Mapping[str, str]) -> str | None:
    """The launcher's own credential when it is already this run's (`probe exec` hands a job a `probe_run_`
    token, which cannot mint another): it records this one run and nothing else."""
    token = environ.get("PROBE_TOKEN", "")
    return token if token.startswith(RUN_TOKEN_PREFIX) else None


def _mint_run_token(client: Any, run_id: str, worker_token_env: str) -> str | None:
    """A `probe_run_` token for this run (`POST /v1/runs/{id}/tokens`); None, warned, when the server or
    the credential cannot mint one (a project-bound token cannot: set ``worker_token_env``)."""
    try:
        minted = client.mint_run_token(run_id)
    except Exception as exc:  # noqa: BLE001 -- fail closed: workers get no credential, never ours
        logger.warning(
            "Probe could not mint a run token for the Ray workers (%s: %s); they will record nothing. "
            "Set %s to a credential they may carry.", type(exc).__name__, exc, worker_token_env,
        )
        return None
    token = minted.get("token") if isinstance(minted, dict) else None
    return token if isinstance(token, str) and token else None


# -- the attempt that wrote a checkpoint, stamped inside it -------------------------------------------------------------
# Names, library defaults above all, collide across a team, and a fresh restart opens `<key>-r2` beside the
# checkpoints the first attempt left: only the checkpoint itself knows which attempt wrote it.

#: The stamp's file name inside a checkpoint folder (verl's and SkyRL's `global_step_N/`). It names the attempt
#: (`external_id`), never the run id.
CHECKPOINT_STAMP = "probe_run.json"
#: A key `open_run` minted (`make_unique_key`), by run id: an offline run's handle has no external_id.
OPENED_KEYS: dict[str, str] = {}
_WARNED_UNSTAMPABLE: set[str] = set()


def stamp_checkpoint(run: Any, folder: Any) -> None:
    """Write which attempt (its `external_id`) wrote the checkpoint in ``folder``, first thing on save; a joined run
    (the verl launcher's, SkyRL's entrypoint's) stamps the key its launcher opened it with. A handle with no key
    (a `probe exec` run, an offline run under a chosen name) or a write that fails removes any older stamp instead:
    this attempt overwrote that checkpoint. A folder that is not a local directory (`s3://...`) gets
    nothing. A resume from an unstamped checkpoint finds its run by name, or opens a new one for a library-default
    name or none. Never raises; a disabled run writes nothing."""
    if getattr(run, "disabled", False):
        return
    data = getattr(run, "data", None) or {}
    external_id = data.get("external_id") or OPENED_KEYS.get(str(getattr(run, "id", "")))
    folder = str(folder or "")
    if "://" in folder or not os.path.isdir(folder):
        if folder and isinstance(external_id, str) and external_id not in _WARNED_UNSTAMPABLE:
            _WARNED_UNSTAMPABLE.add(external_id)
            _diagnostics.warn(f"probe: checkpoints in {folder} cannot record their run; a resume from one "
                              "finds its run by name, or opens a new one for a library-default name or none.")
        return
    path = os.path.join(folder, CHECKPOINT_STAMP)
    if not isinstance(external_id, str) or not external_id:
        _remove_quietly(path)
        return
    partial = None
    try:
        handle, partial = tempfile.mkstemp(dir=folder, prefix=f".{CHECKPOINT_STAMP}.", suffix=".tmp")
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump({"external_id": external_id}, stream)
        os.replace(partial, path)
    except OSError as exc:
        _remove_quietly(path)  # an older attempt's stamp in an overwritten folder would name the wrong run
        if partial is not None:
            _remove_quietly(partial)
        _diagnostics.warn(
            f"probe: could not stamp checkpoint {folder} with its run ({type(exc).__name__}: {exc}); "
            "a resume from it finds its run by name, or opens a new one for a library-default name or none."
        )


def _remove_quietly(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


def read_checkpoint_attempt(folder: str, base_key: str) -> str | None:
    """The `external_id` of the attempt that wrote the checkpoint in ``folder`` when it is this job's: ``base_key``
    itself, a unique key minted from it (`<key>@1a2b3c4d`), or a retry of either (`-r2`). None otherwise."""
    if "://" in str(folder):
        return None
    try:
        with open(os.path.join(folder, CHECKPOINT_STAMP), encoding="utf-8") as handle:
            stamp = json.load(handle)
    except (OSError, ValueError):
        return None
    external_id = stamp.get("external_id") if isinstance(stamp, dict) else None
    mine = re.compile(re.escape(base_key) + r"(?:@[0-9a-f]{8})?(?:-r[0-9]+)?")
    return external_id if isinstance(external_id, str) and mine.fullmatch(external_id) else None


def _is_unchosen(name: Any) -> bool:
    """No name, or one Probe or a library made up (`ComposedName`): it names nobody's job."""
    return not name or isinstance(name, ComposedName)


def make_unique_key(key: str) -> str:
    """A key nobody else has, for a fresh job whose run name is a library default or none
    (`verl:verl_examples/gsm8k@1a2b3c4d`)."""
    return f"{key}@{uuid.uuid4().hex[:8]}"
