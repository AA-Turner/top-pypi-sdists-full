"""Command-line entry point for live provider and task evaluations."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path

from .evaluation import (
    EvaluationRecord,
    EvaluationRun,
    EvaluationRunner,
    ModelJudge,
    ModelTarget,
    run_from_dict,
)
from .errors import LocalArenaError
from .generation import ChatMessage
from .providers import RequestPolicy, create_provider, provider_names
from .report import write_html_report
from .taskpacks import load_task_pack
from .tasks import Contains, PromptTask, evaluator_from_config

_SENSITIVE_HEADER = re.compile(
    r"(?:authorization|api[-_]?key|token|secret|cookie)",
    re.IGNORECASE,
)
_QUICKSTART_ERROR_GUIDANCE = {
    "ProviderAuthError": (
        "provider rejected the credential; check the key and model access"
    ),
    "ProviderConnectionError": (
        "could not reach the provider; check the server and base URL"
    ),
    "ProviderTimeoutError": (
        "request timed out; increase --timeout or warm the model"
    ),
    "ProviderRateLimitError": (
        "provider rate limit reached; wait and check account limits"
    ),
    "ProviderResponseError": (
        "provider returned an incompatible or unsuccessful response; "
        "check the model ID and Chat Completions support"
    ),
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="localarena",
        description="Run live model evaluations against explicit providers.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    providers = subparsers.add_parser(
        "providers",
        help="list built-in provider profiles",
    )
    providers.set_defaults(handler=_providers_command)

    models = subparsers.add_parser(
        "models",
        help="list models from one configured provider",
    )
    models.add_argument("provider", choices=provider_names())
    models.add_argument("--base-url")
    models.add_argument(
        "--api-key-env",
        help="read the API key from this environment variable",
    )
    models.add_argument("--timeout", type=float, default=30)
    models.set_defaults(handler=_models_command)

    quickstart = subparsers.add_parser(
        "quickstart",
        help="run one scored smoke test without creating a config file",
    )
    quickstart.add_argument("provider", choices=provider_names())
    quickstart.add_argument("model", help="exact model ID served by the provider")
    quickstart.add_argument("--base-url")
    quickstart.add_argument(
        "--api-key-env",
        help="read the API key from this environment variable",
    )
    quickstart.add_argument("--timeout", type=float, default=120)
    quickstart.add_argument("--max-tokens", type=int, default=512)
    quickstart.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("localarena-results.json"),
    )
    quickstart.add_argument(
        "--report",
        type=Path,
        default=Path("localarena-report.html"),
    )
    quickstart.add_argument(
        "--include-content",
        action="store_true",
        help=(
            "retain the smoke-test prompt, generated answer, score reason, "
            "and safe diagnostics"
        ),
    )
    quickstart.set_defaults(handler=_quickstart_command)

    run = subparsers.add_parser(
        "run",
        help="run every configured model against every configured task",
    )
    run.add_argument("config", type=Path)
    run.add_argument("--output", "-o", type=Path, required=True)
    run.add_argument("--report", type=Path)
    run.add_argument("--concurrency", type=int)
    run.add_argument("--repetitions", type=int)
    content = run.add_mutually_exclusive_group()
    content.add_argument(
        "--include-content",
        action="store_true",
        help=(
            "retain task content, generated answers, evaluator details, "
            "score reasons, and safe diagnostics"
        ),
    )
    content.add_argument(
        "--no-content",
        action="store_true",
        help=(
            "omit task content, evaluator details, answer text, score reasons, "
            "and error details from results and reports"
        ),
    )
    run.set_defaults(handler=_run_command)

    report = subparsers.add_parser(
        "report",
        help="render a saved result JSON file as standalone HTML",
    )
    report.add_argument("results", type=Path)
    report.add_argument("--output", "-o", type=Path, required=True)
    report.add_argument("--title")
    report.set_defaults(handler=_report_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = _parser()
    arguments = parser.parse_args(argv)
    try:
        return arguments.handler(arguments)
    except (LocalArenaError, OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    return 2


def _providers_command(arguments: argparse.Namespace) -> int:
    del arguments
    for name in provider_names():
        print(name)
    return 0


def _models_command(arguments: argparse.Namespace) -> int:
    api_key = _read_optional_secret(arguments.api_key_env)
    provider = create_provider(
        arguments.provider,
        base_url=arguments.base_url,
        api_key=api_key,
        policy=RequestPolicy(timeout=arguments.timeout),
    )
    for model in provider.list_models():
        print(model.id)
    return 0


def _quickstart_command(arguments: argparse.Namespace) -> int:
    _require_distinct_output_paths(arguments.output, arguments.report)
    api_key = _read_optional_secret(arguments.api_key_env)
    provider = create_provider(
        arguments.provider,
        base_url=arguments.base_url,
        api_key=api_key,
        policy=RequestPolicy(timeout=arguments.timeout),
    )
    target = ModelTarget(
        name=arguments.model,
        provider=provider,
        model=arguments.model,
        max_tokens=arguments.max_tokens,
    )
    task = PromptTask.from_text(
        "arithmetic-smoke-test",
        (
            "Reply with exactly the two characters 42. "
            "Do not add punctuation or an explanation."
        ),
        evaluator=Contains(("42",)),
    )
    run = EvaluationRunner(
        (target,),
        (task,),
        max_concurrency=1,
        include_content=arguments.include_content,
    ).run(
        name=f"{arguments.provider} quickstart",
        progress=_print_progress,
    )
    _write_run_outputs(run, arguments.output, arguments.report)
    _print_summary(run)
    _print_quickstart_errors(run)
    print(f"Results: {arguments.output}")
    print(f"Report: {arguments.report}")
    return _run_exit_code(run)


def _run_command(arguments: argparse.Namespace) -> int:
    _require_distinct_output_paths(arguments.output, arguments.report)
    config = _read_json_object(arguments.config)
    _require_keys(
        config,
        {
            "$schema",
            "name",
            "concurrency",
            "repetitions",
            "include_content",
            "models",
            "tasks",
            "task_files",
        },
        "config",
    )
    models, targets = _models_from_config(config)
    tasks = _tasks_from_config(
        config,
        targets,
        base_directory=arguments.config.parent,
    )
    configured_concurrency = config.get("concurrency", 4)
    configured_repetitions = config.get("repetitions", 1)
    concurrency = (
        arguments.concurrency
        if arguments.concurrency is not None
        else configured_concurrency
    )
    repetitions = (
        arguments.repetitions
        if arguments.repetitions is not None
        else configured_repetitions
    )
    if arguments.include_content:
        include_content = True
    elif arguments.no_content:
        include_content = False
    else:
        include_content = config.get("include_content", False)
    runner = EvaluationRunner(
        models,
        tasks,
        max_concurrency=concurrency,
        repetitions=repetitions,
        include_content=include_content,
    )
    run_name = config.get("name", arguments.config.stem)
    run = runner.run(name=run_name, progress=_print_progress)
    _write_run_outputs(run, arguments.output, arguments.report)
    _print_summary(run)
    return _run_exit_code(run)


def _write_run_outputs(
    run: EvaluationRun,
    output: Path,
    report: Path | None,
) -> None:
    _write_text(output, run.to_json() + "\n")
    if report is not None:
        _ensure_parent(report)
        write_html_report(run, report)


def _print_summary(run: EvaluationRun) -> None:
    print()
    for row in run.summary():
        raw_score = row["average_score"]
        score_text = (
            "unscored"
            if raw_score is None
            else f"{float(raw_score):.3f}"
        )
        decision = row["reliability_adjusted_score"]
        decision_text = (
            "unscored"
            if decision is None
            else f"{float(decision):.3f}"
        )
        confidence = (
            f"{float(row['arena_confidence_lower']):.1f}–"
            f"{float(row['arena_confidence_upper']):.1f}"
        )
        evidence = (
            "inconclusive"
            if row["arena_inconclusive"]
            else "separated"
        )
        print(
            f'{row["rank"]:>2}. {row["name"]}: '
            f"score={score_text} decision={decision_text} "
            f"arena={float(row['arena_rating']):.1f} "
            f"95%CI={confidence} {evidence} "
            f"errors={row['errors']}"
        )


def _run_exit_code(run: EvaluationRun) -> int:
    return 2 if any(record.error is not None for record in run.records) else 0


def _print_quickstart_errors(run: EvaluationRun) -> None:
    for record in run.records:
        if record.error is None:
            continue
        error_type, separator, _ = record.error.partition(":")
        if separator != ":" or error_type not in _QUICKSTART_ERROR_GUIDANCE:
            error_type = "Error"
        status = record.error_metadata.get("status_code")
        status_text = (
            f" (HTTP {status})"
            if type(status) is int
            else ""
        )
        guidance = _QUICKSTART_ERROR_GUIDANCE.get(
            error_type,
            "evaluation failed; inspect the provider logs",
        )
        print(
            f"Quickstart error: {error_type}{status_text}: {guidance}",
            file=sys.stderr,
        )


def _report_command(arguments: argparse.Namespace) -> int:
    run = run_from_dict(_read_json_object(arguments.results))
    _ensure_parent(arguments.output)
    write_html_report(run, arguments.output, title=arguments.title)
    print(arguments.output)
    return 0


def _print_progress(
    completed: int,
    total: int,
    record: EvaluationRecord,
) -> None:
    print(
        f"[{completed}/{total}] {record.target} × {record.task_id}: "
        f"{record.status}",
        file=sys.stderr,
    )


def _models_from_config(
    config: Mapping[str, object],
) -> tuple[tuple[ModelTarget, ...], tuple[ModelTarget, ...]]:
    values = config.get("models")
    if not isinstance(values, list) or not values:
        raise ValueError("config.models must be a non-empty array")
    models: list[ModelTarget] = []
    candidates: list[ModelTarget] = []
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise TypeError(f"config.models[{index}] must be an object")
        _require_keys(
            value,
            {
                "name",
                "provider",
                "base_url",
                "api_key_env",
                "headers",
                "headers_env",
                "policy",
                "model",
                "parameters",
                "judge_only",
            },
            f"config.models[{index}]",
        )
        if "api_key" in value:
            raise ValueError(
                f"config.models[{index}] must use api_key_env, not api_key"
            )
        profile = value.get("provider")
        if type(profile) is not str:
            raise TypeError(f"config.models[{index}].provider must be a string")
        api_key_env = value.get("api_key_env")
        if api_key_env is not None and type(api_key_env) is not str:
            raise TypeError(
                f"config.models[{index}].api_key_env must be a string"
            )
        policy_value = value.get("policy", {})
        if not isinstance(policy_value, Mapping):
            raise TypeError(f"config.models[{index}].policy must be an object")
        _require_keys(
            policy_value,
            {
                "timeout",
                "max_attempts",
                "backoff_seconds",
                "max_backoff_seconds",
                "max_retry_after_seconds",
                "max_response_bytes",
            },
            f"config.models[{index}].policy",
        )
        policy = RequestPolicy(
            timeout=policy_value.get("timeout", 120),  # type: ignore[arg-type]
            max_attempts=policy_value.get("max_attempts", 1),  # type: ignore[arg-type]
            backoff_seconds=policy_value.get("backoff_seconds", 0.5),  # type: ignore[arg-type]
            max_backoff_seconds=policy_value.get("max_backoff_seconds", 8),  # type: ignore[arg-type]
            max_retry_after_seconds=policy_value.get(
                "max_retry_after_seconds", 30
            ),  # type: ignore[arg-type]
            max_response_bytes=policy_value.get(
                "max_response_bytes", 8 * 1024 * 1024
            ),  # type: ignore[arg-type]
        )
        headers = _headers_from_config(value, index)
        provider = create_provider(
            profile,
            base_url=value.get("base_url"),  # type: ignore[arg-type]
            api_key=_read_optional_secret(api_key_env),
            headers=headers,
            policy=policy,
        )
        parameters = value.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise TypeError(
                f"config.models[{index}].parameters must be an object"
            )
        _require_keys(
            parameters,
            {
                "max_tokens",
                "temperature",
                "seed",
                "stop",
                "extra_body",
            },
            f"config.models[{index}].parameters",
        )
        extra_body = parameters.get("extra_body", {})
        if not isinstance(extra_body, Mapping):
            raise TypeError(
                f"config.models[{index}].parameters.extra_body must be an object"
            )
        judge_only = value.get("judge_only", False)
        if type(judge_only) is not bool:
            raise TypeError(
                f"config.models[{index}].judge_only must be a boolean"
            )
        target = ModelTarget(
            name=value.get("name"),  # type: ignore[arg-type]
            provider=provider,
            model=value.get("model"),  # type: ignore[arg-type]
            max_tokens=parameters.get("max_tokens", 512),  # type: ignore[arg-type]
            temperature=parameters.get("temperature"),  # type: ignore[arg-type]
            seed=parameters.get("seed"),  # type: ignore[arg-type]
            stop=parameters.get("stop", ()),  # type: ignore[arg-type]
            extra_body=extra_body,
        )
        models.append(target)
        if not judge_only:
            candidates.append(target)
    names = [model.name for model in models]
    if len(names) != len(set(names)):
        raise ValueError("config model names must be unique")
    if not candidates:
        raise ValueError("config must contain at least one non-judge model")
    return tuple(candidates), tuple(models)


def _tasks_from_config(
    config: Mapping[str, object],
    models: tuple[ModelTarget, ...],
    *,
    base_directory: Path = Path("."),
) -> tuple[PromptTask, ...]:
    values = config.get("tasks", [])
    if not isinstance(values, list):
        raise TypeError("config.tasks must be an array")
    task_files = config.get("task_files", [])
    if not isinstance(task_files, list):
        raise TypeError("config.task_files must be an array")
    if not values and not task_files:
        raise ValueError(
            "config must contain at least one inline task or task file"
        )
    targets = {model.name: model for model in models}
    tasks: list[PromptTask] = []
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise TypeError(f"config.tasks[{index}] must be an object")
        _require_keys(
            value,
            {
                "id",
                "prompt",
                "system",
                "messages",
                "evaluator",
                "metadata",
            },
            f"config.tasks[{index}]",
        )
        evaluator_value = value.get("evaluator")
        evaluator: object
        if (
            isinstance(evaluator_value, Mapping)
            and evaluator_value.get("type") == "model_judge"
        ):
            _require_keys(
                evaluator_value,
                {
                    "type",
                    "model",
                    "rubric",
                    "reference_answer",
                    "pass_threshold",
                },
                f"config.tasks[{index}].evaluator",
            )
            target_name = evaluator_value.get("model")
            if type(target_name) is not str or target_name not in targets:
                raise ValueError(
                    f"config.tasks[{index}].evaluator.model must name "
                    "a configured model target"
                )
            evaluator = ModelJudge(
                target=targets[target_name],
                rubric=evaluator_value.get(
                    "rubric",
                    "Score correctness, relevance, and clarity.",
                ),  # type: ignore[arg-type]
                reference_answer=evaluator_value.get(
                    "reference_answer"
                ),  # type: ignore[arg-type]
                pass_threshold=evaluator_value.get(
                    "pass_threshold", 0.5
                ),  # type: ignore[arg-type]
            )
        else:
            evaluator = evaluator_from_config(evaluator_value)  # type: ignore[arg-type]

        messages_value = value.get("messages")
        if messages_value is not None:
            if "prompt" in value or "system" in value:
                raise ValueError(
                    f"config.tasks[{index}] must use either messages or "
                    "prompt/system, not both"
                )
            if not isinstance(messages_value, list) or not messages_value:
                raise ValueError(
                    f"config.tasks[{index}].messages must be a non-empty array"
                )
            messages = []
            for message_index, message in enumerate(messages_value):
                if not isinstance(message, Mapping):
                    raise TypeError(
                        f"config.tasks[{index}].messages[{message_index}] "
                        "must be an object"
                    )
                _require_keys(
                    message,
                    {"role", "content"},
                    (
                        f"config.tasks[{index}].messages"
                        f"[{message_index}]"
                    ),
                )
                messages.append(
                    ChatMessage(
                        role=message.get("role"),  # type: ignore[arg-type]
                        content=message.get("content"),  # type: ignore[arg-type]
                    )
                )
            task = PromptTask(
                id=value.get("id"),  # type: ignore[arg-type]
                messages=tuple(messages),
                evaluator=evaluator,  # type: ignore[arg-type]
                metadata=value.get("metadata", {}),  # type: ignore[arg-type]
            )
        else:
            prompt = value.get("prompt")
            if type(prompt) is not str:
                raise TypeError(
                    f"config.tasks[{index}] must contain prompt or messages"
                )
            task = PromptTask.from_text(
                id=value.get("id"),  # type: ignore[arg-type]
                prompt=prompt,
                system=value.get("system"),  # type: ignore[arg-type]
                evaluator=evaluator,  # type: ignore[arg-type]
                metadata=value.get("metadata", {}),  # type: ignore[arg-type]
            )
        tasks.append(task)

    for index, path_value in enumerate(task_files):
        if type(path_value) is not str or not path_value.strip():
            raise TypeError(
                f"config.task_files[{index}] must be a non-empty string"
            )
        path = Path(path_value)
        if not path.is_absolute():
            path = base_directory / path
        pack = load_task_pack(path)
        tasks.extend(pack.tasks)
        print(
            f"Loaded {len(pack.tasks)} tasks from {pack.name} "
            f"{pack.version} ({pack.digest})",
            file=sys.stderr,
        )

    task_ids = [task.id for task in tasks]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError(
            "task ids must be unique across inline tasks and task files"
        )
    return tuple(tasks)


def _headers_from_config(
    model: Mapping[str, object],
    index: int,
) -> dict[str, str] | None:
    headers_value = model.get("headers", {})
    headers_env_value = model.get("headers_env", {})
    if not isinstance(headers_value, Mapping):
        raise TypeError(f"config.models[{index}].headers must be an object")
    if not isinstance(headers_env_value, Mapping):
        raise TypeError(f"config.models[{index}].headers_env must be an object")

    headers: dict[str, str] = {}
    seen: set[str] = set()
    for name, raw_value in headers_value.items():
        if type(name) is not str or type(raw_value) is not str:
            raise TypeError(
                f"config.models[{index}].headers must map strings to strings"
            )
        if _SENSITIVE_HEADER.search(name):
            raise ValueError(
                f"config.models[{index}].headers.{name} may contain a "
                "credential; use headers_env"
            )
        lowered = name.casefold()
        if lowered in seen:
            raise ValueError(
                f"config.models[{index}] contains duplicate header {name}"
            )
        seen.add(lowered)
        headers[name] = raw_value

    for name, variable in headers_env_value.items():
        if type(name) is not str or type(variable) is not str:
            raise TypeError(
                f"config.models[{index}].headers_env must map header names "
                "to environment variable names"
            )
        lowered = name.casefold()
        if lowered in seen:
            raise ValueError(
                f"config.models[{index}] contains duplicate header {name}"
            )
        seen.add(lowered)
        headers[name] = _read_optional_secret(variable) or ""
    return headers or None


def _read_optional_secret(variable: str | None) -> str | None:
    if variable is None:
        return None
    if type(variable) is not str or not variable:
        raise ValueError("api_key_env must be a non-empty string")
    value = os.environ.get(variable)
    if not value:
        raise ValueError(f"environment variable {variable} is not set")
    return value


def _require_keys(
    value: Mapping[str, object],
    allowed: set[str],
    field_name: str,
) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(
            f"{field_name} contains unsupported fields: {', '.join(extra)}"
        )


def _read_json_object(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def _require_distinct_output_paths(
    output: Path,
    report: Path | None,
) -> None:
    if report is not None and output.resolve() == report.resolve():
        raise ValueError("--output and --report must be different paths")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_text(path: Path, value: str) -> None:
    _ensure_parent(path)
    path.write_text(value, encoding="utf-8")
