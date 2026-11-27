from enum import Enum


class RunAs(str, Enum):
    """Which identity SDK requests run as.

    - ``AUTO`` — follow the running workflow's own ``on_behalf_of`` declaration: the executing
      user's credentials when the workflow runs on behalf of a user, the
      deployment's service credentials otherwise. Client requests require
      workflow context. This is the default policy.
    - ``DEPLOYMENT`` — always the deployment's (worker's) service identity.
    - ``EXECUTOR`` — always the executing user's credentials; requests fail when the
      workflow does not run on behalf of a user. SDK clients only: connectors reject it.
    """

    AUTO = "auto"
    DEPLOYMENT = "deployment"
    EXECUTOR = "executor"
