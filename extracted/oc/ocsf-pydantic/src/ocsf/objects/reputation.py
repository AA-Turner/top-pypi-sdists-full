from pydantic import BaseModel

class Reputation(BaseModel):
    """
    The Reputation object describes the reputation/risk score of an entity (e.g.
    device, user, domain).
    """

    base_score: float # The reputation score as reported by the event source.
    score_id: int

    # Recommended:
    provider: str | None = None # The provider of the reputation information.

    # Optional:
    score: str | None = None
