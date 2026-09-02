"""
Integration Test: MATRX Pattern Recognition + Fetching

This demonstrates the complete workflow:
1. Parse MATRX patterns from text
2. Fetch data from database
3. Replace patterns with fetched content
"""

from matrx_ai.instructions.tests.variable_recognition_test import MatrxPatternParser
from matrx_ai.instructions.matrx_fetcher import MatrxFetcher
from matrx_utils import vcprint, clear_terminal


def process_text_with_matrx(text: str, verbose: bool = True) -> str:
    """
    Complete workflow: Parse MATRX patterns and replace with fetched data.
    
    Args:
        text: Text containing MATRX patterns
        verbose: Whether to print detailed information
    
    Returns:
        Processed text with patterns replaced
    """
    if verbose:
        print("=" * 80)
        print("PROCESSING TEXT WITH MATRX PATTERNS")
        print("=" * 80)
        print("\n[Step 1] Original Text:")
        print("-" * 80)
        print(text)
    
    # Parse patterns
    patterns = MatrxPatternParser.parse(text)
    
    if verbose:
        print(f"\n[Step 2] Found {len(patterns)} pattern(s):")
        print("-" * 80)
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. {pattern}")
    
    # Fetch and replace
    result = MatrxFetcher.process_text_with_patterns(text, patterns)
    
    if verbose:
        print("\n[Step 3] Processed Text:")
        print("-" * 80)
        print(result)
        print("=" * 80)
    
    return result


if __name__ == "__main__":
    clear_terminal()
    
    # Example 1: Simple pattern with default field
    print("\n[Example 1] Simple Pattern (Default Field)")
    print("=" * 80)
    text1 = """
Create flashcards using this template:

<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<</MATRX>>

This structure should be used for all flashcard content.
"""
    result1 = process_text_with_matrx(text1)
    print("\n✓ Example 1 Complete\n")
    
    # Example 2: Pattern with specific field
    print("\n[Example 2] Pattern with Specific Field")
    print("=" * 80)
    text2 = """
The block name is: <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>label<</MATRX>>

And the full template is:
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>template<</MATRX>>
"""
    result2 = process_text_with_matrx(text2)
    print("\n✓ Example 2 Complete\n")
    
    # Example 3: Multiple patterns from category
    print("\n[Example 3] Fetch Multiple Items by Category")
    print("=" * 80)
    text3 = """
Here are all the interactive content templates:

<<MATRX>><<CONTENT_BLOCKS>><<CATEGORY_ID>>9980e68f-97fc-4f71-bf1d-22583b6cdf38<</MATRX>>

Use these for generating interactive content.
"""
    result3 = process_text_with_matrx(text3)
    print("\n✓ Example 3 Complete\n")
    
    # Example 4: Multiple fields
    print("\n[Example 4] Fetch Multiple Fields")
    print("=" * 80)
    text4 = """
Interactive Content Blocks:
<<MATRX>><<CONTENT_BLOCKS>><<CATEGORY_ID>>9980e68f-97fc-4f71-bf1d-22583b6cdf38<<FIELDS>>label,template<</MATRX>>
"""
    result4 = process_text_with_matrx(text4)
    print("\n✓ Example 4 Complete\n")
    
    # Example 5: Mixed patterns in complex text
    print("\n[Example 5] Complex Text with Multiple Patterns")
    print("=" * 80)
    text5 = """
# AI Content Generation Guide

## Flashcards
Use this structure: <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<<FIELDS>>label<</MATRX>>

Full template:
<<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<</MATRX>>

## Presentations
Template: <<MATRX>><<CONTENT_BLOCKS>><<ID>>b46e284e-ccb0-4d32-8a96-07f85d50d134<</MATRX>>

---
All interactive blocks available:
<<MATRX>><<CONTENT_BLOCKS>><<CATEGORY_ID>>9980e68f-97fc-4f71-bf1d-22583b6cdf38<<FIELDS>>label<</MATRX>>
"""
    result5 = process_text_with_matrx(text5)
    print("\n✓ Example 5 Complete\n")
    
    # Example 6: Demonstrate direct usage without helper
    print("\n[Example 6] Direct API Usage")
    print("=" * 80)
    text6 = "Template: <<MATRX>><<CONTENT_BLOCKS>><<BLOCK_ID>>flashcards<</MATRX>>"
    
    # Manual workflow
    patterns = MatrxPatternParser.parse(text6)
    print(f"Parsed {len(patterns)} pattern(s)")
    
    for pattern in patterns:
        print(f"\nPattern details:")
        print(f"  Table:  {pattern.table}")
        print(f"  Column: {pattern.column}")
        print(f"  Value:  {pattern.value}")
        print(f"  Fields:  {pattern.fields or '(default)'}")
        
        # Fetch manually
        fetched = MatrxFetcher.fetch(
            pattern.table,
            pattern.column,
            pattern.value,
            pattern.fields
        )
        vcprint(fetched, "Fetched Content", color="cyan")
    
    print("\n✓ Example 6 Complete\n")
    
    print("\n" + "=" * 80)
    print("ALL INTEGRATION TESTS PASSED! ✓")
    print("=" * 80)
    print("\n📚 USAGE SUMMARY:\n")
    print("1. Parse patterns:")
    print("   patterns = MatrxPatternParser.parse(text)")
    print("\n2. Fetch data:")
    print("   result = MatrxFetcher.fetch(table, column, value, field)")
    print("\n3. Or use all-in-one:")
    print("   result = MatrxFetcher.process_text_with_patterns(text, patterns)")
    print("\n4. Or use the helper:")
    print("   result = process_text_with_matrx(text)")
    print("=" * 80 + "\n")
