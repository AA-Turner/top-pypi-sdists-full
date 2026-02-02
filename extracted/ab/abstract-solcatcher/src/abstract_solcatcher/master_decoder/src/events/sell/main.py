from .schema import *
from .imports import *
class SellDecoder:
    """Decoder for Pump.fun Sell instructions"""
    
def SellDecoder( data: bytes) -> DecodedSell:
    """Decode Sell instruction data"""
    discriminator = data[0:8]
    token_amount = struct.unpack('<Q', data[8:16])[0]
    min_sol_output = struct.unpack('<Q', data[16:24])[0]
    
    return DecodedSell(
        discriminator=discriminator,
        token_amount=token_amount,
        min_sol_output_lamports=min_sol_output
    )

