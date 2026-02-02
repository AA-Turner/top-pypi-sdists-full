from .schema import *
from .imports import *

def BuyDecoder(data: bytes) -> DecodedBuy:
    """
    Decode Buy instruction data
    
    Structure (based on empirical analysis):
    - 0-7:   Discriminator (8 bytes)
    - 8-39:  Bonding curve pubkey (32 bytes)
    - 40-47: SOL amount in lamports (u64)
    - 48-55: Token amount with decimals (u64)
    - 56+:   Additional data (fees, slippage, etc.)
    """
    discriminator = data[0:8]
    bonding_curve = data[8:40]
    sol_amount_lamports = struct.unpack('<Q', data[40:48])[0]
    token_amount = struct.unpack('<Q', data[48:56])[0]
    
    return DecodedBuy(
        discriminator=discriminator,
        bonding_curve=bonding_curve,
        sol_amount_lamports=sol_amount_lamports,
        token_amount=token_amount
    )
