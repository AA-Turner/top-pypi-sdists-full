"""The SDK's enum base and the entity vocabulary.

A leaf module: it imports nothing else from the package, so any module may name
:class:`EntityKind`.
"""

from __future__ import annotations

# Python internals
import enum


class StrEnum(enum.StrEnum):
    """Base for the SDK's public enums: an unknown value maps to ``UNKNOWN``."""

    @classmethod
    def _missing_(cls, value: object) -> StrEnum | None:
        # A member the platform added must not crash an older SDK. None lets Enum
        # raise its own ValueError for an enum without an UNKNOWN.
        return cls.__members__.get("UNKNOWN")


class EntityKind(StrEnum):
    """The things the platform addresses.

    One vocabulary for error messages, reprs and context scope, so no call site
    spells out ``"workspace"``.

    Attributes:
        ORGANIZATION: An organization.
        WORKSPACE: A workspace within an organization.
        JOB: A deployed job within a workspace.
        JOB_RUN: One execution of a job.
        PIPELINE_RUN: One dlt pipeline run inside a job run, as telemetry saw it.
        DATAPLANE: A data plane a workspace can live on.
        DEPLOYMENT: A version of the code a workspace runs.
        CONFIGURATION: A version of the settings a workspace runs with.
        VARIABLE: A configuration value a run reads.
        UNKNOWN: A kind this SDK version does not know.
    """

    ORGANIZATION = "organization"
    WORKSPACE = "workspace"
    JOB = "job"
    JOB_RUN = "job_run"
    PIPELINE_RUN = "pipeline_run"
    DATAPLANE = "dataplane"
    DEPLOYMENT = "deployment"
    CONFIGURATION = "configuration"
    VARIABLE = "variable"
    UNKNOWN = "unknown"
