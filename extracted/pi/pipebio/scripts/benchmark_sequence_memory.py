"""Benchmark PipeBio sequence-download paths in isolated processes.

Each invocation measures one method and its associated local resource use.
Run every case in a fresh process so ``ru_maxrss`` is comparable. The
``legacy`` mode intentionally requires an explicit acknowledgement because it
builds every sequence record in memory and can exhaust the host.

This is a developer-only script and runs on POSIX hosts only: it reports peak
memory through the standard-library ``resource`` module, which is unavailable
on Windows.

Examples:
    Default Parquet-backed record streaming:
    uv run python scripts/benchmark_sequence_memory.py stream \
        --entity-id ent_dGxiDi2OnvQJbkSr \
        --project-id d5406aa3-fd24-448f-a5cf-161cbfb2db88

    Raw ExportJob artifact download:
    uv run python scripts/benchmark_sequence_memory.py export \
        --entity-id ent_dGxiDi2OnvQJbkSr \
        --project-id d5406aa3-fd24-448f-a5cf-161cbfb2db88 \
        --export-format parquet

    Legacy full in-memory map (do not use with a large entity on a low-memory
    machine):
    uv run python scripts/benchmark_sequence_memory.py legacy \
        --entity-id ent_dGxiDi2OnvQJbkSr \
        --project-id d5406aa3-fd24-448f-a5cf-161cbfb2db88 \
        --confirm-legacy-memory-risk
"""

import argparse
import json
import os
import resource
import sys
import tempfile
import threading
import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from pipebio.models.export_format import ExportFormat
from pipebio.pipebio_client import PipebioClient

DEFAULT_DISK_SAMPLE_INTERVAL_SECONDS = 0.05


def peak_rss_bytes() -> int:
    """Return the process high-water RSS mark in bytes."""
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value * 1024


def bytes_to_mib(value: Optional[int]) -> Optional[float]:
    """Convert a byte count to MiB without inventing a value for absent output."""
    return None if value is None else round(value / (1024 * 1024), 2)


def path_size_bytes(path: Path) -> int:
    """Return the byte size of one file or all regular files below a directory."""
    if path.is_file():
        return path.stat().st_size
    if not path.exists():
        return 0

    total = 0
    for child in path.rglob('*'):
        try:
            if child.is_file():
                total += child.stat().st_size
        except OSError:
            # Files may disappear while a temporary export directory is cleaned
            # up. The next sampler pass will observe the remaining files.
            pass
    return total


class DiskUsageSampler:
    """Track the maximum file bytes below one benchmark workspace."""

    def __init__(self, directory: Path, interval_seconds: float) -> None:
        self.directory = directory
        self.interval_seconds = interval_seconds
        self.peak_bytes = 0
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def sample(self) -> int:
        """Sample disk usage once and return the observed byte count."""
        observed = path_size_bytes(self.directory)
        self.peak_bytes = max(self.peak_bytes, observed)
        return observed

    def start(self) -> None:
        """Start periodic sampling."""
        self.sample()
        self._thread = threading.Thread(
            target=self._run,
            name='pipebio-benchmark-disk-sampler',
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop sampling and include a final workspace measurement."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
        self.sample()

    def _run(self) -> None:
        while not self._stop_event.wait(self.interval_seconds):
            self.sample()


@contextmanager
def benchmark_workspace(parent: Optional[str]) -> Iterator[Path]:
    """Create an isolated workspace and direct SDK temporary files into it."""
    parent_path = Path(parent).expanduser() if parent else None
    if parent_path is not None:
        parent_path.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix='pipebio-benchmark-',
        dir=parent_path,
    ) as directory:
        previous_tempdir = tempfile.tempdir
        tempfile.tempdir = directory
        try:
            yield Path(directory)
        finally:
            tempfile.tempdir = previous_tempdir


@dataclass
class BenchmarkOutcome:
    """Method-specific data collected before the temporary workspace is removed."""

    method: str
    format: Optional[ExportFormat]
    record_count: Optional[int] = None
    first_compound_id: Optional[str] = None
    output_paths: List[Path] = field(default_factory=list)


def build_client(args: argparse.Namespace) -> PipebioClient:
    """Create a client and confirm the entity is in the expected project."""
    url = args.url or os.environ.get("PIPE_API_URL")
    if not url:
        raise ValueError("Provide --url or set PIPE_API_URL.")

    client = PipebioClient(url=url)
    entity = client.entities.get(args.entity_id)
    owner_id = entity.get("ownerId")
    if owner_id != args.project_id:
        raise ValueError(
            f"Entity {args.entity_id} belongs to project {owner_id!r}, not "
            f"{args.project_id!r}."
        )
    return client


def stream_records(
    client: PipebioClient,
    entity_id: str,
    progress_every: int,
    timeout_seconds: Optional[int],
) -> Tuple[int, str]:
    """Consume the ExportJob-backed iterator without retaining records."""
    first_compound_id = ""
    count = 0
    for count, (compound_id, _record) in enumerate(
        client.iter_sequence_records(
            [entity_id],
            timeout_seconds=timeout_seconds,
        ),
        start=1,
    ):
        if not first_compound_id:
            first_compound_id = compound_id
        if count % progress_every == 0:
            print(f"streamed {count:,} records", file=sys.stderr, flush=True)
    return count, first_compound_id


def load_legacy_records(client: PipebioClient, entity_id: str) -> Tuple[int, str]:
    """Run the memory-intensive legacy method."""
    warnings.simplefilter("default", DeprecationWarning)
    records = client.sequences.download_to_memory([entity_id])
    first_compound_id = next(iter(records), "")
    return len(records), first_compound_id


def run_download(
    client: PipebioClient,
    entity_id: str,
    output_directory: Path,
) -> BenchmarkOutcome:
    """Run the deprecated disk-download path."""
    destination = output_directory / 'sequences.tsv'
    output_path = client.sequences.download(
        entity_id,
        destination=str(destination),
    )
    return BenchmarkOutcome(
        method='Sequences.download',
        format=ExportFormat.TSV,
        output_paths=[Path(output_path)],
    )


def run_export(
    client: PipebioClient,
    entity_id: str,
    output_directory: Path,
    export_format: ExportFormat,
    timeout_seconds: Optional[int],
) -> BenchmarkOutcome:
    """Run a raw ExportJob artifact download without decoding it."""
    destination_filename = (
        'sequences.tsv' if export_format == ExportFormat.TSV else 'sequences.zip'
    )
    output_paths = client.export(
        entity_id,
        export_format,
        destination_folder=str(output_directory),
        destination_filename=destination_filename,
        timeout_seconds=timeout_seconds,
    )
    return BenchmarkOutcome(
        method='PipebioClient.export',
        format=export_format,
        output_paths=[Path(path) for path in output_paths],
    )


def run_stream(
    client: PipebioClient,
    entity_id: str,
    progress_every: int,
    timeout_seconds: Optional[int],
) -> BenchmarkOutcome:
    """Run the ExportJob-backed streaming record reader."""
    count, first_compound_id = stream_records(
        client,
        entity_id,
        progress_every,
        timeout_seconds,
    )
    return BenchmarkOutcome(
        method='PipebioClient.iter_sequence_records',
        format=ExportFormat.PARQUET,
        record_count=count,
        first_compound_id=first_compound_id,
    )


def run_legacy(client: PipebioClient, entity_id: str) -> BenchmarkOutcome:
    """Run the deprecated full in-memory record map."""
    count, first_compound_id = load_legacy_records(client, entity_id)
    return BenchmarkOutcome(
        method='Sequences.download_to_memory',
        format=ExportFormat.TSV,
        record_count=count,
        first_compound_id=first_compound_id,
    )


def run_case(
    args: argparse.Namespace,
    client: PipebioClient,
    output_directory: Path,
) -> BenchmarkOutcome:
    """Dispatch the selected benchmark mode."""
    if args.mode == 'download':
        return run_download(client, args.entity_id, output_directory)
    if args.mode == 'export':
        return run_export(
            client,
            args.entity_id,
            output_directory,
            ExportFormat[args.export_format.upper()],
            args.timeout_seconds,
        )
    if args.mode == 'stream':
        return run_stream(
            client,
            args.entity_id,
            args.progress_every,
            args.timeout_seconds,
        )

    if not args.confirm_legacy_memory_risk:
        raise ValueError(
            'Legacy mode can exhaust memory for large documents. Re-run with '
            '--confirm-legacy-memory-risk to proceed.'
        )
    return run_legacy(client, args.entity_id)


def run(args: argparse.Namespace) -> Dict[str, Any]:
    """Run one benchmark mode and return a machine-readable result."""
    client = build_client(args)
    started = time.monotonic()

    with benchmark_workspace(args.work_directory) as workspace:
        output_directory = workspace / 'output'
        output_directory.mkdir()
        sampler = DiskUsageSampler(
            workspace,
            args.disk_sample_interval_seconds,
        )
        sampler.start()
        try:
            outcome = run_case(args, client, output_directory)
        finally:
            sampler.stop()

        artifact_output_bytes = (
            sum(path_size_bytes(path) for path in outcome.output_paths)
            if outcome.output_paths
            else None
        )

    return {
        'mode': args.mode,
        'method': outcome.method,
        'format': outcome.format.value if outcome.format else None,
        'entityId': args.entity_id,
        'projectId': args.project_id,
        'recordCount': outcome.record_count,
        'firstCompoundId': outcome.first_compound_id,
        'artifactOutputBytes': artifact_output_bytes,
        'artifactOutputMiB': bytes_to_mib(artifact_output_bytes),
        'peakTempDiskBytes': sampler.peak_bytes,
        'peakTempDiskMiB': bytes_to_mib(sampler.peak_bytes),
        'exportFormat': args.export_format if args.mode == 'export' else None,
        'timeoutSeconds': args.timeout_seconds,
        'elapsedSeconds': round(time.monotonic() - started, 2),
        'peakRssMiB': round(peak_rss_bytes() / (1024 * 1024), 2),
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse benchmark options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('download', 'legacy', 'export', 'stream'))
    parser.add_argument('--entity-id', required=True)
    parser.add_argument('--project-id', required=True)
    parser.add_argument(
        '--url',
        help='PipeBio URL. Defaults to PIPE_API_URL.',
    )
    parser.add_argument(
        '--progress-every',
        type=int,
        default=1_000_000,
        help='Streaming progress interval. Defaults to 1,000,000 records.',
    )
    parser.add_argument(
        '--export-format',
        choices=('tsv', 'parquet'),
        default='tsv',
        help='ExportJob artifact format for export mode. Defaults to TSV.',
    )
    parser.add_argument(
        '--timeout-seconds',
        type=int,
        help='Optional ExportJob wait limit for export and stream modes.',
    )
    parser.add_argument(
        '--work-directory',
        help='Optional parent directory for the isolated temporary workspace.',
    )
    parser.add_argument(
        '--disk-sample-interval-seconds',
        type=float,
        default=DEFAULT_DISK_SAMPLE_INTERVAL_SECONDS,
        help='Temporary-disk sampling interval. Defaults to 0.05 seconds.',
    )
    parser.add_argument(
        '--confirm-legacy-memory-risk',
        action='store_true',
        help='Required to invoke the in-memory legacy method.',
    )
    args = parser.parse_args(argv)
    if args.progress_every <= 0:
        parser.error('--progress-every must be positive.')
    if args.timeout_seconds is not None and args.timeout_seconds <= 0:
        parser.error('--timeout-seconds must be positive.')
    if args.disk_sample_interval_seconds <= 0:
        parser.error('--disk-sample-interval-seconds must be positive.')
    return args


if __name__ == '__main__':
    arguments = parse_args()
    try:
        print(json.dumps(run(arguments), sort_keys=True))
    except (MemoryError, ValueError) as error:
        print(f'Benchmark failed: {error}', file=sys.stderr)
        raise SystemExit(2)
