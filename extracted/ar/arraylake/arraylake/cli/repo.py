import json
from datetime import datetime
from enum import Enum, StrEnum
from uuid import UUID

import typer
import zarr
from pydantic import SecretStr
from rich import print_json
from rich.table import Table
from rich.text import Text

from arraylake import AsyncClient
from arraylake.cli.utils import coro, rich_console, simple_progress
from arraylake.log_util import get_logger
from arraylake.types import DatasetFilter, NodeFilter, RepoOperationMode, SubscriptionType

app = typer.Typer(help="Manage Arraylake repositories", no_args_is_help=True)
logger = get_logger(__name__)


class ListOutputType(StrEnum):
    rich = "rich"
    json = "json"


def format_metadata(metadata: dict, max_line_length=25) -> Text:
    """Format metadata for display."""
    lines = []

    for k, v in metadata.items():
        v_str = ", ".join(map(str, v)) if isinstance(v, list) else str(v)
        prefix = f"{k}: "
        available = max_line_length - len(prefix)

        if available <= 0:
            # If the key itself is too long, truncate everything to fit
            truncated = prefix[: max_line_length - 1] + "…"
            lines.append(Text(truncated))
            continue
        # Truncate value string if needed
        if len(v_str) > available:
            v_str = v_str[: available - 1] + "…"
        line = Text.assemble((k, "bold cyan"), f": {v_str}")
        lines.append(line)

    return Text("\n").join(lines)


def _repos_table(repos, org):
    table = Table(title=f"Arraylake Repositories for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=45)
    table.add_column("Created", justify="right", style="green", min_width=25)
    table.add_column("Updated", justify="right", style="green", min_width=25)
    table.add_column("Description", justify="right", style="green", min_width=25)
    table.add_column("Metadata", justify="left", style="green", min_width=25)
    table.add_column("Status", justify="right", style="green", min_width=15)

    mode_colors = {"online": "green", "maintenance": "yellow", "offline": "red"}

    for repo in repos:
        table.add_row(
            repo.name,
            repo.created.isoformat(),
            repo.updated.isoformat(),
            repo.description,
            format_metadata(repo.metadata, max_line_length=25) if repo.metadata else None,
            repo.status.mode,
            style=mode_colors[repo.status.mode],
        )

    return table


def _make_json_safe(obj):
    """Convert an object to a JSON-safe format."""
    if isinstance(obj, dict):
        return {k: _make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_json_safe(i) for i in obj]
    elif isinstance(obj, set):
        return _make_json_safe(list(obj))
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, SecretStr):
        return "[REDACTED]"
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


@app.command(name="list")
@coro  # type: ignore
async def list_repos(
    org: str = typer.Argument(..., help="The organization name"),
    filter_metadata: str | None = typer.Option(None, help="Optional metadata to filter the repos by"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """**List** repositories in the specified organization

    **Examples**

    - List repos in _default_ org

        ```
        $ arraylake repo list my-org
        ```

    - List repos in _default_ org with metadata filter
        ```
        $ arraylake repo list my-org --filter-metadata '{"key": "value"}'
        ```
    """
    with simple_progress(f"Listing repos for [bold]{org}[/bold]...", quiet=(output != "rich")):
        metadata_filter_dict = json.loads(filter_metadata) if filter_metadata else None
        repos = await AsyncClient().list_repos(org, filter_metadata=metadata_filter_dict)

    if output == "json":
        repos_json = [_make_json_safe(r._asdict()) for r in repos]
        print_json(data=repos_json)
    elif repos:
        rich_console.print(_repos_table(repos, org))
    else:
        rich_console.print("\nNo results")


@app.command()
@coro  # type: ignore
async def create(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    bucket_config_nickname: str | None = typer.Option(None, help="Bucket config nickname"),
    prefix: str = typer.Option(
        None, help="Optional prefix for the repo's storage. If not provided, a random ID + the repo name will be used."
    ),
    description: str | None = typer.Option(None, help="Description of the repo"),
    metadata: str | None = typer.Option(None, help="Optional metadata for the repo"),
):
    """**Create** a new repository

    **Examples**

    - Create new repository

        ```
        $ arraylake repo create my-org/example-repo --bucket-config-nickname arraylake-bucket --metadata '{"key": "value"}'
        ```
    """
    metadata_dict = json.loads(metadata) if metadata else None
    with simple_progress(f"Creating repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().create_repo(
            repo_name,
            bucket_config_nickname=bucket_config_nickname,
            prefix=prefix,
            description=description,
            metadata=metadata_dict,
        )


@app.command(name="import")
@coro  # type: ignore
async def import_repo(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    bucket_config_nickname: str = typer.Argument(..., help="Bucket config nickname"),
    prefix: str = typer.Argument(..., help="Prefix in which the Icechunk repo exists in the bucket"),
    description: str | None = typer.Option(None, help="Description of the repo"),
    metadata: str | None = typer.Option(None, help="Optional metadata for the repo"),
):
    """**Import** an existing Icechunk repository

    **Examples**

    - Import existing Icechunk repository

        ```
        $ arraylake repo import my-org/example-repo icechunk-bucket my-icechunk-prefix --metadata '{"key": "value"}'
        ```
    """
    metadata_dict = json.loads(metadata) if metadata else None
    with simple_progress(f"Importing repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().import_repo(
            repo_name,
            bucket_config_nickname,
            prefix,
            description=description,
            metadata=metadata_dict,
        )


@app.command()
@coro  # type: ignore
async def subscribe(
    repo_name: str = typer.Argument(..., help="Name of the subscriber repository {ORG}/{REPO_NAME}"),
    listing_id: str = typer.Argument(..., help="ID of the exchange listing"),
    subscription_type: SubscriptionType = typer.Option(SubscriptionType.DIRECT, help="Subscription type"),
    include_path: list[str] | None = typer.Option(None, help="Group or array to copy (filtered/private). Repeat for more paths."),
    exclude_path: list[str] | None = typer.Option(None, help="Group or array to leave out (filtered/private). Repeat for more paths."),
    bucket_config_nickname: str | None = typer.Option(None, help="Bucket for the copied data (filtered/private)"),
    prefix: str | None = typer.Option(None, help="Optional prefix in the bucket. If not provided, one is generated."),
    description: str | None = typer.Option(None, help="Description of the repo"),
    metadata: str | None = typer.Option(None, help="Optional metadata for the repo"),
):
    """**Subscribe** to an exchange listing

    **Examples**

    - Subscribe to a free listing

        ```
        $ arraylake repo subscribe my-org/era5 6720f1c2a9e3b4d5e6f70812
        ```

    - Copy two arrays from a paid listing into your bucket

        ```
        $ arraylake repo subscribe my-org/era5-subset 6720f1c2a9e3b4d5e6f70812 --subscription-type filtered --include-path /t2m --include-path /u10 --bucket-config-nickname my-bucket
        ```
    """
    target_filter = (
        DatasetFilter(nodes=NodeFilter(include_paths=include_path or [], exclude_paths=exclude_path or []))
        if include_path or exclude_path
        else None
    )
    metadata_dict = json.loads(metadata) if metadata else None
    with simple_progress(f"Subscribing [bold]{repo_name}[/bold]..."):
        await AsyncClient().subscribe_to_listing(
            repo_name,
            listing_id,
            subscription_type=subscription_type,
            target_filter=target_filter,
            bucket_config_nickname=bucket_config_nickname,
            prefix=prefix,
            description=description,
            metadata=metadata_dict,
        )


@app.command()
@coro  # type: ignore
async def claim(
    repo_name: str = typer.Argument(..., help="Name of the subscriber repository {ORG}/{REPO_NAME}"),
    claim_code: str = typer.Argument(..., help="Claim code from the provider"),
    bucket_config_nickname: str | None = typer.Option(None, help="Bucket for the copied data (filtered/private)"),
    prefix: str | None = typer.Option(None, help="Optional prefix in the bucket. If not provided, one is generated."),
    description: str | None = typer.Option(None, help="Description of the repo"),
    metadata: str | None = typer.Option(None, help="Optional metadata for the repo"),
):
    """**Claim** a subscription with a claim code

    **Examples**

    - Claim a subscription

        ```
        $ arraylake repo claim my-org/era5 ABCD-1234
        ```
    """
    metadata_dict = json.loads(metadata) if metadata else None
    with simple_progress(f"Claiming [bold]{repo_name}[/bold]..."):
        await AsyncClient().claim_subscription(
            repo_name,
            claim_code,
            bucket_config_nickname=bucket_config_nickname,
            prefix=prefix,
            description=description,
            metadata=metadata_dict,
        )


@app.command()
@coro  # type: ignore
async def modify(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    description: str | None = typer.Option(None, help="Optional description for the repo"),
    add_metadata: str | None = typer.Option(None, "--add-metadata", "-a", help="Optional metadata to add to the repo"),
    remove_metadata: list[str] | None = typer.Option(
        None, "--remove-metadata", "-r", help="Optional metadata keys to remove from the repo"
    ),
    update_metadata: str | None = typer.Option(None, "--update-metadata", "-u", help="Optional metadata to update in the repo"),
):
    """**Modify** a repository

    **Examples**

    - Modify repository description

        ```
        $ arraylake repo modify my-org/example-repo --description "New description"
        ```

    - Modify repository metadata

        ```
        $ arraylake repo modify my-org/example-repo -a '{"new_key": "value"}' -r "bad_key1" -r "bad_key2" -u '{"existing_key": "new_value"}'
        ```
    """
    aclient = AsyncClient()
    with simple_progress(f"Updating repo [bold]{repo_name}[/bold]..."):
        await aclient.modify_repo(
            repo_name,
            description=description,
            add_metadata=json.loads(add_metadata) if add_metadata else None,
            remove_metadata=remove_metadata,
            update_metadata=json.loads(update_metadata) if update_metadata else None,
        )


@app.command()
@coro  # type: ignore
async def delete(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    confirm: bool = typer.Option(False, help="confirm deletion without prompting"),
    immediate: bool = typer.Option(False, help="skip the recovery grace period and move straight to cleanup (cannot be restored)"),
    retain_data: bool = typer.Option(False, help="leave the bucket bytes in place; only remove Arraylake metadata"),
):
    """**Delete** a repository

    By default the repo enters a recoverable state for a grace period before its
    data is cleaned up. Pass --immediate to skip the grace period.

    **Examples**

    - Delete repository without confirmation prompt

        ```
        $ arraylake repo delete my-org/example-repo --confirm
        ```

    - Delete immediately, freeing the name right away

        ```
        $ arraylake repo delete my-org/example-repo --confirm --immediate
        ```
    """
    if not confirm:
        confirm = typer.confirm(
            f"{_delete_outcome(repo_name, immediate=immediate, retain_data=retain_data, done=False)} Continue?",
            abort=True,
        )

    client = AsyncClient()

    with simple_progress(f"Deleting repo [bold]{repo_name}[/bold]..."):
        await client.delete_repo(repo_name, imsure=confirm, imreallysure=confirm, immediate=immediate, retain_data=retain_data)

    rich_console.print(_delete_outcome(repo_name, immediate=immediate, retain_data=retain_data, done=True))


def _delete_outcome(repo_name: str, *, immediate: bool, retain_data: bool, done: bool) -> str:
    verb = "Deleted" if done else "This will delete"
    if not immediate:
        return f"{verb} {repo_name}. You can restore it from the web app until the grace period ends."
    if retain_data:
        return f"{verb} {repo_name} from Arraylake. Its data stays in your storage bucket."
    return f"{verb} {repo_name} and its data. You cannot restore it."


@app.command()
@coro  # type: ignore
async def tree(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    depth: int = typer.Option(10, help="Maximum depth to descend into hierarchy."),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """Show tree representation of a repository

    **Examples**

    - Show the tree representation of a repo up to level 5

        ```
        $ arraylake repo tree my-org/example-repo --depth 5
        ```
    """

    client = AsyncClient()
    repo = await client.get_repo(repo_name)

    session = repo.readonly_session(branch="main")

    try:
        root = await zarr.api.asynchronous.open_group(session.store, mode="r")
    except FileNotFoundError:
        # If the store doesnt have a root group yet, then there is no tree so it is not found
        rich_console.print("Repo is empty!")
        return

    # TODO: support prefix?
    _tree = await root.tree(level=depth)

    if output == "json":
        print_json(_tree.model_dump_json())
    else:
        print(_tree)


@app.command(hidden=True)
@coro  # type: ignore
async def get_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    repo = await AsyncClient().get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)


@app.command(hidden=True)
@coro  # type: ignore
async def set_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    mode: RepoOperationMode = typer.Argument(..., help="An option"),
    message: str = typer.Option(None, help="Optional message to bind to state"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    c = AsyncClient()
    await c._set_repo_status(repo_name, mode, message)
    repo = await c.get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)


@app.command()
@coro  # type: ignore
async def tune(
    org_name: str = typer.Argument(..., help="Name of organization"),
    bucket_config_nickname: str | None = typer.Option(None, help="Bucket config to benchmark. Defaults to the org's default bucket."),
):
    """Diagnose I/O configuration for optimal performance

    **Examples**

    - Tune the organization with a specific bucket config nickname

        ```
        $ arraylake repo tune my-org --bucket-config-nickname my-bucket-config
        ```

    """
    from arraylake.tuning import tune_org

    await tune_org(org_name, bucket_config_nickname)
