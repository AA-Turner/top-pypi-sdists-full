from .imports import dataclass,Optional
@dataclass
class SetParamsEvent:
    """Protocol parameter update (admin only)"""
    fee_recipient: str
    initial_virtual_token_reserves: int
    initial_virtual_sol_reserves: int
    initial_real_token_reserves: int
    token_total_supply: int
    fee_basis_points: int
