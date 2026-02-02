from .schema import *
from .imports import *
def decode_instruction_data(program_data: str) -> Optional[InstructionData]:
    """
    Decodes instruction data (CreateV2 format).
    Handles data starting with 'G3' or 'X3'.
    
    TypeScript equivalent: decodeInstructionData()
    """
    try:
        decoded_data = base64.b64decode(program_data)
        offset = 0
        
        # Discriminator (8 bytes)
        if len(decoded_data) < offset + 8:
            raise ValueError("Not enough data to read discriminator")
        
        discriminator = decoded_data[offset:offset + 8].hex()
        offset += 8
        
        # Name
        name, offset = read_string(decoded_data, offset)
        
        # Symbol
        symbol, offset = read_string(decoded_data, offset)
        
        # URI
        uri, offset = read_string(decoded_data, offset)
        
        # Mint (32 bytes, optional)
        mint = None
        if len(decoded_data) >= offset + 32:
            mint = base58.b58encode(decoded_data[offset:offset + 32]).decode()
            offset += 32
        
        # Bonding curve (32 bytes, optional)
        bonding_curve = None
        if len(decoded_data) >= offset + 32:
            bonding_curve = base58.b58encode(decoded_data[offset:offset + 32]).decode()
            offset += 32
        
        # User (32 bytes, optional)
        user = None
        if len(decoded_data) >= offset + 32:
            user = base58.b58encode(decoded_data[offset:offset + 32]).decode()
            offset += 32
        
        return InstructionData(
            discriminator=discriminator,
            name=name,
            symbol=symbol,
            uri=uri,
            mint=mint,
            bonding_curve=bonding_curve,
            user=user,
        )
    
    except Exception as e:
        print(f"Error decoding instruction data: {e}")
        return None


