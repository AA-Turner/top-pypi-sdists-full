from .imports import dataclass
@dataclass
class ExtendAccountEvent:
    """Account extension/reallocation"""
    bonding_curve: str
    virtual_sol_reserves: int
    virtual_token_reserves: int
    real_sol_reserves: int
    real_token_reserves: int
