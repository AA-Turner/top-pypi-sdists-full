from .schema import *
from .imports import *
def decode_program_data(program_data: str, all_js: Optional[dict] = None) -> Optional[ProgramData]:
    """
    Decodes program data (TradeEvent format with extended fields).
    Handles data starting with 'vdt/'.
    
    TypeScript equivalent: decodeProgramData()
    
    Extended layout (267 bytes):
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
       -- extended (if present) --
       32    bonding_curve
        8    _padding
        8    platform_fee (u64)
       32    creator
        8    creator_fee (u64)
        8    protocol_fee (u64)
       32    referrer (optional, null = zeros)
    """
    try:
        decoded_data = base64.b64decode(program_data)
        offset = 8  # Skip discriminator
        
        # Mint (32 bytes)
        mint = base58.b58encode(decoded_data[offset:offset + 32]).decode()
        offset += 32
        
        # Sol amount (u64)
        sol_amount = struct.unpack_from('<Q', decoded_data, offset)[0]
        offset += 8
        
        # Token amount (u64)
        token_amount = struct.unpack_from('<Q', decoded_data, offset)[0]
        offset += 8
        
        # Is buy (bool, 1 byte)
        is_buy = decoded_data[offset] != 0
        offset += 1
        
        # User (32 bytes)
        user_address = base58.b58encode(decoded_data[offset:offset + 32]).decode()
        offset += 32
        
        # Timestamp (i64)
        timestamp = struct.unpack_from('<q', decoded_data, offset)[0]
        offset += 8
        
        # Virtual SOL reserves (u64)
        virtual_sol_reserves = struct.unpack_from('<Q', decoded_data, offset)[0]
        offset += 8
        
        # Virtual token reserves (u64)
        virtual_token_reserves = struct.unpack_from('<Q', decoded_data, offset)[0]
        offset += 8
        
        # Initialize extended fields
        real_sol_reserves = None
        real_token_reserves = None
        bonding_curve = None
        platform_fee = None
        creator = None
        creator_fee = None
        protocol_fee = None
        referrer = None
        
        # Real SOL reserves (u64, optional)
        if offset + 8 <= len(decoded_data):
            real_sol_reserves = struct.unpack_from('<Q', decoded_data, offset)[0]
            offset += 8
        
        # Real token reserves (u64, optional)
        if offset + 8 <= len(decoded_data):
            real_token_reserves = struct.unpack_from('<Q', decoded_data, offset)[0]
            offset += 8
        
        # Bonding curve (32 bytes, optional)
        if offset + 32 <= len(decoded_data):
            bonding_curve = base58.b58encode(decoded_data[offset:offset + 32]).decode()
            offset += 32
        
        # Skip padding (8 bytes)
        if offset + 8 <= len(decoded_data):
            offset += 8
        
        # Platform fee (u64, optional)
        if offset + 8 <= len(decoded_data):
            platform_fee = struct.unpack_from('<Q', decoded_data, offset)[0]
            offset += 8
        
        # Creator (32 bytes, optional)
        if offset + 32 <= len(decoded_data):
            creator = base58.b58encode(decoded_data[offset:offset + 32]).decode()
            offset += 32
        
        # Creator fee (u64, optional)
        if offset + 8 <= len(decoded_data):
            creator_fee = struct.unpack_from('<Q', decoded_data, offset)[0]
            offset += 8
        
        # Protocol fee (u64, optional)
        if offset + 8 <= len(decoded_data):
            protocol_fee = struct.unpack_from('<Q', decoded_data, offset)[0]
            offset += 8
        
        # Referrer (32 bytes, optional - null pubkey = all zeros)
        if offset + 32 <= len(decoded_data):
            ref_bytes = decoded_data[offset:offset + 32]
            if ref_bytes != bytes(32):
                referrer = base58.b58encode(ref_bytes).decode()
            offset += 32
        
        return ProgramData(
            mint=mint,
            sol_amount=BN(sol_amount),
            token_amount=BN(token_amount),
            is_buy=is_buy,
            user_address=user_address,
            timestamp=timestamp,
            virtual_sol_reserves=BN(virtual_sol_reserves),
            virtual_token_reserves=BN(virtual_token_reserves),
            real_sol_reserves=BN(real_sol_reserves) if real_sol_reserves else None,
            real_token_reserves=BN(real_token_reserves) if real_token_reserves else None,
            bonding_curve=bonding_curve,
            platform_fee=platform_fee,
            creator=creator,
            creator_fee=creator_fee,
            protocol_fee=protocol_fee,
            referrer=referrer,
        )
    
    except Exception as e:
        print(f"Error in decode_program_data: {e}")
        return None
