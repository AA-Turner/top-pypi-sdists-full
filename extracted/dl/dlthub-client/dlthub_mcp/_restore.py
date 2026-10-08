"""Restore a pipeline's local state from its destination."""

from __future__ import annotations

# Python internals
import os
from contextlib import suppress
from dataclasses import dataclass

# Other libraries
import dlt
from dlt.common.runtime.run_context import active
from dlt.common.utils import set_working_dir

# Current package
from dlthub_mcp._client import tool_error


@dataclass(frozen=True)
class RestoredPipeline:
    """A pipeline whose state now lives in the local workspace.

    Attributes:
        pipeline_name: The name dlt's ``pipeline`` and ``dataset`` tools take.
        destination: The destination its state was read from.
        dataset: The dataset on that destination.
        workspace_dir: The workspace the state was restored into.
        schema_names: The schemas restored with it.
        default_schema_name: Its default schema.
    """

    pipeline_name: str
    destination: str
    dataset: str
    workspace_dir: str
    schema_names: tuple[str, ...]
    default_schema_name: str | None


def workspace_root() -> str:
    """Return the active workspace's directory.

    Returns:
        Its absolute path.

    Raises:
        Exception: A ``ToolError`` when there is none.
    """
    run_dir = active().run_dir
    if not run_dir or not os.path.isdir(run_dir):
        raise tool_error(
            "No active workspace directory. Run this from inside a dlt workspace."
        )
    return os.path.abspath(run_dir)


def restore_pipeline(
    pipeline_name: str, destination: str, dataset: str
) -> RestoredPipeline:
    """Sync a pipeline's state from its destination into the local workspace.

    Args:
        pipeline_name: The pipeline to restore.
        destination: The destination it loaded to.
        dataset: The dataset it loaded to.

    Returns:
        What was restored, and where.

    Raises:
        Exception: A ``ToolError`` when the destination is unreachable or holds
            no state for the pipeline.
    """
    root = workspace_root()
    # No pipelines dir is passed: a bare `dlt.attach` must find the state, and
    # credentials resolve from the workspace only with its root as cwd.
    with set_working_dir(root):
        try:
            pipeline = dlt.pipeline(
                pipeline_name=pipeline_name,
                destination=destination,
                dataset_name=dataset,
            )
            pipeline.sync_destination()
        except Exception as e:
            raise tool_error(
                f"Could not restore pipeline {pipeline_name!r} from dataset"
                f" {dataset!r} on destination {destination!r}: {e}. The"
                " workspace profile must hold credentials for that destination."
            ) from e

        # Still a first run means the destination held no state for it.
        if pipeline.first_run:
            with suppress(Exception):
                pipeline._wipe_working_folder()
            raise tool_error(
                f"Pipeline {pipeline_name!r} was not found in dataset"
                f" {dataset!r} on destination {destination!r}."
            )

        return RestoredPipeline(
            pipeline_name=pipeline_name,
            destination=destination,
            dataset=dataset,
            workspace_dir=root,
            schema_names=tuple(pipeline.schema_names),
            default_schema_name=pipeline.default_schema_name,
        )
