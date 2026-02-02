from .imports import dataclass,Optional
@dataclass
class TradeEvent:
    """
    Extended TradeEvent from Pump.fun logs.
    Includes fee breakdown and bonding curve info.
    """
    # Core trade info
    mint: str
    sol_amount: int          # lamports
    token_amount: int        # raw (6 decimals)
    is_buy: bool
    user: str
    timestamp: int
    
    # Reserves
    virtual_sol_reserves: int
    virtual_token_reserves: int
    real_sol_reserves: int
    real_token_reserves: int
    
    # Extended fields
    bonding_curve: str
    platform_fee: int        # lamports
    creator: str
    creator_fee: int         # lamports
    protocol_fee: int        # lamports
    referrer: Optional[str]  # None if null pubkey
    
    @property
    def sol_ui(self) -> float:
        return self.sol_amount / 1e9
    
    @property
    def token_ui(self) -> float:
        return self.token_amount / 1e6
    
    @property
    def price(self) -> float:
        """SOL per token"""
        return self.sol_ui / self.token_ui if self.token_ui > 0 else 0.0
    
    @property
    def side(self) -> str:
        return "BUY" if self.is_buy else "SELL"
    
    @property
    def total_fees_lamports(self) -> int:
        return self.platform_fee + self.creator_fee + self.protocol_fee
    
    @property
    def total_fees_sol(self) -> float:
        return self.total_fees_lamports / 1e9
