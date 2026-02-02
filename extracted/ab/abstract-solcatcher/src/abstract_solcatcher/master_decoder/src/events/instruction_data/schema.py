from .imports import dataclass,Optional
@dataclass
class InstructionData:
    """Decoded instruction data (CreateV2-like)"""
    discriminator: str
    name: str
    symbol: str
    uri: str
    mint: Optional[str] = None
    bonding_curve: Optional[str] = None
    user: Optional[str] = None
