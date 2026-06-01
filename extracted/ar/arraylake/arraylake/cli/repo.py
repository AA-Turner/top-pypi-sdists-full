import json
import warnings
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

import typer
import zarr
from pydantic import SecretStr
from rich import print_json
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from arraylake import AsyncClient, Client
from arraylake.cli.utils import coro, rich_console, simple_progress
from arraylake.compute.doctor import (
    CFDiagnosisSummary,
    check_cf_attribute_completeness,
    fix_cf_noncompliance,
)
from arraylake.log_util import get_logger
from arraylake.types import RepoOperationMode

if TYPE_CHECKING:
    import xarray as xr  # noqa: F401
    from xarray import Dataset

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
    prefix: str = typer.Option(None, help="Optional prefix for Icechunk repo. If not provided, a random ID + the repo name will be used."),
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
):
    """**Delete** a repository

    **Examples**

    - Delete repository without confirmation prompt

        ```
        $ arraylake repo delete my-org/example-repo --confirm
        ```
    """
    if not confirm:
        confirm = typer.confirm(
            f"This will permanently remove the {repo_name} repo. Are you sure you want to continue?",
            abort=True,
        )

    client = AsyncClient()

    with simple_progress(f"Deleting repo [bold]{repo_name}[/bold]..."):
        await client.delete_repo(repo_name, imsure=confirm, imreallysure=confirm)

    # If the repo is a icechunk repo, print message that the bucket must be deleted manually
    rich_console.print(f"Repo [bold]{repo_name}[/bold] removed from Arraylake. \nThe underlying Icechunk bucket must be deleted manually.")


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


def diagnose_dataset(ds: "Dataset") -> CFDiagnosisSummary:
    """Checks if a dataset is CF compliant."""
    rich_console.print("[bold]Diagnosing dataset...[/bold] :stethoscope:")
    # TODO: pause the spinner while this is running
    diagnosis: CFDiagnosisSummary = check_cf_attribute_completeness(ds)

    rich_console.print("[bold]Checking compatibilty with compute services...[/bold] :stethoscope:")
    if diagnosis.compatible_services:
        for service in diagnosis.compatible_services:
            rich_console.print(f"  :white_check_mark: {service}")
    if diagnosis.incompatible_services:
        for service in diagnosis.incompatible_services:
            rich_console.print(f"  :x: {service}")

    if diagnosis.is_healthy:
        # Dataset is already compliant
        rich_console.print("Dataset is healthy! :apple:")
    else:
        rich_console.print("[bold]Dataset is unhealthy[/bold] :face_with_thermometer:")
        rich_console.print("[bold]Diagnosis:[/bold] :woman_health_worker::clipboard:")
        if diagnosis.missing_required_keys:
            rich_console.print("  Missing CF Attributes:")
            for missing_key in diagnosis.sorted_missing_keys:
                missing_required = " (required)" if missing_key.required else ""
                color = "default"
                if missing_key.required:
                    color = "red"
                elif missing_key.proposed_variable:
                    color = "yellow"
                rich_console.print(f"    [bold][{color}]- {missing_key.attr_name}: {missing_key.name}{missing_required}[/{color}][/bold]")
                if missing_key.proposed_variable:
                    rich_console.print(f"      Possible variable: {missing_key.proposed_variable}")
        if diagnosis.has_invalid_keys:
            rich_console.print("  Invalid CF Attributes:")
            for invalid_key in diagnosis.invalid:
                rich_console.print(f"    [bold][red]- {invalid_key.attr_name}: {invalid_key.name}: {invalid_key.issue}[/red][/bold]")
    return diagnosis


def treat_dataset(diagnosis: CFDiagnosisSummary, store, group) -> tuple[CFDiagnosisSummary, Optional["Dataset"]]:
    """Treats a dataset to make it CF compliant."""
    if diagnosis.is_healthy:
        rich_console.print("Dataset does not need to be treated :muscle:")
        return diagnosis, None
    else:
        rich_console.print("[bold]Treating dataset... [/bold]:ambulance:")
        fix_cf_noncompliance(diagnosis, store, group)
        # Read the data back in
        import xarray as xr  # noqa: F811

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            treated_ds = xr.open_zarr(store, zarr_format=3, group=group, consolidated=False)
        # Run the compliance check again to see if we actually fixed it
        new_diagnosis = check_cf_attribute_completeness(treated_ds)
        if not new_diagnosis.is_healthy:
            raise ValueError(
                "[bold]Failed to treat dataset![/bold] :coffin: \n "
                "Please use the diagnosis to manually update the necessary attributes :hammer:"
            )
        return new_diagnosis, treated_ds


def get_treatment_plan(og_ds: "Dataset", treated_ds: "Dataset"):
    """Prints the treatment plan for a dataset by comparing variable attrs."""
    all_vars = set(og_ds.variables).union(treated_ds.variables)

    for var in all_vars:
        og_attrs = og_ds[var].attrs if var in og_ds else {}
        treated_attrs = treated_ds[var].attrs if var in treated_ds else {}

        if og_attrs != treated_attrs:
            rich_console.print(f"\n  [bold]Treatment plan for variable '{var}' metadata: [/bold]")

            for key in set(og_attrs.keys()).union(treated_attrs.keys()):
                og_val = og_attrs.get(key, "MISSING")
                new_val = treated_attrs.get(key, "MISSING")

                if og_val != new_val:
                    color = "green" if key in treated_attrs else "red"
                    rich_console.print(f"    - [bold][{color}]{key}:[/{color}][/bold]")
                    rich_console.print(f"      [bold]Original:[/bold] [red]{og_val}[/red]")
                    rich_console.print(f"      [bold]Treated:[/bold] [green]{new_val}[/green]")


@app.command(name="doctor")
@coro  # type: ignore
async def doctor_dataset(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    group: str | None = typer.Option(None, help="The path to the zarr group"),
    treat: bool = typer.Option(default=False, hidden=True, help="Fix and commit the changes automatically"),
    dry_run: bool = typer.Option(default=False, hidden=True, help="Run the doctor without committing changes"),
):
    """**Doctor** a dataset to make it usable by the Arraylake compute engine.

    **Examples**


    """
    if not treat and dry_run:
        rich_console.print("[bold][yellow]Warning: [/bold][/yellow] Treat must be enabled for dry run mode.")

    group_str = group if group is not None else ""
    rich_console.print(f"Admitting dataset [bold]{repo_name}/{group_str}[/bold] to the Arraylake hospital :hospital:")
    client = Client()
    repo = client.get_repo(repo_name)

    session = repo.writable_session(branch="main") if treat else repo.readonly_session(branch="main")
    store = session.store

    # with ekg_progress(""):
    import xarray as xr  # noqa: F811

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ds = xr.open_zarr(store, zarr_format=3, group=group, consolidated=False)
    diagnosis = diagnose_dataset(ds)

    if treat:
        updated_diagnosis, treated_ds = treat_dataset(diagnosis, store, group=group)
        # If the dataset was already healthy, treatment is not needed
        if treated_ds is None:
            return
        # Check that the only the dataset was modified using session status
        diff = session.status()
        assert len(diff.new_groups) == 0
        assert len(diff.new_arrays) == 0
        assert len(diff.deleted_groups) == 0
        assert len(diff.deleted_arrays) == 0
        assert len(diff.updated_chunks) == 0
        assert diff.updated_arrays  # type: ignore[unused-ignore,attr-defined]
        rich_console.print("[bold]Proposed treatment:[/bold] :pill:")
        get_treatment_plan(ds, treated_ds)

        if updated_diagnosis.is_healthy and not dry_run:
            lets_commit = Confirm.ask("Do you want to commit the proposed changes?")
            if lets_commit:
                rich_console.print("[bold]Committing changes...[/bold] :sparkles:")
                message = "Updated metadata attributes for use with Arraylake Flux using repo doctor"
                snapshot_id = session.commit(message)
                rich_console.print(f"Dataset successfully treated and committed to the repo with ID {snapshot_id} :dizzy:")
    else:
        if not diagnosis.is_healthy:
            rich_console.print("\nTo manually treat the dataset, use the diagnosis provided above to update the dataset metadata")


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
    bucket_config_nickname: str | None = typer.Option(None, help="Chunkstore bucket config nickname"),
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
