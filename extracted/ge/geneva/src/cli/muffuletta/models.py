# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pydantic models for Geneva API responses."""

import contextlib
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job status enum."""

    # API returns uppercase values
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    # Also support lowercase for compatibility
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class Cluster(BaseModel):
    """Geneva cluster model."""

    name: str
    cluster_type: str | None = None
    created_at: datetime | None = None
    created_by: str | None = None
    ray_address: str | None = None
    kuberay: dict[str, Any] | None = None

    class Config:
        populate_by_name = True


class Manifest(BaseModel):
    """Geneva manifest model."""

    name: str
    version: str | None = None
    pip: list[str] = Field(default_factory=list)
    py_modules: list[str] = Field(default_factory=list)
    head_image: str | None = None
    worker_image: str | None = None
    skip_site_packages: bool = False
    zips: list[list[str]] = Field(default_factory=list)
    checksum: str | None = None
    created_at: datetime | None = None
    created_by: str | None = None

    class Config:
        populate_by_name = True


class JobMetric(BaseModel):
    """Job metric model."""

    name: str
    n: int = 0
    total: int = 0
    done: bool = False
    desc: str = ""


class Job(BaseModel):
    """Geneva job model."""

    job_id: str
    table_name: str | None = None
    column_name: str | None = None
    job_type: str | None = None
    object_ref: str | None = None
    status: JobStatus
    launched_at: datetime | None = None
    completed_at: datetime | None = None
    launched_by: str | None = None
    manifest_id: str | None = None
    manifest_checksum: str | None = None
    config: str | dict[str, Any] = Field(default_factory=dict)
    metrics: list[Any] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    updated_at: datetime | None = None

    class Config:
        populate_by_name = True

    @property
    def id(self) -> str:
        """Alias for job_id."""
        return self.job_id

    def get_config_dict(self) -> dict[str, Any]:
        """Parse config if it's a JSON string."""
        if isinstance(self.config, str):
            import json

            try:
                return json.loads(self.config)
            except json.JSONDecodeError:
                return {}
        return self.config

    def get_metrics_parsed(self) -> list[JobMetric]:
        """Parse metrics from JSON strings to JobMetric objects."""
        import json

        result = []
        for m in self.metrics:
            if m:
                if isinstance(m, str):
                    with contextlib.suppress(json.JSONDecodeError, TypeError):
                        result.append(JobMetric(**json.loads(m)))
                elif isinstance(m, dict):
                    with contextlib.suppress(TypeError):
                        result.append(JobMetric(**m))
        return result


class RayCluster(BaseModel):
    """Ray cluster model from Kubernetes."""

    name: str
    namespace: str
    status: str | None = None
    head_pod: str | None = None
    worker_replicas: int | None = None
    created_at: datetime | None = None
