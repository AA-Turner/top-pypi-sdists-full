from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING

from . import config, dockerfile

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mistralai.vibe_agents.sdk.authoring.connector_selection import AllConnectors
    from mistralai.vibe_agents.sdk.authoring.contracts import Harness
    from mistralai.vibe_agents.sdk.authoring.subagent import Subagent
    from mistralai.workflows.plugins.mistralai.connectors.decorator import ConnectorSlot

    from .loader import AgentApp

# A mounted service-account token authenticates a worker just as an API key does, and is what a
# managed deployment gets instead of one; the Workflows auth factory already prefers it. Requiring a
# key here would reject the very workers the platform runs.
_CREDENTIAL_VARS = ("MISTRAL_API_KEY", "PROD_MISTRAL_API_KEY", "MISTRAL_SA_TOKEN_PATH")
DEFAULT_DOCKERFILE = "Dockerfile"
# MistralSandbox imports koyeb-sdk only when a session creates its first sandbox, so without this check
# a worker missing the extra starts, registers and fails every session instead of refusing to start.
_KOYEB_EXTRA = "mistralai-agents[koyeb]"
_MISSING_KOYEB_EXTRA = "This agent uses MistralSandbox, which needs the koyeb extra"


class PreflightError(Exception):
    """Raised when the environment or the project cannot run the command; one line per issue."""

    def __init__(self, issues: list[str]) -> None:
        super().__init__("; ".join(issues))
        self.issues = issues


def worker_config_issues(env: Mapping[str, str] | None = None) -> list[str]:
    # Friendly, actionable pre-flight for `agents serve`. Returns one line per missing requirement so
    # the CLI can print them and stop BEFORE run_worker raises a raw ValueError / exits the process.
    source = os.environ if env is None else env
    issues: list[str] = []
    if not any(source.get(name, "").strip() for name in _CREDENTIAL_VARS):
        # The CLI does not read .env itself: `uv run --env-file .env` loads it, as every docs example does.
        issues.append(
            "MISTRAL_API_KEY is not set. Export it in your shell, or put it in .env and run the command with "
            "`uv run --env-file .env`."
        )
    # DEPLOYMENT_NAME is intentionally NOT required: when it is unset, the control plane chooses the task
    # queue at registration, and serve shows it in the banner.
    return issues


def sandbox_config_issues(harness: Harness) -> list[str]:
    # The sandbox is created by the first session's activity; without this check a worker missing its
    # sandbox credentials starts, registers, and then fails every session.
    from mistralai.vibe_agents.sdk.authoring.contracts import MistralSandbox  # noqa: PLC0415

    if not isinstance(harness.sandbox, MistralSandbox):
        return []
    if config.KoyebSandboxRuntimeSettings().has_credential():
        return []
    return [
        "The agent uses a MistralSandbox but the worker has no credential to create it with. Set "
        "MISTRAL_API_KEY, or AGENTS_SDK_KOYEB_SANDBOX_API_TOKEN (or KOYEB_API_KEY) for a Koyeb organization."
    ]


def worker_secret_issues(harness: Harness, env: Mapping[str, str] | None = None) -> list[str]:
    """Name each ``worker_env`` secret that the worker environment does not set.

    A deployed worker gets them from the platform at boot; ``agents serve`` takes them from the shell.
    """
    from mistralai.vibe_agents.sdk.authoring.secrets import MistralSecret  # noqa: PLC0415

    values = os.environ if env is None else env
    return [
        f"Secret {name} has worker_env=True but the worker environment does not set {name}. "
        "Export it in your shell, or put it in .env and start the worker with `uv run --env-file .env`."
        for name, origin in harness.secrets.items()
        if isinstance(origin, MistralSecret) and origin.worker_env and not values.get(name, "").strip()
    ]


def connector_issues(harness: Harness, subagents: Sequence[Subagent] = ()) -> list[str]:
    """The connector declarations a Session would refuse to start with, the root's and each Subagent's.

    For example ``all_connectors()`` beside a ``run_as="deployment"`` connector, or one connector twice.
    Assembly applies these rules only when a Session starts; checking them here turns that failure
    into one ``agents info`` and ``agents serve`` report up front. A Subagent that leaves
    ``connectors`` unset inherits its parent's, already checked.
    """
    from mistralai.vibe_agents.sdk.assembly import assemble  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.assembly.subagents import authored_subagent_layers  # noqa: PLC0415

    layers: list[tuple[tuple[str, ...], Sequence[ConnectorSlot], AllConnectors | None]] = [
        ((), harness.connectors, harness.connector_discovery)
    ]
    layers.extend(
        (path, layer.connectors, layer.connector_discovery)
        for path, layer in authored_subagent_layers(subagents)
        if layer.connectors is not None
    )
    issues: list[str] = []
    for path, slots, discovery in layers:
        try:
            assemble._build_connector_configuration(tuple(slots), discovery)
        except ValueError as exc:
            issues.append(f"In subagent {'/'.join(path)!r}: {exc}" if path else str(exc))
    return issues


def mcp_credential_issues(harness: Harness, subagents: Sequence[Subagent] = ()) -> list[str]:
    """Name each RemoteMCP credential variable that the worker cannot send.

    The worker reads these variables when a Session lists the source's tools, by the same rule as
    this check; an unusable one there drops the source behind a notice only the model sees, so the
    worker refuses to start instead. A Subagent that leaves ``mcps`` unset inherits its parent's
    sources, already checked.
    """
    from mistralai.vibe.harness.runtime.capabilities.mcp_credentials import HeaderCredentialProblem  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.assembly.mcp import credential_problems  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.assembly.subagents import authored_mcp_layers  # noqa: PLC0415

    # A managed worker gets its variables only from secret bindings, so the fix is a redeploy.
    fix = (
        "Bind each with `agents deploy --secret-binding NAME=secret:workspace:SECRET`, then deploy again."
        if config.is_managed_worker()
        else "Export each in your shell, or put it in .env and start the worker with `uv run --env-file .env`."
    )
    issues: list[str] = []
    for path, mcps in authored_mcp_layers(harness.mcps, subagents):
        where = f" in subagent {'/'.join(path)!r}" if path else ""
        for name, problems in sorted(credential_problems(mcps).items()):
            if unset := problems.get(HeaderCredentialProblem.UNSET):
                verb = "is" if len(unset) == 1 else "are"
                issues.append(
                    f"MCP server {name!r}{where} reads its auth headers from {', '.join(unset)}, which {verb} not "
                    f"set in the worker environment. {fix}"
                )
            if illegal := problems.get(HeaderCredentialProblem.ILLEGAL):
                # Named, never quoted: the value is a credential.
                issues.append(
                    f"MCP server {name!r}{where} reads its auth headers from {', '.join(illegal)}, which holds a "
                    "character a header cannot carry, such as a newline inside the value. Set it to the header "
                    "value on one line."
                )
    return issues


def require_worker_sandbox_config(harness: Harness) -> None:
    """Raise PreflightError if the worker environment cannot create the harness's sandbox."""
    issues = sandbox_config_issues(harness)
    if issues:
        raise PreflightError(issues)


def load_worker_app(path: Path) -> AgentApp:
    """Check the worker environment, then load the project's agent.

    Raises PreflightError for a missing requirement and AgentProjectError for an invalid project.
    """
    from . import loader  # noqa: PLC0415

    issues = worker_config_issues()
    if issues:
        raise PreflightError(issues)
    app = loader.load_app(path)
    issues = sandbox_dependency_issues(app)
    if issues:
        raise PreflightError(issues)
    harness = app.agent._resolve_harness(app.harness)
    require_worker_sandbox_config(harness)
    issues = [
        *connector_issues(harness, app.agent.subagents),
        *worker_secret_issues(harness),
        *mcp_credential_issues(harness, app.agent.subagents),
    ]
    if issues:
        raise PreflightError(issues)
    return app


def sandbox_dependency_issues(app: AgentApp, env: Mapping[str, str] | None = None) -> list[str]:
    """Check that this environment can create the agent's sandbox. For `agents info`, `agents serve` and the worker."""
    if not _uses_mistral_sandbox(app):
        return []
    from mistralai.vibe_agents.sdk.sandbox.koyeb import koyeb_sandbox_class  # noqa: PLC0415

    if koyeb_sandbox_class() is not None:
        return []
    if config.is_managed_worker(env):
        # Installing into the running container fixes nothing: the image is rebuilt from the project.
        return [
            f"{_MISSING_KOYEB_EXTRA}, and this deployment's image is missing it or has a version that is too old. "
            f"In your project, run "
            f"`uv add '{_KOYEB_EXTRA}'`, make sure your Dockerfile installs the project's dependencies, "
            "then commit, push and run `agents deploy` again."
        ]
    return [
        f"{_MISSING_KOYEB_EXTRA}, and it is not installed or is too old. Install it with `uv add '{_KOYEB_EXTRA}'` "
        f"(or `pip install '{_KOYEB_EXTRA}'`), then run the command again."
    ]


def _uses_mistral_sandbox(app: AgentApp) -> bool:
    from mistralai.vibe_agents.sdk.authoring import contracts  # noqa: PLC0415

    return isinstance(getattr(app.harness, "sandbox", None), contracts.MistralSandbox)


def deploy_project_issues(path: Path, dockerfile_path: str | None = None) -> list[str]:
    # A managed deployment builds the project's Dockerfile: the one it has, or the one the deploy writes
    # for a uv project. Checking it here turns a failure that would otherwise surface minutes later in a
    # remote build log into an error raised before anything is created.
    project_path = path.resolve()
    issues: list[str] = []
    try:
        config.reject_project_runtime_declaration(project_path)
    except ValueError as exc:
        issues.append(str(exc))
    if dockerfile_path is not None:
        if not (project_path / dockerfile_path).is_file():
            issues.append(f"No Dockerfile at {dockerfile_path}. Check the path passed to --dockerfile.")
    elif not (project_path / DEFAULT_DOCKERFILE).is_file():
        issues.extend(dockerfile.generation_issues(project_path))
    return issues
