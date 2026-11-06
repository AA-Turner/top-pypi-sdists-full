"""Wait for a checkpoint export, then download and extract its ZIP.

Beta: built on the `checkpoint-exports-2026-10-29` beta API, so these helpers may change in a
minor release. Your organization needs checkpoint exports enabled.
"""

from __future__ import annotations

import math
import shutil
import tempfile
import time
import zipfile
from contextlib import nullcontext
from pathlib import Path

import httpx2

from trajectory import Client
from trajectory._exceptions import TrajectoryError
from trajectory.types.beta.checkpoint_exports.checkpoint_export import CheckpointExport

DEFAULT_DOWNLOAD_TIMEOUT = 600.0
_PENDING = {"queued", "preparing"}
_CHUNK_BYTES = 8 * 1024 * 1024


class CheckpointExportError(TrajectoryError):
  """A checkpoint export failed or has no download link."""

  def __init__(self, message: str, *, export: CheckpointExport) -> None:
    super().__init__(message)
    self.message = message
    self.export = export


def wait_for_checkpoint_export(
  client: Client,
  checkpoint_id: str,
  *,
  timeout: float | None = 3600,
  poll_interval: float = 5,
) -> CheckpointExport:
  """Create or reuse the checkpoint's export and wait until it is ready.

  timeout bounds the wait for the export to become ready, in seconds; each API request
  keeps the client's own timeout and retries.
  """
  if timeout is not None and (timeout < 0 or not math.isfinite(timeout)):
    raise ValueError("timeout must be finite and non-negative, or None")
  if poll_interval <= 0 or not math.isfinite(poll_interval):
    raise ValueError("poll_interval must be positive and finite")
  deadline = None if timeout is None else time.monotonic() + timeout
  export = client.beta.checkpoint_exports.create(checkpoint_id)
  while export.state in _PENDING:
    remaining = None if deadline is None else deadline - time.monotonic()
    if remaining is not None and remaining <= 0:
      raise TimeoutError(
        f"Timed out waiting for export {export.export_id}; the server keeps preparing it"
      )
    time.sleep(poll_interval if remaining is None else min(poll_interval, remaining))
    export = client.beta.checkpoint_exports.retrieve(export.export_id)
  if export.state == "failed":
    raise CheckpointExportError(
      f"Checkpoint export {export.export_id} failed; call again to retry it", export=export
    )
  # Creating an export that is already ready returns it without a download link.
  if export.download is None:
    export = client.beta.checkpoint_exports.retrieve(export.export_id)
  if export.download is None:
    raise CheckpointExportError(f"Export {export.export_id} has no download link", export=export)
  return export


def download_checkpoint(
  client: Client,
  checkpoint_id: str,
  output_dir: str | Path = ".",
  *,
  overwrite: bool = False,
  timeout: float | None = 3600,
  poll_interval: float = 5,
  http_client: httpx2.Client | None = None,
) -> Path:
  """Download the checkpoint and extract it into output_dir/<checkpoint_id>/.

  The directory holds the adapter files and manifest.json. An existing directory raises
  FileExistsError unless overwrite is set.
  """
  output_dir = Path(output_dir)
  target = output_dir / checkpoint_id
  if (target.exists() or target.is_symlink()) and not overwrite:
    raise FileExistsError(f"{target} already exists; pass overwrite=True to replace it")
  export = wait_for_checkpoint_export(
    client, checkpoint_id, timeout=timeout, poll_interval=poll_interval
  )
  assert export.download is not None
  output_dir.mkdir(parents=True, exist_ok=True)
  http_context = (
    nullcontext(http_client)
    if http_client is not None
    else httpx2.Client(timeout=DEFAULT_DOWNLOAD_TIMEOUT)
  )
  # The ZIP and its extraction share a temporary directory next to target, so a failed call
  # leaves nothing behind and the rename into place stays on one filesystem.
  with tempfile.TemporaryDirectory(dir=output_dir) as temp_dir:
    zip_path = Path(temp_dir) / "checkpoint.zip"
    with http_context as http:
      with http.stream("GET", export.download.url, follow_redirects=True) as response:
        response.raise_for_status()
        with zip_path.open("wb") as output:
          for chunk in response.iter_bytes(_CHUNK_BYTES):
            output.write(chunk)
    extracted = Path(temp_dir) / checkpoint_id
    # Extraction checks each file's CRC, so a corrupt download raises zipfile.BadZipFile.
    with zipfile.ZipFile(zip_path) as zip_file:
      zip_file.extractall(extracted)
    if overwrite and target.is_dir() and not target.is_symlink():
      shutil.rmtree(target)
    elif overwrite:
      target.unlink(missing_ok=True)
    extracted.rename(target)
  return target
