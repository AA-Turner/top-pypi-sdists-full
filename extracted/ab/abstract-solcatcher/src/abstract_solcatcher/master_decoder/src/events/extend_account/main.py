from .schema import *
from .imports import *
def decode_extend_account_event(raw: bytes) -> ExtendAccountEvent:
    o = 8
    bonding_curve, o = read_pubkey(raw, o)
    v_sol, o = read_u64(raw, o)
    v_token, o = read_u64(raw, o)
    r_sol, o = read_u64(raw, o)
    r_token, o = read_u64(raw, o)
    
    return ExtendAccountEvent(
        bonding_curve=bonding_curve,
        virtual_sol_reserves=v_sol, virtual_token_reserves=v_token,
        real_sol_reserves=r_sol, real_token_reserves=r_token
    )
