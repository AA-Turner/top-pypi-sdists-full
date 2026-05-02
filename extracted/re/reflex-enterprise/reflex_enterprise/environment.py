"""Enterprise environment variables."""

from reflex.environment import EnvironmentVariables, EnvVar, env_var


class EnvironmentEnterpriseVariables(EnvironmentVariables):
    """Enterprise environment variables."""

    # Set the access token needed to authenticate with the Reflex backend.
    REFLEX_ACCESS_TOKEN: EnvVar[str | None] = env_var(None)

    CI: EnvVar[bool] = env_var(False)


environment = EnvironmentEnterpriseVariables()
