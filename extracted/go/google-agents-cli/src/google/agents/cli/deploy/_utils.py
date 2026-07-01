# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared utilities for deploy commands."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.agents.cli._project import ProjectConfig

# Shared machine-shape defaults for the imperative deploy paths: the deploy
# command (Cloud Run) and deploy_agent_runtime() both pull from here. The Cloud
# Run Terraform (service.tf) duplicates these values and must be kept in sync by
# hand — Terraform can't import them.
DEFAULT_CPU = "1"
DEFAULT_MEMORY = "4Gi"
DEFAULT_MIN_INSTANCES = 1
DEFAULT_MAX_INSTANCES = 10
# Max in-flight requests per container. Conservative on purpose: the worker is
# I/O-bound (CPU isn't the limit), but peak memory grows with concurrency and is
# agent-specific, so 8 keeps a RAG/large-context agent inside 4Gi. Lighter agents
# can raise --concurrency (and --memory) after load testing.
# https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/optimize-and-scale#underutilized-workers
DEFAULT_CONCURRENCY = 8
# One async worker per vCPU (DEFAULT_CPU); a single GIL-bound process saturates
# one core, so worker count tracks CPU.
DEFAULT_NUM_WORKERS = 1


def resolve_service_name(cfg: ProjectConfig, override: str | None) -> str:
    """Deployed service name.

    Precedence: the explicit ``override`` (``--service-name`` flag) wins, then the
    project name, then a generic fallback when deploying without a manifest.
    """
    return override or cfg.project_name or "agent"


def parse_key_value_pairs(kv_string: str | None) -> dict[str, str]:
    """Parse key-value pairs from a comma-separated KEY=VALUE string."""
    result = {}
    if kv_string:
        for pair in kv_string.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                result[key.strip()] = value.strip()
            else:
                logging.warning(f"Skipping malformed key-value pair: {pair}")
    return result
