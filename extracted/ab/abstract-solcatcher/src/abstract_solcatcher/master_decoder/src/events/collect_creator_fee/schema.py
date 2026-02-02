from .imports import dataclass
@dataclass
class CollectCreatorFeeEvent:
    """Creator fee collection (from 6EF8... program)"""
    timestamp: int
    recipient: str
    fee_lamports: int
    
    @property
    def fee_sol(self) -> float:
        return self.fee_lamports / 1e9
