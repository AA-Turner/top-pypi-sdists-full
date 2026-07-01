"""Model subcommands for the cyclopts CLI."""

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
    name="model",
    help="Fine-tuned weights and adapters — checkpoints from training, LoRAs, and quantized models ready for deployment.",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _summarize_model(p: dict[str, t.Any]) -> str:
    name = p.get("full_name") or p.get("name", "unknown")
    version = p.get("latest_version") or p.get("version", "unknown")
    visibility = p.get("visibility", "private")
    summary = p.get("summary")
    suffix = f" [dim]-[/dim] {summary}" if summary else ""
    return f"[cyan]{name}[/cyan]@[dim]{version}[/dim] {_visibility_markup(visibility)}{suffix}"


_MODEL_LIST_ROW_FIELDS: tuple[str, ...] = (
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
    """Preview a local model directory before publishing.

    Reads model.yaml and the artifact files to show framework, task,
    architecture, and file listing — so you can catch problems before
    pushing.

    Args:
        path: Model directory containing model.yaml.
        as_json: Output raw JSON instead of a table.
    """
    from dreadnode.models.local import LocalModel
    from dreadnode.storage.storage import Storage

    resolved = path.resolve()
    if not resolved.is_dir():
        raise FileNotFoundError(f"Directory not found: {resolved}")
    if not (resolved / "model.yaml").exists():
        raise FileNotFoundError(f"No model.yaml found in {resolved}")

    storage = Storage()
    model = LocalModel.from_dir(resolved, storage)

    if as_json:
        _print_json(
            {
                "name": model.name,
                "version": model.version,
                "framework": model.framework,
                "task": model.task,
                "architecture": model.architecture,
                "files": model.files,
            }
        )
        return

    console.print(f"[cyan]{model.name}[/cyan]@[dim]{model.version}[/dim]")
    console.print(f"  [dim]framework:[/dim]    {model.framework}")
    if model.task:
        console.print(f"  [dim]task:[/dim]         {model.task}")
    if model.architecture:
        console.print(f"  [dim]architecture:[/dim] {model.architecture}")

    if model.files:
        console.print()
        table = Table(title="Files", show_header=True, title_style="bold")
        table.add_column("Path", style="cyan")
        for f in model.files:
            table.add_row(f)
        console.print(table)


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------


@cli.command(alias="upload")
def push(
    path: Path,
    *,
    name: str | None = None,
    skip_upload: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Publish a model to your organization's registry.

    Packages a model directory (with model.yaml manifest) and uploads it
    as a versioned artifact. Supports LoRA adapters, quantized checkpoints,
    and full model weights.

    Args:
        path: Model directory containing model.yaml.
        name: Override the registry name.
        skip_upload: Build and validate locally without publishing.
        publish: Ensure the model is publicly discoverable after publishing.
    """
    publish = resolve_publish_flag(publish, public_compat)
    dn = configured_dreadnode(platform)
    result = dn.push_model(path, name=name, skip_upload=skip_upload, publish=publish)
    if not result.success:
        raise RuntimeError("; ".join(result.errors) or "Model push failed")

    if result.package_name is None or result.package_version is None:
        raise RuntimeError("Model push returned incomplete metadata")

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
    """Make one or more model families visible to other organizations."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_model_visibility(ref.org, ref.name, is_public=True)
        print_success(f"Published {ref.qualified_name}")


@cli.command()
def unpublish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more model families private."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_model_visibility(ref.org, ref.name, is_public=False)
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
    """Show models in your organization.

    Args:
        search: Search by name or description.
        limit: Maximum results to show.
        include_public: Include public models from other organizations.
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_models(
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
        summary=_summarize_model,
        empty_msg="No models found",
        fields=_MODEL_LIST_ROW_FIELDS,
    )
    if not as_json and items:
        example = items[0].get("name", "<name>")
        _hint(f"dn model info {example}")


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
    """Show details and available versions for a model.

    Version is optional — defaults to the latest.

    Args:
        ref: Model to inspect (e.g. my-model, my-model@1.0.0).
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    vref = ensure_version(api, "model", ArtifactRef.parse(ref, profile.org_key))

    detail = api.get_model(vref.org, vref.name, vref.version)
    versions_payload = api.list_model_versions(vref.org, vref.name)

    if as_json:
        payload = detail.model_dump(mode="json") if hasattr(detail, "model_dump") else detail
        payload["available_versions"] = versions_payload.get("versions", [])
        _print_json(payload)
        return

    console.print(
        _summarize_model(
            detail.model_dump(mode="json") if hasattr(detail, "model_dump") else detail
        )
    )
    version_items = versions_payload.get("versions", [])
    if version_items:
        console.print(f"  [dim]versions:[/dim] {', '.join(str(v) for v in version_items)}")
    _hint(f"dn model pull {vref.qualified_name}")


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


@cli.command()
def compare(
    ref: str,
    versions: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Compare model versions side-by-side with metrics.

    Shows a table of framework, task, metrics, aliases, and more across
    2-5 versions. Essential for picking the best checkpoint after a
    training run.

    Args:
        ref: Model name (e.g. my-model).
        versions: Versions to compare (2-5, e.g. 1.0.0 2.0.0 3.0.0).
        as_json: Output raw JSON instead of a table.
    """
    if len(versions) < 2:
        raise ValueError("At least 2 versions required for comparison")
    if len(versions) > 5:
        raise ValueError("At most 5 versions can be compared")

    api, profile = platform.connect()
    parsed = ArtifactRef.parse(ref, profile.org_key)

    result = api.compare_model_versions(parsed.org, parsed.name, versions)

    if as_json:
        _print_json(result)
        return

    items = result.get("versions", [])
    metric_keys = result.get("metric_keys", [])

    table = Table(
        title=f"[cyan]{parsed.name}[/cyan] version comparison",
        show_header=True,
        title_style="bold",
    )
    table.add_column("", style="bold")
    for item in items:
        table.add_column(item["version"], justify="right")

    # Fixed rows
    table.add_row("framework", *[item.get("framework", "-") for item in items])
    if any(item.get("task") for item in items):
        table.add_row("task", *[item.get("task") or "-" for item in items])
    if any(item.get("architecture") for item in items):
        table.add_row("architecture", *[item.get("architecture") or "-" for item in items])
    if any(item.get("base_model") for item in items):
        table.add_row("base model", *[item.get("base_model") or "-" for item in items])
    if any(item.get("file_size_bytes") for item in items):
        table.add_row(
            "size",
            *[
                f"{item['file_size_bytes'] / 1_048_576:.1f} MB"
                if item.get("file_size_bytes")
                else "-"
                for item in items
            ],
        )
    if any(item.get("aliases") for item in items):
        table.add_row(
            "aliases",
            *[", ".join(item.get("aliases") or []) or "-" for item in items],
        )

    # Metric rows
    for key in metric_keys:
        values = []
        for item in items:
            metrics = item.get("metrics") or {}
            val = metrics.get(key)
            values.append(str(val) if val is not None else "-")
        table.add_row(f"[yellow]{key}[/yellow]", *values)

    console.print(table)


# ---------------------------------------------------------------------------
# alias
# ---------------------------------------------------------------------------


@cli.command()
def alias(
    ref: str,
    name: str,
    *,
    remove: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Tag a model version with a named alias like 'champion' or 'staging'.

    Aliases let you reference a model version by role instead of number.
    Setting an alias that already exists on another version moves it
    automatically.

    Args:
        ref: Model version (e.g. my-model@1.0.0). Version is required.
        name: Alias name (e.g. champion, staging, latest-stable).
        remove: Remove the alias instead of setting it.
    """
    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    if remove:
        api.remove_model_alias(vref.org, vref.name, vref.version, name)
        print_success(f"Removed alias [yellow]{name}[/yellow] from {vref.format()}")
    else:
        api.set_model_alias(vref.org, vref.name, vref.version, name)
        print_success(f"[yellow]{name}[/yellow] → {vref.format()}")


# ---------------------------------------------------------------------------
# metrics
# ---------------------------------------------------------------------------


@cli.command()
def metrics(
    ref: str,
    *args: str,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Attach evaluation metrics to a model version.

    Pass metrics as key=value pairs. Numeric values are stored as numbers.
    Existing metrics are merged — keys you don't mention are preserved.

    Args:
        ref: Model version (e.g. my-model@1.0.0). Version is required.
        args: Metrics as key=value pairs (e.g. accuracy=0.95 f1=0.88).
        as_json: Output updated model detail as JSON.
    """
    if not args:
        raise ValueError("At least one metric required (e.g. accuracy=0.95)")

    metrics_dict: dict[str, float | int | str] = {}
    for arg in args:
        if "=" not in arg:
            raise ValueError(f"Invalid metric format: {arg!r} — expected key=value")
        key, value = arg.split("=", 1)
        try:
            parsed_val: float | int | str = int(value)
        except ValueError:
            try:
                parsed_val = float(value)
            except ValueError:
                parsed_val = value
        metrics_dict[key.strip()] = parsed_val

    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    result = api.update_model_metrics(vref.org, vref.name, vref.version, metrics_dict)

    if as_json:
        _print_json(result)
        return

    pairs = [f"[yellow]{k}[/yellow]={v}" for k, v in metrics_dict.items()]
    print_success(f"Updated {vref.format()}: {', '.join(pairs)}")


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
    """Remove a model version from the registry.

    Args:
        ref: Model to delete (e.g. my-model@1.0.0). Version is required.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    # Verify it exists before prompting
    api.get_model(vref.org, vref.name, vref.version)

    if not confirm_destructive(f"Delete {vref.format()}?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    api.delete_model(vref.org, vref.name, vref.version)
    print_success(f"Deleted {vref.format()}")


# ---------------------------------------------------------------------------
# pull
# ---------------------------------------------------------------------------


@cli.command(alias="download")
def pull(
    ref: str,
    *,
    output: Path | None = None,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Pull a model to your local machine.

    Version is optional — defaults to the latest. Without --output, prints
    a pre-signed download URL you can use with curl or a browser.

    Args:
        ref: Model to pull (e.g. my-model, my-model@1.0.0).
        output: Save to this path instead of printing the URL.
    """
    import urllib.request

    api, profile = platform.connect()
    vref = ensure_version(api, "model", ArtifactRef.parse(ref, profile.org_key))

    result = api.download_model(vref.org, vref.name, vref.version)
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
