from enum import Enum


class ConnectorRunAs(str, Enum):
    """Which identity a connector runs as for its preflight and tool calls.

    - ``AUTO`` — follow the workflow's ``on_behalf_of`` flag: the executing
      user's credentials when the workflow runs on behalf of a user, the
      deployment's service credentials otherwise. Client requests require
      workflow context. This is the default policy.
    - ``DEPLOYMENT`` — always the deployment's (worker's) service identity.
    """

    AUTO = "auto"
    DEPLOYMENT = "deployment"
