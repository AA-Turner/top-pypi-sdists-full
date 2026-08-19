# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from importlib.metadata import version

_REST_NAMESPACE_IMPL = "rest"
_USER_AGENT_PROPERTY = "header.user-agent"


def with_geneva_user_agent(impl: str, properties: dict[str, str]) -> dict[str, str]:
    """Return namespace properties with this Geneva runtime's User-Agent."""
    if impl != _REST_NAMESPACE_IMPL:
        return properties

    properties = properties.copy()
    properties[_USER_AGENT_PROPERTY] = f"Geneva-Python-Client/{version('geneva')}"
    return properties
