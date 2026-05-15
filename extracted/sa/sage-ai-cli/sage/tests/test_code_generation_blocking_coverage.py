"""Full-branch tests for sage.core.code_generation_blocking.CodeBlockerV2."""

from __future__ import annotations

import pytest

from sage.core.code_generation_blocking import CodeBlockerV2


@pytest.fixture
def blocker():
    return CodeBlockerV2()


class TestCheck:

    def test_clean_text_passes(self, blocker):
        violated, issues = blocker.check("This is just analysis text.")
        assert not violated
        assert issues == []

    def test_file_block_always_violates(self, blocker):
        violated, issues = blocker.check("FILE: foo.py\n```py\nprint(1)\n```")
        assert violated
        assert any("FILE:" in i for i in issues)

    def test_language_code_block_violates(self, blocker):
        text = "Here is the implementation:\n```python\ndef x(): pass\n```"
        violated, issues = blocker.check(text)
        assert violated

    def test_short_alias_language_block_violates(self, blocker):
        text = "```py\ndef x(): pass\n```"
        violated, _ = blocker.check(text)
        assert violated

    def test_bash_block_is_allowed(self, blocker):
        violated, _ = blocker.check("```bash\nls -la\n```")
        assert not violated

    def test_inline_code_reference_is_allowed(self, blocker):
        violated, _ = blocker.check("Modify the `foo()` function.")
        assert not violated

    def test_illustrative_context_allows_code(self, blocker):
        text = "Current code:\n```python\ndef broken(): pass\n```"
        violated, _ = blocker.check(text)
        assert not violated

    def test_numbered_list_context_allows_code(self, blocker):
        text = "1. ```python\ndef x(): pass\n```"
        violated, _ = blocker.check(text)
        assert not violated


class TestHelpers:

    def test_has_code_true_for_python_block(self, blocker):
        assert blocker.has_code("```python\nx=1\n```") is True

    def test_has_code_false_for_plain_text(self, blocker):
        assert blocker.has_code("just words") is False

    def test_detect_language_python(self, blocker):
        assert blocker.detect_language("```python\nx=1\n```") == "python"

    def test_detect_language_alias_resolves(self, blocker):
        assert blocker.detect_language("```py\nx=1\n```") == "python"
        assert blocker.detect_language("```ts\nx=1\n```") == "typescript"

    def test_detect_language_none_when_absent(self, blocker):
        assert blocker.detect_language("no code here") is None

    def test_strip_code_removes_blocks(self, blocker):
        text = "before\n```python\nx=1\n```\nafter"
        result = blocker.strip_code(text, remove_completely=True)
        assert "x=1" not in result
        assert "before" in result and "after" in result

    def test_strip_code_marker_mode(self, blocker):
        text = "```python\nx=1\n```"
        result = blocker.strip_code(text, remove_completely=False)
        assert "x=1" not in result
        assert "Code block removed" in result

    def test_has_file_blocks_true(self, blocker):
        assert blocker.has_file_blocks("FILE: x.py") is True

    def test_has_file_blocks_false(self, blocker):
        assert blocker.has_file_blocks("just analysis") is False

    def test_has_commands_detects_inline(self, blocker):
        assert blocker.has_commands("Run: `pip install x`") is True

    def test_has_commands_detects_bash_block(self, blocker):
        assert blocker.has_commands("```bash\nls\n```") is True

    def test_has_commands_false_for_plain(self, blocker):
        assert blocker.has_commands("nothing here") is False

    def test_contains_code_returns_bool(self, blocker):
        assert blocker.contains_code("```python\nx=1\n```") is True
        assert blocker.contains_code("plain words") is False

    def test_extract_code_blocks_returns_metadata(self, blocker):
        text = "```python\nA=1\n```\nstuff\n```js\nB=2\n```"
        blocks = blocker.extract_code_blocks(text)
        assert len(blocks) == 2
        assert blocks[0]["language"] == "python"
        assert "A=1" in blocks[0]["code"]
        assert blocks[1]["language"] == "js"


class TestBlockingPrompt:

    def test_returns_empty_when_not_read_only(self, blocker):
        from types import SimpleNamespace
        cls = SimpleNamespace(strict_read_only=False)
        assert blocker.get_blocking_prompt(cls) == ""

    def test_includes_quantity_reminder(self, blocker):
        from types import SimpleNamespace
        cls = SimpleNamespace(
            strict_read_only=True, quantity_required=10,
            request_type=SimpleNamespace(name="ANALYSIS"),
            pipeline_type=SimpleNamespace(name="READ_ONLY"),
        )
        out = blocker.get_blocking_prompt(cls)
        assert "10+ ITEMS" in out
        assert "ANALYSIS" in out

    def test_request_type_falls_back_when_not_enum(self, blocker):
        from types import SimpleNamespace
        cls = SimpleNamespace(
            strict_read_only=True, quantity_required=0,
            request_type="ANALYSIS",  # plain string, no .name
            pipeline_type="READ_ONLY",
        )
        out = blocker.get_blocking_prompt(cls)
        # Plain-string branch of the .name fallback
        assert "ANALYSIS" in out
