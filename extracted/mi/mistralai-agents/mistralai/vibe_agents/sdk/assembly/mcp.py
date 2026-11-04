"""Authored remote MCP sources and the credential check that runs before a Session starts.

A `RemoteMCP` declaring `auth_header_env_vars` carries the NAMES of the variables holding its
header values; the Runtime's HTTP Host reads them at call time, so no credential enters
`AgentConfig` or Workflow history and a resumed Session re-reads the environment it resumes in.

The Runtime resolves those names where the request is made, which is the right place but also a
place the caller never hears from: a source that fails to list is dropped behind a notice that
reaches the model's context only. `verify_credentials` therefore checks the declarations here,
before the Session starts, so a mistyped variable name is an error rather than an agent that
quietly has no tools. It reads each variable by the Host's own rule (`read_header_credential`), so a
whitespace-only value or one holding a newline fails here too instead of passing and then being
refused, unseen, at call time.
"""

from collections.abc import Iterator, Mapping

from mistralai.vibe.harness.app_server.session import (
    AgentConfig,
    McpHttpSourceConfiguration,
    McpSourceConfiguration,
    SubagentConfig,
)
from mistralai.vibe.harness.app_server.session.models.configuration import is_environment_variable_name
from mistralai.vibe.harness.runtime.capabilities.mcp_credentials import HeaderCredentialProblem, read_header_credential
from mistralai.vibe_agents.sdk.authoring.errors import SdkError


class RemoteMcpCredentialError(SdkError, RuntimeError):
    """A declared RemoteMCP credential environment variable is unset, blank, or not a legal header value.

    An `SdkError` so a caller can catch it with everything else the SDK rejects, and a
    `RuntimeError` because a missing environment variable is a runtime condition, not a bad
    argument -- the same mixin the legacy `AIStudioMCP` hook uses for the same reason.
    """


def verify_credentials(mcps: Mapping[str, McpSourceConfiguration]) -> None:
    """Raise before a Session starts if a declared credential variable is unset or unusable here."""

    _raise_for_missing(_missing_credentials(mcps))


def verify_tree_credentials(config: AgentConfig) -> None:
    """Run `verify_credentials` for the root and every Subagent level that declares its own MCPs.

    A child that leaves `mcps` unset inherits its parent's sources, which the parent's level
    already checked. A child that sets `mcps` replaces them, so its own sources need the same
    check; otherwise a missing credential would surface only when the model first spawns it.
    """

    missing = _missing_credentials(config.mcps)
    for path, mcps in _subagent_mcp_layers(config.subagents):
        owner = "/".join(path)
        missing.update(
            {f"{name} (subagent {owner!r})": variables for name, variables in _missing_credentials(mcps).items()}
        )
    _raise_for_missing(missing)


def _subagent_mcp_layers(
    subagents: Mapping[str, SubagentConfig] | None, path: tuple[str, ...] = ()
) -> Iterator[tuple[tuple[str, ...], Mapping[str, McpSourceConfiguration]]]:
    if subagents is None:
        return
    for name, subagent in subagents.items():
        layer_path = (*path, name)
        if subagent.mcps is not None:
            yield layer_path, subagent.mcps
        yield from _subagent_mcp_layers(subagent.subagents, layer_path)


def credential_problems(
    mcps: Mapping[str, McpSourceConfiguration],
) -> dict[str, dict[HeaderCredentialProblem, list[str]]]:
    """Map each source to the credential variables that cannot be sent from here, by problem.

    Each variable is read by the Host's own rule, `read_header_credential`.
    """

    problems: dict[str, dict[HeaderCredentialProblem, list[str]]] = {}
    for name, source in mcps.items():
        if not isinstance(source, McpHttpSourceConfiguration):
            continue
        found: dict[HeaderCredentialProblem, set[str]] = {}
        for header, variable in source.auth_header_env_vars.items():
            result = read_header_credential(variable)
            if isinstance(result, HeaderCredentialProblem):
                found.setdefault(result, set()).add(_printable(header, variable))
        if found:
            problems[name] = {problem: sorted(variables) for problem, variables in found.items()}
    return problems


def declared_credential_variables(mcps: Mapping[str, McpSourceConfiguration]) -> dict[str, list[str]]:
    """Map each source that declares credential variables to their names."""

    return {
        name: sorted({_printable(header, variable) for header, variable in source.auth_header_env_vars.items()})
        for name, source in mcps.items()
        if isinstance(source, McpHttpSourceConfiguration) and source.auth_header_env_vars
    }


def _missing_credentials(mcps: Mapping[str, McpSourceConfiguration]) -> dict[str, list[str]]:
    """Describe, per source name, why each of its credential variables cannot be sent."""

    missing: dict[str, list[str]] = {}
    for name, problems in credential_problems(mcps).items():
        reasons = []
        if unset := problems.get(HeaderCredentialProblem.UNSET):
            reasons.append(f"needs {', '.join(unset)}")
        if illegal := problems.get(HeaderCredentialProblem.ILLEGAL):
            # Named, never quoted: the value is a credential.
            reasons.append(f"reads {', '.join(illegal)}, which contains characters that cannot be sent in a header")
        missing[name] = reasons
    return missing


def _printable(header: str, variable: str) -> str:
    # `RemoteMCP` rejects a value that is not a variable name, but a source built without
    # validation can still carry one, and it may be a credential pasted in place of its name.
    if is_environment_variable_name(variable):
        return variable
    return f"<invalid variable name for header {header!r}>"


def _raise_for_missing(missing: Mapping[str, list[str]]) -> None:
    if not missing:
        return
    declarations = "; ".join(f"{name} {' and '.join(reasons)}" for name, reasons in sorted(missing.items()))
    raise RemoteMcpCredentialError(
        f"MCP sources cannot authenticate: {declarations}. Environment variables must be set "
        "wherever the session runs, including on resume."
    )


__all__ = [
    "RemoteMcpCredentialError",
    "credential_problems",
    "declared_credential_variables",
    "verify_credentials",
    "verify_tree_credentials",
]
