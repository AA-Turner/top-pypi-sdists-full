# ============================================================================
# ROUTER
# ============================================================================

def decode_data(data: str) -> Optional[Union[InstructionData, ProgramData]]:
    """
    Route to appropriate decoder based on prefix.
    
    TypeScript equivalent: decodeData()
    """
    if data.startswith('G3') or data.startswith('X3'):
        return decode_instruction_data(data)
    elif data.startswith('vdt/'):
        result = decode_program_data(data)
        if result:
            result = update_token_variables(result)
        return result
    else:
        # Try to decode as generic event
        return decode_program_data(data)


def decode_program_data_list(data_list: List[str]) -> List[ProgramData]:
    """
    Batch decode program data.
    
    TypeScript equivalent: decodeProgramDataList()
    """
    results: List[ProgramData] = []
    
    for program_data in data_list:
        try:
            decoded = decode_program_data(program_data)
            if decoded:
                decoded = update_token_variables(decoded)
                results.append(decoded)
            else:
                print(f"Failed to decode program data: {program_data[:50]}...")
        except Exception as e:
            print(f"Error decoding program data: {e}")
    
    return results
