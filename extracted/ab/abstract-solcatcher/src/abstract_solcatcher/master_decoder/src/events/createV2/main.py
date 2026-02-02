from .schema import *
from .imports import *

def CreateDecoder(data: bytes) -> DecodedCreate:
    """
    Decode CreateV2 instruction data
    
    Structure:
    - 0-7: Discriminator (8 bytes)
    - 8+: Token name (length-prefixed string)
    - ... : Token symbol (length-prefixed string)
    - ... : Token URI (length-prefixed string)
    """
    offset = 0
    
    # Discriminator
    discriminator = data[offset:offset+8]
    offset += 8
    
    # Name (u32 length prefix + UTF-8 string)
    name_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    name = data[offset:offset+name_len].decode('utf-8')
    offset += name_len
    
    # Symbol
    symbol_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    symbol = data[offset:offset+symbol_len].decode('utf-8')
    offset += symbol_len
    
    # URI
    uri_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    uri = data[offset:offset+uri_len].decode('utf-8')
    
    metadata = TokenMetadata(name=name, symbol=symbol, uri=uri)
    return DecodedCreate(discriminator=discriminator, metadata=metadata)
