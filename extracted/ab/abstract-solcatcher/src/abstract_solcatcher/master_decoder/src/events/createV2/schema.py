from .imports import dataclass,TokenMetadata
@dataclass
class DecodedCreate:
    """Schema for CreateV2 instruction"""
    discriminator: bytes
    metadata: TokenMetadata
    
    @property
    def instruction_type(self) -> str:
        return "CreateV2"
    
    def __repr__(self) -> str:
        return (
            f"DecodedCreate(\n"
            f"  discriminator={self.discriminator.hex()},\n"
            f"  name='{self.metadata.name}',\n"
            f"  symbol='{self.metadata.symbol}',\n"
            f"  uri='{self.metadata.uri}'\n"
            f")"
        )
