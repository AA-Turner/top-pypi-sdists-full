from __future__ import annotations

import re
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict
from uuid import UUID

import httpx
from pydantic import BaseModel, ConfigDict

from mistralai.vibe_agents.agents_client import AgentsClient, ManagedAgentResponse, api_models
from mistralai.vibe_agents.agents_client.api_models import (
    BashkitNetworkInput,
    ConnectorInput,
    ConnectorSelectionInput,
    GitHubProxyInput,
    HarnessConfigInput,
    PlainMCPServerInput,
    SandboxConfigInput,
    SandboxImageInput,
    SandboxProxyInput,
    SecretBindingInput,
    SessionInputSchemas,
    SkillInput,
)
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring import types as authoring_types
from mistralai.vibe_agents.sdk.authoring.agent import AgentAuthoring
from mistralai.vibe_agents.sdk.authoring.sandbox_policy import GitHubBinding
from mistralai.vibe_agents.sdk.authoring.secrets import SecretOrigin
from mistralai.vibe_agents.sdk.transport import telemetry
from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy

from . import config
from .dockerfile import build_inputs as dockerfile_build_inputs
from .dockerfile import missing as missing_build_files
from .dockerfile import write_missing as write_missing_build_files
from .loader import AgentApp, declared_session_input_schemas, declared_subagent_policy

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.authoring.subagent import Subagent

    from .deploy_wait import DeployProgress

_GITHUB_REMOTE_RE = re.compile(r"^(?:https://github\.com/|git@github\.com:)(.+?)(?:\.git)?$")
_GIT_TIMEOUT_SECONDS = 30


class DeployError(Exception):
    pass


class WorkerStartError(DeployError):
    """The image was built and the worker did not come up: its own output may say why."""


class BuildFilesMissing(DeployError):
    """The project lacks build files that `write_build_files` can write; the caller decides whether to."""

    def __init__(self, project: Path, names: list[str]) -> None:
        super().__init__(f"{project} has no {' and no '.join(names)}.")
        self.project = project
        self.names = names


class GitContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    github_url: str
    revision: str
    working_dir: str


class DeploySpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    agent_name: str
    workflow_name: str
    github_url: str
    revision: str
    working_dir: str | None
    dockerfile_path: str | None


def resolve_git_context(path: Path) -> GitContext:
    root = Path(_run_git(path, ["rev-parse", "--show-toplevel"]).stdout.strip())
    remote_url = _run_git(root, ["remote", "get-url", "origin"]).stdout.strip()
    match = _GITHUB_REMOTE_RE.match(remote_url)
    if match is None:
        raise DeployError(f"Origin remote is not a GitHub URL: {remote_url}")
    upstream = _run_git(root, ["rev-parse", "--abbrev-ref", "@{u}"], check=False)
    if upstream.returncode != 0:
        raise DeployError("Current branch has no upstream. Push to GitHub before deploying.")
    if _run_git(root, ["log", "@{u}..HEAD", "--oneline"]).stdout.strip():
        raise DeployError("Current branch has unpushed commits. Push to GitHub before deploying.")
    revision = _run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    working_dir = _relative_working_dir(path, root)
    return GitContext(
        github_url=f"https://github.com/{match.group(1)}",
        revision=revision,
        working_dir=working_dir,
    )


def require_committed(path: Path, files: Sequence[str]) -> None:
    """Raise unless ``files``, relative to ``path``, are in HEAD: the platform builds that commit, not the checkout."""
    missing = [file for file in files if _run_git(path, ["cat-file", "-e", f"HEAD:./{file}"], check=False).returncode]
    if not missing:
        return
    if len(missing) == 1:
        raise DeployError(f"{missing[0]} is not committed. Commit and push it, then run `agents deploy` again.")
    raise DeployError(f"{', '.join(missing)} are not committed. Commit and push them, then run `agents deploy` again.")


def parse_secret_bindings(values: list[str]) -> list[SecretBindingInput]:
    """Turn repeated ``--secret-binding ENV_VAR=secret:workspace:NAME`` values into bindings.

    Only a reference is accepted, never a secret's value: the platform reads the named
    secret at boot, so nothing sensitive is typed on the command line or sent from here.
    """
    bindings: list[SecretBindingInput] = []
    seen: set[str] = set()
    for value in values:
        env_var_name, separator, reference = value.partition("=")
        if not separator:
            raise DeployError("--secret-binding must be ENV_VAR=secret:workspace:NAME")
        problem = api_models.env_var_name_error(env_var_name)
        if problem is not None:
            raise DeployError(f"--secret-binding environment variable {env_var_name!r} {problem}.")
        if env_var_name in seen:
            raise DeployError(f"--secret-binding sets {env_var_name} more than once.")
        if not api_models.is_valid_secret_reference(reference):
            # The rejected value is never echoed: it may be a secret pasted by mistake, and
            # this message reaches terminals and CI logs.
            raise DeployError(f"--secret-binding {env_var_name} {api_models.SECRET_REFERENCE_ERROR}")
        seen.add(env_var_name)
        bindings.append(SecretBindingInput(env_var_name=env_var_name, reference=reference))
    return bindings


def resolve_secret_bindings(
    secrets: Mapping[str, SecretOrigin],
    overrides: Sequence[SecretBindingInput],
) -> list[SecretBindingInput]:
    """Resolve each declared Secret Manager origin, and return what the worker gets as env vars.

    A ``--secret-binding`` sets or overrides the origin of a declared secret. A declared secret left
    without any reference fails the deploy, so every secret the agent gets shows in the code or on
    the command line. A binding for an undeclared name stays a plain worker env var, such as the
    worker's own settings.
    """
    by_name = {binding.env_var_name: binding.reference for binding in overrides}
    bindings = [binding for binding in overrides if binding.env_var_name not in secrets]
    unbound: list[str] = []
    for name, origin in secrets.items():
        reference = by_name.get(name, origin.ref)
        if reference is None:
            unbound.append(name)
        elif origin.worker_env:
            bindings.append(SecretBindingInput(env_var_name=name, reference=reference))
    if unbound:
        flags = " ".join(f"--secret-binding {name}=secret:workspace:NAME" for name in unbound)
        raise DeployError(
            f"Secrets {', '.join(unbound)} have no reference. Pass {flags}, or use MistralSecret.workspace(...)."
        )
    return bindings


def build_deploy_spec(git: GitContext, dockerfile_path: str | None = None) -> DeploySpec:
    return DeploySpec(
        agent_name="",
        workflow_name="",
        github_url=git.github_url,
        revision=git.revision,
        working_dir=git.working_dir or None,
        dockerfile_path=dockerfile_path,
    )


async def create_managed_deployment(
    *,
    agent_name: str,
    workflow_name: str,
    github_url: str,
    revision: str,
    working_dir: str | None,
    dockerfile_path: str | None,
    api_key: str,
    server_url: str,
    is_hardened: bool,
    description: str | None = None,
    harness_config: HarnessConfigInput | None = None,
    skills: list[SkillInput] | None = None,
    connectors: list[ConnectorInput] | None = None,
    secret_bindings: list[SecretBindingInput] | None = None,
    connector_selection: ConnectorSelectionInput | None = None,
    required_session_inputs: SessionInputSchemas | None = None,
    default_subagent_policy: SubagentPolicy | None = None,
    sandbox_config: SandboxConfigInput | None = None,
    mcp_servers: list[PlainMCPServerInput] | None = None,
) -> ManagedAgentResponse:
    async with AgentsClient(
        base_url=server_url,
        api_key=api_key,
    ) as client:
        try:
            return await client.create_managed_agent(
                agent_name=agent_name,
                workflow_name=workflow_name,
                github_url=github_url,
                revision=revision,
                working_dir=working_dir,
                dockerfile_path=dockerfile_path,
                is_hardened=is_hardened,
                description=description,
                harness_config=harness_config,
                skills=skills,
                connectors=connectors,
                secret_bindings=secret_bindings,
                connector_selection=connector_selection,
                required_session_inputs=required_session_inputs,
                default_subagent_policy=default_subagent_policy,
                sandbox_config=sandbox_config,
                mcp_servers=mcp_servers,
            )
        except httpx.HTTPStatusError as exc:
            await telemetry.agent_registration_failed(
                exc, agent_name=agent_name, workflow_name=workflow_name, worker_hosting="managed"
            )
            if exc.response.status_code == httpx.codes.FAILED_DEPENDENCY:
                raise DeployError(f"Cannot deploy: {_response_detail(exc.response)}") from exc
            message = f"Failed to create managed deployment (HTTP {exc.response.status_code})"
            detail = exc.response.text.strip()
            if detail:
                message = f"{message}: {detail}"
            raise DeployError(message) from exc
        # ValueError also covers a 2xx whose body is not JSON (JSONDecodeError) and a pydantic ValidationError.
        except (httpx.HTTPError, ValueError) as exc:
            await telemetry.agent_registration_failed(
                exc, agent_name=agent_name, workflow_name=workflow_name, worker_hosting="managed"
            )
            raise DeployError(f"Failed to create managed deployment: {exc}") from exc


def _response_detail(response: httpx.Response) -> str:
    try:
        detail = response.json().get("detail")
    except (ValueError, AttributeError):
        detail = None
    if isinstance(detail, dict):
        detail = detail.get("detail")
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    return response.text.strip() or f"HTTP {response.status_code}"


class AgentConfiguration(TypedDict):
    harness_config: HarnessConfigInput
    sandbox_config: SandboxConfigInput | None
    connectors: list[ConnectorInput]
    connector_selection: ConnectorSelectionInput | None
    mcp_servers: list[PlainMCPServerInput]


class PublishedConfig(AgentConfiguration):
    """What `agents deploy` and `agents serve` both send the control plane about the agent."""

    description: str | None
    skills: list[SkillInput] | None


class DeployConfig(PublishedConfig):
    required_session_inputs: SessionInputSchemas
    default_subagent_policy: SubagentPolicy | None


def agent_configuration(agent: AgentAuthoring, harness: contracts.Harness) -> AgentConfiguration:
    """The Agent in the control plane's typed configuration, the one shape every deploy sends.

    It carries everything those fields can express, for every Agent.
    """
    discovery = harness.connector_discovery
    return {
        "harness_config": HarnessConfigInput(
            model_name=agent.model,
            instructions=agent.instructions,
            permission_mode=agent.permission_mode,
            permission_policy=agent.permission_policy,
            auto_compact_threshold=agent.auto_compact_threshold,
            max_iterations=agent.max_iterations,
            temperature=agent.temperature,
            thinking=agent.reasoning_effort,
            first_output_timeout_seconds=agent.first_output_timeout_seconds,
            builtins=None if agent.builtins == authoring_types.Builtins() else agent.builtins.model_dump(mode="json"),
        ),
        "sandbox_config": _sandbox_config(harness.sandbox),
        "connectors": [
            ConnectorInput(
                connector_name=c.connector_name,
                run_as=c.run_as.value,
                auto_auth=c.auto_auth,
                credentials_name=c.credentials_name,
                allow_mcp_ui=c.allow_mcp_ui,
            )
            for c in harness.connectors
        ],
        "connector_selection": (
            None
            if discovery is None
            else ConnectorSelectionInput(
                exclude=list(discovery.exclude),
                max_connectors=discovery.max_connectors,
                auto_auth=discovery.auto_auth,
                allow_mcp_ui=discovery.allow_mcp_ui,
            )
        ),
        "mcp_servers": [
            PlainMCPServerInput(
                name=name,
                url=source.url,
                disabled_tools=list(source.disabled_tools),
                startup_timeout_sec=source.startup_timeout_seconds,
                tool_timeout_sec=source.tool_timeout_seconds,
            )
            for name, source in harness.mcps.items()
        ],
    }


# The authored MistralSandbox settings the typed sandbox config carries; access and the proxy are passed apart.
_TYPED_SANDBOX_SETTINGS = (
    frozenset(SandboxConfigInput.model_fields) - {"kind", "image", "access", "sandbox_proxy", "bashkit_network"}
) | frozenset(SandboxImageInput.model_fields)


def _sandbox_config(sandbox: contracts.Sandbox) -> SandboxConfigInput | None:
    if isinstance(sandbox, contracts.BashkitSandbox):
        network = sandbox.network
        return SandboxConfigInput(
            kind="bashkit",
            access=sandbox.access,
            bashkit_network=(
                None
                if network.mode == "none"
                else BashkitNetworkInput(allow=list(network.hosts), allow_all=network.mode == "all")
            ),
        )
    if isinstance(sandbox, contracts.MistralSandbox):
        # Only what the author passed: the worker that makes the sandbox applies its own defaults.
        values = {key: value for key, value in sandbox.authored_settings.items() if key in _TYPED_SANDBOX_SETTINGS}
        image_values = {
            key: values.pop(key) for key in ("image", "instance_type", "region", "name_prefix") if key in values
        }
        github = [binding for binding in sandbox.header_bindings if isinstance(binding, GitHubBinding)]
        return SandboxConfigInput(
            kind="mistral",
            access=sandbox.access,
            image=SandboxImageInput(**image_values) if image_values else None,
            **values,
            sandbox_proxy=(
                SandboxProxyInput(
                    integrations=[
                        GitHubProxyInput(
                            repo_whitelist=[] if binding.repos == "all" else list(binding.repos),
                            all_accessible_repos=binding.repos == "all",
                            ttl_seconds=binding.ttl_seconds,
                            host=binding.host,
                        )
                        for binding in github
                    ]
                )
                if github
                else None
            ),
        )
    return None


def published_config(app: AgentApp) -> PublishedConfig:
    """The agent's configuration, as the control plane stores it for both a deployed and a served agent.

    Secrets are never part of it: a secret is bound by reference, and an MCP server's credential
    stays in the environment variables its `auth_header_env_vars` name.
    """
    return {
        **agent_configuration(app.agent, app.harness),
        "description": app.description,
        "skills": [SkillInput(name=s.name, body=s.content, description=s.description) for s in app.skills] or None,
    }


def build_deploy_config(app: AgentApp) -> DeployConfig:
    """Extract deployable config from a loaded AgentApp for forwarding to the control plane.

    Returns keyword arguments suitable for ``create_managed_deployment(**config)``.
    """
    return {
        **published_config(app),
        "required_session_inputs": declared_session_input_schemas(app.agent, app.harness),
        "default_subagent_policy": declared_subagent_policy(app.agent),
    }


class DeployPlan(BaseModel):
    """Everything a deploy sends, resolved and checked before anything is created."""

    model_config = ConfigDict(frozen=True)

    spec: DeploySpec
    secret_bindings: list[SecretBindingInput]
    deploy_config: DeployConfig
    settings: config.DeploySettings
    hardened: bool
    warnings: list[str] = []


def resolve_hardened(app: AgentApp, hardened: bool | None) -> bool:
    """Decide whether the deployment is hardened.

    An explicit choice always wins. Without one, an agent that acts on behalf of the
    session user is hardened by default
    """
    if hardened is not None:
        return hardened
    return contracts.requires_on_behalf_of(app.harness, app.agent.subagents)


def plan_deploy(
    path: Path,
    *,
    name: str | None = None,
    dockerfile: str | None = None,
    secret_bindings: Sequence[str] = (),
    hardened: bool | None = None,
    on_stage: Callable[[str], None] | None = None,
) -> DeployPlan:
    """Check the environment and the project, and resolve what `agents deploy` would send.

    Raises PreflightError for missing requirements, AgentProjectError for an invalid project, and
    DeployError for a bad secret binding, git state or setting. BuildFilesMissing names the Dockerfile,
    and the `.python-version` it builds with, when the project lacks them: nothing is written here.
    """
    from . import entrypoint, loader, preflight  # noqa: PLC0415

    stage = on_stage or (lambda _stage: None)
    issues = [*preflight.worker_config_issues(), *preflight.deploy_project_issues(path, dockerfile)]
    if issues:
        raise preflight.PreflightError(issues)
    try:
        settings = config.load_deploy_settings()
    except config.SettingsError as exc:
        raise DeployError(str(exc)) from exc
    # Parsed before the slow work so a mistyped reference fails immediately.
    bindings = parse_secret_bindings(list(secret_bindings))
    stage("Loading agent...")
    app = loader.load_app(path)
    agent_name = entrypoint.resolve_agent_name(app.name, name)
    # Reported only once the agent loads, so a broken project is not offered a Dockerfile it cannot use.
    if dockerfile is None:
        project = path.resolve()
        missing = missing_build_files(project, preflight.DEFAULT_DOCKERFILE)
        if missing:
            raise BuildFilesMissing(project, missing)
    stage("Detecting git context...")
    git = resolve_git_context(path)
    built = dockerfile or preflight.DEFAULT_DOCKERFILE
    require_committed(path, [built, *dockerfile_build_inputs(path / built)])
    spec = build_deploy_spec(git, dockerfile).model_copy(update={"agent_name": agent_name, "workflow_name": app.name})
    harness = app.agent._resolve_harness(app.harness)
    resolved_bindings = resolve_secret_bindings(harness.secrets, bindings)
    return DeployPlan(
        spec=spec,
        secret_bindings=resolved_bindings,
        deploy_config=build_deploy_config(app),
        settings=settings,
        hardened=resolve_hardened(app, hardened),
        warnings=unbound_mcp_credential_warnings(harness, app.agent.subagents, resolved_bindings),
    )


def unbound_mcp_credential_warnings(
    harness: contracts.Harness,
    subagents: Sequence[Subagent],
    bindings: Sequence[SecretBindingInput],
) -> list[str]:
    """Warn for each RemoteMCP credential variable that no secret binding sets on the deployed worker.

    The control plane never sees ``auth_header_env_vars``, so only this check can tell. It is a
    warning, not an error, because the project's Dockerfile can set the variable itself.
    """
    from mistralai.vibe_agents.sdk.assembly.mcp import declared_credential_variables  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.assembly.subagents import authored_mcp_layers  # noqa: PLC0415

    bound = {binding.env_var_name for binding in bindings}
    warnings: list[str] = []
    for path, mcps in authored_mcp_layers(harness.mcps, subagents):
        where = f" in subagent {'/'.join(path)!r}" if path else ""
        for name, variables in sorted(declared_credential_variables(mcps).items()):
            warnings.extend(
                f"MCP server {name!r}{where} reads its auth headers from {variable}, which no secret binding "
                f"sets. Unless the Dockerfile sets it, the worker will refuse to start: pass "
                f"--secret-binding {variable}=secret:workspace:NAME."
                for variable in variables
                if variable not in bound
            )
    return warnings


def write_build_files(project: Path) -> list[str]:
    """Write the build files a BuildFilesMissing named, and return their names.

    The platform builds the pushed commit, so the deploy cannot go on until the user commits and pushes them.
    """
    from . import preflight  # noqa: PLC0415

    return write_missing_build_files(project, preflight.DEFAULT_DOCKERFILE)


async def create_deployment(plan: DeployPlan) -> ManagedAgentResponse:
    return await create_managed_deployment(
        agent_name=plan.spec.agent_name,
        workflow_name=plan.spec.workflow_name,
        github_url=plan.spec.github_url,
        revision=plan.spec.revision,
        working_dir=plan.spec.working_dir,
        dockerfile_path=plan.spec.dockerfile_path,
        api_key=plan.settings.api_key,
        server_url=plan.settings.deploy_control_plane_url,
        is_hardened=plan.hardened,
        secret_bindings=plan.secret_bindings,
        **plan.deploy_config,
    )


async def wait_until_live(
    plan: DeployPlan,
    agent_id: UUID,
    *,
    on_progress: Callable[[DeployProgress, float], None],
) -> float:
    """Wait until the created agent's worker is live; return the seconds it took."""
    from . import deploy_wait  # noqa: PLC0415

    return await deploy_wait.wait_for_deploy(
        agent_id=agent_id,
        api_key=plan.settings.api_key,
        server_url=plan.settings.deploy_control_plane_url,
        timeout_seconds=plan.settings.deploy_wait_timeout_seconds,
        poll_interval_seconds=plan.settings.deploy_poll_interval_seconds,
        on_progress=on_progress,
    )


async def worker_output(plan: DeployPlan, service_id: str) -> list[str] | None:
    """What the deployed worker printed on its latest start, or None if its logs could not be read."""
    from . import deploy_logs  # noqa: PLC0415

    return await deploy_logs.fetch_worker_output(
        service_id=service_id,
        api_key=plan.settings.api_key,
        logs_url=plan.settings.deploy_runtime_logs_url,
    )


def worker_logs_command(plan: DeployPlan, service_id: str) -> str:
    from . import runtime_logs  # noqa: PLC0415

    return runtime_logs.logs_command(plan.settings.deploy_runtime_logs_url, service_id)


def _relative_working_dir(path: Path, root: Path) -> str:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return ""
    rel_str = str(rel)
    return "" if rel_str == "." else rel_str


def _run_git(cwd: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or "").strip()
        raise DeployError(message or f"Git command failed: git {' '.join(args)}") from exc
    except subprocess.TimeoutExpired as exc:
        raise DeployError(f"Git command timed out after {_GIT_TIMEOUT_SECONDS}s: git {' '.join(args)}") from exc
