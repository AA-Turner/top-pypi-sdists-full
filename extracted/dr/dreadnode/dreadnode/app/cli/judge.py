"""`dn judge` — entry point for running judges over agent evidence.

Subcommands:

- `dn judge outcome` — evaluate a trajectory against a configured outcome
  judge. Used sandbox-side by the platform's `verify_task` flow and locally
  by anyone running an outcome judge against an exported trajectory.

The CLI reads a judge config JSON + a serialized trajectory from disk,
constructs the appropriate judge implementation, runs it, and writes a
wrapped envelope back to disk. The platform's `verify_task` consumes the
envelope.

Wire format on the output file:

    {"ok": true,  "judgement": { /* OutcomeJudgement */ }}
    {"ok": false, "error": {"type": "...", "message": "...", "judge_kind": "..."}}

Wrapping in `ok` keeps the file format authoritative even if the CLI's exit
code is lost to sandbox plumbing.
"""

import asyncio
import json
import os
import sys
import traceback
import typing as t
from pathlib import Path

import cyclopts
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from dreadnode.judges import (
    JudgeContext,
    MaxStepsExhaustedError,
    OutcomeJudge,
    OutcomeJudgement,
    TrajectoryOutcomeJudge,
)
from dreadnode.judges.outcome import VerdictParseError

cli = cyclopts.App(
    name="judge",
    help="Run a judge over an agent trajectory or other evidence.",
)


# ---------------------------------------------------------------------------
# Config models (discriminated union; v1 has one kind)
# ---------------------------------------------------------------------------


class _BaseJudgeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TrajectoryJudgeConfig(_BaseJudgeConfig):
    """Config payload for a `TrajectoryOutcomeJudge`."""

    kind: t.Literal["trajectory"] = "trajectory"
    model: str = Field(min_length=1)
    rubric: str = Field(min_length=1)
    max_steps: int = Field(default=50, ge=1, le=500)
    system_prompt: str | None = None
    model_params: dict[str, t.Any] = Field(default_factory=dict)
    task_context: dict[str, t.Any] = Field(default_factory=dict)


JudgeConfig = t.Annotated[
    TrajectoryJudgeConfig,
    Field(discriminator="kind"),
]
"""v1 union has one member. Adding `kind="llm"` etc. is a single new branch."""


# ---------------------------------------------------------------------------
# Output envelope
# ---------------------------------------------------------------------------


class _JudgeError(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    message: str
    judge_kind: str | None = None


def _envelope_ok(judgement: OutcomeJudgement) -> dict[str, t.Any]:
    return {"ok": True, "judgement": judgement.model_dump(mode="json")}


def _envelope_error(*, type_: str, message: str, judge_kind: str | None = None) -> dict[str, t.Any]:
    return {
        "ok": False,
        "error": _JudgeError(type=type_, message=message, judge_kind=judge_kind).model_dump(
            mode="json"
        ),
    }


def _write_envelope(output: Path, envelope: dict[str, t.Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2))


# ---------------------------------------------------------------------------
# Judge construction
# ---------------------------------------------------------------------------


def _build_judge(config: TrajectoryJudgeConfig) -> OutcomeJudge:
    if config.kind == "trajectory":
        return TrajectoryOutcomeJudge(
            model=config.model,
            rubric=config.rubric,
            max_steps=config.max_steps,
            system_prompt=config.system_prompt,
            model_params=config.model_params,
        )
    # Exhaustiveness: when a new kind is added to the discriminator, mypy /
    # ty / pyright flag this line. `assert_never` keeps the runtime guard
    # without a type-ignore.
    t.assert_never(config.kind)


TrajectoryInputFormat = t.Literal["native", "openai"]
"""Supported on-disk shapes for the trajectory file.

- ``native``: output of `Trajectory.to_dict()` (event-graph serialization).
  This is what notebook users produce when round-tripping an SDK
  Trajectory through JSON.
- ``openai``: a flat list of OpenAI Chat Completions message dicts (with
  ``tool_calls`` / ``tool_call_id`` preserved). This is what the
  platform's session-trajectory exporter emits for
  ``format="openai"`` and is the format the API hands the CLI when it
  invokes verification.
"""


def _load_trajectory(path: Path, *, input_format: TrajectoryInputFormat) -> t.Any:
    """Deserialize a `Trajectory` from disk. Imported lazily so help text
    doesn't pay the import cost."""
    from dreadnode.agents.trajectory import Trajectory, trajectory_from_openai_format

    data = json.loads(path.read_text())
    if input_format == "openai":
        if not isinstance(data, list):
            raise ValueError(
                "openai-format trajectory file must contain a JSON list of "
                f"message dicts; got {type(data).__name__}"
            )
        return trajectory_from_openai_format(data)
    return Trajectory.from_dict(data)


class _SessionFetchConfigError(RuntimeError):
    """Raised when required env vars or arguments for session fetch are missing."""


def _fetch_trajectory_by_session_id(session_id: str, *, include_compacted: bool) -> t.Any:
    """Fetch a session's trajectory from the platform API and deserialize.

    Reads ``DREADNODE_SERVER``, ``DREADNODE_API_KEY``, ``DREADNODE_ORGANIZATION``,
    ``DREADNODE_WORKSPACE`` from the environment (all four are injected into
    evaluation sandboxes; SESSIONS_READ scope is granted for the sandbox key).
    Calls ``ApiClient.get_session_trajectory`` with ``format="openai"`` and
    converts the result to a ``Trajectory`` via the same helper used for
    on-disk openai-format inputs.

    Raises ``_SessionFetchConfigError`` for missing env vars (caller maps to
    ConfigError envelope) and re-raises any HTTP/parse failure as-is (caller
    maps to RuntimeError envelope).
    """
    from dreadnode.agents.trajectory import trajectory_from_openai_format
    from dreadnode.app.api.client import ApiClient

    base_url = os.environ.get("DREADNODE_SERVER")
    api_key = os.environ.get("DREADNODE_API_KEY")
    org = os.environ.get("DREADNODE_ORGANIZATION")
    workspace = os.environ.get("DREADNODE_WORKSPACE")
    missing = [
        name
        for name, value in (
            ("DREADNODE_SERVER", base_url),
            ("DREADNODE_API_KEY", api_key),
            ("DREADNODE_ORGANIZATION", org),
            ("DREADNODE_WORKSPACE", workspace),
        )
        if not value
    ]
    if missing:
        raise _SessionFetchConfigError(
            f"Cannot fetch trajectory by session id: missing env vars: {', '.join(missing)}"
        )

    # mypy/ty: the missing check above guarantees these are non-None.
    assert base_url is not None
    assert org is not None
    assert workspace is not None

    client = ApiClient(base_url, api_key=api_key)
    data = client.get_session_trajectory(
        org,
        workspace,
        session_id,
        format="openai",
        include_compacted=include_compacted,
    )
    if not isinstance(data, list):
        raise TypeError(
            "session trajectory response must be a JSON list of message dicts; "
            f"got {type(data).__name__}"
        )
    return trajectory_from_openai_format(data)


# ---------------------------------------------------------------------------
# `dn judge outcome` — evaluate a trajectory against an outcome judge.
# ---------------------------------------------------------------------------


@cli.command(name="outcome")
def outcome(
    *,
    config: t.Annotated[
        Path, cyclopts.Parameter(help="Path to the judge config JSON (JudgeConfig).")
    ],
    output: t.Annotated[
        Path,
        cyclopts.Parameter(help="Path to write the wrapped judgement envelope JSON."),
    ],
    trajectory: t.Annotated[
        Path | None,
        cyclopts.Parameter(
            help=(
                "Path to the serialized trajectory JSON. Mutually exclusive "
                "with --session-id. Omit both for filesystem-only judges that "
                "don't need a trajectory."
            )
        ),
    ] = None,
    session_id: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Session UUID to fetch the trajectory for via the platform "
                "API. Mutually exclusive with --trajectory. Requires "
                "DREADNODE_SERVER, DREADNODE_API_KEY, DREADNODE_ORGANIZATION, "
                "and DREADNODE_WORKSPACE in the environment."
            )
        ),
    ] = None,
    include_compacted: t.Annotated[
        bool,
        cyclopts.Parameter(
            help=(
                "When fetching by --session-id, include pre-compaction "
                "history so the judge sees the full trajectory. Defaults "
                "to True for the judge use case."
            )
        ),
    ] = True,
    working_dir: t.Annotated[
        Path | None,
        cyclopts.Parameter(help="The agent's working directory inside the sandbox. Optional."),
    ] = None,
    input_format: t.Annotated[
        TrajectoryInputFormat,
        cyclopts.Parameter(
            help=(
                "Shape of the trajectory file (only applies to --trajectory "
                "mode). 'native' is `Trajectory.to_dict()` (notebook/CLI "
                "users); 'openai' is a flat OpenAI Chat Completions messages "
                "array (platform-side verification path)."
            ),
        ),
    ] = "native",
) -> None:
    """Evaluate a serialized trajectory against a configured outcome judge.

    Always writes an envelope JSON to ``--output``. Exits 0 on success
    (envelope's ``ok`` field is true). Exits non-zero on any error
    (envelope's ``ok`` field is false). The envelope is the source of truth
    for the platform; the exit code is defense-in-depth.
    """
    judge_kind: str | None = None

    # 1. Load + validate config
    try:
        config_data = json.loads(config.read_text())
        judge_kind = config_data.get("kind") if isinstance(config_data, dict) else None
        judge_config = TrajectoryJudgeConfig.model_validate(config_data)
        judge_kind = judge_config.kind
    except FileNotFoundError as exc:
        _write_envelope(
            output,
            _envelope_error(
                type_="ConfigError",
                message=f"Judge config file not found: {exc.filename}",
                judge_kind=judge_kind,
            ),
        )
        sys.exit(2)
    except (json.JSONDecodeError, ValidationError) as exc:
        _write_envelope(
            output,
            _envelope_error(
                type_="ConfigError",
                message=str(exc),
                judge_kind=judge_kind,
            ),
        )
        sys.exit(2)

    # 2. Build judge
    try:
        judge = _build_judge(judge_config)
    except Exception as exc:
        _write_envelope(
            output,
            _envelope_error(
                type_="ConfigError",
                message=f"Failed to build judge: {exc}",
                judge_kind=judge_kind,
            ),
        )
        sys.exit(2)

    # 3. Load trajectory. Three modes:
    #    a) --session-id  → fetch from platform API
    #    b) --trajectory  → read from local file
    #    c) neither       → filesystem-only judge with no trajectory
    if trajectory is not None and session_id is not None:
        _write_envelope(
            output,
            _envelope_error(
                type_="ConfigError",
                message="--trajectory and --session-id are mutually exclusive",
                judge_kind=judge_kind,
            ),
        )
        sys.exit(2)

    loaded_trajectory: t.Any | None = None
    if session_id is not None:
        try:
            loaded_trajectory = _fetch_trajectory_by_session_id(
                session_id, include_compacted=include_compacted
            )
        except _SessionFetchConfigError as exc:
            _write_envelope(
                output,
                _envelope_error(
                    type_="ConfigError",
                    message=str(exc),
                    judge_kind=judge_kind,
                ),
            )
            sys.exit(2)
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            _write_envelope(
                output,
                _envelope_error(
                    type_="RuntimeError",
                    message=f"Failed to deserialize fetched trajectory: {exc}",
                    judge_kind=judge_kind,
                ),
            )
            sys.exit(3)
        except Exception as exc:
            _write_envelope(
                output,
                _envelope_error(
                    type_="RuntimeError",
                    message=(
                        f"Failed to fetch trajectory for session "
                        f"{session_id}: {exc.__class__.__name__}: {exc}"
                    ),
                    judge_kind=judge_kind,
                ),
            )
            sys.exit(3)
    elif trajectory is not None:
        try:
            loaded_trajectory = _load_trajectory(trajectory, input_format=input_format)
        except FileNotFoundError as exc:
            _write_envelope(
                output,
                _envelope_error(
                    type_="RuntimeError",
                    message=f"Trajectory file not found: {exc.filename}",
                    judge_kind=judge_kind,
                ),
            )
            sys.exit(3)
        except (json.JSONDecodeError, ValueError) as exc:
            _write_envelope(
                output,
                _envelope_error(
                    type_="RuntimeError",
                    message=f"Failed to deserialize trajectory: {exc}",
                    judge_kind=judge_kind,
                ),
            )
            sys.exit(3)

    context = JudgeContext(
        trajectory=loaded_trajectory,
        task_context=judge_config.task_context,
        working_dir=working_dir,
    )

    # 4. Run judge
    try:
        judgement = asyncio.run(judge.evaluate(context))
    except MaxStepsExhaustedError as exc:
        _write_envelope(
            output,
            _envelope_error(
                type_="MaxStepsExhausted",
                message=str(exc),
                judge_kind=judge_kind,
            ),
        )
        sys.exit(4)
    except VerdictParseError as exc:
        _write_envelope(
            output,
            _envelope_error(
                type_="ParseError",
                message=str(exc),
                judge_kind=judge_kind,
            ),
        )
        sys.exit(4)
    except ValueError as exc:
        # Anything else that comes out as ValueError (e.g. missing trajectory)
        # is a usage/config error, not a parse error.
        _write_envelope(
            output,
            _envelope_error(
                type_="ConfigError",
                message=str(exc),
                judge_kind=judge_kind,
            ),
        )
        sys.exit(2)
    except Exception as exc:
        # Catch-all so the envelope is always written. We include a traceback
        # in metadata-style messaging so the platform debugger can see it.
        tb = traceback.format_exc()
        _write_envelope(
            output,
            _envelope_error(
                type_="RuntimeError",
                message=f"{exc.__class__.__name__}: {exc}\n{tb}",
                judge_kind=judge_kind,
            ),
        )
        sys.exit(5)

    # 5. Happy path
    _write_envelope(output, _envelope_ok(judgement))


__all__ = ["JudgeConfig", "TrajectoryJudgeConfig", "cli"]
