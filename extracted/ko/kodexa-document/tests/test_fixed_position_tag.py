"""
Diagnostic test for fixed_position tagging issue.

The NumberStrategy uses fixed_position=[start, end] with sort_by_bbox=True
to tag words within a specific character range of a line's content.

This test verifies whether the Go library correctly implements this feature.
"""
import pytest
from kodexa_document import Document


def test_fixed_position_tag_basic():
    """
    Test that fixed_position tagging works to tag words within a character range.

    The legacy Python behavior:
    1. Get child words of a line
    2. Sort them by bounding box if sort_by_bbox=True
    3. Build content string by joining word contents with spaces
    4. Find which words fall within fixed_position character range
    5. Tag those specific words
    """
    doc = Document.create_in_memory()

    # Create a page
    page = doc.create_node(node_type="page", content="Page 1")

    # Create a line node
    line = doc.create_node(node_type="line", content="", parent=page)

    # Create word nodes with bounding boxes
    # Simulating: "Sales of products $ 12,044 $ 11,165 $ 11,016"
    words = [
        ("Sales", 0, 0, 30, 10),
        ("of", 35, 0, 45, 10),
        ("products", 50, 0, 100, 10),
        ("$", 105, 0, 115, 10),
        ("12,044", 120, 0, 160, 10),
        ("$", 165, 0, 175, 10),
        ("11,165", 180, 0, 220, 10),
        ("$", 225, 0, 235, 10),
        ("11,016", 240, 0, 280, 10),
    ]

    for word_text, x1, y1, x2, y2 in words:
        word = doc.create_node(node_type="word", content=word_text, parent=line)
        word.set_bbox([x1, y1, x2, y2])

    # Build the expected content string (space-separated)
    # "Sales of products $ 12,044 $ 11,165 $ 11,016"
    content = " ".join([w[0] for w in words])
    print(f"Content: {content}")
    print(f"Content length: {len(content)}")

    # Find position of "12,044"
    target = "12,044"
    start_idx = content.find(target)
    end_idx = start_idx + len(target)
    print(f"Target '{target}' at positions [{start_idx}, {end_idx}]")

    # Now try to tag with fixed_position
    tag_name = "test_number_tag"
    line.tag(tag_name, fixed_position=[start_idx, end_idx], sort_by_bbox=True)

    # Check which nodes got tagged
    tagged_nodes = line.select(f'//word[hasTag("{tag_name}")]')
    print(f"Tagged nodes count: {len(tagged_nodes)}")
    for node in tagged_nodes:
        print(f"  - Tagged: '{node.content}'")

    # The expected behavior: the word "12,044" should be tagged
    assert len(tagged_nodes) > 0, "Expected at least one node to be tagged"
    assert any(n.content == "12,044" for n in tagged_nodes), "Expected '12,044' to be tagged"


def test_fixed_position_options_passed_to_go():
    """
    Minimal test to check if fixed_position options are passed to Go correctly.
    """
    doc = Document.create_in_memory()
    page = doc.create_node(node_type="page", content="")
    line = doc.create_node(node_type="line", content="", parent=page)

    # Create some word children
    word1 = doc.create_node(node_type="word", content="Hello", parent=line)
    word2 = doc.create_node(node_type="word", content="World", parent=line)

    # Try tagging with fixed_position - this shouldn't crash
    # Even if it doesn't work correctly, we want to see if it at least runs
    try:
        line.tag("test_tag", fixed_position=[0, 5], sort_by_bbox=True)
        print("tag() with fixed_position succeeded (no crash)")
    except Exception as e:
        pytest.fail(f"tag() with fixed_position raised: {e}")

    # Check what got tagged
    tagged = line.select('//word[hasTag("test_tag")]')
    print(f"Tagged word count: {len(tagged)}")

    # Also check if the line itself got tagged (incorrect behavior)
    line_has_tag = line.has_tag("test_tag")
    print(f"Line has tag: {line_has_tag}")


if __name__ == "__main__":
    print("=" * 60)
    print("Test 1: Options passed to Go")
    print("=" * 60)
    test_fixed_position_options_passed_to_go()

    print("\n" + "=" * 60)
    print("Test 2: Basic fixed_position tagging")
    print("=" * 60)
    test_fixed_position_tag_basic()
