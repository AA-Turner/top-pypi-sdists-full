from .policy import Policy

from .data_classification import DataClassification


class DataSecurity(DataClassification):
    """
    The Data Security object describes the characteristics, techniques and content
    of a Data Loss Prevention (DLP), Data Loss Detection (DLD), Data Classification,
    or similar tools' finding, alert, or detection mechanism(s).
    """

    # Recommended:
    data_lifecycle_state_id: int | None = None
    detection_pattern: str | None = None
    detection_system_id: int | None = None
    policy: Policy | None = None # Details about the policy that triggered the finding.

    # Optional:
    data_lifecycle_state: str | None = None
    detection_system: str | None = None
    pattern_match: str | None = None
