"""Download a ready merged checkpoint export as a Hugging Face folder.

Beta: built on the `checkpoint-exports-2026-10-29` beta API, so this helper may change in a minor
release. Your organization needs merged checkpoint exports enabled.
"""

from __future__ import annotations

import base64
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath, PureWindowsPath

import pooch

from trajectory import Client
from trajectory.lib.beta.checkpoint_exports import DEFAULT_DOWNLOAD_TIMEOUT, CheckpointExportError
from trajectory.types.checkpoint_export_file import CheckpointExportFile

_CHUNK_BYTES = 8 * 1024 * 1024

# pooch logs each download's URL, and these signed links grant access until they expire.
pooch.get_logger().addFilter(lambda record: "X-Goog-Signature" not in record.getMessage())


def download_merged_export(
  client: Client,
  export_id: str,
  output_dir: str | Path = ".",
  *,
  overwrite: bool = False,
  max_workers: int = 8,
) -> Path:
  """Download a ready export's files into output_dir/<checkpoint_id>-merged-<precision>/.

  Files download in parallel and are checked against their MD5s. If a call fails, the files it
  finished stay in a hidden folder next to the target, and calling again downloads only the rest
  with fresh links. An existing target raises FileExistsError unless overwrite is set.
  """
  export = client.beta.checkpoint_exports.retrieve(export_id)
  if export.state != "ready" or export.export_type != "merged_model":
    raise CheckpointExportError(
      f"Export {export_id} is a {export.state} {export.export_type} export, not a ready "
      "merged_model one",
      export=export,
    )
  output_dir = Path(output_dir)
  target = output_dir / f"{export.checkpoint_id}-merged-{export.precision or 'bf16'}"
  if (target.exists() or target.is_symlink()) and not overwrite:
    raise FileExistsError(f"{target} already exists; pass overwrite=True to replace it")
  partial = output_dir / f".{target.name}.partial"
  files = list(client.beta.checkpoint_exports.list_files(export_id))

  def get_local_path(file: CheckpointExportFile) -> Path:
    path = PurePosixPath(file.path)
    if (
      path.is_absolute()
      or ".." in path.parts
      or "\\" in file.path
      or PureWindowsPath(file.path).drive
    ):
      raise ValueError(f"Unsafe export file path: {file.path!r}")
    return partial / path

  def download(file: CheckpointExportFile) -> None:
    local = get_local_path(file)
    # pooch skips a file that already has this hash, and checks the rest before keeping them.
    pooch.retrieve(
      file.url,
      f"md5:{base64.b64decode(file.md5).hex()}",
      fname=local.name,
      path=local.parent,
      downloader=pooch.HTTPDownloader(chunk_size=_CHUNK_BYTES, timeout=DEFAULT_DOWNLOAD_TIMEOUT),
    )

  for file in files:
    get_local_path(file)
  partial.mkdir(parents=True, exist_ok=True)
  with ThreadPoolExecutor(max_workers) as pool:
    list(pool.map(download, files))
  if overwrite and target.is_dir() and not target.is_symlink():
    shutil.rmtree(target)
  elif overwrite:
    target.unlink(missing_ok=True)
  partial.rename(target)
  return target
