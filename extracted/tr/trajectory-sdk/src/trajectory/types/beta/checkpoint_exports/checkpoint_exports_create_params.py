# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypedDict


class CheckpointExportsCreateParams(TypedDict, total=False):
  export_type: Literal["lora_adapter", "merged_model"]
  """
  lora_adapter downloads the adapter weights as one ZIP. merged_model downloads the full base
  model with the adapter merged in, as a Hugging Face folder of files, which is far larger and
  takes longer to prepare.
  """
  precision: Literal["bf16", "f32", "mxfp8", "nvfp4"] | None
  """
  The merged model's weight format, from the checkpoint's available_merge_precisions. Only
  merged_model exports take one, and they default to bf16.
  """
