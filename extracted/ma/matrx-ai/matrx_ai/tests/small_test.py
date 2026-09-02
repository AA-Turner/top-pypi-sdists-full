

DEBUG_OVERRIDE = False

def test_debug_override(debug: bool = False):
    
    DEBUG = DEBUG_OVERRIDE or debug
    
    print(f"DEBUG: {DEBUG}")
    return DEBUG



if __name__ == "__main__":
    print("\nTest 1: True")
    test_debug_override(True)
    print("\nTest 2: False")
    test_debug_override(False)
