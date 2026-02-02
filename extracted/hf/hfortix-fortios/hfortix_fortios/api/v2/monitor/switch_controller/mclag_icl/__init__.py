"""FortiOS CMDB - MclagIcl category"""

from .eligible_peer import EligiblePeer
from .set_tier1 import SetTier1
from .set_tier_plus import SetTierPlus
from .tier_plus_candidates import TierPlusCandidates

__all__ = [
    "EligiblePeer",
    "MclagIcl",
    "SetTier1",
    "SetTierPlus",
    "TierPlusCandidates",
]


class MclagIcl:
    """MclagIcl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """MclagIcl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.eligible_peer = EligiblePeer(client)
        self.set_tier1 = SetTier1(client)
        self.set_tier_plus = SetTierPlus(client)
        self.tier_plus_candidates = TierPlusCandidates(client)
