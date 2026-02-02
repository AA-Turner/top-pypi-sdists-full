import os


def get_default_env() -> dict[str, str]:
    """
    Returns default environment variables for CLI-spawned processes.
    These are merged with the parent process environment.
    """
    return {
        "GIT_EDITOR": "true",
    }


def get_process_env(env_overrides: dict[str, str] | None = None) -> dict[str, str]:
    """
    Returns the complete environment for spawned processes.
    Merges parent environment with default variables, then applies overrides.

    Priority order (lowest to highest):
    1. Parent process environment (os.environ)
    2. Default environment variables (get_default_env())
    3. Explicit overrides (env_overrides parameter)

    Args:
        env_overrides: Optional dict of environment variables that override defaults
    """
    env = os.environ.copy()
    env.update(get_default_env())
    if env_overrides:
        env.update(env_overrides)
    return env
