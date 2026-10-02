from enum import StrEnum

class ManagedAgentsSessionEligibilityReason(StrEnum):
    MISSING_AGENT_ATTRIBUTION = "missing_agent_attribution"
    NON_PUBLIC_ACCESS = "non_public_access"
    NOT_ROOT = "not_root"
    NO_SNAPSHOT_EVENT = "no_snapshot_event"
    UNSUPPORTED_KIND = "unsupported_kind"

    def __str__(self) -> str:
        return str(self.value)
