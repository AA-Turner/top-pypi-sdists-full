"""Report Registry skill loads, catalogue listings and installs to an observer.

A worker supplies one that records runtime metrics. In-process runs keep the default, which records nothing.
"""

from typing import Literal, Protocol

SkillLoadSource = Literal["lazy_registry", "provisioned"]
"""``lazy_registry``: a discovered Registry skill, installed on first use. ``provisioned``: in the sandbox from the
Session's start, whether declared or found in the workspace."""
SkillCatalogOutcome = Literal["complete", "incomplete", "failed"]
"""``incomplete``: the listing stopped after at least one page. ``failed``: the Session got no catalogue."""
SkillCatalogReason = Literal[
    "none",
    "unauthorized",
    "forbidden",
    "rate_limited",
    "client_error",
    "server_error",
    "timeout",
    "network_error",
    "invalid_response",
    "identity",
    "repeated_page_token",
    "other",
]
SkillMaterializationOutcome = Literal["success", "failure"]
SkillMaterializationReason = Literal[
    "none", "download", "write", "receipt_mismatch", "cache_check", "invalid_binding", "unconfigured", "other"
]


class SkillCatalogMetrics(Protocol):
    """Observe Registry catalogue listings. An implementation never raises."""

    def record_skill_registry_catalog(self, outcome: SkillCatalogOutcome, reason: SkillCatalogReason) -> None: ...


class SkillMetrics(SkillCatalogMetrics, Protocol):
    """Observe skill outcomes. An implementation never raises."""

    def record_skill_load(self, source: SkillLoadSource) -> None: ...

    def record_skill_materialization(
        self, outcome: SkillMaterializationOutcome, reason: SkillMaterializationReason
    ) -> None: ...


class _NoopSkillMetrics:
    def record_skill_load(self, source: SkillLoadSource) -> None:
        pass

    def record_skill_registry_catalog(self, outcome: SkillCatalogOutcome, reason: SkillCatalogReason) -> None:
        pass

    def record_skill_materialization(
        self, outcome: SkillMaterializationOutcome, reason: SkillMaterializationReason
    ) -> None:
        pass


NOOP_SKILL_METRICS: SkillMetrics = _NoopSkillMetrics()


__all__ = [
    "NOOP_SKILL_METRICS",
    "SkillCatalogMetrics",
    "SkillCatalogOutcome",
    "SkillCatalogReason",
    "SkillLoadSource",
    "SkillMaterializationOutcome",
    "SkillMaterializationReason",
    "SkillMetrics",
]
