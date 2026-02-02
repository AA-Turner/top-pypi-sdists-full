from .schema import *
from .imports import *
def decode_trade_event(raw: bytes) -> TradeEvent:
    """
    Decode extended TradeEvent (267 bytes typical).
    
    Layout:
        8    discriminator
       32    mint
        8    sol_amount (u64)
        8    token_amount (u64)
        1    is_buy (bool)
       32    user
        8    timestamp (i64)
        8    virtual_sol_reserves (u64)
        8    virtual_token_reserves (u64)
        8    real_sol_reserves (u64)
        8    real_token_reserves (u64)
       -- extended --
       32    bonding_curve
        8    fee_amount_1 (dust/padding, skip)
        8    platform_fee (u64)
       32    creator
        8    creator_fee (u64)
        8    protocol_fee (u64)
       32    referrer (optional, null = zeros)
       ...   tail (padding + instruction name)
    """
    o = 8  # skip discriminator
    
    mint, o = read_pubkey(raw, o)
    sol_amount, o = read_u64(raw, o)
    token_amount, o = read_u64(raw, o)
    is_buy, o = read_bool(raw, o)
    user, o = read_pubkey(raw, o)
    timestamp, o = read_i64(raw, o)
    virtual_sol, o = read_u64(raw, o)
    virtual_token, o = read_u64(raw, o)
    real_sol, o = read_u64(raw, o)
    real_token, o = read_u64(raw, o)

    # Extended fields (if present)
    bonding_curve = ""
    platform_fee = 0
    creator = ""
    creator_fee = 0
    protocol_fee = 0
    referrer = None
    
    if o + 32 <= len(raw):
        bonding_curve, o = read_pubkey(raw, o)
    if o + 8 <= len(raw):
        _, o = read_u64(raw, o)  # skip dust/padding
    if o + 8 <= len(raw):
        platform_fee, o = read_u64(raw, o)
    if o + 32 <= len(raw):
        creator, o = read_pubkey(raw, o)
    if o + 8 <= len(raw):
        creator_fee, o = read_u64(raw, o)
    if o + 8 <= len(raw):
        protocol_fee, o = read_u64(raw, o)
    if o + 32 <= len(raw):
        if not _is_null_pubkey(raw, o):
            referrer, _ = read_pubkey(raw, o)
    
    return TradeEvent(
        mint=mint,
        sol_amount=sol_amount,
        token_amount=token_amount,
        is_buy=is_buy,
        user=user,
        timestamp=timestamp,
        virtual_sol_reserves=virtual_sol,
        virtual_token_reserves=virtual_token,
        real_sol_reserves=real_sol,
        real_token_reserves=real_token,
        bonding_curve=bonding_curve,
        platform_fee=platform_fee,
        creator=creator,
        creator_fee=creator_fee,
        protocol_fee=protocol_fee,
        referrer=referrer,
    )
