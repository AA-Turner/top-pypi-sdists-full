"""SDK-owned replay command backed by a project-owned function registry."""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import shlex
import signal
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TextIO

from bitfab.replay import (
    _REPLAY_PERSISTENCE_TIMEOUT_SECONDS,
    JUDGE_ASSERTIONS_DEPRECATION,
    ReplayConcurrency,
    ReplayError,
    ReplayExperimentStart,
    ReplayItem,
    ReplayItemFinishEvent,
    ReplayItemFinishProgress,
    ReplayResult,
    execute_replay_item,
    report_replay_progress,
    serialize_replay_item,
    serialize_replay_result,
)
from bitfab.replay_interrupt import (
    ReplayInterrupt,
    ReplayInterruptSignal,
    describe_replay_interrupt,
)
from bitfab.replay_invocation import cli_flags
from bitfab.replay_processes import build_process_launcher

if TYPE_CHECKING:
    from bitfab.client import Bitfab


@dataclass(frozen=True)
class ReplayRegistration:
    """One project function exposed through the SDK replay command."""

    client: Bitfab
    fn: Callable[..., Any]
    trace_function_key: str
    options: dict[str, Any] = field(default_factory=dict)
    options_factory: Callable[[ReplayRegistryContext], dict[str, Any]] | None = None


@dataclass(frozen=True)
class ReplayRegistryContext:
    """Caller-supplied values used to build per-run executable options."""

    params: Mapping[str, Any]


_MAX_PINNED_TRACE_IDS = 100

_REGISTRY_OPTION_NAMES = frozenset(
    {
        "limit",
        "trace_ids",
        "name",
        "notes",
        "metadata",
        "max_concurrency",
        "code_change_description",
        "code_change_files",
        "experiment_group_id",
        "dataset_id",
        "dataset_ids",
        "grader_ids",
        "only_with_assertions",
        "skip_assertion_judging",
        "judge_assertions",
        "mock",
        "mock_override",
        "adapt_inputs",
        "db_branch",
        "dry_run",
        "attempts",
        "concurrency",
        "on_item_finish",
    }
)


def _validate_registry_options(options: Mapping[str, Any]) -> None:
    unknown = sorted(set(options) - _REGISTRY_OPTION_NAMES)
    if unknown:
        allowed = ", ".join(sorted(_REGISTRY_OPTION_NAMES))
        raise ValueError(
            f"Unknown replay registry option(s): {', '.join(unknown)}. "
            f"Allowed options: {allowed}."
        )
    on_item_finish = options.get("on_item_finish")
    if on_item_finish is not None and not callable(on_item_finish):
        raise ValueError("Replay registry option on_item_finish must be callable.")


_child_command_context: dict[str, Any] | None = None


def record_child_command_context(
    registry_path: str, replay_args: Sequence[str], environ: Mapping[str, str]
) -> None:
    """Remember how this process was invoked, before the registry module runs.

    ``primitive="process"`` re-execs this command once per work item, and the
    environment it must hand each child is the one the PARENT was started with.
    A registry module boots the project's world at import (Noah mints a sandbox
    settings module and database path with ``setdefault``), and passing that
    booted environment on would point every child at the parent's sandbox, or
    be refused outright by an entrypoint that checks. Captured here because
    this runs before ``runpy`` loads the registry.
    """
    global _child_command_context
    environ = {
        key: value
        for key, value in environ.items()
        if key != "BITFAB_REPLAY_RESULT_PATH"
    }
    _child_command_context = {
        "registry_path": registry_path,
        "replay_args": list(replay_args),
        "environ": environ,
    }


def child_command_context() -> dict[str, Any] | None:
    return _child_command_context


class ReplayRegistry:
    """Project-owned registry of production replay roots."""

    def __init__(self) -> None:
        self._entries: dict[str, ReplayRegistration] = {}

    @property
    def names(self) -> tuple[str, ...]:
        """Return registered command names in registration order."""
        return tuple(self._entries)

    def register(
        self,
        name: str,
        client: Bitfab,
        fn: Callable[..., Any],
        *,
        trace_function_key: str | None = None,
        options_factory: (
            Callable[[ReplayRegistryContext], dict[str, Any]] | None
        ) = None,
        **options: Any,
    ) -> ReplayRegistry:
        """Register the exact callable production invokes.

        Decorated functions carry their trace function key automatically.
        Handler-instrumented or otherwise plain callables must pass
        ``trace_function_key`` explicitly. Pass executable per-function replay
        behavior such as ``mock_override`` and ``adapt_inputs`` as keyword
        options; the installed command forwards them to ``Bitfab.replay``.
        """
        if not name:
            raise ValueError("Replay registry names cannot be empty.")
        if name in self._entries:
            raise ValueError(f"Replay registry already contains '{name}'.")
        if options_factory is not None and not callable(options_factory):
            raise ValueError("Replay registry options_factory must be callable.")
        key = trace_function_key or getattr(fn, "_bitfab_trace_function_key", None)
        if not key:
            raise ValueError(
                "Replay registry entry uses a plain function. Set "
                "trace_function_key to the key its production handler records."
            )
        _validate_registry_options(options)
        self._entries[name] = ReplayRegistration(
            client, fn, key, dict(options), options_factory
        )
        return self

    def get(self, name: str) -> ReplayRegistration:
        """Return a registration by its command name."""
        return self._entries[name]


def _positive_integer(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def _attempt_count(raw: str) -> int:
    value = _positive_integer(raw)
    if value > 100:
        raise argparse.ArgumentTypeError("must be at most 100")
    return value


def _metadata_pair(raw: str) -> tuple[str, str]:
    key, separator, value = raw.partition("=")
    if not separator or not key.strip():
        raise argparse.ArgumentTypeError(
            f"'{raw}' is not a key=value pair, such as schedule=eod"
        )
    return key.strip(), value


def _comma_separated(raw: str) -> list[str]:
    values = [value.strip() for value in raw.split(",") if value.strip()]
    if not values:
        raise argparse.ArgumentTypeError("must contain at least one value")
    return values


def _registry_dataset_ids(options: Mapping[str, Any]) -> list[str] | None:
    dataset_id = options.get("dataset_id")
    dataset_ids = options.get("dataset_ids")
    if dataset_id is not None and dataset_ids is not None:
        raise ValueError(
            "Replay registry options dataset_id and dataset_ids are the same "
            "selector: set one of them."
        )
    if dataset_id is not None:
        return [dataset_id]
    return list(dataset_ids) if dataset_ids is not None else None


def _describe_selection(options: Mapping[str, Any]) -> str:
    trace_ids = options.get("trace_ids")
    if trace_ids:
        return f"{len(trace_ids)} traces"
    limit = options.get("limit")
    if limit is not None:
        return f"{limit} traces"
    dataset_count = len(options.get("dataset_ids") or [None])
    return (
        f"{dataset_count} datasets' traces" if dataset_count > 1 else "dataset traces"
    )


def _parser(registry: ReplayRegistry | None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay production traces",
        epilog=(
            "Under primitive='process' a child launches only when the machine "
            "has memory for it. Tune with BITFAB_REPLAY_MEMORY_THROTTLE=off, "
            "BITFAB_REPLAY_CHILD_MEMORY_MB, BITFAB_REPLAY_MEMORY_FLOOR_MB."
        ),
    )
    parser.add_argument(
        "pipeline", choices=registry.names if registry is not None else None
    )
    parser.add_argument(
        "--limit",
        type=_positive_integer,
        help=(
            "How many traces to replay. With no trace IDs or datasets "
            "selected it takes the most recent N. Otherwise it bounds that "
            "selection instead of replacing it."
        ),
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--trace-ids", type=_comma_separated)
    selection.add_argument(
        "--dataset-ids",
        "--dataset-id",
        dest="dataset_ids",
        type=_comma_separated,
        help="Datasets to replay, comma separated. Replays the union of their traces, graded by the union of their graders.",
    )
    parser.add_argument(
        "--name",
        help=(
            "What this run is testing, in a few words, such as 'baseline' or "
            "'shorter system prompt'. Bitfab records the commit, branch, tree "
            "state, datasets, and who ran it with every experiment, so do not "
            "repeat them here."
        ),
    )
    parser.add_argument(
        "--notes",
        help=(
            "Run conditions Bitfab cannot see on its own, such as an "
            "environment override or a forced feature flag. Kept on the "
            "experiment next to its name."
        ),
    )
    parser.add_argument(
        "--metadata",
        action="append",
        type=_metadata_pair,
        metavar="KEY=VALUE",
        help=(
            "A caller-owned tag on the experiment, such as schedule=eod. "
            "Repeat the flag for more tags. Read back and filtered on "
            "through client.experiments."
        ),
    )
    parser.add_argument(
        "--concurrency",
        "--max-concurrency",
        dest="max_concurrency",
        type=_positive_integer,
    )
    code_change = parser.add_mutually_exclusive_group()
    code_change.add_argument("--code-change")
    code_change.add_argument("--no-code-change", action="store_true")
    parser.add_argument("--experiment-group-id")
    parser.add_argument("--grader-ids", type=_comma_separated)
    parser.add_argument(
        "--only-with-assertions",
        action="store_true",
        dest="only_with_assertions",
    )
    parser.add_argument(
        "--skip-assertion-judging",
        action="store_true",
        dest="skip_assertion_judging",
        help="don't judge approved assertions on each replay; judging is on by default and costs model calls",
    )
    parser.add_argument(
        "--judge-assertions",
        action="store_true",
        dest="judge_assertions",
        help="deprecated: judging is on by default",
    )
    parser.add_argument("--mock", choices=("none", "all", "marked"))
    db_branch = parser.add_mutually_exclusive_group()
    db_branch.add_argument("--db-branch", action="store_true", dest="db_branch")
    db_branch.add_argument("--no-db-branch", action="store_false", dest="db_branch")
    parser.set_defaults(db_branch=None)
    parser.add_argument("--params")
    parser.add_argument("--param", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        dest="fail_on_error",
        help=(
            "Exit 1 after printing the result when any replayed item errored. "
            "Under --dry-run, items whose inputs failed to resolve count."
        ),
    )
    parser.add_argument("--attempts", type=_attempt_count)
    parser.add_argument("--seed")
    parser.add_argument(
        "--resume",
        metavar="EXPERIMENT_ID",
        help=(
            "Continue this experiment: run only the traces and attempts that "
            "did not finish, and keep the ones that did. The traces, attempts "
            "and graders come from the experiment, so selection flags are refused."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "With --resume, continue even when the experiment had activity in "
            "the last two minutes or its code change differs."
        ),
    )
    parser.add_argument("--execute-item", help=argparse.SUPPRESS)
    return parser


_CLI_INVOCATION_SKIPPED = frozenset({"help", "seed", "execute_item"})


def _cli_flag_value(dest: str, value: Any) -> Any:
    if dest == "param":
        return [raw.partition("=")[0] for raw in value]
    return value


def _cli_invocation_flags(
    parser: argparse.ArgumentParser, args: argparse.Namespace
) -> dict[str, Any]:
    flags: dict[str, Any] = {}
    for action in parser._actions:
        if not action.option_strings or action.dest in _CLI_INVOCATION_SKIPPED:
            continue
        value = getattr(args, action.dest, None)
        if value is None or value == parser.get_default(action.dest):
            continue
        name = action.option_strings[0].lstrip("-")
        if action.nargs == 0:
            if value == action.const:
                flags[name] = True
            continue
        flags[name] = _cli_flag_value(action.dest, value)
    return flags


_RESUME_REFUSED_FLAGS = (
    ("trace_ids", "--trace-ids"),
    ("dataset_ids", "--dataset-ids"),
    ("limit", "--limit"),
    ("attempts", "--attempts"),
    ("grader_ids", "--grader-ids"),
    ("only_with_assertions", "--only-with-assertions"),
    ("dry_run", "--dry-run"),
)

_RESUME_FIXED_OPTIONS = (
    "limit",
    "trace_ids",
    "dataset_id",
    "dataset_ids",
    "grader_ids",
    "only_with_assertions",
    "attempts",
    "dry_run",
)


def _refuse_selection_flags_with_resume(args: argparse.Namespace) -> None:
    if args.force and args.resume is None:
        raise ValueError("--force only applies to --resume <experiment ID>.")
    if args.resume is None:
        return
    passed = [
        flag
        for name, flag in _RESUME_REFUSED_FLAGS
        if getattr(args, name) not in (None, False)
    ]
    if passed:
        raise ValueError(
            f"--resume continues experiment {args.resume} with the traces, "
            "attempts and graders it was started with, so it cannot be combined "
            f"with {', '.join(passed)}. Drop them, or start a new replay."
        )


def _resume_command(args: argparse.Namespace, experiment_id: str) -> str:
    context = child_command_context()
    registry_path = (
        shlex.quote(str(context["registry_path"])) if context is not None else "<path>"
    )
    carried: list[str] = []
    if args.mock is not None:
        carried += ["--mock", args.mock]
    if args.params is not None:
        carried += ["--params", args.params]
    for param in args.param:
        carried += ["--param", param]
    return " ".join(
        [
            "Resume with: bitfab-replay --registry",
            registry_path,
            shlex.quote(args.pipeline),
            *(shlex.quote(arg) for arg in carried),
            "--resume",
            shlex.quote(experiment_id),
        ]
    )


SIGINT_EXIT_CODE = 128 + signal.SIGINT
_INTERRUPT_EXIT_CODES: dict[ReplayInterruptSignal, int] = {
    "SIGINT": SIGINT_EXIT_CODE,
    "SIGTERM": 128 + signal.SIGTERM,
}


def _exit_on_interrupt(
    stderr: TextIO, args: argparse.Namespace, interrupted_experiment_ids: list[str]
) -> Callable[[ReplayInterrupt], None]:
    def on_interrupt(interrupt: ReplayInterrupt) -> None:
        experiment_id = interrupt["experiment_id"]
        interrupted_experiment_ids.append(experiment_id)
        print(
            f"{describe_replay_interrupt(experiment_id, interrupt['marked_interrupted'])} "
            f"{_resume_command(args, experiment_id)}",
            file=stderr,
        )
        raise SystemExit(_INTERRUPT_EXIT_CODES[interrupt["signal"]])

    return on_interrupt


def _parse_seed_cases(raw: str, path: str) -> list[dict[str, Any]]:
    stripped = raw.strip()
    if not stripped:
        raise ValueError(f"Seed file '{path}' is empty.")
    if stripped.startswith("["):
        values = json.loads(stripped)
    else:
        values = [json.loads(line) for line in stripped.splitlines() if line.strip()]

    cases: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ValueError(
                f'Seed case {index} in {path!r} must be an object with an "input" array.'
            )
        if not isinstance(value.get("input"), list):
            raise ValueError(
                f'Seed case {index} in {path!r} is missing an "input" array. '
                "Wrap a single argument as [arg]."
            )
        if "expected" in value:
            raise ValueError(
                f'Seed case {index} in {path!r} carries "expected", which seeding '
                "does not record: the case is run once and its output is what the "
                "run produced. Remove the field."
            )
        cases.append(value)
    return cases


def _resolve_registry_options(
    registration: ReplayRegistration, params: Mapping[str, Any]
) -> dict[str, Any]:
    options = dict(registration.options)
    if registration.options_factory is not None:
        dynamic_options = registration.options_factory(
            ReplayRegistryContext(params=params)
        )
        if not isinstance(dynamic_options, dict):
            raise ValueError("Replay registry options_factory must return a dict.")
        _validate_registry_options(dynamic_options)
        options.update(dynamic_options)
    return options


def seed_from_registry(
    registry: ReplayRegistry,
    pipeline: str,
    cases: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Run each case once through an already-registered pipeline and record it.

    The registration is the point: it already holds the client, the exact
    callable production invokes, and the trace function key replay selects by,
    so a seeded case lands as an original of the function the later replay
    selects. A case's ``input`` and ``kwargs`` are the call itself, recorded
    as-is. The registration's ``adapt_inputs`` is a replay hook and is not run
    here: it reshapes a recorded call at replay time (with the case's
    ``metadata`` on ``ctx``), and running it on the case too would apply it
    twice to the same trace.
    """
    registration = registry.get(pipeline)
    trace_ids = [
        registration.client.seed_trace(
            registration.trace_function_key,
            registration.fn,
            args=list(case.get("input", [])),
            kwargs=dict(case.get("kwargs") or {}),
            metadata=case.get("metadata"),
            session_id=case.get("session_id"),
        )
        for case in cases
    ]
    return {
        "pipeline": pipeline,
        "traceFunctionKey": registration.trace_function_key,
        "traceIds": trace_ids,
    }


def reseed_from_registry(
    registry: ReplayRegistry,
    pipeline: str,
    trace_ids: Sequence[str],
) -> dict[str, Any]:
    registration = registry.get(pipeline)
    reseeded = [
        registration.client.reseed_trace(
            registration.trace_function_key, registration.fn, trace_id=trace_id
        )
        for trace_id in trace_ids
    ]
    return {
        "pipeline": pipeline,
        "traceFunctionKey": registration.trace_function_key,
        "reseeded": [
            {
                "traceId": entry["trace_id"],
                "previousRunTraceId": entry["previous_run_trace_id"],
            }
            for entry in reseeded
        ],
    }


def _seed_parser(registry: ReplayRegistry) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bitfab-seed",
        description="Seed cases, or re-seed traces, through a registered pipeline",
    )
    parser.add_argument("pipeline", choices=registry.names)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--from-trace",
        dest="from_trace",
        type=_comma_separated,
        help=(
            "Re-seed these traces: run the registered function once on each "
            "trace's recorded inputs and record the result under the same trace "
            "id, keeping the previous run as history under a new id. Nothing is "
            "mocked and no experiment is created; labels, assertions, and "
            "dataset membership stay on the trace."
        ),
    )
    source.add_argument(
        "--cases",
        "--seed",
        dest="cases",
        help=(
            "Seed new cases from a JSON or JSONL file. Each case runs once "
            "through the registered function and is recorded as an original."
        ),
    )
    return parser


def run_seed_cli(
    registry: ReplayRegistry,
    argv: list[str] | None = None,
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> dict[str, Any]:
    """Run the SDK-owned seed command against a project registry."""
    args = _seed_parser(registry).parse_args(argv)
    if args.from_trace:
        print(
            f'[seed] Re-seeding {len(args.from_trace)} trace(s) through "{args.pipeline}"...',
            file=stderr,
        )
        reseed_result = reseed_from_registry(registry, args.pipeline, args.from_trace)
        for entry in reseed_result["reseeded"]:
            print(
                f"[seed] {entry['traceId']} now holds the fresh run; the previous "
                f"run is kept as {entry['previousRunTraceId']}",
                file=stderr,
            )
        print(json.dumps(reseed_result, indent=2), file=stdout)
        return reseed_result
    cases = _parse_seed_cases(Path(args.cases).read_text(encoding="utf-8"), args.cases)
    print(
        f'[seed] Running {len(cases)} case(s) through "{args.pipeline}"...',
        file=stderr,
    )
    result = seed_from_registry(registry, args.pipeline, cases)
    trace_ids = result["traceIds"]
    preview = ",".join(trace_ids[:3]) + (",..." if len(trace_ids) > 3 else "")
    print(
        f'[seed] Recorded {len(trace_ids)} trace(s) for "{result["traceFunctionKey"]}". '
        f"Replay them with --trace-ids {preview}",
        file=stderr,
    )
    print(json.dumps(result, indent=2), file=stdout)
    return result


def _load_code_change(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("description"), str):
        raise ValueError(
            f"Invalid --code-change file '{path}': expected {{ description, files }}."
        )
    if not isinstance(value.get("files"), list):
        raise ValueError(
            f"Invalid --code-change file '{path}': expected {{ description, files }}."
        )
    return value


def _parse_parameter(raw: str) -> tuple[str, Any]:
    key, separator, value = raw.partition("=")
    key = key.strip()
    if not separator or not key:
        raise ValueError(
            f"Invalid --param '{raw}': expected a non-empty name=value pair."
        )
    try:
        return key, json.loads(value)
    except json.JSONDecodeError:
        return key, value


def _load_parameters(path: str | None, raw_parameters: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if path is not None:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"Invalid --params file '{path}': expected a JSON object.")
        params.update(value)
    for raw in raw_parameters:
        key, value = _parse_parameter(raw)
        params[key] = value
    return params


def _render_summary(pipeline: str, result: ReplayResult, stderr: TextIO) -> None:
    same = 0
    changed = 0
    errors = 0
    carried_over = 0
    for item in result["items"]:
        if item.get("carried_over"):
            carried_over += 1
        elif item["error"] is not None:
            errors += 1
        elif item["result"] == item["original_output"]:
            same += 1
        else:
            changed += 1

    print("\n─── Summary ───", file=stderr)
    print(f"  Pipeline: {pipeline}", file=stderr)
    print(f"  Replayed: {len(result['items']) - carried_over}", file=stderr)
    if carried_over > 0:
        print(f"  Finished before resume: {carried_over}", file=stderr)
    print(f"  Same:     {same}", file=stderr)
    print(f"  Changed:  {changed}", file=stderr)
    if errors > 0:
        print(f"  Errors:   {errors}", file=stderr)
    print(f"\n  {result['experiment_url']}", file=stderr)


def _exit_if_items_errored(result: ReplayResult, dry_run: bool, stderr: TextIO) -> None:
    items = [item for item in result["items"] if not item.get("carried_over")]
    errored = sum(1 for item in items if item["error"] is not None)
    if errored == 0:
        return
    noun = "resolved" if dry_run else "replayed"
    print(
        f"[replay] {errored} of {len(items)} {noun} items errored; "
        "exiting 1 because of --fail-on-error",
        file=stderr,
    )
    raise SystemExit(1)


def _render_dry_run(pipeline: str, result: ReplayResult, stderr: TextIO) -> None:
    print("\n─── Dry run ───", file=stderr)
    print(f"  Pipeline: {pipeline}", file=stderr)
    print(f"  Resolved: {len(result['items'])} (nothing was executed)", file=stderr)
    for item in result["items"]:
        print(f"\n  {item['original_trace_id']}", file=stderr)
        print(f"    args: {json.dumps(item['input'], default=str)}", file=stderr)
    # Current servers record no experiment for a dry run; an older one still does.
    if result["experiment_url"] is not None:
        print(f"\n  {result['experiment_url']}", file=stderr)


_CHILD_OPTION_NAMES = (
    "mock",
    "mock_override",
    "adapt_inputs",
    "db_branch",
    "dry_run",
)


def _item_label(item: Mapping[str, Any]) -> str:
    return f"{item.get('original_trace_id')}#{item.get('attempt')}"


def _report_item_finish_in_child_process(
    callback: Callable[[ReplayItemFinishEvent], None],
    experiment_id: str,
    item: ReplayItem,
    stderr: TextIO,
    hook_error_path: str | None = None,
) -> None:
    try:
        callback(
            ReplayItemFinishEvent(
                experiment_id=experiment_id, test_run_id=experiment_id, item=item
            )
        )
        return
    except Exception as error:
        message = (
            "[replay] on_item_finish_in_child_process failed for "
            f"{_item_label(item)}: {error}"
        )
    print(message, file=stderr)
    if hook_error_path is None:
        return
    with contextlib.suppress(OSError):
        Path(hook_error_path).write_text(f"{message}\n", encoding="utf-8")


_DELIVERY_LOGGER_NAMES = ("bitfab.otel", "bitfab.http", "bitfab.replay")


class _DeliveryProblems(logging.Handler):
    def __init__(self) -> None:
        super().__init__(logging.WARNING)
        self.counts: dict[str, int] = {}

    def add(self, message: str) -> None:
        with self.lock:
            self.counts[message] = self.counts.get(message, 0) + 1

    def emit(self, record: logging.LogRecord) -> None:
        message = record.getMessage()
        if record.exc_info is not None and record.exc_info[1] is not None:
            message = f"{message}: {record.exc_info[1]}"
        self.add(message)
        if not logging.getLogger().handlers and logging.lastResort is not None:
            logging.lastResort.handle(record)

    def __enter__(self) -> _DeliveryProblems:
        for name in _DELIVERY_LOGGER_NAMES:
            logging.getLogger(name).addHandler(self)
        return self

    def __exit__(self, *exc: object) -> None:
        for name in _DELIVERY_LOGGER_NAMES:
            logging.getLogger(name).removeHandler(self)

    def report(self, label: str) -> str:
        with self.lock:
            counts = list(self.counts.items())
        return "".join(
            f"[replay] span delivery problem for {label}: {message}"
            + (f" (x{count})" if count > 1 else "")
            + "\n"
            for message, count in counts
        )


def _report_experiment_start(
    stderr: TextIO, started_experiment_ids: list[str]
) -> Callable[[ReplayExperimentStart], None]:
    def on_experiment_start(experiment: ReplayExperimentStart) -> None:
        started_experiment_ids.append(experiment["experiment_id"])
        print(
            f"[replay] Experiment {experiment['experiment_id']}: "
            f"{experiment['experiment_url']}",
            file=stderr,
        )

    return on_experiment_start


def _chain_item_finish(
    reporter: Callable[[ReplayItemFinishProgress], None],
    registry_callback: Callable[[ReplayItemFinishProgress], None] | None,
    stderr: TextIO,
) -> Callable[[ReplayItemFinishProgress], None]:
    if registry_callback is None:
        return reporter

    def on_item_finish(progress: ReplayItemFinishProgress) -> None:
        reporter(progress)
        try:
            registry_callback(progress)
        except Exception as error:
            print(
                "[replay] on_item_finish failed for "
                f"{_item_label(progress['item'])}: {error}",
                file=stderr,
            )

    return on_item_finish


def _run_assigned_item(
    registration: ReplayRegistration,
    options: dict[str, Any],
    assignment_path: str,
    on_item_finish_in_child_process: Callable[[ReplayItemFinishEvent], None] | None,
    delivery_timeout: float | None,
    *,
    stdout: TextIO,
    stderr: TextIO,
) -> ReplayItem:
    from bitfab.http import flush_traces

    assignment = json.loads(Path(assignment_path).read_text(encoding="utf-8"))
    if "db_branch" in assignment:
        options = {**options, "db_branch": assignment["db_branch"]}
    dry_run = bool(options.get("dry_run"))
    if delivery_timeout is None:
        delivery_timeout = _REPLAY_PERSISTENCE_TIMEOUT_SECONDS
    with _DeliveryProblems() as problems:
        item = execute_replay_item(
            registration.client,
            registration.fn,
            trace_function_key=registration.trace_function_key,
            experiment_id=assignment["experiment_id"],
            server_item=assignment["server_item"],
            replayed_trace_id=assignment["replayed_trace_id"],
            attempt=assignment["attempt"],
            delivery_timeout=delivery_timeout,
            **{name: options[name] for name in _CHILD_OPTION_NAMES if name in options},
        )
        serialized = serialize_replay_item(item)
        result_path = Path(assignment["result_path"])
        partial_path = result_path.with_name(f"{result_path.name}.partial")
        partial_path.write_text(serialized, encoding="utf-8")
        partial_path.replace(result_path)
        print(serialized, file=stdout)
        if on_item_finish_in_child_process is not None:
            _report_item_finish_in_child_process(
                on_item_finish_in_child_process,
                assignment["experiment_id"],
                item,
                stderr,
                assignment.get("hook_error_path"),
            )
        if not dry_run and not flush_traces(delivery_timeout):
            problems.add(
                "delivery was not confirmed within child_delivery_timeout "
                f"({delivery_timeout:g}s). Spans that failed or were still "
                "sending when the child exited may never reach Bitfab."
            )
    delivery_error_path = assignment.get("delivery_error_path")
    report = problems.report(_item_label(item))
    if report:
        print(report, end="", file=stderr)
        if delivery_error_path is not None:
            with contextlib.suppress(OSError):
                Path(delivery_error_path).write_text(report, encoding="utf-8")
    return item


def _has_approved_assertion(assertions: list[dict[str, Any]]) -> bool:
    return any(assertion.get("approvalState") == "approved" for assertion in assertions)


def _bound_trace_ids(
    client: Bitfab, trace_ids: list[str], limit: int, only_with_assertions: bool
) -> list[str]:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Replay limit must be a positive integer.")
    if not only_with_assertions or limit >= len(trace_ids):
        return trace_ids[:limit]
    selected = []
    for trace_id in trace_ids:
        result = client.traces.get_assertions(trace_id)
        if result["inheritedFrom"] is None and _has_approved_assertion(
            result["assertions"]
        ):
            selected.append(trace_id)
            if len(selected) == limit:
                break
    if not selected:
        raise ValueError(
            "No traces with approved assertions matched this replay selection."
        )
    return selected


def _pinned_dataset_members(
    client: Bitfab,
    dataset_ids: list[str],
    limit: int,
    only_with_assertions: bool = False,
) -> list[str] | None:
    members = sorted(
        {
            trace_id
            for dataset_id in dataset_ids
            for trace_id in client.datasets.list_traces(dataset_id)["traceIds"]
        }
    )
    if limit >= len(members):
        return None
    if limit > _MAX_PINNED_TRACE_IDS:
        raise ValueError(
            f"Bounding a dataset replay to {limit} names one trace ID per "
            f"replayed item, and a replay accepts at most "
            f"{_MAX_PINNED_TRACE_IDS}. Drop the limit to replay every "
            "selected dataset in full."
        )
    return _bound_trace_ids(client, members, limit, only_with_assertions)


def check_replay_arguments(argv: list[str]) -> None:
    args = _parser(None).parse_args(argv)
    _refuse_selection_flags_with_resume(args)


def registration_for_args(
    registry: ReplayRegistry, argv: list[str]
) -> ReplayRegistration:
    return registry.get(_parser(registry).parse_args(argv).pipeline)


def run_replay_cli(
    registry: ReplayRegistry,
    argv: list[str] | None = None,
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> ReplayResult | dict[str, Any]:
    """Run the SDK-owned replay command against a project registry.

    The installed ``bitfab-replay`` executable calls this after loading the
    registry passed through ``--registry``. SDK upgrades own common flags,
    lifecycle progress, result serialization, and summary output.
    """
    parser = _parser(registry)
    args = parser.parse_args(argv)
    if args.seed is not None:
        return run_seed_cli(registry, argv, stdout=stdout, stderr=stderr)
    registration = registry.get(args.pipeline)
    options = _resolve_registry_options(
        registration, _load_parameters(args.params, args.param)
    )

    _refuse_selection_flags_with_resume(args)
    if args.resume is not None:
        for name in _RESUME_FIXED_OPTIONS:
            options.pop(name, None)
        options["resume"] = args.resume
        if args.force:
            options["force"] = True
    else:
        registry_dataset_ids = _registry_dataset_ids(options)
        options.pop("dataset_id", None)
        options.pop("dataset_ids", None)
        if registry_dataset_ids is not None:
            options["dataset_ids"] = registry_dataset_ids

        if options.get("trace_ids") is not None and registry_dataset_ids is not None:
            raise ValueError(
                "Replay registry options trace_ids and dataset_ids select different "
                "sources and cannot be used together."
            )

        if args.trace_ids is not None:
            options.pop("dataset_ids", None)
            options["trace_ids"] = args.trace_ids
        elif args.dataset_ids is not None:
            options.pop("trace_ids", None)

        only_with_assertions = args.only_with_assertions or options.get(
            "only_with_assertions", False
        )
        bound = args.limit if args.limit is not None else options.get("limit")
        options.pop("limit", None)
        selected_dataset_ids = args.dataset_ids or options.get("dataset_ids")

        if options.get("trace_ids") is not None:
            if bound is not None:
                options["trace_ids"] = _bound_trace_ids(
                    registration.client,
                    options["trace_ids"],
                    bound,
                    only_with_assertions,
                )
        elif selected_dataset_ids is not None:
            if bound is not None:
                pinned = _pinned_dataset_members(
                    registration.client,
                    selected_dataset_ids,
                    bound,
                    only_with_assertions,
                )
                if pinned is not None:
                    options["trace_ids"] = pinned
        else:
            options["limit"] = bound if bound is not None else 10

    registry_scalars = {
        name for name in ("attempts", "max_concurrency") if name in options
    }
    command_values: dict[str, Any] = {
        "name": args.name,
        "notes": args.notes,
        "metadata": dict(args.metadata) if args.metadata else None,
        "max_concurrency": args.max_concurrency,
        "experiment_group_id": args.experiment_group_id,
        "dataset_ids": args.dataset_ids,
        "grader_ids": args.grader_ids,
        "mock": args.mock,
        "attempts": args.attempts,
        "only_with_assertions": args.only_with_assertions or None,
        "skip_assertion_judging": args.skip_assertion_judging or None,
    }
    options.update(
        {key: value for key, value in command_values.items() if value is not None}
    )

    if args.judge_assertions:
        print(f"bitfab: {JUDGE_ASSERTIONS_DEPRECATION}", file=stderr)

    if args.dry_run:
        options["dry_run"] = True

    if args.db_branch is not None:
        if args.db_branch:
            configured = options.get("db_branch")
            options["db_branch"] = (
                configured if configured not in (None, False) else True
            )
        else:
            options["db_branch"] = False

    code_change = _load_code_change(args.code_change)
    if code_change is not None:
        options["code_change_description"] = code_change["description"]
        options["code_change_files"] = code_change["files"]
    elif args.no_code_change:
        options["code_change_description"] = None
        options["code_change_files"] = None

    concurrency = options.get("concurrency")
    if concurrency is not None:
        if not isinstance(concurrency, ReplayConcurrency):
            raise ValueError(
                "Replay registry option concurrency must be a ReplayConcurrency."
            )
        overrides: dict[str, Any] = {}
        if args.max_concurrency is not None:
            overrides["max_concurrency"] = args.max_concurrency
        if args.attempts is not None:
            overrides["attempts"] = args.attempts
        if overrides:
            concurrency = replace(concurrency, **overrides)
        options["concurrency"] = concurrency
        # Only the flags this command merged above are dropped. A scalar the
        # REGISTRY set alongside concurrency= is left in place so replay()
        # raises on the pairing, rather than being silently outranked by the
        # object's default.
        for name in ("attempts", "max_concurrency"):
            if name not in registry_scalars:
                options.pop(name, None)

    on_item_finish_in_child_process = (
        None
        if concurrency is None or options.get("dry_run")
        else concurrency.on_item_finish_in_child_process
    )

    if args.execute_item is not None:
        return _run_assigned_item(
            registration,
            options,
            args.execute_item,
            on_item_finish_in_child_process,
            None if concurrency is None else concurrency.child_delivery_timeout,
            stdout=stdout,
            stderr=stderr,
        )

    registry_on_item_finish = (
        None if options.get("dry_run") else options.get("on_item_finish")
    )
    options["on_item_start"] = report_replay_progress
    started_experiment_ids: list[str] = []
    options["on_experiment_start"] = _report_experiment_start(
        stderr, started_experiment_ids
    )
    options["on_item_finish"] = _chain_item_finish(
        report_replay_progress, registry_on_item_finish, stderr
    )

    if concurrency is not None and concurrency.primitive == "process":
        context = child_command_context()
        if context is None:
            raise ValueError(
                "concurrency primitive 'process' re-execs this command per "
                "work item, so it only runs under the installed bitfab-replay "
                "entrypoint."
            )
        options["process_launcher"] = build_process_launcher(
            registry_path=context["registry_path"],
            replay_args=context["replay_args"],
            environ=context["environ"],
            max_concurrency=concurrency.max_concurrency,
            on_item_start=options["on_item_start"],
            on_item_finish=options["on_item_finish"],
            memory_throttle=bool(concurrency.memory_throttle),
        )

    if args.resume is not None:
        print(
            f'[replay] Resuming experiment {args.resume} from "{registration.trace_function_key}"...',
            file=stderr,
        )
    else:
        attempts = (
            concurrency.attempts
            if concurrency is not None
            else options.get("attempts", 1)
        )
        attempts_note = f" x{attempts} attempts" if attempts > 1 else ""
        print(
            f'[replay] Replaying {_describe_selection(options)}{attempts_note} from "{registration.trace_function_key}"...',
            file=stderr,
        )

    interrupted_experiment_ids: list[str] = []
    options["on_interrupt"] = _exit_on_interrupt(
        stderr, args, interrupted_experiment_ids
    )
    try:
        with cli_flags(_cli_invocation_flags(parser, args)):
            result = registration.client.replay(
                registration.trace_function_key, registration.fn, **options
            )
    except ReplayError as error:
        for item in error.items:
            item_error = item["trace_error"] or item["replay_error"] or item["error"]
            print(f"{item['original_trace_id']}: {item_error}", file=stderr)
        print(f"Experiment {error.experiment_id}: {error.experiment_url}", file=stderr)
        print(_resume_command(args, error.experiment_id), file=stderr)
        raise
    except BaseException as error:
        if started_experiment_ids and not interrupted_experiment_ids:
            experiment_id = started_experiment_ids[0]
            interrupted = (
                f"[replay] Experiment {experiment_id} stopped. If it did not "
                "finish, Bitfab marks it interrupted within 15 minutes. "
                if isinstance(error, KeyboardInterrupt)
                else ""
            )
            print(
                interrupted + _resume_command(args, experiment_id),
                file=stderr,
            )
        raise

    if args.dry_run:
        _render_dry_run(args.pipeline, result, stderr)
    else:
        _render_summary(args.pipeline, result, stderr)
    print(serialize_replay_result(result), file=stdout)
    # A command that selected nothing did nothing, so it must not exit 0. This
    # is the shape an unseeded corpus takes: --limit 10 against a trace function
    # with no traces reads as a clean run rather than as no run.
    if not result["items"]:
        raise ValueError(
            f'No traces matched "{registration.trace_function_key}", so nothing '
            "was replayed. Seed cases with --seed, or capture a trace first."
        )
    if args.fail_on_error:
        _exit_if_items_errored(result, args.dry_run, stderr)
    return result
