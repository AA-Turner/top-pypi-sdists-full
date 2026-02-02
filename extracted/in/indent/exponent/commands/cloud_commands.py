import asyncio
import sys
from typing import Any, cast

import click

from exponent.commands.common import (
    redirect_to_login,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.commands.utils import (
    launch_exponent_browser,
)
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.generated_client import (
    ExponentModels,
    RepositoryInput,
    SandboxProvider,
)
from exponent.core.graphql.generated_client.create_cloud_chat_from_repository import (
    CreateCloudChatFromRepositoryCreateCloudChatChat,
)
from exponent.core.graphql.generated_client.enable_cloud_repository import (
    EnableCloudRepositoryEnableCloudRepositoryEnableCloudRepositoriesResult,
)
from exponent.core.graphql.generated_client.github_repositories import (
    GithubRepositoriesGithubRepositoriesRepositories,
)
from exponent.core.graphql.generated_client.rebuild_cloud_repository import (
    RebuildCloudRepositoryRebuildCloudRepositoryContainerImages,
)
from exponent.utils.version import check_exponent_version_and_upgrade


@exponent_cli_group(hidden=True)
def cloud_cli() -> None:
    pass


async def enable_cloud_repository(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    org_name: str,
    repo_name: str,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )

    result = await graphql_client.enable_cloud_repository(
        repositories=[RepositoryInput(orgName=org_name, repoName=repo_name)]
    )

    enable_result = result.enable_cloud_repository
    if isinstance(
        enable_result,
        EnableCloudRepositoryEnableCloudRepositoryEnableCloudRepositoriesResult,
    ):
        if enable_result.results and enable_result.results[0].success:
            repo_result = enable_result.results[0]
            return {
                "__typename": "EnableCloudRepositoriesResult",
                "buildRef": repo_result.images[0].build_ref
                if repo_result.images
                else None,
                "createdAt": repo_result.images[0].created_at
                if repo_result.images
                else None,
                "updatedAt": repo_result.images[0].updated_at
                if repo_result.images
                else None,
            }
        elif enable_result.results:
            return {
                "__typename": "Error",
                "message": enable_result.results[0].error_message or "Unknown error",
            }
        else:
            return {
                "__typename": "Error",
                "message": "No results returned",
            }
    else:
        return {
            "__typename": enable_result.typename__,
            "message": enable_result.message,
        }


async def rebuild_cloud_repository(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    org_name: str,
    repo_name: str,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )

    result = await graphql_client.rebuild_cloud_repository(org_name, repo_name)

    # Convert typed response to dict for backward compatibility
    rebuild_result = result.rebuild_cloud_repository
    if isinstance(
        rebuild_result, RebuildCloudRepositoryRebuildCloudRepositoryContainerImages
    ):
        # Return the first image for backward compatibility
        if rebuild_result.images:
            first_image = rebuild_result.images[0]
            return {
                "__typename": "ContainerImage",
                "buildRef": first_image.build_ref,
                "createdAt": first_image.created_at,
                "updatedAt": first_image.updated_at,
            }
        else:
            return {
                "__typename": "Error",
                "message": "No container images returned",
            }
    else:
        return {
            "__typename": rebuild_result.typename__,
            "message": rebuild_result.message,
        }


async def list_github_repositories(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )

    result = await graphql_client.get_github_repositories()

    # Convert typed response to dict for backward compatibility
    github_repos = result.github_repositories
    if isinstance(github_repos, GithubRepositoriesGithubRepositoriesRepositories):
        return {
            "__typename": "GithubRepositories",
            "repositories": [
                {
                    "uuid": repo.uuid,
                    "githubOrgName": repo.github_org_name,
                    "githubRepoName": repo.github_repo_name,
                    "createdAt": repo.created_at,
                    "updatedAt": repo.updated_at,
                    "baseHost": None,
                    "containerImageId": None,
                }
                for repo in github_repos.repositories
            ],
        }
    else:
        return {
            "__typename": "Error",
            "message": github_repos.message,
        }


async def create_cloud_chat_from_repository(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    repository_id: str,
    provider: SandboxProvider | None = None,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )

    result = await graphql_client.create_cloud_chat_from_repository(
        repository_id=repository_id, provider=provider
    )

    create_cloud_chat = result.create_cloud_chat
    if isinstance(create_cloud_chat, CreateCloudChatFromRepositoryCreateCloudChatChat):
        return {
            "__typename": "Chat",
            "chatUuid": create_cloud_chat.chat_uuid,
        }
    else:
        return {
            "__typename": create_cloud_chat.typename__,
            "message": create_cloud_chat.message
            if hasattr(create_cloud_chat, "message")
            else "Unknown error",
        }


async def start_chat_turn_with_prompt(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    chat_uuid: str,
    prompt: str,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )

    result = await graphql_client.start_chat_turn(
        chat_uuid=chat_uuid,
        prompt=prompt,
        parent_uuid=None,
        exponent_model=ExponentModels.PREMIUM,
        require_confirmation=False,
        read_only=False,
        depth_limit=20,
    )

    # Convert typed response to dict for backward compatibility
    return {
        "__typename": result.start_chat_turn.typename__,
        "chatUuid": getattr(result.start_chat_turn, "chat_uuid", None),
        "message": getattr(result.start_chat_turn, "message", None),
    }


@cloud_cli.command(hidden=True)
@click.option(
    "--org-name",
    help="GitHub organization name",
    required=True,
)
@click.option(
    "--repo-name",
    help="GitHub repository name",
    required=True,
)
@use_settings
def enable_repo(
    settings: Settings,
    org_name: str,
    repo_name: str,
) -> None:
    """Test utility for enabling cloud repository."""
    check_exponent_version_and_upgrade(settings)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    try:
        result = asyncio.run(
            enable_cloud_repository(
                api_key, base_api_url, base_ws_url, org_name, repo_name
            )
        )

        if result["__typename"] == "EnableCloudRepositoriesResult":
            click.secho(
                f"✓ Successfully enabled repository {org_name}/{repo_name}", fg="green"
            )
            click.echo(f"  Build ref: {result.get('buildRef', 'N/A')}")
            click.echo(f"  Created at: {result.get('createdAt', 'N/A')}")
            click.echo(f"  Updated at: {result.get('updatedAt', 'N/A')}")
        else:
            click.secho(
                f"✗ Failed to enable repository: {result.get('message', 'Unknown error')}",
                fg="red",
            )
            click.echo(f"  Error type: {result['__typename']}")

    except Exception as e:
        click.secho(f"✗ Error enabling repository: {e!s}", fg="red")
        sys.exit(1)


@cloud_cli.command(hidden=True)
@click.option(
    "--org-name",
    help="GitHub organization name",
    required=True,
)
@click.option(
    "--repo-name",
    help="GitHub repository name",
    required=True,
)
@use_settings
def rebuild(
    settings: Settings,
    org_name: str,
    repo_name: str,
) -> None:
    """Test utility for full rebuild of cloud repository."""
    check_exponent_version_and_upgrade(settings)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    try:
        result = asyncio.run(
            rebuild_cloud_repository(
                api_key, base_api_url, base_ws_url, org_name, repo_name
            )
        )

        if result["__typename"] == "ContainerImage":
            click.secho(
                f"✓ Successfully triggered rebuild for {org_name}/{repo_name}",
                fg="green",
            )
            click.echo(f"  Build ref: {result.get('buildRef', 'N/A')}")
            click.echo(f"  Created at: {result.get('createdAt', 'N/A')}")
            click.echo(f"  Updated at: {result.get('updatedAt', 'N/A')}")
        else:
            click.secho(
                f"✗ Failed to trigger rebuild: {result.get('message', 'Unknown error')}",
                fg="red",
            )
            click.echo(f"  Error type: {result['__typename']}")

    except Exception as e:
        click.secho(f"✗ Error triggering rebuild: {e!s}", fg="red")
        sys.exit(1)


@cloud_cli.command(hidden=True)
@use_settings
def list_repos(
    settings: Settings,
) -> None:
    """Test utility for listing GitHub repositories."""
    check_exponent_version_and_upgrade(settings)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    try:
        result = asyncio.run(
            list_github_repositories(api_key, base_api_url, base_ws_url)
        )

        if result["__typename"] == "GithubRepositories":
            repositories = result.get("repositories", [])
            if repositories:
                click.secho(f"✓ Found {len(repositories)} repositories:", fg="green")
                for repo in repositories:
                    click.echo(
                        f"\n  Repository: {repo['githubOrgName']}/{repo['githubRepoName']}"
                    )
                    click.echo(f"    ID: {repo['id']}")
                    if repo.get("baseHost"):
                        click.echo(f"    Base Host: {repo['baseHost']}")
                    if repo.get("containerImageId"):
                        click.echo(
                            f"    Container Image ID: {repo['containerImageId']}"
                        )
                    click.echo(f"    Created: {repo['createdAt']}")
                    click.echo(f"    Updated: {repo['updatedAt']}")
            else:
                click.secho("No repositories found", fg="yellow")
        else:
            click.secho(
                f"✗ Failed to list repositories: {result.get('message', 'Unknown error')}",
                fg="red",
            )
            click.echo(f"  Error type: {result['__typename']}")

    except Exception as e:
        click.secho(f"✗ Error listing repositories: {e!s}", fg="red")
        sys.exit(1)


def filter_repositories(
    repositories: list[dict[str, Any]], org_name: str | None, repo_name: str | None
) -> list[dict[str, Any]]:
    """Filter repositories by organization and/or repository name."""
    if not (org_name or repo_name):
        return repositories

    filtered = []
    for repo in repositories:
        if org_name and repo["githubOrgName"] != org_name:
            continue
        if repo_name and repo["githubRepoName"] != repo_name:
            continue
        filtered.append(repo)

    return filtered


def select_repository_interactive(repositories: list[dict[str, Any]]) -> dict[str, Any]:
    """Interactively select a repository from a list."""
    if len(repositories) == 1:
        selected = repositories[0]
        click.secho(
            f"Using repository: {selected['githubOrgName']}/{selected['githubRepoName']}",
            fg="cyan",
        )
        return selected

    # Show numbered list for selection
    click.secho("Available repositories:", fg="cyan")
    for i, repo in enumerate(repositories, 1):
        click.echo(f"  {i}. {repo['githubOrgName']}/{repo['githubRepoName']}")

    # Get user selection
    while True:
        try:
            choice = click.prompt("Select a repository (number)", type=int)
            if 1 <= choice <= len(repositories):
                return cast(dict[str, Any], repositories[choice - 1])
            else:
                click.secho(
                    f"Please enter a number between 1 and {len(repositories)}",
                    fg="red",
                )
        except (ValueError, KeyboardInterrupt):
            click.secho("\nCancelled", fg="yellow")
            sys.exit(0)


def send_initial_prompt(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    chat_uuid: str,
    prompt: str,
) -> None:
    """Send an initial prompt to the chat if provided."""
    click.secho(
        f"\nSending initial prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}",
        fg="cyan",
    )

    prompt_result = asyncio.run(
        start_chat_turn_with_prompt(
            api_key, base_api_url, base_ws_url, chat_uuid, prompt
        )
    )

    if prompt_result["__typename"] == "Chat":
        click.secho("✓ Prompt sent successfully", fg="green")
    else:
        click.secho(
            f"⚠ Failed to send prompt: {prompt_result.get('message', 'Unknown error')}",
            fg="yellow",
        )
        click.echo(f"  Error type: {prompt_result['__typename']}")


def fetch_repositories(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> list[dict[str, Any]]:
    """Fetch the list of GitHub repositories."""
    result = asyncio.run(list_github_repositories(api_key, base_api_url, base_ws_url))

    if result["__typename"] != "GithubRepositories":
        click.secho(
            f"✗ Failed to list repositories: {result.get('message', 'Unknown error')}",
            fg="red",
        )
        sys.exit(1)

    repositories = result.get("repositories", [])
    if not repositories:
        click.secho("No repositories found", fg="yellow")
        sys.exit(1)

    return cast(list[dict[str, Any]], repositories)


@cloud_cli.command(hidden=True)
@click.option(
    "--org-name",
    help="GitHub organization name (optional, for filtering)",
    required=False,
)
@click.option(
    "--repo-name",
    help="GitHub repository name (optional, for direct selection)",
    required=False,
)
@click.option(
    "--prompt",
    help="Initial prompt to send to the chat after creation",
    required=False,
)
@use_settings
def create_chat(
    settings: Settings,
    org_name: str | None,
    repo_name: str | None,
    prompt: str | None,
) -> None:
    """Create a cloud chat for a GitHub repository with optional initial prompt."""
    check_exponent_version_and_upgrade(settings)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_url = settings.base_url
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    try:
        # Fetch repositories
        repositories = fetch_repositories(api_key, base_api_url, base_ws_url)

        # Filter if criteria provided
        filtered_repos = filter_repositories(repositories, org_name, repo_name)

        if not filtered_repos:
            click.secho(
                f"No repositories found matching {org_name}/{repo_name or '*'}",
                fg="yellow",
            )
            sys.exit(1)

        # Select repository
        selected_repo = select_repository_interactive(filtered_repos)

        # Create cloud chat
        click.secho(
            f"\nCreating cloud chat for {selected_repo['githubOrgName']}/{selected_repo['githubRepoName']}...",
            fg="cyan",
        )

        chat_result = asyncio.run(
            create_cloud_chat_from_repository(
                api_key, base_api_url, base_ws_url, selected_repo["id"]
            )
        )

        if chat_result["__typename"] != "Chat":
            click.secho(
                f"✗ Failed to create cloud chat: {chat_result.get('message', 'Unknown error')}",
                fg="red",
            )
            click.echo(f"  Error type: {chat_result['__typename']}")
            sys.exit(1)

        # Success - handle chat creation
        chat_uuid = chat_result["chatUuid"]
        click.secho(f"✓ Successfully created cloud chat: {chat_uuid}", fg="green")
        click.echo(f"\nChat URL: {base_url}/chats/{chat_uuid}")

        # Send initial prompt if provided
        if prompt:
            send_initial_prompt(api_key, base_api_url, base_ws_url, chat_uuid, prompt)

        # Open browser
        launch_exponent_browser(settings.environment, base_url, chat_uuid)

    except Exception as e:
        click.secho(f"✗ Error creating cloud chat: {e!s}", fg="red")
        sys.exit(1)
