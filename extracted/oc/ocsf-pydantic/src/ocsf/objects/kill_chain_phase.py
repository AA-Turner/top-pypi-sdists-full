from pydantic import BaseModel

class KillChainPhase(BaseModel):
    """
    The Kill Chain Phase object represents a single phase of a cyber attack,
    including the initial reconnaissance and planning stages up to the final
    objective of the attacker. It provides a detailed description of each phase and
    its associated activities within the broader context of a cyber attack
    See: https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
    """

    phase_id: int

    # Recommended:
    phase: str | None = None
