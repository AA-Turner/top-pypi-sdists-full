# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Required, TypedDict

from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam


class TasksAppendParams(TypedDict, total=False):
  """
  One batch of files to sign PUT urls for; the owning id comes from the path or is minted.
  """

  files: Required[Iterable[BenchmarkUploadFileParam]]
  """
  Files to sign upload URLs for, one URL returned per declared path.
  """
