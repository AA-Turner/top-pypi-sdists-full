"""Typed data structures for the local CI job runner."""

from dataclasses import dataclass, field


@dataclass
class CiVariable:
    """A single CI/CD variable with its provenance.

    ``source`` is a short label (``predefined``, ``yaml-global``, ``yaml-job``,
    ``group:<path>``, ``project``, ``cli``) used for inspection. The value is
    held here but never printed by the inspection paths — only the key/source.
    """

    key: str
    value: str
    source: str
    environment_scope: str = "*"
    masked: bool = False
    protected: bool = False
    raw: bool = False


@dataclass
class EnvResult:
    """The fully resolved environment for a job.

    ``env`` is the final flat mapping (after precedence + ``$VAR`` expansion).
    ``provenance`` keeps, per final key, the source label of the winning
    definition — for inspection without leaking values.
    """

    env: dict[str, str] = field(default_factory=dict)
    provenance: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ResolvedJob:
    """A CI job after resolving ``extends``, ``default``, and ``!reference``."""

    name: str
    stage: str = "test"
    image: str = ""
    image_entrypoint: list[str] | None = None
    before_script: list[str] = field(default_factory=list)
    script: list[str] = field(default_factory=list)
    after_script: list[str] = field(default_factory=list)
    # YAML-declared variables (global merged with job-level), pre-expansion.
    variables: dict[str, str] = field(default_factory=dict)
    needs: list[str] = field(default_factory=list)
    # ``None`` means no explicit ``dependencies:`` key (fall back to needs).
    dependencies: list[str] | None = None
    services: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class RunResult:
    """Outcome of a local run, serialised to JSON on stdout."""

    job: str
    backend: str
    image: str = ""
    script_path: str = ""
    env_path: str = ""
    exit_code: int = 0
    downloaded_artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    generated_only: bool = False
