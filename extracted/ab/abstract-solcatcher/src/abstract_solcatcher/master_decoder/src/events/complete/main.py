from .schema import *
from .imports import *
def decode_complete_event(raw: bytes) -> CompleteEvent:
    o = 8
    mint, o = read_pubkey(raw, o)
    bonding_curve, o = read_pubkey(raw, o)
    timestamp, o = read_i64(raw, o)
    virtual_sol, o = read_u64(raw, o)
    virtual_token, o = read_u64(raw, o)
    real_sol, o = read_u64(raw, o)
    real_token, o = read_u64(raw, o)
    
    return CompleteEvent(
        mint=mint, bonding_curve=bonding_curve, timestamp=timestamp,
        virtual_sol_reserves=virtual_sol, virtual_token_reserves=virtual_token,
        real_sol_reserves=real_sol, real_token_reserves=real_token
    )

