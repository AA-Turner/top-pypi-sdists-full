"""`probe.environment(name, version, ...)`: register an RL environment (dashboard redesign D9) and record
that the run uses it.

    env = probe.environment("primeintellect/minibugs", "0.1.0", tasks={"train": 8, "eval": 2})
    parts = [{**part, **env.sample_labels()} for part in parts]     # every episode names it

Idempotent per name@version (`POST /v1/environments`): a second call returns the same environment and only
fills what is still empty. The answer's name and version are the ONE spelling samples carry, so the
environment page joins on them, never on a re-spelled name. With a run (the given one, else the active one)
the use is recorded too (`POST /v1/runs/{run}/uses`, role `train` unless told). NEVER RAISES INTO A JOB.
"""

from __future__ import annotations

import threading
import time
from collections import Counter, deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Mapping

from .vocab import Provider, Role

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client
    from ..run.run import Run

#: The sample columns an environment fills (T3, #5439); never `environment`, which holds Harbor's trial link/files.
SAMPLE_LABEL_NAME = "environment_name"
SAMPLE_LABEL_VERSION = "environment_version"
_PARTS = ("train", "eval")
#: How long a trainer's close waits for `RunEnvironments` registrations still in flight.
CLOSE_WAIT_SECONDS = 10.0


@dataclass
class EnvironmentRef:
    """What `probe.environment(...)` registered. ``ref`` is ``source:<id>``, or None when it could not be
    registered (the warning said why); ``name`` and ``version`` are the server's spelling when it answered."""

    name: str
    version: str = ""
    ref: str | None = None
    id: str | None = None
    provider: str | None = None
    is_created: bool | None = None

    def __str__(self) -> str:
        return self.ref or ""

    def sample_labels(self) -> dict[str, str]:
        """The labels each sample of this environment carries: `{environment_name, environment_version}`."""
        labels = {SAMPLE_LABEL_NAME: self.name}
        if self.version:
            labels[SAMPLE_LABEL_VERSION] = self.version
        return labels

    @classmethod
    def as_sent(cls, name: Any, version: Any = None) -> "EnvironmentRef":
        """The environment as `POST /v1/environments` is sent it, unregistered: name and version stripped, which is
        exactly the `canonical_key` / `revision` the server stores (it strips and never re-spells), so these labels
        equal the answer's whether or not the registration lands."""
        return cls(name=str(name).strip() if isinstance(name, str) else "", version=str(version or "").strip())

    @classmethod
    def from_row(cls, row: Mapping[str, Any], *, name: str, version: str) -> "EnvironmentRef":
        env_id = row.get("id")
        return cls(
            name=str(row.get("name") or name),
            version=str(row.get("version") if row.get("version") is not None else version),
            ref=row.get("ref") or (f"source:{env_id}" if env_id else None),
            id=str(env_id) if env_id else None,
            provider=row.get("provider"),
            is_created=row.get("created"),
        )


def get_default_provider(name: str) -> Provider:
    """`owner/name` is a Prime Environments Hub id; a bare name a local verifiers package."""
    return Provider.PRIME_HUB if "/" in name else Provider.VERIFIERS


def _build_tasks_body(tasks: Mapping[str, Any] | None) -> dict[str, int] | None:
    if not tasks:
        return None
    unknown = set(tasks) - set(_PARTS)
    if unknown:
        from .refs import CatalogRefused

        raise CatalogRefused(f"task counts are per part ({', '.join(_PARTS)}), not {', '.join(sorted(unknown))}")
    found = {part: int(tasks[part]) for part in _PARTS if tasks.get(part) is not None}
    return found or None


def build_environment_body(
    name: str,
    version: str | None = None,
    *,
    provider: str | None = None,
    tasks: Mapping[str, Any] | None = None,
    title: str | None = None,
    description: str | None = None,
    package: str | None = None,
    tags: list[str] | None = None,
    readme: str | None = None,
    homepage: str | None = None,
    license: str | None = None,  # noqa: A002 - the field's name
) -> dict:
    """The `POST /v1/environments` body (the server checks the name, version and provider)."""
    from .refs import CatalogRefused

    if not isinstance(name, str) or not name.strip():
        raise CatalogRefused("an environment needs a name (`owner/name` or `name`)")
    name = name.strip()
    try:
        chosen = Provider(str(provider)) if provider is not None else get_default_provider(name)
    except ValueError:
        raise CatalogRefused(f"`{provider}` is not a provider") from None
    fields = {
        "name": name,
        "version": (str(version).strip() or None) if version is not None else None,
        "provider": chosen.value,
        "tasks": _build_tasks_body(tasks),
        "title": title,
        "description": description,
        "package": package,
        "tags": list(tags) if tags else None,
        "readme": readme,
        "homepage": homepage,
        "license": license,
    }
    return {k: v for k, v in fields.items() if v is not None}


def _get_active_run() -> "Run | None":
    try:
        from ..fluent.fluent import active_run

        return active_run()
    except Exception:  # noqa: BLE001 - never into the job
        return None


def environment(
    name: str,
    version: str | None = None,
    *,
    provider: str | None = None,
    tasks: Mapping[str, Any] | None = None,
    title: str | None = None,
    description: str | None = None,
    package: str | None = None,
    tags: list[str] | None = None,
    readme: str | None = None,
    homepage: str | None = None,
    license: str | None = None,  # noqa: A002 - the field's name
    run: "Run | None" = None,
    role: str = Role.TRAIN.value,
    client: "Client | None" = None,
) -> EnvironmentRef:
    """Register an RL environment version (idempotent per name@version) and, with a run (the given one,
    else the active one), record that the run uses it for ``role``. ``provider`` defaults to `prime_hub` for
    `owner/name` and `verifiers` for a bare name; ``tasks`` is `{train, eval}` task counts. Never raises: a
    failure warns once and returns an `EnvironmentRef` with ``ref`` None, whose labels still name it."""
    from .catalog import REQUEST_SECONDS, _client_for, use
    from .server import _warn_failure

    unsent = EnvironmentRef.as_sent(name, version)
    try:
        body = build_environment_body(
            name, version, provider=provider, tasks=tasks, title=title, description=description,
            package=package, tags=tags, readme=readme, homepage=homepage, license=license,
        )
        bound = run if run is not None else _get_active_run()
        owner = _client_for(client if client is not None else getattr(bound, "_client", None))
        if owner is None:
            return unsent
        from ..delivery.transport.deadlines import deadline_scope

        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            row = owner.create_environment(body)
        found = EnvironmentRef.from_row(row or {}, name=body["name"], version=body.get("version") or "")
        if found.ref and bound is not None and not getattr(bound, "disabled", False):
            use(bound, found.ref, role=role, what="use_environment")
        return found
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, f"probe.environment({name!r})")
        return unsent


class RunEnvironments:
    """The environments one run's trainer names on its own (D9): verl's `data_source`, a SkyRL Gym env class.
    `register` is called per sample on the trainer's hot path, so it NEVER waits: it answers the canonical labels at
    once (`EnvironmentRef.as_sent`, the spelling the server stores) and hands the registration to one background
    thread, which registers each name once per run (``provider``, ``version``) and records each new role (`train`,
    `eval`) once. ``get_tasks`` (called once, on that thread, before the first registration) gives each name's
    `{train, eval}` task counts, or None. A failed registration is not retried; its samples already carry the name
    it sent. Thread-safe; never raises."""

    def __init__(self, run: "Run | None", *, provider: Provider, version: str = "",
                 get_tasks: Callable[[], Mapping[str, Mapping[str, int]] | None] | None = None) -> None:
        self._run = run
        self._provider = provider
        self._version = version
        self._get_tasks = get_tasks
        self._tasks: Mapping[str, Mapping[str, int]] | None = None
        #: Each name's registration answer, filled by the background thread.
        self._found: dict[str, EnvironmentRef] = {}
        self._seen: set[tuple[str, str]] = set()
        self._pending: deque[tuple[str, str]] = deque()
        self._worker: threading.Thread | None = None
        self._idle = threading.Event()
        self._idle.set()
        self._lock = threading.Lock()

    def set_task_source(self, get_tasks: Callable[[], Mapping[str, Mapping[str, int]] | None]) -> None:
        """Where the task counts come from, once the trainer has built its datasets (before any registration)."""
        with self._lock:
            if self._get_tasks is None:
                self._get_tasks = get_tasks

    def register(self, name: str, *, role: str = Role.TRAIN.value) -> EnvironmentRef:
        """``name``'s labels, at once; its registration and the run's use of it for ``role`` go in the background
        the first time each is seen."""
        labels = EnvironmentRef.as_sent(name, self._version)
        if not labels.name or not self._is_recording():
            return labels
        try:
            with self._lock:
                if (labels.name, role) not in self._seen:
                    self._seen.add((labels.name, role))
                    self._pending.append((labels.name, role))
                    self._start_worker()
        except Exception:  # noqa: BLE001 - a thread that cannot start costs the registration, never the sample
            pass
        return labels

    def get_registered(self, name: str) -> EnvironmentRef | None:
        """``name``'s registration answer once it landed (``ref`` None when it failed); None before."""
        with self._lock:
            return self._found.get(name.strip())

    def wait(self, timeout: float | None = None) -> bool:
        """Block until every registration seen so far was sent (or failed); False on ``timeout``. For a close path
        or a test, never for the hot path."""
        return self._idle.wait(timeout)

    def close(self) -> bool:
        """A trainer's end: the registrations still in flight get at most `CLOSE_WAIT_SECONDS` to land (the worker
        thread is a daemon, so a process that exits sooner drops them)."""
        return self.wait(CLOSE_WAIT_SECONDS)

    def _is_recording(self) -> bool:
        return self._run is not None and not getattr(self._run, "disabled", False)

    def _start_worker(self) -> None:  # under the lock
        self._idle.clear()
        if self._worker is None:
            self._worker = threading.Thread(target=self._send_pending, name="probe-environments", daemon=True)
            self._worker.start()

    def _send_pending(self) -> None:
        while True:
            with self._lock:
                if not self._pending:
                    self._worker = None
                    self._idle.set()
                    return
                name, role = self._pending.popleft()
            try:
                self._send(name, role)
            except Exception:  # noqa: BLE001 - never into the job
                pass

    def _send(self, name: str, role: str) -> None:
        found = self._found.get(name)
        if found is not None:  # the queue is in order: the name's registration went first
            if found.ref:
                from .catalog import use

                use(self._run, found.ref, role=role, what="use_environment")
            return
        if self._tasks is None:
            self._tasks = self._read_tasks()
        found = environment(name, self._version or None, provider=self._provider.value, tasks=self._tasks.get(name),
                            run=self._run, role=role)
        with self._lock:
            self._found[name] = found

    def _read_tasks(self) -> Mapping[str, Mapping[str, int]]:
        try:
            return dict(self._get_tasks() or {}) if self._get_tasks is not None else {}
        except Exception:  # noqa: BLE001 - task counts are a convenience; the registration still goes
            return {}


#: Rows `count_tasks` reads per batch: memory stays at one batch of one column, whatever the dataset's size.
COUNT_BATCH_ROWS = 65_536


def _count_column(table: Any, column: str) -> Counter:
    """``column``'s values counted a batch at a time (a Hugging Face `datasets.Dataset`: just that column, as Arrow,
    counted in Arrow), never the whole column in memory. A table that cannot stream counts nothing."""
    counts: Counter = Counter()
    select, iterate = getattr(table, "select_columns", None), getattr(table, "iter", None)
    if not (callable(select) and callable(iterate)):
        return counts
    narrow = select([column])
    as_arrow = getattr(narrow, "with_format", None)
    narrow = as_arrow("arrow") if callable(as_arrow) else narrow
    for batch in narrow.iter(batch_size=COUNT_BATCH_ROWS):
        values = batch[column]
        value_counts = getattr(values, "value_counts", None)
        if callable(value_counts):  # an Arrow column: counted without a Python object per row
            pairs = ((item["values"].as_py(), item["counts"].as_py()) for item in value_counts())
        else:
            pairs = Counter(values).items()
        for value, count in pairs:
            if value:
                counts[str(value)] += int(count)
    return counts


def count_tasks(datasets: Mapping[str, Any], column: str) -> dict[str, dict[str, int]]:
    """Each environment name's task count per part (`{"train": dataset, "eval": dataset}`), from the column that
    names a row's environment in a Hugging Face `datasets.Dataset` (or the trainer's wrapper's `.dataframe`),
    streamed a batch at a time (`_count_column`). A dataset without that column, or one that cannot be read,
    counts nothing."""
    counts: dict[str, dict[str, int]] = {}
    for part, dataset in datasets.items():
        table = getattr(dataset, "dataframe", dataset)
        names = getattr(table, "column_names", None) or ()
        if part not in _PARTS or column not in names:
            continue
        try:
            found = _count_column(table, column)
        except Exception:  # noqa: BLE001 - an unreadable dataset counts nothing
            continue
        for name, count in found.items():
            counts.setdefault(name.strip(), {})[part] = count
    return counts
