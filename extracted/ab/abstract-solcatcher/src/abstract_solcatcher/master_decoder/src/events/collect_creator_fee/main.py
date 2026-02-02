from .schema import *
from .imports import *
def decode_collect_creator_fee_event(raw: bytes) -> CollectCreatorFeeEvent:
    """For discriminator 7a027f010ebf0caf"""
    o = 8
    timestamp, o = read_i64(raw, o)
    recipient, o = read_pubkey(raw, o)
    fee_lamports, o = read_u64(raw, o)
    
    return CollectCreatorFeeEvent(
        timestamp=timestamp, recipient=recipient, fee_lamports=fee_lamports
    )
