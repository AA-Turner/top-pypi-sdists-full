from .imports import dataclass
@dataclass  
class DecodedBuy:
    """Schema for Buy instruction"""
    discriminator: bytes
    bonding_curve: bytes  # 32-byte pubkey
    sol_amount_lamports: int  # u64
    token_amount: int  # u64 (with decimals)
    
    @property
    def instruction_type(self) -> str:
        return "Buy"
    
    @property
    def sol_amount(self) -> float:
        """Convert lamports to SOL"""
        return self.sol_amount_lamports / 1e9
    
    @property
    def token_amount_ui(self) -> float:
        """Convert raw token amount to UI amount (6 decimals for Pump.fun)"""
        return self.token_amount / 1e6
    
    def __repr__(self) -> str:
        return (
            f"DecodedBuy(\n"
            f"  discriminator={self.discriminator.hex()},\n"
            f"  bonding_curve={self.bonding_curve.hex()[:8]}...{self.bonding_curve.hex()[-8:]},\n"
            f"  sol_amount={self.sol_amount:.9f} SOL ({self.sol_amount_lamports:,} lamports),\n"
            f"  token_amount={self.token_amount_ui:,.6f} ({self.token_amount:,} raw)\n"
            f")"
        )
