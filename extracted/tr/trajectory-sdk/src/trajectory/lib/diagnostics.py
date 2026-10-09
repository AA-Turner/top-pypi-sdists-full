"""One-task diagnostic submission with optional local runtime files."""

from pathlib import Path

from trajectory import BenchmarkSpec, Client, TaskSpec, omit
from trajectory.lib.benchmarks import _BenchmarkPackage, wait_for_benchmark_images
from trajectory.lib.files import UPLOAD_BATCH_FILES, put_files
from trajectory.types.start_benchmark_diagnostics_response import StartBenchmarkDiagnosticsResponse


def start_task_diagnostic(
  client: Client,
  task: TaskSpec,
  agent_id: str,
  root: Path = Path("."),
  base_model_slug: str | None = None,
  timeout_seconds: float = 1800,
) -> StartBenchmarkDiagnosticsResponse:
  """Upload one task, wait for its runtime build, and start its diagnostic run."""
  if timeout_seconds < 0:
    raise ValueError("timeout_seconds must be non-negative")
  package = _BenchmarkPackage(BenchmarkSpec(name="task-diagnostic", tasks=[task]), root)
  files = package.files()
  bench_id = None
  for offset in range(0, len(files), UPLOAD_BATCH_FILES):
    batch = files[offset : offset + UPLOAD_BATCH_FILES]
    upload = client.benchmarks.create_upload(
      files=[file.declaration() for file in batch], bench_id=bench_id or omit
    )
    put_files(batch, upload.urls, max_retries=client.max_retries)
    bench_id = upload.bench_id

  registered = client.diagnostics.ingest_task(
    agent_id=agent_id, task=package.manifest.tasks[0], bench_id=bench_id or omit
  )
  wait_for_benchmark_images(client, registered.bench_id, timeout_seconds=timeout_seconds)
  return client.diagnostics.start_task(
    bench_id=registered.bench_id,
    base_model_slug=base_model_slug if base_model_slug is not None else omit,
  )
