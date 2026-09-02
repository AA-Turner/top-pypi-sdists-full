from matrx_ai.instructions.pattern_parser import MatrxPatternParser
from matrx_ai.instructions.pattern_parser import MatrxPattern

if __name__ == "__main__":
    print("=" * 80)
    print("MATRX Pattern Parser - Test Suite")
    print("=" * 80)
    
    # Test 1: Basic parsing
    print("\n[Test 1] Basic Pattern Parsing")
    print("-" * 80)
    test_text_1 = "<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>sample-thinking<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_1)
    print(f"Input: {test_text_1}")
    print(f"Result: {patterns[0]}")
    assert len(patterns) == 1
    assert patterns[0].table == "CONTENT_BLOCKS"
    assert patterns[0].column == "BLOCK_ID"
    assert patterns[0].value == "sample-thinking"
    print("✓ PASSED")
    
    # Test 2: UUID value
    print("\n[Test 2] Pattern with UUID Value")
    print("-" * 80)
    test_text_2 = "<<MATRX>><<CONTENT_BLOCKS>><<ID>>b46e284e-ccb0-4d32-8a96-07f85d50d134<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_2)
    print(f"Input: {test_text_2}")
    print(f"Result: {patterns[0]}")
    assert len(patterns) == 1
    assert patterns[0].table == "CONTENT_BLOCKS"
    assert patterns[0].column == "ID"
    assert patterns[0].value == "b46e284e-ccb0-4d32-8a96-07f85d50d134"
    print("✓ PASSED")
    
    # Test 3: Multiple patterns in text
    print("\n[Test 3] Multiple Patterns in Text")
    print("-" * 80)
    test_text_3 = """
    Here is some text with a pattern: <<MATRX>><<USERS>><<EMAIL>>john@example.com<</MATRX>>
    And here's another one: <<MATRX>><<POSTS>><<TITLE>>My Blog Post<</MATRX>>
    """
    patterns = MatrxPatternParser.parse(test_text_3)
    print(f"Input: {test_text_3.strip()}")
    print(f"Found {len(patterns)} patterns:")
    for i, p in enumerate(patterns, 1):
        print(f"  {i}. {p}")
    assert len(patterns) == 2
    assert patterns[0].table == "USERS"
    assert patterns[0].column == "EMAIL"
    assert patterns[0].value == "john@example.com"
    assert patterns[1].table == "POSTS"
    assert patterns[1].column == "TITLE"
    assert patterns[1].value == "My Blog Post"
    print("✓ PASSED")
    
    # Test 4: Pattern surrounded by other text
    print("\n[Test 4] Pattern Surrounded by Text")
    print("-" * 80)
    test_text_4 = "The user email is <<MATRX>><<USERS>><<EMAIL>>admin@test.com<</MATRX>> and that's it!"
    patterns = MatrxPatternParser.parse(test_text_4)
    print(f"Input: {test_text_4}")
    print(f"Result: {patterns[0]}")
    assert len(patterns) == 1
    assert patterns[0].value == "admin@test.com"
    assert patterns[0].start_pos == 18
    print("✓ PASSED")
    
    # Test 5: Empty or special values
    print("\n[Test 5] Special Values (numbers, symbols, etc.)")
    print("-" * 80)
    test_text_5 = "<<MATRX>><<SETTINGS>><<PORT>>8080<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_5)
    print(f"Input: {test_text_5}")
    print(f"Result: {patterns[0]}")
    assert patterns[0].value == "8080"
    print("✓ PASSED")
    
    # Test 6: Value with spaces
    print("\n[Test 6] Value with Spaces and Special Characters")
    print("-" * 80)
    test_text_6 = "<<MATRX>><<ARTICLES>><<TITLE>>How to Use AI: A Guide<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_6)
    print(f"Input: {test_text_6}")
    print(f"Result: {patterns[0]}")
    assert patterns[0].value == "How to Use AI: A Guide"
    print("✓ PASSED")
    
    # Test 7: No pattern in text
    print("\n[Test 7] No Pattern Found")
    print("-" * 80)
    test_text_7 = "This is just regular text without any patterns."
    patterns = MatrxPatternParser.parse(test_text_7)
    print(f"Input: {test_text_7}")
    print(f"Result: {patterns}")
    assert len(patterns) == 0
    print("✓ PASSED")
    
    # Test 8: find_first helper
    print("\n[Test 8] Find First Pattern Helper")
    print("-" * 80)
    test_text_8 = """
    First: <<MATRX>><<TABLE1>><<COL1>>value1<</MATRX>>
    Second: <<MATRX>><<TABLE2>><<COL2>>value2<</MATRX>>
    """
    first = MatrxPatternParser.find_first(test_text_8)
    print(f"First pattern found: {first}")
    assert first is not None
    assert first.table == "TABLE1"
    print("✓ PASSED")
    
    # Test 9: replace_patterns functionality
    print("\n[Test 9] Replace Patterns with Custom Function")
    print("-" * 80)
    test_text_9 = "Get <<MATRX>><<USERS>><<NAME>>John<</MATRX>> and <<MATRX>><<USERS>><<AGE>>30<</MATRX>>"
    
    def replacement_func(pattern: MatrxPattern) -> str:
        return f"{{DB.{pattern.table}.{pattern.column}[{pattern.value}]}}"
    
    result = MatrxPatternParser.replace_patterns(test_text_9, replacement_func)
    print(f"Input:  {test_text_9}")
    print(f"Output: {result}")
    assert result == "Get {DB.USERS.NAME[John]} and {DB.USERS.AGE[30]}"
    print("✓ PASSED")
    
    # Test 10: Complex real-world example
    print("\n[Test 10] Complex Real-World Example")
    print("-" * 80)
    test_text_10 = """
    You are working with content block <<MATRX>><<CONTENT_BLOCKS>><<ID>>b46e284e-ccb0-4d32-8a96-07f85d50d134<</MATRX>>
    which belongs to user <<MATRX>><<USERS>><<EMAIL>>admin@example.com<</MATRX>>.
    The block type is <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>sample-thinking<</MATRX>>.
    """
    patterns = MatrxPatternParser.parse(test_text_10)
    print(f"Input: {test_text_10.strip()}")
    print(f"\nFound {len(patterns)} patterns:")
    for i, p in enumerate(patterns, 1):
        print(f"  {i}. Table: {p.table:20} Column: {p.column:15} Value: {p.value}")
    assert len(patterns) == 3
    assert patterns[0].table == "CONTENT_BLOCKS"
    assert patterns[0].column == "ID"
    assert patterns[1].table == "USERS"
    assert patterns[2].column == "BLOCK_ID"
    print("✓ PASSED")
    
    # Test 11: Pattern with optional fields
    print("\n[Test 11] Pattern with Optional Fields Specification")
    print("-" * 80)
    test_text_11 = "<<MATRX>><<CONTENT_BLOCKS>><<ID>>b46e284e-ccb0-4d32-8a96-07f85d50d134<<FIELDS>>template<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_11)
    print(f"Input: {test_text_11}")
    print(f"Result: {patterns[0]}")
    assert len(patterns) == 1
    assert patterns[0].table == "CONTENT_BLOCKS"
    assert patterns[0].column == "ID"
    assert patterns[0].value == "b46e284e-ccb0-4d32-8a96-07f85d50d134"
    assert patterns[0].fields == "template"
    print("✓ PASSED")
    
    # Test 12: Multiple patterns with and without fields
    print("\n[Test 12] Mixed Patterns (With and Without Fields)")
    print("-" * 80)
    test_text_12 = """
    Get block: <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>label<</MATRX>>
    And user: <<MATRX>><<USERS>><<EMAIL>>john@test.com<</MATRX>>
    """
    patterns = MatrxPatternParser.parse(test_text_12)
    print(f"Input: {test_text_12.strip()}")
    print(f"Found {len(patterns)} patterns:")
    for i, p in enumerate(patterns, 1):
        print(f"  {i}. {p}")
    assert len(patterns) == 2
    assert patterns[0].fields == "label"
    assert patterns[1].fields is None
    print("✓ PASSED")
    
    # Test 13: Pattern with fields containing multiple attributes
    print("\n[Test 13] Pattern with List-like Fields Values")
    print("-" * 80)
    test_text_13 = "<<MATRX>><<CONTENT_BLOCKS>><<CATEGORY_ID>>uuid-here<<FIELDS>>template,label<</MATRX>>"
    patterns = MatrxPatternParser.parse(test_text_13)
    print(f"Input: {test_text_13}")
    print(f"Result: {patterns[0]}")
    print(f"Fields value: '{patterns[0].fields}'")
    assert patterns[0].fields == "template,label"
    print("✓ PASSED - Note: Comma-separated fields can be parsed at application level")
    
    print("\n" + "=" * 80)
    print("All tests passed! ✓")
    print("=" * 80)
