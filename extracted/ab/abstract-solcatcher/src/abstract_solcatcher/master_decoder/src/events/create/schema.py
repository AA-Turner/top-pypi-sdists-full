from .imports import dataclass
@dataclass
class CreateEvent:
    """Token creation event"""
    mint: str
    name: str
    symbol: str
    uri: str
    bonding_curve: str
    creator: str
    decimals: int
    initial_supply: int
