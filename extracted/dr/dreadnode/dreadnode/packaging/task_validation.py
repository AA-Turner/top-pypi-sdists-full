"""Local validation for task directories (task.yaml + docker-compose.yaml)."""

from __future__ import annotations

import re
import typing as t
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from pathlib import Path

import yaml
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from dreadnode.core.util import valid_version

# Spec: contract.md "name" must be kebab-case ``[a-z0-9][a-z0-9-]*``.
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# TSK-MOD-002: ceiling on declared inference model identifiers (must match the
# API-side cap so author-side validation predicts platform ingest).
MAX_MODELS = 50

# TSK-VER-006: supported hash algorithms with their hex digest length.
_HASH_ALGORITHMS: dict[str, int] = {
    "sha256": 64,
    "sha512": 128,
    "sha1": 40,
    "md5": 32,
}
_HEX_RE = re.compile(r"^[0-9a-fA-F]+$")


def parse_flag_hash(value: str) -> tuple[str, str]:
    """Parse a flag hash string into ``(algorithm, hex_digest)``.

    Accepts both ``{alg}:{hex}`` and bare hex. Per TSK-VER-005, a *bare* digest
    always means sha256; sha512/sha1/md5 must use the explicit ``{alg}:{hex}``
    form. (This matches the platform ingest validator so ``dn task validate``
    predicts what the API will accept.)
    """
    if not isinstance(value, str) or not value:
        raise ValueError("must be a non-empty string like 'sha256:<hex>' or a bare hex digest")

    supported = ", ".join(sorted(_HASH_ALGORITHMS))

    if ":" in value:
        alg, _, hex_digest = value.partition(":")
        alg = alg.lower()
        if alg not in _HASH_ALGORITHMS:
            raise ValueError(
                f"unsupported hash algorithm '{alg}' — supported algorithms are {supported}"
            )
    else:
        hex_digest = value
        alg = "sha256"
        if len(hex_digest) != _HASH_ALGORITHMS[alg]:
            raise ValueError(
                f"a bare hash is read as sha256 ({_HASH_ALGORITHMS[alg]} hex chars), "
                f"got {len(hex_digest)} — use the 'algorithm:hex' form for {supported}"
            )

    if not hex_digest:
        raise ValueError(f"missing the hex digest after '{alg}:' — example: {alg}:abc123...")
    if not _HEX_RE.fullmatch(hex_digest):
        raise ValueError(f"'{hex_digest}' is not a hex digest — use only characters 0-9 and a-f")
    if len(hex_digest) != _HASH_ALGORITHMS[alg]:
        raise ValueError(f"{alg} expects {_HASH_ALGORITHMS[alg]} hex chars, got {len(hex_digest)}")

    return alg, hex_digest.lower()


class TrajectoryJudgeConfig(BaseModel):
    """Inline config for a judge-backed verification (kind=trajectory).

    Wire-compatible with the platform's `app.tasks.schemas.TrajectoryJudgeConfig`
    and the SDK CLI's `dn judge outcome` config model. Any field added
    one side must be added on the other.

    ``rubric`` is required for ``method: outcome_judge`` but optional for
    ``method: script_and_judge`` and ``method: flag_and_judge``, where the
    platform falls back to a default spirit/cheating rubric. The per-method
    rule is enforced by ``VerificationConfig._validate_method_rules``.
    """

    model_config = ConfigDict(extra="forbid")

    kind: Literal["trajectory"] = "trajectory"
    model: str = Field(min_length=1, description="Generator identifier for the judge.")
    rubric: str | None = Field(default=None, min_length=1, description="Inline rubric text.")
    max_steps: int = Field(default=50, ge=1, le=500)
    system_prompt: str | None = None
    model_params: dict[str, Any] = Field(default_factory=dict)
    task_context: dict[str, Any] = Field(default_factory=dict)


class VerificationConfig(BaseModel):
    """Verification configuration for task results.

    Accepts legacy keys ``flag_hash`` and ``submission_path`` as input aliases
    for ``hash`` and ``path`` so older task.yaml files keep validating.
    """

    model_config = ConfigDict(populate_by_name=True)

    script: str | None = Field(None, min_length=1, description="Verification script path")
    timeout: int = Field(30, description="Verification timeout in seconds")
    method: (
        Literal["script", "flag", "outcome_judge", "script_and_judge", "flag_and_judge"] | None
    ) = Field(None, description="Verification method")
    hash: str | None = Field(
        None,
        description="Flag hash (e.g. sha256:...). Mutually exclusive with value.",
        validation_alias=AliasChoices("hash", "flag_hash"),
    )
    value: str | None = Field(
        None,
        description="Plaintext expected value. Mutually exclusive with hash.",
    )
    path: str | None = Field(
        None,
        description="Path on the agent machine where the flag file is read from.",
        validation_alias=AliasChoices("path", "submission_path"),
    )
    where: Literal["agent", "environment"] = Field(
        "environment",
        description="Where the verification script runs (method: script only).",
    )
    judge: TrajectoryJudgeConfig | None = Field(
        None,
        description="Outcome-judge config (required when method is outcome_judge).",
    )

    @model_validator(mode="after")
    def _validate_method_rules(self) -> VerificationConfig:
        method = self.method
        if method is None:
            # Infer from presence of script/judge/flag-fields. Order matters:
            # script+judge → script_and_judge, judge+flag → flag_and_judge,
            # judge alone → outcome_judge, script alone → script.
            has_flag_fields = bool(self.path or self.hash or self.value)
            if self.judge is not None and self.script:
                method = "script_and_judge"
            elif self.judge is not None and has_flag_fields:
                method = "flag_and_judge"
            elif self.judge is not None:
                method = "outcome_judge"
            elif self.script:
                method = "script"
            else:
                raise ValueError(
                    "must specify 'method: flag', 'method: script', "
                    "'method: outcome_judge', 'method: script_and_judge', or "
                    "'method: flag_and_judge'. Use 'flag' to compare a file's "
                    "contents, 'script' to run a custom verifier, "
                    "'outcome_judge' to grade the agent's trajectory via an "
                    "LLM judge, or one of the combined forms to gate the "
                    "judge on a flag/script check first.",
                )

        if method == "outcome_judge":
            if self.judge is None:
                raise ValueError(
                    "'judge' is required when method is 'outcome_judge'. "
                    "Provide a trajectory-judge config with model + rubric.",
                )
            if self.judge.rubric is None:
                raise ValueError(
                    "'judge.rubric' is required when method is 'outcome_judge'. "
                    "Provide an inline rubric describing what the judge should "
                    "evaluate.",
                )
            conflicting = [
                name
                for name, val in (
                    ("hash", self.hash),
                    ("value", self.value),
                    ("path", self.path),
                    ("script", self.script),
                )
                if val
            ]
            if conflicting:
                raise ValueError(
                    f"'{conflicting[0]}' must not be set when method is "
                    f"'outcome_judge' (found: {', '.join(conflicting)})"
                )
            return self

        if method == "script_and_judge":
            if not self.script:
                raise ValueError(
                    "'script' is required when method is 'script_and_judge'. "
                    "Example: script: verify.sh",
                )
            if self.judge is None:
                raise ValueError(
                    "'judge' is required when method is 'script_and_judge'. "
                    "Provide a trajectory-judge config; 'judge.rubric' is "
                    "optional (the platform falls back to a default rubric).",
                )
            conflicting = [
                name
                for name, val in (
                    ("hash", self.hash),
                    ("value", self.value),
                    ("path", self.path),
                )
                if val
            ]
            if conflicting:
                raise ValueError(
                    f"'{conflicting[0]}' must not be set when method is "
                    f"'script_and_judge' (found: {', '.join(conflicting)})"
                )
            return self

        if method == "flag_and_judge":
            if self.judge is None:
                raise ValueError(
                    "'judge' is required when method is 'flag_and_judge'. "
                    "Provide a trajectory-judge config; 'judge.rubric' is "
                    "optional (the platform falls back to a default rubric).",
                )
            if self.script:
                raise ValueError(
                    "'script' must not be set when method is 'flag_and_judge' "
                    "— use 'script_and_judge' if a verify script is also needed.",
                )
            # Same flag rules as method=flag: exactly one of hash/value, path required.
            if self.hash and self.value:
                raise ValueError(
                    "'hash' and 'value' are mutually exclusive — specify exactly one. Use "
                    "'value' for a plaintext flag (e.g. value: \"FLAG{ok}\") or 'hash' for a "
                    "hashed flag (e.g. hash: sha256:...)",
                )
            if not self.hash and not self.value:
                raise ValueError(
                    "flag_and_judge verification requires either 'value' (plaintext) or "
                    "'hash' (hashed). Example: value: \"FLAG{example}\" — or — "
                    "hash: sha256:abc123...",
                )
            if not self.path:
                raise ValueError(
                    "'path' is required when method is 'flag_and_judge' — it's the file "
                    "the agent writes its answer to. Example: path: /tmp/result.txt",
                )
            if self.hash:
                try:
                    parse_flag_hash(self.hash)
                except ValueError as exc:
                    raise ValueError(f"invalid hash: {exc}") from exc
            return self

        if method == "script":
            if not self.script:
                raise ValueError(
                    "'script' is required when method is 'script'. Example: script: verify.sh",
                )
            if self.judge is not None:
                raise ValueError("'judge' must not be set when method is 'script'")
            return self

        # method == "flag"
        if self.judge is not None:
            raise ValueError("'judge' must not be set when method is 'flag'")
        if self.hash and self.value:
            raise ValueError(
                "'hash' and 'value' are mutually exclusive — specify exactly one. Use "
                "'value' for a plaintext flag (e.g. value: \"FLAG{ok}\") or 'hash' for a "
                "hashed flag (e.g. hash: sha256:...)",
            )
        if not self.hash and not self.value:
            raise ValueError(
                "flag verification requires either 'value' (plaintext) or 'hash' (hashed). "
                'Example: value: "FLAG{example}" — or — hash: sha256:abc123...',
            )
        if not self.path:
            raise ValueError(
                "'path' is required when method is 'flag' — it's the file the agent writes "
                "its answer to. Example: path: /tmp/result.txt",
            )
        if self.hash:
            try:
                parse_flag_hash(self.hash)
            except ValueError as exc:
                raise ValueError(f"invalid hash: {exc}") from exc
        return self


class ProvisionConfig(BaseModel):
    """Pre-agent provisioning script configuration."""

    script: str = Field(..., min_length=1, description="Provision script path")
    timeout: int = Field(120, description="Provision timeout in seconds")


class TeardownConfig(BaseModel):
    """Post-evaluation teardown script configuration."""

    script: str = Field(..., min_length=1, description="Teardown script path")
    timeout: int = Field(120, description="Teardown timeout in seconds")


class SolutionConfig(BaseModel):
    script: str = Field(..., min_length=1, description="Solution script path")


def _coerce_author(v: t.Any) -> t.Any:
    """Normalize author input to a flat name string.

    Spec allows ``author`` to be a string or an object with ``name``, ``email``,
    and ``url``. We flatten to the name to match the catalog model.
    """
    if v is None:
        return None
    if isinstance(v, dict):
        name = v.get("name")
        return str(name) if name is not None else None
    return str(v)


def _coerce_str(v: t.Any) -> str | None:
    """Coerce scalar values to strings (YAML parses bare ints like ``2022`` as int)."""
    if v is None:
        return None
    return str(v)


def _coerce_str_list(v: t.Any) -> list[str] | None:
    """Coerce list items to strings."""
    if v is None:
        return None
    if isinstance(v, list):
        return [str(item) for item in v]
    return v  # let pydantic reject non-list


class TaskYamlFields(BaseModel):
    """Fields extracted from task.yaml.

    The four fields ``name``, ``version``, ``instruction``, and
    ``verification`` are required. ``extra="allow"`` silently accepts
    dropped fields (``category``, ``author_email``) so older task.yaml
    files still validate as long as they have the required four.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(..., description="Task name (kebab-case)")
    version: str = Field(..., description="Task version (fixed semver MAJOR.MINOR.PATCH)")
    instruction: str = Field(..., min_length=1, description="Task instruction")
    verification: VerificationConfig = Field(..., description="Verification configuration")
    description: str | None = Field(
        None, description="Short human-readable summary for catalog display"
    )
    tags: t.Annotated[list[str] | None, BeforeValidator(_coerce_str_list)] = Field(
        None, description="Task tags"
    )
    difficulty: t.Annotated[str | None, BeforeValidator(_coerce_str)] = Field(
        None, description="Task difficulty level"
    )
    source: str | None = Field(None, description="Task source")
    author: t.Annotated[str | None, BeforeValidator(_coerce_author)] = Field(
        None,
        description="Task author name",
        validation_alias=AliasChoices("author", "author_name"),
    )
    license: str | None = Field(None, description="SPDX license identifier")
    repository: str | None = Field(None, description="Source repository URL")
    max_agent_timeout_sec: int | None = Field(None, description="Max agent timeout in seconds")
    ports: dict[str, list[int]] | None = Field(None, description="Port mappings by service name")
    provision: ProvisionConfig | None = Field(
        None, description="Pre-agent provisioning configuration"
    )
    teardown: TeardownConfig | None = Field(
        None, description="Post-evaluation teardown configuration"
    )
    solution: SolutionConfig | None = Field(None, description="Solution configuration")
    models: list[str] | None = Field(
        None,
        description=(
            "Platform model identifiers the task's environment needs inference "
            "access to. When present, the environment is provisioned with a "
            "scoped inference key + base URL enumerated to exactly these ids."
        ),
    )

    @field_validator("models")
    @classmethod
    def validate_models(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        seen: list[str] = []
        for entry in value:
            stripped = entry.strip()
            if not stripped:
                raise ValueError("models entries must be non-empty model identifiers")
            if any(ch.isspace() for ch in stripped):
                raise ValueError(f"models entry {entry!r} must not contain whitespace")
            if stripped not in seen:
                seen.append(stripped)
        if len(seen) > MAX_MODELS:
            raise ValueError(f"models may declare at most {MAX_MODELS} identifiers")
        return seen or None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not NAME_PATTERN.fullmatch(value):
            raise ValueError(
                f"{value!r} is not kebab-case. Use lowercase letters, digits, and hyphens, "
                "starting with a letter or digit. Example: 'sql-injection-lab-1'",
            )
        return value

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        if not valid_version(value):
            raise ValueError(
                f"{value!r} is not fixed semver. Use MAJOR.MINOR.PATCH, e.g. '0.1.0' or '1.2.3'",
            )
        return value


@dataclass
class ValidationIssue:
    level: Literal["error", "warning", "info"]
    component: str
    message: str


class TaskValidationError(Exception):
    """Raised when a task directory fails error-level validation before upload.

    Carries the offending error-level issues so callers can render them; the
    string form lists them so a bare ``str(exc)`` is already user-readable.
    """

    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        joined = "; ".join(f"{i.component}: {i.message}" for i in issues)
        super().__init__(f"task failed validation: {joined}")


def assert_task_directory_valid(
    task_dir: Path, *, root_dir: Path | None = None
) -> list[ValidationIssue]:
    """Validate *task_dir* and raise ``TaskValidationError`` on error-level issues.

    This is the gate the push/sync path runs so ``dn task validate`` predicts
    platform ingest: anything the SDK marks ``error`` would also be rejected by
    the API at upload, so we block locally first. Warnings and infos are
    returned (not raised) for the caller to surface.
    """
    issues = validate_task_directory(task_dir, root_dir=root_dir)
    errors = [issue for issue in issues if issue.level == "error"]
    if errors:
        raise TaskValidationError(errors)
    return [issue for issue in issues if issue.level != "error"]


def _collect_known_keys(
    model: type[BaseModel],
) -> tuple[frozenset[str], dict[str, tuple[str, ...]]]:
    """Return (all known keys, {canonical field → extra aliases})."""
    keys: set[str] = set()
    field_aliases: dict[str, tuple[str, ...]] = {}
    for name, info in model.model_fields.items():
        keys.add(name)
        aliases: list[str] = []
        alias = info.validation_alias
        if isinstance(alias, str):
            aliases.append(alias)
        elif isinstance(alias, AliasChoices):
            for choice in alias.choices:
                if isinstance(choice, str):
                    aliases.append(choice)
        for a in aliases:
            keys.add(a)
        extras = tuple(a for a in aliases if a != name)
        if extras:
            field_aliases[name] = extras
    return frozenset(keys), field_aliases


_KNOWN_TASK_KEYS, _FIELD_ALIASES = _collect_known_keys(TaskYamlFields)

# Best-practice metadata nudges: absence doesn't block validation but surfaces
# fields that improve catalog discoverability, provenance, and regression
# coverage. Warnings are things we really think every task should have; info
# items are nice-to-haves that aid filtering and attribution.
_BEST_PRACTICE_WARN: tuple[tuple[str, str], ...] = (
    ("description", "helps catalog/browse discoverability"),
    ("source", "records where the task came from"),
    ("solution", "enables smoke-test regression signal (solution.script)"),
)
_BEST_PRACTICE_INFO: tuple[tuple[str, str], ...] = (
    ("tags", "improves filterability in the catalog"),
    ("difficulty", "improves filterability in the catalog"),
    ("author", "attribution / provenance"),
    ("license", "SPDX identifier for redistribution"),
)

# Roots that are world-writable on virtually every Linux image and don't
# depend on the agent container's filesystem layout or cwd. Anything under
# these is considered safe for `verification.path` (the file the agent writes
# its flag to).
_SAFE_FLAG_PATH_ROOTS: tuple[str, ...] = (
    "/tmp/",  # noqa: S108 — documented safe root
    "/var/tmp/",  # noqa: S108 — documented safe root
    "/dev/shm/",  # noqa: S108 — documented safe root
)

# Split at source level so the repo's local-machine-path linter doesn't trip
# on our own detection constants. At runtime these equal the full prefix.
_HOME_PREFIX = "/home" + "/"
_USERS_PREFIX = "/Users" + "/"


def _unsafe_flag_path_reason(path: str) -> str | None:
    """Return a human reason if `path` is a risky flag output path, else None.

    The flag path is written by the agent from an unprivileged context, so it
    must live somewhere that (a) exists on a standard Linux image and (b) is
    writable without elevated permissions. Known-safe roots are `/tmp/`,
    `/var/tmp/`, and `/dev/shm/`. Anything else — `/app/` (image-specific,
    often read-only), per-account `/home` or `/Users` subdirectories,
    `/root/` (privileged) — is flagged so task authors catch it before their
    agents hit a permission error mid-run.
    """
    if not isinstance(path, str) or not path:
        return None
    # Cheap prefix match — safe roots win outright.
    for safe in _SAFE_FLAG_PATH_ROOTS:
        if path == safe.rstrip("/") or path.startswith(safe):
            return None
    # Specific known-bad prefixes get a tailored explanation.
    if path.startswith("/app/") or path == "/app":
        return (
            "'/app/' is image-specific and often read-only or missing — agents "
            "frequently can't write there. Use /tmp/ instead"
        )
    if path.startswith((_HOME_PREFIX, _USERS_PREFIX)):
        return (
            f"{path!r} references a user-specific directory that isn't "
            "guaranteed to exist in the agent's container. Use /tmp/ instead"
        )
    if path.startswith("/root/") or path == "/root":
        return (
            "'/root/' is only writable when the agent runs as root, which "
            "isn't guaranteed. Use /tmp/ instead"
        )
    # Relative paths are ambiguous — they depend on the agent's cwd.
    if not path.startswith("/"):
        return (
            f"{path!r} is a relative path; the agent's working directory "
            "isn't guaranteed. Use an absolute path under /tmp/"
        )
    # Generic catch-all for other absolute paths outside the safe roots.
    return (
        f"{path!r} isn't under a standard world-writable root "
        f"({', '.join(r.rstrip('/') for r in _SAFE_FLAG_PATH_ROOTS)}). "
        "Use /tmp/ unless you've verified the agent can write there"
    )


def _extract_flag_verification_path(raw: dict[str, t.Any]) -> str | None:
    """Return verification.path when the method writes a flag file, else None.

    Covers both ``method: flag`` and ``method: flag_and_judge``, since both
    have the agent write to a caller-controlled path. Handles the legacy
    ``submission_path`` alias.
    """
    verification = raw.get("verification")
    if not isinstance(verification, dict):
        return None
    method = verification.get("method")
    # method may be omitted — downstream schema validation catches that.
    # Infer a flag-writing method when hash/value is present (matches
    # VerificationConfig inference).
    if method not in ("flag", "flag_and_judge", None):
        return None
    if method is None and not any(k in verification for k in ("hash", "value")):
        return None
    for key in ("path", "submission_path"):
        value = verification.get(key)
        if isinstance(value, str) and value:
            return value
    return None


# ---------------------------------------------------------------------------
# Schema error formatting
# ---------------------------------------------------------------------------
#
# pydantic's default `str(ValidationError)` dumps `input_value=...`, links to
# pydantic.dev, and glues all errors into a single multi-line blob. That's
# unusable as a CLI error surface. `_format_schema_error` walks the error
# list and produces one `ValidationIssue` per error with:
#
#   - a `component` derived from the first element of the error location
#     (`task.yaml`, `verification`, `ports`, ...), matching the existing
#     output convention used by the downstream rules.
#   - a curated user-facing `message` that tells the author what to put in
#     the file, not what pydantic thought the input was.

# Top-level required fields get curated examples in the "field is required"
# message so the user sees a concrete shape for each one.
_REQUIRED_FIELD_EXAMPLES: dict[str, str] = {
    "name": "name: my-task",
    "version": "version: 0.1.0",
    "instruction": 'instruction: "Solve the challenge and write the flag to /tmp/result.txt"',
    "verification": (
        'verification:\n  method: flag\n  path: /tmp/result.txt\n  value: "FLAG{example}"'
    ),
}


def _format_location(loc: tuple[t.Any, ...]) -> str:
    """Format a pydantic error location tuple into a human-readable dotted path."""
    parts: list[str] = []
    for elem in loc:
        if isinstance(elem, int):
            parts.append(f"[{elem}]")
        else:
            parts.append(str(elem))
    # Join: a.b.c but [0].x for list indices
    out = ""
    for i, p in enumerate(parts):
        if p.startswith("["):
            out += p
        elif i == 0:
            out = p
        else:
            out += f".{p}"
    return out


def _component_for_loc(loc: tuple[t.Any, ...]) -> str:
    """Pick a user-facing component label for a pydantic error location.

    First-level locations map to friendly surface names; anything else falls
    back to ``task.yaml`` so the message itself carries the field path.
    """
    if not loc:
        return "task.yaml"
    first = loc[0]
    if isinstance(first, str):
        return first
    return "task.yaml"


def _format_schema_error(exc: ValidationError) -> list[ValidationIssue]:
    """Convert a pydantic ``ValidationError`` into a list of curated issues.

    One ``ValidationIssue`` is emitted per pydantic error. Built-in error
    types (``missing``, ``string_type``, ``literal_error``, …) are rewritten
    into user-facing messages; ``ValueError`` messages raised by our own
    validators are passed through verbatim since they're already curated.
    """
    out: list[ValidationIssue] = []
    for err in exc.errors():
        loc = err.get("loc", ())
        err_type = err.get("type", "")
        msg = err.get("msg", "")
        component = _component_for_loc(loc)

        # Drop the component prefix from the field path so we don't emit
        # `name: name is required`. The component is the first loc element
        # and already appears on the issue, so subpaths like `verification.hash`
        # collapse to `hash` under the `verification` component.
        subpath = _format_location(loc[1:]) if len(loc) > 1 and isinstance(loc[0], str) else ""
        prefix = f"{subpath}: " if subpath else ""

        # Our own validators raise ValueError → pydantic tags them
        # `value_error` and prefixes the msg with `Value error, `. Those
        # messages are already curated; pass through unchanged.
        if err_type == "value_error":
            clean = msg.removeprefix("Value error, ")
            out.append(ValidationIssue("error", component, f"{prefix}{clean}"))
            continue

        if err_type == "missing":
            if len(loc) == 1 and isinstance(loc[0], str):
                example = _REQUIRED_FIELD_EXAMPLES.get(loc[0])
                if example:
                    out.append(
                        ValidationIssue("error", component, f"required. Example:\n{example}")
                    )
                    continue
            out.append(ValidationIssue("error", component, f"{prefix}required"))
            continue

        if err_type in ("string_type", "str_type"):
            out.append(
                ValidationIssue(
                    "error",
                    component,
                    f"{prefix}must be a string — wrap it in quotes if it looks like a number",
                )
            )
            continue

        if err_type in ("int_type", "int_parsing"):
            out.append(ValidationIssue("error", component, f"{prefix}must be an integer"))
            continue

        if err_type == "list_type":
            out.append(ValidationIssue("error", component, f"{prefix}must be a list"))
            continue

        if err_type in ("dict_type", "model_type"):
            out.append(ValidationIssue("error", component, f"{prefix}must be a mapping"))
            continue

        if err_type == "literal_error":
            ctx = err.get("ctx") or {}
            expected = ctx.get("expected", "")
            body = f"must be one of {expected}" if expected else msg
            out.append(ValidationIssue("error", component, f"{prefix}{body}"))
            continue

        if err_type == "string_too_short":
            out.append(ValidationIssue("error", component, f"{prefix}must not be empty"))
            continue

        if err_type == "extra_forbidden":
            out.append(ValidationIssue("error", component, f"{prefix}is not a recognized field"))
            continue

        # Fallback: use the pydantic-provided message, prefixed by the
        # subpath if any so the user can locate it.
        out.append(ValidationIssue("error", component, f"{prefix}{msg}"))

    return out


# ---------------------------------------------------------------------------
# Lenient raw-dict view
# ---------------------------------------------------------------------------
#
# Downstream rules (compose presence, script existence, port cross-checks,
# hardcoded URL detection, ...) need a handful of values from task.yaml but
# do not benefit from full schema validation. Working directly off ``raw``
# with defensive lookups lets them run even when `TaskYamlFields.model_validate`
# failed — so a migrating user sees all structural problems in one pass
# instead of fixing the schema, re-running, fixing the structure, re-running,
# and so on.


def _raw_str(raw: dict[str, t.Any], key: str) -> str | None:
    value = raw.get(key)
    return value if isinstance(value, str) else None


def _raw_dict(raw: dict[str, t.Any], key: str) -> dict[str, t.Any]:
    value = raw.get(key)
    return value if isinstance(value, dict) else {}


def _raw_ports(raw: dict[str, t.Any]) -> dict[str, list[int]]:
    """Pull ports mapping out of raw, discarding any malformed entries."""
    ports = raw.get("ports")
    if not isinstance(ports, dict):
        return {}
    result: dict[str, list[int]] = {}
    for svc, entries in ports.items():
        if not isinstance(svc, str) or not isinstance(entries, list):
            continue
        ints = [e for e in entries if isinstance(e, int)]
        if ints:
            result[svc] = ints
    return result


def _raw_nested_script(raw: dict[str, t.Any], key: str) -> str | None:
    """Pull a nested ``{key: {script: <str>}}`` path from raw."""
    nested = _raw_dict(raw, key)
    script = nested.get("script")
    return script if isinstance(script, str) and script else None


def discover_task_directories(root: Path) -> tuple[list[Path], list[tuple[Path, Path]]]:
    """Recursively discover task directories under *root*.

    A directory is a task if it contains ``task.yaml``.  Once a task directory
    is found we do **not** descend into it — a task cannot contain other tasks.
    If that situation is detected (a ``task.yaml`` exists inside another task
    directory) it is reported as a conflict.

    Returns:
        ``(task_dirs, conflicts)`` where *conflicts* is a list of
        ``(parent_task_dir, nested_task_dir)`` pairs.
    """
    import os
    from pathlib import Path

    task_dirs: list[Path] = []
    conflicts: list[tuple[Path, Path]] = []
    task_dir_set: set[str] = set()  # resolved string paths for fast prefix check

    root_str = str(root.resolve())

    for dirpath, dirnames, filenames in os.walk(root_str):
        # Skip hidden directories
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))

        if "task.yaml" not in filenames:
            continue

        dir_path = Path(dirpath)

        # Check if nested inside an already-found task directory
        nested = False
        for ancestor in task_dir_set:
            if dirpath.startswith(ancestor + os.sep):
                conflicts.append((Path(ancestor), dir_path))
                nested = True
                break

        if nested:
            continue

        task_dirs.append(dir_path)
        task_dir_set.add(dirpath)

        # Don't descend into task directories
        dirnames.clear()

    return task_dirs, conflicts


# ---------------------------------------------------------------------------
# Compose helpers
# ---------------------------------------------------------------------------

# Matches compose port strings like "8080:8080", "3000", "8080:8080/tcp",
# "127.0.0.1:8080:8080", or long-form with target/published.
_PORT_RE = re.compile(
    r"""
    ^                  # anchor to start of string
    (?:[\d.]+:)?       # optional host IP
    (?:\d+:)?          # optional host port
    (\d+)              # container port (the one we care about)
    (?:/\w+)?          # optional protocol
    $                  # anchor to end of string
    """,
    re.VERBOSE,
)


def _extract_compose_ports(
    service_config: dict[str, t.Any],
) -> tuple[set[int], list[str]]:
    """Extract container ports from a compose service definition.

    Returns:
        A tuple of (parsed_ports, unparseable_entries) where *unparseable_entries*
        contains string representations of port entries that could not be parsed.
    """
    ports: set[int] = set()
    unparseable: list[str] = []
    raw_ports = service_config.get("ports")
    if not raw_ports or not isinstance(raw_ports, list):
        return ports, unparseable

    for entry in raw_ports:
        if isinstance(entry, int):
            ports.add(entry)
        elif isinstance(entry, str):
            m = _PORT_RE.match(entry)
            if m:
                ports.add(int(m.group(1)))
            else:
                unparseable.append(entry)
        elif isinstance(entry, dict):
            # Long-form: {target: 8080, published: 8080}
            target = entry.get("target")
            if isinstance(target, int):
                ports.add(target)
            else:
                unparseable.append(str(entry))
        else:
            unparseable.append(str(entry))
    return ports, unparseable


def _extract_build_dockerfile(service_config: dict[str, t.Any]) -> str | None:
    """Return the Dockerfile path referenced by a compose build config, or None."""
    build = service_config.get("build")
    if build is None:
        return None
    if isinstance(build, str):
        # Short form: build: ./dir — uses default Dockerfile
        return "Dockerfile"
    if isinstance(build, dict):
        if build.get("dockerfile_inline"):
            return None  # inline, no file to check
        return build.get("dockerfile", "Dockerfile")
    return None


# ---------------------------------------------------------------------------
# Template variable helpers
# ---------------------------------------------------------------------------

_TEMPLATE_VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")

# Captures host (group 1) for any http(s) URL not preceded by ``{`` (template
# substitutions look like ``{{var}}``). Stops the host at ``:`` or ``/``.
_URL_HOST_RE = re.compile(r"(?<!\{)\bhttps?://([^\s/:]+)")

# TSK-PORT-003 / TSK-INST-002: any of these hostnames in the instruction
# implies a hardcoded compose service URL when the task declares ``ports``.
_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "host.docker.internal"})


def _extract_template_vars(instruction: str) -> set[str]:
    """Extract ``{{var_name}}`` template variables from an instruction string."""
    return set(_TEMPLATE_VAR_RE.findall(instruction))


def _extract_url_hosts(instruction: str) -> list[tuple[str, str]]:
    """Extract ``(full_url, hostname)`` tuples from an instruction string.

    Skips URLs preceded by ``{`` so template substitutions like
    ``{{challenge_url}}`` are not matched as literal hosts.
    """
    return [(m.group(0), m.group(1)) for m in _URL_HOST_RE.finditer(instruction)]


def _ports_to_expected_vars(ports: dict[str, list[int]]) -> set[str]:
    """Build the set of template variable names that ports should provide.

    Convention: ``{{service_url}}``, ``{{service_url_PORT}}``,
    ``{{service_host}}``, ``{{service_port}}``.
    """
    names: set[str] = set()
    for service, port_list in ports.items():
        names.add(f"{service}_url")
        names.add(f"{service}_host")
        names.add(f"{service}_port")
        for port in port_list:
            names.add(f"{service}_url_{port}")
    return names


def _find_compose_file(task_dir: Path) -> Path | None:
    """Locate ``docker-compose.yaml``/``.yml`` at the task root only."""
    candidates = ("docker-compose.yaml", "docker-compose.yml")
    for name in candidates:
        candidate = task_dir / name
        if candidate.is_file():
            return candidate
    return None


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------


def validate_task_directory(
    task_dir: Path, *, root_dir: Path | None = None
) -> list[ValidationIssue]:
    """Validate a task directory, returning a list of issues found.

    Enforces every mechanically-testable rule from the task contract spec
    (``specs/tasks/contract.md``).

    Schema validation (required fields, name regex, semver, hash format,
    flag-method rules) runs first and produces per-field issues via
    ``_format_schema_error``. Structural rules (compose discovery, port
    cross-checks, build contexts, script existence, hardcoded URLs, client
    service) run afterwards regardless of whether schema validation
    succeeded, operating directly on the parsed YAML dict so the author
    sees every problem in a single pass.

    Args:
        task_dir: Path to the task directory.
        root_dir: Root directory of the tasks tree. Build contexts that
            escape the task directory but remain within *root_dir* are
            considered valid (shared infrastructure pattern).
    """
    issues: list[ValidationIssue] = []

    task_yaml_path = task_dir / "task.yaml"
    if not task_yaml_path.is_file():
        issues.append(ValidationIssue("error", "task.yaml", "file not found"))
        return issues

    try:
        raw = yaml.safe_load(task_yaml_path.read_text())
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue("error", "task.yaml", f"could not parse YAML: {exc}"))
        return issues

    if not isinstance(raw, dict):
        issues.append(
            ValidationIssue("error", "task.yaml", "must contain a YAML mapping at the top level")
        )
        return issues

    # --- Schema validation: per-field issues, never early-return -----------
    try:
        TaskYamlFields.model_validate(raw)
    except ValidationError as exc:
        issues.extend(_format_schema_error(exc))

    # --- Info: unrecognized top-level keys (silently ignored) -------------
    unknown_keys = sorted(str(k) for k in raw if str(k) not in _KNOWN_TASK_KEYS)
    if unknown_keys:
        for key in unknown_keys:
            issues.append(ValidationIssue("info", key, "not recognized - will be ignored"))

    # --- Best-practice nudges for optional metadata -----------------------
    # These don't block validation but surface fields that improve catalog
    # discoverability, provenance, and regression coverage.
    def _raw_has(key: str) -> bool:
        # Also accept legacy validation aliases (e.g. author_name → author).
        aliases = _FIELD_ALIASES.get(key, ())
        return any(raw.get(candidate) not in (None, "", [], {}) for candidate in (key, *aliases))

    for field, reason in _BEST_PRACTICE_WARN:
        if not _raw_has(field):
            issues.append(ValidationIssue("warning", field, f"not set — {reason}"))
    for field, reason in _BEST_PRACTICE_INFO:
        if not _raw_has(field):
            issues.append(ValidationIssue("info", field, f"not set — {reason}"))

    # --- Flag path sanity: warn on paths the agent likely can't write -----
    flag_path = _extract_flag_verification_path(raw)
    if flag_path is not None:
        reason = _unsafe_flag_path_reason(flag_path)
        if reason is not None:
            issues.append(ValidationIssue("warning", "verification.path", reason))

    # --- Compose discovery + parse ----------------------------------------
    declared_ports = _raw_ports(raw)
    compose_path = _find_compose_file(task_dir)
    compose_services: dict[str, t.Any] = {}

    if compose_path is None:
        if declared_ports:
            issues.append(
                ValidationIssue(
                    "error",
                    "compose",
                    "docker-compose.yaml is required when task.yaml declares 'ports'",
                )
            )
    else:
        try:
            compose = yaml.safe_load(compose_path.read_text())
        except yaml.YAMLError as exc:
            issues.append(ValidationIssue("error", "compose", f"could not parse YAML: {exc}"))
            compose = None

        if compose is not None:
            if not isinstance(compose, dict):
                issues.append(
                    ValidationIssue(
                        "error",
                        "compose",
                        "docker-compose.yaml must be a YAML mapping with a top-level "
                        "'services:' block",
                    )
                )
            else:
                services = compose.get("services")
                if services is None:
                    issues.append(
                        ValidationIssue(
                            "error",
                            "compose",
                            "docker-compose.yaml is missing the required 'services:' block",
                        )
                    )
                elif not isinstance(services, dict):
                    issues.append(
                        ValidationIssue(
                            "error", "compose", "'services' must be a mapping of service names"
                        )
                    )
                else:
                    compose_services = services

    # --- Vestigial 'client' service (warning, not error) ------------------
    # Tasks ported from terminal-bench style harnesses often carry a `client`
    # service that used to host the agent. The platform runs agents in a
    # separate runtime sandbox, so the client container is dead weight but
    # does not break anything — warn rather than block.
    if "client" in compose_services:
        issues.append(
            ValidationIssue(
                "warning",
                "compose",
                "the 'client' service in docker-compose.yaml is unused — the agent runs in "
                "a separate runtime sandbox, so a client container is never started. Remove "
                "it to avoid wasted resources",
            )
        )

    # --- Ports cross-validation -------------------------------------------
    if declared_ports and compose_services:
        for service_name, ports in declared_ports.items():
            if service_name not in compose_services:
                issues.append(
                    ValidationIssue(
                        "error",
                        "ports",
                        f"service '{service_name}' is declared in task.yaml but not found "
                        "in docker-compose.yaml. Either add it to compose or remove the "
                        "entry from task.yaml",
                    )
                )
                continue
            exposed, unparseable = _extract_compose_ports(compose_services[service_name])
            for entry in unparseable:
                issues.append(
                    ValidationIssue(
                        "warning",
                        "ports",
                        f"service '{service_name}' has unparseable port entry: {entry}",
                    )
                )
            for port in ports:
                if exposed and port not in exposed:
                    issues.append(
                        ValidationIssue(
                            "error",
                            "ports",
                            f"port {port} is declared for service '{service_name}' but the "
                            f"compose service only exposes {sorted(exposed)}. Update one to "
                            "match the other",
                        )
                    )

    # --- Warn on compose services exposing undeclared ports ---------------
    declared_service_names = set(declared_ports.keys())
    for svc_name, svc_config in compose_services.items():
        if not isinstance(svc_config, dict):
            continue
        exposed, unparseable = _extract_compose_ports(svc_config)
        for entry in unparseable:
            issues.append(
                ValidationIssue(
                    "warning",
                    "ports",
                    f"service '{svc_name}' has unparseable port entry: {entry}",
                )
            )
        if exposed and svc_name not in declared_service_names:
            issues.append(
                ValidationIssue(
                    "warning",
                    "ports",
                    f"service '{svc_name}' exposes {sorted(exposed)} in docker-compose.yaml "
                    "but is not listed in task.yaml 'ports'. Declare it so agents get a "
                    "template variable for the URL",
                )
            )

    # --- Build contexts + Dockerfile resolution ---------------------------
    resolved_task = task_dir.resolve()
    resolved_root = root_dir.resolve() if root_dir else resolved_task
    for svc_name, svc_config in compose_services.items():
        if not isinstance(svc_config, dict):
            continue
        dockerfile = _extract_build_dockerfile(svc_config)
        if dockerfile is None:
            continue
        build = svc_config.get("build", {})
        if isinstance(build, str):
            context = build
        elif isinstance(build, dict):
            context = build.get("context", ".")
        else:
            context = "."
        dockerfile_path = (task_dir / context / dockerfile).resolve()
        try:
            dockerfile_path.relative_to(resolved_task)
        except ValueError:
            try:
                dockerfile_path.relative_to(resolved_root)
            except ValueError:
                issues.append(
                    ValidationIssue(
                        "error",
                        "dockerfile",
                        f"service '{svc_name}' build context escapes the task directory "
                        f"(resolves to {dockerfile_path}). Move the Dockerfile under the "
                        "task directory or into the tasks root",
                    )
                )
                continue
        if not dockerfile_path.is_file():
            try:
                rel = dockerfile_path.relative_to(resolved_task)
            except ValueError:
                rel = dockerfile_path.relative_to(resolved_root)
            issues.append(
                ValidationIssue(
                    "error",
                    "dockerfile",
                    f"service '{svc_name}' references '{dockerfile}' but the file was not "
                    f"found (looked at {rel})",
                )
            )

    # --- Hardcoded compose URLs in instruction ----------------------------
    # Only flags URLs whose host resolves to a compose service or loopback
    # when ``ports`` is declared. External lab URLs pass through untouched.
    instruction = _raw_str(raw, "instruction") or ""
    if declared_ports and instruction:
        port_service_names = set(declared_ports.keys())
        for url, host in _extract_url_hosts(instruction):
            if host in port_service_names or host in _LOOPBACK_HOSTS:
                var = host if host in port_service_names else "challenge"
                issues.append(
                    ValidationIssue(
                        "error",
                        "instruction",
                        f"instruction hardcodes '{url}'. Use the template variable "
                        f"'{{{{{var}_url}}}}' instead — the platform substitutes it per "
                        "attempt",
                    )
                )

    # --- Referenced scripts must exist ------------------------------------
    verify_script = _raw_nested_script(raw, "verification")
    if verify_script and not (task_dir / verify_script).is_file():
        issues.append(
            ValidationIssue(
                "error",
                "verification",
                f"script '{verify_script}' was not found in the task directory — create it "
                "or update the reference",
            )
        )

    solution_script = _raw_nested_script(raw, "solution")
    if solution_script and not (task_dir / solution_script).is_file():
        issues.append(
            ValidationIssue(
                "error",
                "solution",
                f"script '{solution_script}' was not found in the task directory — create it "
                "or update the reference",
            )
        )

    provision_script = _raw_nested_script(raw, "provision")
    if provision_script and not (task_dir / provision_script).is_file():
        issues.append(
            ValidationIssue(
                "error",
                "provision",
                f"script '{provision_script}' was not found in the task directory — create "
                "it or update the reference",
            )
        )

    teardown_script = _raw_nested_script(raw, "teardown")
    if teardown_script and not (task_dir / teardown_script).is_file():
        issues.append(
            ValidationIssue(
                "error",
                "teardown",
                f"script '{teardown_script}' was not found in the task directory — create "
                "it or update the reference",
            )
        )

    return issues
