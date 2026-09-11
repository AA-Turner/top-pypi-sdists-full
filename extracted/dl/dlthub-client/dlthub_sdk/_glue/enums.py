"""The SDK's enum base and the entity vocabulary.

A leaf module: it imports nothing else from the package, so any module may name
:class:`EntityKind`.
"""

from __future__ import annotations

# Python internals
from enum import Enum


class StrEnum(str, Enum):
    """Base for the SDK's public enums.

    Not ``enum.StrEnum``, which needs 3.11 while the SDK supports 3.10. The two
    dunders make ``str()`` and f-strings render the value rather than
    ``Cls.MEMBER`` on every supported version.
    """

    __str__ = str.__str__
    __format__ = str.__format__  # type: ignore[assignment]

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
