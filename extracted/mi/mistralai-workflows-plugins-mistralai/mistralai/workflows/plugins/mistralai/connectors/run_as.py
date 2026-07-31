from __future__ import annotations

from enum import Enum
from typing import Literal

from mistralai.workflows.client import should_use_executor_credentials


class ConnectorRunAs(str, Enum):
    """Which identity a connector runs as for its preflight and tool calls.

    - ``AUTO`` — follow the workflow's ``on_behalf_of`` flag: the executing
      user's credentials when the workflow runs on behalf of a user, the
      deployment's service credentials otherwise. This is the default,
      backward-compatible behaviour.
    - ``DEPLOYMENT`` — always the deployment's (worker's) service identity.
    """

    AUTO = "auto"
    DEPLOYMENT = "deployment"


RunAsArg = Literal["auto", "deployment"] | None


def normalize_run_as(value: RunAsArg) -> ConnectorRunAs:
    """Coerce the public ``run_as=`` argument into a :class:`ConnectorRunAs`.

    ``None`` (unspecified) maps to ``AUTO`` — follow the workflow's
    ``on_behalf_of`` flag.
    """
    if value is None:
        return ConnectorRunAs.AUTO
    try:
        return ConnectorRunAs(value)
    except ValueError:
        raise ValueError(f"Invalid connector run_as {value!r}; expected 'auto', 'deployment', or None") from None


def use_executor_credentials_for(run_as: ConnectorRunAs = ConnectorRunAs.AUTO) -> bool:
    """Whether a connector running as ``run_as`` should use executor (OBO) credentials.

    ``DEPLOYMENT`` always uses the deployment's service identity; ``AUTO`` follows
    the workflow's ``on_behalf_of`` flag.
    """
    if run_as == ConnectorRunAs.DEPLOYMENT:
        return False
    return should_use_executor_credentials()
