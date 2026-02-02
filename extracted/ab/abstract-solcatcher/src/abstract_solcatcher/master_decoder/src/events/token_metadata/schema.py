from .imports import dataclass
@dataclass
class TokenMetadata:
    """Schema for token metadata"""
    name: str
    symbol: str
    uri: str
