from datetime import datetime
from pydantic import BaseModel

class EPSS(BaseModel):
    """
    The Exploit Prediction Scoring System (EPSS) object describes the estimated
    probability a vulnerability will be exploited. EPSS is a community-driven effort
    to combine descriptive information about vulnerabilities (CVEs) with evidence of
    actual exploitation in-the-wild. (<a target='_blank'
    href='https://www.first.org/epss/'>EPSS</a>).
    """

    score: str # The EPSS score representing the probability [0-1] of exploitation in the
               # wild in the next 30 days (following score publication).

    # Recommended:
    created_time: datetime | None = None # The timestamp indicating when the EPSS score was calculated.
    version: str | None = None # The version of the EPSS model used to calculate the score.

    # Optional:
    percentile: float | None = None
