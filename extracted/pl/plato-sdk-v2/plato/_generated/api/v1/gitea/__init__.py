"""API endpoints."""

from . import (
    create_gitea_repository,
    create_simulator_repository,
    delete_gitea_repository,
    get_accessible_simulators,
    get_gitea_credentials,
    get_gitea_repository,
    get_my_gitea_info,
    get_my_repositories,
    get_repository_branches,
    get_repository_contents,
    get_simulator_file_content,
    get_simulator_repository,
    get_simulator_repository_branches,
    get_simulator_repository_contents,
)

__all__ = [
    "get_my_repositories",
    "get_my_gitea_info",
    "get_gitea_credentials",
    "create_gitea_repository",
    "get_gitea_repository",
    "delete_gitea_repository",
    "get_repository_contents",
    "get_repository_branches",
    "get_accessible_simulators",
    "get_simulator_repository",
    "create_simulator_repository",
    "get_simulator_repository_contents",
    "get_simulator_repository_branches",
    "get_simulator_file_content",
]
