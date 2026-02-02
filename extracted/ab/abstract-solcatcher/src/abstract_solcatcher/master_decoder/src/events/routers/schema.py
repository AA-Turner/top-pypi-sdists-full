from .imports import dataclass,Optional
@dataclass
class DecodeError:
    """Logged when decoding fails"""
    signature: Optional[str]
    program_id: Optional[str]
    discriminator: str
    payload_len: int
    reason: str
    b64: str

