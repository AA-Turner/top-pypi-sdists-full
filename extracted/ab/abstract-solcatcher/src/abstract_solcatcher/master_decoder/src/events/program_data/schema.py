from .imports import dataclass,Optional,BN,SOL_LAMPORTS
@dataclass
class ProgramData:
    """Decoded program data (TradeEvent format with extended fields)"""
    mint: str
    sol_amount: BN
    token_amount: BN
    is_buy: bool
    user_address: str
    timestamp: int
    virtual_sol_reserves: BN
    virtual_token_reserves: BN
    
    # Extended fields (populated if present in data)
    real_sol_reserves: Optional[BN] = None
    real_token_reserves: Optional[BN] = None
    bonding_curve: Optional[str] = None
    platform_fee: Optional[int] = None
    creator: Optional[str] = None
    creator_fee: Optional[int] = None
    protocol_fee: Optional[int] = None
    referrer: Optional[str] = None
    
    # Derived fields (populated by update_token_variables)
    price: Optional[BN] = None
    token_decimals: Optional[int] = None
    sol_amount_ui: Optional[float] = None
    token_amount_ui: Optional[float] = None
    
    @property
    def side(self) -> str:
        return "BUY" if self.is_buy else "SELL"
    
    @property
    def total_fees_lamports(self) -> int:
        return (self.platform_fee or 0) + (self.creator_fee or 0) + (self.protocol_fee or 0)
    
    @property
    def total_fees_sol(self) -> float:
        return self.total_fees_lamports / SOL_LAMPORTS
