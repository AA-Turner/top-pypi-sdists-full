from .imports import dataclass
@dataclass
class CompleteEvent:
    """Bonding curve graduation to Raydium"""
    mint: str
    bonding_curve: str
    timestamp: int
    virtual_sol_reserves: int
    virtual_token_reserves: int
    real_sol_reserves: int
    real_token_reserves: int
