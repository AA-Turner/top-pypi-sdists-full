from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ServerContextVariable:
    """A typed handle identifying a server-side context variable.

    Server-side context variables are computed once per deployment (out of band
    from any individual query or stream message) and read in resolvers via
    :func:`chalk.functions.get_server_context`. Using a typed handle rather than
    a bare string lets Chalk attach and enforce the related metadata (provider,
    refresh period, output type) when a context variable is defined, and keeps
    call sites pointing at a single registered definition.
    """

    context_variable_name: str


# Built-in context variable: the ``(model_name, model_version)`` pairs that were
# active when the deployment was applied. The ``__chalk__.`` prefix namespaces
# context variables that Chalk provides out of the box.
ACTIVE_MODEL_VERSIONS = ServerContextVariable("__chalk__.active_model_versions")
