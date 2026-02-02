from .imports import dataclass,Optional
@dataclass
class DecodedSell:
    """Schema for Sell instruction"""
    discriminator: bytes
    token_amount: int
    min_sol_output_lamports: int
    
    @property
    def instruction_type(self) -> str:
        return "Sell"
    
    @property
    def min_sol_output(self) -> float:
        return self.min_sol_output_lamports / 1e9
    
    @property
    def token_amount_ui(self) -> float:
        return self.token_amount / 1e6
