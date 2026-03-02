from .metric import Metric

from pydantic import BaseModel

class CVSSScore(BaseModel):
    """
    The Common Vulnerability Scoring System (https://www.first.org/cvss/) object provides
    a way to capture the principal characteristics of a vulnerability and produce a numerical
    score reflecting its severity.
    """

    base_score: float # The CVSS base score. For example: `9.1`.
    version: str # The CVSS version. For example: `3.1`.

    # Recommended:
    depth: str | None = None
    overall_score: float | None = None # The CVSS overall score, impacted by base, temporal, and
                                       # environmental metrics. For example: `9.1`.

    # Optional:
    metrics: list[Metric] | None = None # The Common Vulnerability Scoring System metrics. This
                                        # attribute contains information on the CVE's impact. If the
                                        # CVE has been analyzed, this attribute will contain any CVSSv2
                                        # or CVSSv3 information associated with the vulnerability. For
                                        # example: `{ {"Access Vector", "Network"}, {"Access
                                        # Complexity", "Low"}, ...}`.
    severity: str | None = None # The Common Vulnerability Scoring System (CVSS) Qualitative
                                # Severity Rating.
                                # A textual representation of the numeric score
                                # CVSS v2.0:
                                #   * Low (0.0 – 3.9)
                                #   * Medium (4.0 – 6.9)
                                #   * High (7.0 – 10.0)
                                # CVSS v3.0:
                                #   * None (0.0)
                                #   * Low (0.1 - 3.9)
                                #   * Medium (4.0 - 6.9)
                                #   * High (7.0 - 8.9)
                                #   * Critical (9.0 - 10.0)
    vector_string: str | None = None
