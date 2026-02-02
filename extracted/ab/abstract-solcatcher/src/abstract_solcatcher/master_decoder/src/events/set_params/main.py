from .schema import *
from .imports import *
def decode_set_params_event(raw: bytes) -> SetParamsEvent:
    o = 8
    fee_recipient, o = read_pubkey(raw, o)
    init_v_token, o = read_u64(raw, o)
    init_v_sol, o = read_u64(raw, o)
    init_r_token, o = read_u64(raw, o)
    total_supply, o = read_u64(raw, o)
    fee_bps, o = read_u64(raw, o)
    
    return SetParamsEvent(
        fee_recipient=fee_recipient,
        initial_virtual_token_reserves=init_v_token,
        initial_virtual_sol_reserves=init_v_sol,
        initial_real_token_reserves=init_r_token,
        token_total_supply=total_supply,
        fee_basis_points=fee_bps
    )
