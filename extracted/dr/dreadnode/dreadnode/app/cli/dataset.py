"""Dataset subcommands for the cyclopts CLI."""

import typing as t
from pathlib import Path

import cyclopts
from rich.table import Table

from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _FLAG_SEARCH,
    ArtifactRef,
    _collect_pages,
    _hint,
    _print_json,
    _render_list,
    _visibility_markup,
    configured_dreadnode,
    confirm_destructive,
    console,
    ensure_name_only_refs,
    ensure_version,
    print_success,
    resolve_publish_flag,
)

cli = cyclopts.App(
    name="dataset",
    help="Versioned data for training, optimization, and evaluation — the ground truth your agents learn from.",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _summarize_dataset(p: dict[str, t.Any]) -> str:
    name = p.get("full_name") or p.get("name", "unknown")
    version = p.get("latest_version") or p.get("version", "unknown")
    visibility = p.get("visibility", "private")
    summary = p.get("summary")
    suffix = f" [dim]-[/dim] {summary}" if summary else ""
    return f"[cyan]{name}[/cyan]@[dim]{version}[/dim] {_visibility_markup(visibility)}{suffix}"


_DATASET_LIST_ROW_FIELDS: tuple[str, ...] = (
    "full_name",
    "summary",
    "visibility",
    "type",
    "package_type",
    "latest_version",
    "created_at",
    "updated_at",
)


# ---------------------------------------------------------------------------
# inspect
# ---------------------------------------------------------------------------


@cli.command()
def inspect(
    path: Path,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
) -> None:
    """Preview a local dataset directory before publishing.

    Reads dataset.yaml and the data files to show schema, row counts,
    splits, and format — so you can catch problems before pushing.

    Args:
        path: Dataset directory containing dataset.yaml.
        as_json: Output raw JSON instead of a table.
    """
    from dreadnode.datasets.local import LocalDataset
    from dreadnode.storage.storage import Storage

    resolved = path.resolve()
    if not resolved.is_dir():
        raise FileNotFoundError(f"Directory not found: {resolved}")
    if not (resolved / "dataset.yaml").exists():
        raise FileNotFoundError(f"No dataset.yaml found in {resolved}")

    storage = Storage()
    ds = LocalDataset.from_dir(resolved, storage)

    if as_json:
        _print_json(
            {
                "name": ds.name,
                "version": ds.version,
                "format": ds.format,
                "row_count": ds.row_count,
                "splits": ds.splits,
                "schema": ds.schema,
                "files": ds.files,
            }
        )
        return

    console.print(f"[cyan]{ds.name}[/cyan]@[dim]{ds.version}[/dim]")
    console.print(f"  [dim]format:[/dim]  {ds.format}")
    if ds.row_count is not None:
        console.print(f"  [dim]rows:[/dim]    {ds.row_count:,}")
    if ds.splits:
        console.print(f"  [dim]splits:[/dim]  {', '.join(ds.splits)}")

    if ds.schema:
        console.print()
        table = Table(title="Schema", show_header=True, title_style="bold")
        table.add_column("Column", style="cyan")
        table.add_column("Type", style="dim")
        for col, dtype in ds.schema.items():
            table.add_row(col, dtype)
        console.print(table)


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------


@cli.command(alias="upload")
def push(
    path: Path | None = None,
    *,
    hf: str | None = None,
    hf_config: str | None = None,
    hf_split: str = "train",
    user_field: str | None = None,
    assistant_field: str | None = None,
    system_prompt: str | None = None,
    name: str | None = None,
    dataset_version: t.Annotated[
        str,
        cyclopts.Parameter(name="--dataset-version"),
    ] = "0.1.0",
    summary: str | None = None,
    hf_format: t.Annotated[
        t.Literal["parquet", "jsonl"],
        cyclopts.Parameter(
            name="--hf-format",
            help=(
                "Output format for --hf pushes. Defaults to parquet "
                "(the platform default). jsonl writes line-delimited JSON."
            ),
        ),
    ] = "parquet",
    skip_upload: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Publish a dataset to your organization's registry.

    Two input shapes (mutually exclusive):

    - **Local directory**: ``dn dataset push <dir>`` — packages a directory
      with ``dataset.yaml`` and data files as a versioned artifact.
    - **HuggingFace**: ``dn dataset push --hf <hf_path> [--hf-split ...]
      [--user-field ...] [--assistant-field ...]`` — pulls a dataset from
      HuggingFace Hub and pushes it under ``--name`` (default: the HF
      path). When both ``--user-field`` and ``--assistant-field`` are set,
      rows are transformed to OpenAI messages format for Tinker SFT.

    Args:
        path: Dataset directory (mutually exclusive with --hf).
        hf: HuggingFace dataset path, e.g. ``"openai/gsm8k"``.
        hf_config: Optional HF config (e.g. ``"main"`` for gsm8k).
        hf_split: HF split spec (``"train"``, ``"train[:100]"``, etc).
        user_field: Row field → user message (requires assistant_field).
        assistant_field: Row field → assistant message.
        system_prompt: Optional system message prepended to each conversation.
        name: Override the registry name.
        dataset_version: Registry version string (renamed from ``version`` to
            avoid collision with the CLI's global ``--version`` flag).
        summary: Optional human-readable summary.
        skip_upload: Build and validate locally without publishing.
        publish: Ensure the dataset is publicly discoverable after publishing.
    """
    if (path is None) == (hf is None):
        raise ValueError("provide either a dataset directory or --hf <path>, not both")

    publish = resolve_publish_flag(publish, public_compat)
    dn = configured_dreadnode(platform)
    if hf is not None:
        result = dn.push_hf_dataset(
            hf,
            config=hf_config,
            split=hf_split,
            name=name,
            version=dataset_version,
            summary=summary,
            user_field=user_field,
            assistant_field=assistant_field,
            system_prompt=system_prompt,
            format=hf_format,
            skip_upload=skip_upload,
            publish=publish,
        )
    else:
        assert path is not None  # narrow for type-checker
        result = dn.push_dataset(path, name=name, skip_upload=skip_upload, publish=publish)
    if not result.success:
        raise RuntimeError("; ".join(result.errors) or "Dataset push failed")

    if result.package_name is None or result.package_version is None:
        raise RuntimeError("Dataset push returned incomplete metadata")

    ref = f"[cyan]{result.package_name}[/cyan]@[dim]{result.package_version}[/dim]"
    if skip_upload or not dn.can_sync:
        console.print(f"Built {ref}")
        return

    digest = result.manifest_digest or "unknown"
    console.print(f"Pushed {ref} [dim]({digest})[/dim]")


@cli.command()
def publish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more dataset families visible to other organizations."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_dataset_visibility(ref.org, ref.name, is_public=True)
        print_success(f"Published {ref.qualified_name}")


@cli.command()
def unpublish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more dataset families private."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_dataset_visibility(ref.org, ref.name, is_public=False)
        print_success(f"Unpublished {ref.qualified_name}")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    search: t.Annotated[str | None, cyclopts.Parameter(name=_FLAG_SEARCH)] = None,
    limit: int = 50,
    include_public: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show datasets in your organization.

    Args:
        search: Search by name or description.
        limit: Maximum results to show.
        include_public: Include public datasets from other organizations.
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_datasets(
            profile.org_key,
            search=search,
            page=page,
            limit=page_size,
            include_public=include_public,
        ),
        limit=limit,
        page_size=200,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_dataset,
        empty_msg="No datasets found",
        fields=_DATASET_LIST_ROW_FIELDS,
    )
    if not as_json and items:
        example = items[0].get("name", "<name>")
        _hint(f"dn dataset info {example}")


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------


@cli.command()
def info(
    ref: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show details and available versions for a dataset.

    Version is optional — defaults to the latest.

    Args:
        ref: Dataset to inspect (e.g. my-dataset, my-dataset@1.0.0).
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    vref = ensure_version(api, "dataset", ArtifactRef.parse(ref, profile.org_key))

    detail = api.get_dataset(vref.org, vref.name, vref.version)
    versions_payload = api.list_dataset_versions(vref.org, vref.name)

    if as_json:
        payload = detail.model_dump(mode="json") if hasattr(detail, "model_dump") else detail
        payload["available_versions"] = versions_payload.get("versions", [])
        _print_json(payload)
        return

    console.print(
        _summarize_dataset(
            detail.model_dump(mode="json") if hasattr(detail, "model_dump") else detail
        )
    )
    version_items = versions_payload.get("versions", [])
    if version_items:
        console.print(f"  [dim]versions:[/dim] {', '.join(str(v) for v in version_items)}")
    _hint(f"dn dataset pull {vref.qualified_name}")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    ref: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Remove a dataset version from the registry.

    Args:
        ref: Dataset to delete (e.g. my-dataset@1.0.0). Version is required.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    # Verify it exists before prompting
    api.get_dataset(vref.org, vref.name, vref.version)

    if not confirm_destructive(f"Delete {vref.format()}?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    api.delete_dataset(vref.org, vref.name, vref.version)
    print_success(f"Deleted {vref.format()}")


# ---------------------------------------------------------------------------
# pull
# ---------------------------------------------------------------------------


@cli.command(alias="download")
def pull(
    ref: str,
    *,
    output: Path | None = None,
    split: str | None = None,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Pull a dataset to your local machine.

    Version is optional — defaults to the latest. Without --output, prints
    a pre-signed download URL you can use with curl or a browser.

    Args:
        ref: Dataset to pull (e.g. my-dataset, my-dataset@1.0.0).
        output: Save to this path instead of printing the URL.
        split: Download a specific split (e.g. train, test).
    """
    import urllib.request

    api, profile = platform.connect()
    vref = ensure_version(api, "dataset", ArtifactRef.parse(ref, profile.org_key))

    result = api.download_dataset(vref.org, vref.name, vref.version, split=split)
    url = result.get("url")
    if not url:
        raise RuntimeError(f"Download not ready: {result.get('status', 'unknown')}")

    if output:
        console.print(f"Downloading {vref.format()}...")
        urllib.request.urlretrieve(url, str(output))  # noqa: S310
        print_success(f"Saved to {output}")
    else:
        console.print(f"[dim]Download URL (expires {result.get('expires_at', 'soon')}):[/dim]")
        console.print(url)
