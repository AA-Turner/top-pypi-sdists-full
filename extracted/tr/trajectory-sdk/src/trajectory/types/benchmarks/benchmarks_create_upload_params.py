# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Required, TypedDict

from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam


class BenchmarksCreateUploadParams(TypedDict, total=False):
  files: Required[Iterable[BenchmarkUploadFileParam]]
  """
  Files to sign upload URLs for, one URL returned per declared path.
  """
  bench_id: str | None
  """
  Omit to mint a new benchmark. Pass a bench_id returned by an earlier batch to add these files
  to that benchmark's upload prefix, which is how a file set larger than the per-request limit
  is uploaded. An already-ingested bench_id is rejected.
  """
