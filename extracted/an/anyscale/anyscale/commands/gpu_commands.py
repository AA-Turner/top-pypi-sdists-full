"""`anyscale gpu get`, plus the GPU rendering `anyscale node gpus` shares.

One command over the backend's single-GPU endpoint: the GPU is addressed by UUID within
a cluster, and the backend checks read permission on that cluster.

Output is the model as the API returned it, in every format. Text is the model as YAML
(the same convention as `anyscale job status`), table is one row per GPU with a column
per field, json and yaml are the model. Field names and values are not rewritten.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the GPUs module in `_private/docgen/__main__.py`) publishes it.
"""

from dataclasses import fields
from datetime import datetime
import json
from typing import Any, Dict, List, Optional

import click

import anyscale
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import parse_timestamp
from anyscale.commands.util import AnyscaleCommand
from anyscale.gpus.models import Gpu, GpuPlacement, GpuTelemetry
from anyscale.util import AnyscaleJSONEncoder


OUTPUT_FORMATS = [OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML, OutputFormat.TABLE]

# Table columns: every field of a GPU's telemetry, under its API name, in model order.
GPU_COLUMNS: List[str] = [field.name for field in fields(GpuTelemetry)]
# `gpu get` adds the fields only the placement carries, plus the snapshot time.
_PLACEMENT_ONLY_COLUMNS: List[str] = [
    field.name
    for field in fields(GpuPlacement)
    if field.name not in {f.name for f in fields(GpuTelemetry)}
]
GPU_DETAIL_COLUMNS: List[str] = ["gpu_uuid", "time", *_PLACEMENT_ONLY_COLUMNS, *GPU_COLUMNS]


@click.group("gpu", help="Inspect a GPU of a cluster.", hidden=True)
def gpu_cli() -> None:
    pass


# --- shared flags and helpers, used by `anyscale node gpus` too -----------------------------

option_cluster_id = click.option(
    "--cluster-id", required=True, help="ID of the cluster, e.g. ses_abc123."
)
option_time = click.option(
    "--time",
    default=None,
    help="Snapshot as of this moment. ISO 8601, e.g. 2026-09-01T13:45:00Z. Defaults to "
    "now. The backend looks back over the cluster's lifetime (up to seven days), so a "
    "terminated or dead node still shows its last-known telemetry, as OFFLINE GPUs.",
)
option_output = click.option(
    "-o",
    "--output",
    "output_format",
    type=click.Choice([fmt.value for fmt in OUTPUT_FORMATS]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)


def beta_metadata(*examples: CommandExample):
    return command_metadata(
        status=ReleaseStatus.BETA,
        since="0.0.0",
        output_formats=OUTPUT_FORMATS,
        examples=list(examples),
    )


def print_text(model: Any) -> None:
    """The text format: the model as YAML, every field under its API name.

    Same as `-o yaml`, and the same convention `anyscale job status` follows. A field the
    API did not report (None) is left out, as in json.
    """
    print_output(model, OutputFormat.YAML.value)


def table_row(model: Any) -> Dict[str, Any]:
    """One table row: the model's fields as returned, flattened for a single cell each.

    A nested object or list (xids, workload) is written as compact JSON in its cell; a
    datetime as ISO 8601; a missing field as an empty cell.
    """
    # to_dict() leaves None out, as json does, so a nested object is written exactly as
    # `-o json` would; the top-level fields are then listed in full so every column exists.
    plain = model.to_dict()
    return {field.name: _cell(plain.get(field.name)) for field in fields(model)}


def _cell(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (dict, list)):
        return json.dumps(value, cls=AnyscaleJSONEncoder, separators=(",", ":"))
    if isinstance(value, float):
        # tabulate prints a float with 6 significant digits (15.910468656252082 as
        # 15.9105). Its text form is what json prints, and the table renderer keeps a
        # number-like string as given whenever parsing it would change the text.
        return repr(value)
    return value


# --- get -------------------------------------------------------------------------------------


@beta_metadata(
    CommandExample(
        description="Where a GPU is and what it reports right now.",
        command="anyscale gpu get --id GPU-8f2e... --cluster-id <cluster-id>",
    ),
    CommandExample(
        description="The same GPU during an incident.",
        command=(
            "anyscale gpu get --id GPU-8f2e... --cluster-id <cluster-id> "
            "--time 2026-09-01T13:45:00Z"
        ),
    ),
    CommandExample(
        description="JSON for scripts.",
        command="anyscale gpu get --id GPU-8f2e... --cluster-id <cluster-id> -o json",
    ),
)
@gpu_cli.command(name="get", cls=AnyscaleCommand, short_help="Get one GPU by UUID.")
@click.option(
    "--id",
    "--gpu-id",
    "gpu_uuid",
    required=True,
    help="UUID of the GPU (GPU-...), as the driver and DCGM report it.",
)
@option_cluster_id
@option_time
@option_output
def get(gpu_uuid: str, cluster_id: str, time: Optional[str], output_format: str) -> None:
    """Get one GPU of a cluster by UUID: its node and instance, the workload holding it,
    and its DCGM telemetry.

    The backend looks back over the cluster's lifetime (up to seven days), so a GPU whose
    node is already terminated still resolves, as OFFLINE with its last-known telemetry.
    Only a UUID the cluster never reported in that window is an error.
    """
    gpu = anyscale.gpus.get(cluster_id, gpu_uuid, time=parse_timestamp(time, "--time"))
    _print_gpu(gpu, output_format)


def _print_gpu(gpu: Gpu, output_format: str) -> None:
    if output_format == OutputFormat.TEXT.value:
        print_text(gpu)
        return
    if output_format == OutputFormat.TABLE.value:
        # One row: the placement and telemetry fields side by side.
        row = {
            "gpu_uuid": gpu.gpu_uuid,
            "time": _cell(gpu.time),
            **table_row(gpu.placement),
            **table_row(gpu.telemetry),
        }
        print_output([row], output_format, GPU_DETAIL_COLUMNS)
        return
    print_output(gpu, output_format)


__all__: List[str] = [
    "GPU_COLUMNS",
    "GPU_DETAIL_COLUMNS",
    "OUTPUT_FORMATS",
    "beta_metadata",
    "get",
    "gpu_cli",
    "option_cluster_id",
    "option_output",
    "option_time",
    "print_text",
    "table_row",
]
