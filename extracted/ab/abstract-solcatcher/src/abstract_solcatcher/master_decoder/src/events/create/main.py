from .schema import *
from .imports import *
def decode_create_event(raw: bytes) -> CreateEvent:
    o = 8
    mint, o = read_pubkey(raw, o)
    name, o = read_string(raw, o)
    symbol, o = read_string(raw, o)
    uri, o = read_string(raw, o)
    bonding_curve, o = read_pubkey(raw, o)
    creator, o = read_pubkey(raw, o)
    decimals = raw[o]; o += 1
    initial_supply, o = read_u64(raw, o)
    
    return CreateEvent(
        mint=mint, name=name, symbol=symbol, uri=uri,
        bonding_curve=bonding_curve, creator=creator,
        decimals=decimals, initial_supply=initial_supply
    )
