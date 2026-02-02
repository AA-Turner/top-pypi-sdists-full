def update_token_variables(data: ProgramData) -> ProgramData:
    """
    Populate derived fields on ProgramData.
    
    TypeScript equivalent: update_token_variables()
    """
    try:
        # Derive price
        if not data.virtual_token_reserves.is_zero():
            data.price = derive_price(data.virtual_sol_reserves, data.virtual_token_reserves)
        
        # Derive token decimals
        data.token_decimals = derive_token_decimals_from_reserves(
            data.virtual_sol_reserves.to_int(),
            data.virtual_token_reserves.to_int(),
        )
        
        # UI amounts
        data.sol_amount_ui = data.sol_amount.to_number() / SOL_LAMPORTS
        
        if data.token_decimals is not None:
            data.token_amount_ui = data.token_amount.to_number() / (10 ** data.token_decimals)
    
    except Exception as e:
        print(f"Error updating token variables: {e}")
    
    return data
