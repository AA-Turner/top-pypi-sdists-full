"""Tests for block_detector.py — the Python port of content-splitter-v2."""

import pytest
from matrx_ai.processing.blocks.block_detector import (
    DetectedBlock,
    detect_code_block,
    detect_image,
    detect_json_block_type,
    detect_table_row,
    detect_video,
    detect_xml_block_type,
    normalize_line,
    split_content_into_blocks,
    validate_json_block,
)


class TestLineNormalization:
    def test_normalize_line_passthrough(self):
        assert normalize_line("Hello world") == "Hello world"

    def test_normalize_line_blanks_whitespace_only(self):
        assert normalize_line("   \t  ") == ""


class TestCodeBlockDetection:
    def test_detect_code_block_with_language(self):
        is_code, lang = detect_code_block("```python")
        assert is_code is True
        assert lang == "python"

    def test_detect_code_block_no_language(self):
        is_code, lang = detect_code_block("```")
        assert is_code is True
        assert lang is None

    def test_not_code_block(self):
        is_code, lang = detect_code_block("hello world")
        assert is_code is False


class TestJsonBlockDetection:
    def test_detect_quiz(self):
        content = '{"quiz_title": "My Quiz", "multiple_choice": []}'
        assert detect_json_block_type(content) == "quiz"

    def test_detect_diagram(self):
        content = '{"diagram": {"title": "Test", "nodes": []}}'
        assert detect_json_block_type(content) == "diagram"

    def test_detect_unknown_json(self):
        content = '{"foo": "bar"}'
        assert detect_json_block_type(content) is None

    def test_validate_complete_quiz(self):
        import json
        quiz = {"quiz_title": "Test", "multiple_choice": [{"id": 1, "question": "Q?", "options": ["A"], "correctAnswer": 0, "explanation": "E"}]}
        result = validate_json_block(json.dumps(quiz), "quiz")
        assert result["is_complete"] is True
        assert result["should_show"] is True


class TestXmlBlockDetection:
    def test_detect_flashcards(self):
        assert detect_xml_block_type("<flashcards>") == ("flashcards", "<flashcards>")

    def test_detect_thinking(self):
        assert detect_xml_block_type("<thinking>") == ("thinking", "<thinking>")
        assert detect_xml_block_type("<think>") == ("thinking", "<think>")

    def test_detect_unknown(self):
        assert detect_xml_block_type("<unknown>") is None


class TestMediaDetection:
    def test_detect_image(self):
        is_img, src, alt = detect_image("![Alt text](https://example.com/img.png)")
        assert is_img is True
        assert src == "https://example.com/img.png"
        assert alt == "Alt text"

    def test_detect_custom_image(self):
        is_img, src, alt = detect_image("[Image URL: https://example.com/img.png]")
        assert is_img is True
        assert src == "https://example.com/img.png"

    def test_detect_video(self):
        is_vid, src, alt = detect_video("[Video URL: https://example.com/vid.mp4]")
        assert is_vid is True
        assert src == "https://example.com/vid.mp4"

    def test_no_image(self):
        is_img, _, _ = detect_image("Just some text")
        assert is_img is False


class TestTableDetection:
    def test_detect_table_row(self):
        assert detect_table_row("| col1 | col2 |") is True
        assert detect_table_row("not a table") is False


class TestSplitContentIntoBlocks:
    def test_plain_text(self):
        blocks = split_content_into_blocks("Hello world")
        assert len(blocks) == 1
        assert blocks[0].type == "text"
        assert "Hello world" in blocks[0].content

    def test_code_block(self):
        md = "Some text\n```python\nprint('hi')\n```\nMore text"
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "text" in types
        assert "code" in types

    def test_code_block_language(self):
        md = "```javascript\nconsole.log('hi')\n```"
        blocks = split_content_into_blocks(md)
        code_blocks = [b for b in blocks if b.type == "code"]
        assert len(code_blocks) == 1
        assert code_blocks[0].language == "javascript"

    def test_embedded_kind_json_escapes_non_json_fence_losslessly(self):
        payload = '{"__kind":"rating","value":4.5}'
        source = f"before\n{payload}\nafter"
        blocks = split_content_into_blocks(f"```python\n{source}\n```")

        assert [block.type for block in blocks] == ["code", "code", "code"]
        assert blocks[1].language == "json"
        assert blocks[1].content == payload
        assert "".join(block.content for block in blocks) == source

    def test_kind_marker_in_value_and_malformed_json_stay_in_container(self):
        source = '{"label":"__kind"}\n{"__kind":"unfinished".'
        blocks = split_content_into_blocks(f"```text\n{source}\n```")

        assert len(blocks) == 1
        assert blocks[0].content == source

    def test_xml_tag_block(self):
        md = "Intro text\n<flashcards>\nFront: Q1\nBack: A1\n</flashcards>\nOutro"
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "flashcards" in types

    def test_image_detection(self):
        md = "Text before\n![Alt](https://example.com/img.png)\nText after"
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "image" in types

    def test_table_detection(self):
        md = "Text\n| A | B |\n|---|---|\n| 1 | 2 |\nMore text"
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "table" in types

    def test_json_quiz_detection(self):
        import json
        quiz = {"quiz_title": "Test", "multiple_choice": [{"id": 1, "question": "Q?", "options": ["A", "B"], "correctAnswer": 0, "explanation": "E"}]}
        md = f"Text\n```json\n{json.dumps(quiz)}\n```\nMore"
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "quiz" in types

    def test_multiple_block_types(self):
        md = """Here is some text.

```python
x = 1
```

| Col1 | Col2 |
|------|------|
| A    | B    |

More text here."""
        blocks = split_content_into_blocks(md)
        types = [b.type for b in blocks]
        assert "text" in types
        assert "code" in types
        assert "table" in types

    def test_special_code_language_transcript(self):
        md = "```transcript\n[00:01] Hello\n[00:05] World\n```"
        blocks = split_content_into_blocks(md)
        assert any(b.type == "transcript" for b in blocks)

    def test_special_code_language_tasks(self):
        md = "```tasks\n## Section\n- [x] Task 1\n- [ ] Task 2\n```"
        blocks = split_content_into_blocks(md)
        assert any(b.type == "tasks" for b in blocks)
