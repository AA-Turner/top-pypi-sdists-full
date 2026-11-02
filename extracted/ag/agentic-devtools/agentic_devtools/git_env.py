"""Environment isolation for Git commands in temporary test repositories."""

from collections.abc import Mapping

GIT_ROUTING_VARIABLES = frozenset(
    {
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_COMMON_DIR",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_NAMESPACE",
        "GIT_PREFIX",
        "GIT_CONFIG",
        "GIT_CONFIG_PARAMETERS",
        "GIT_CONFIG_COUNT",
    }
)
GIT_ROUTING_PREFIXES = ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")


def sanitize_git_environment(environment: Mapping[str, str]) -> dict[str, str]:
    """Copy an environment without inherited repository routing or config overrides."""
    return {
        key: value
        for key, value in environment.items()
        if key.upper() not in GIT_ROUTING_VARIABLES and not key.upper().startswith(GIT_ROUTING_PREFIXES)
    }
