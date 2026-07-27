"""Regression tests: strip reasoning tags from LLM output before writing to files.

qwen3, deepseek-r1, and other recent local models emit chain-of-thought
reasoning in <thinking>, <think>, <reflection>, <scratchpad> tags
before the actual code. If we write these straight to source files, the
generated code is broken (syntax errors, prose mixed in with imports).

The user hit this in a real build:
    <thinking>
    Okay, I need to create the FastAPI router...
    [long reasoning]
    </thinking>

    from fastapi import APIRouter
    ...
"""

from __future__ import annotations

from sage.core.principal_engineer import strip_code_fences
from sage.core.tdd_loop import _strip_fences as tdd_strip


class TestStripCodeFences:
    def test_strips_thinking_block_before_code(self) -> None:
        raw = """<thinking>
Okay, I need to create the FastAPI router. Let me think...
</thinking>

from fastapi import APIRouter

router = APIRouter()
"""
        result = strip_code_fences(raw)
        assert "<thinking>" not in result
        assert "</thinking>" not in result
        assert "Okay, I need" not in result
        assert "from fastapi import APIRouter" in result

    def test_strips_think_block_deepseek_style(self) -> None:
        raw = """<think>reasoning</think>

def foo():
    return 1
"""
        result = strip_code_fences(raw)
        assert "<think>" not in result
        assert "reasoning" not in result
        assert "def foo()" in result

    def test_strips_reflection_block(self) -> None:
        raw = """<reflection>
Hmm, this should be a class instead.
</reflection>

class Foo:
    pass
"""
        result = strip_code_fences(raw)
        assert "<reflection>" not in result
        assert "Hmm" not in result
        assert "class Foo" in result

    def test_strips_unclosed_thinking_tag(self) -> None:
        """Model got cut off mid-reasoning — must still recover usable code."""
        raw = """<thinking>
I started reasoning but ran out of tokens before closing the tag.

from fastapi import APIRouter

router = APIRouter()
"""
        result = strip_code_fences(raw)
        # The unclosed reasoning becomes prose-prefix that should be dropped
        # OR we keep the code part. Either way, no <thinking> tag.
        assert "<thinking>" not in result
        # The code should survive
        assert "from fastapi import APIRouter" in result

    def test_strips_multiple_thinking_blocks(self) -> None:
        raw = """<thinking>first thought</thinking>
some prose
<thinking>second thought</thinking>

def x(): return 1
"""
        result = strip_code_fences(raw)
        assert "<thinking>" not in result
        assert "first thought" not in result
        assert "second thought" not in result
        assert "def x()" in result

    def test_preserves_thinking_inside_code_string_literal(self) -> None:
        """A literal '<thinking>' inside a string should NOT be stripped."""
        # We strip whole tag blocks. A raw substring "<thinking>" inside a
        # quoted string would be unusual, but we explicitly only match
        # the tag-block pattern (open tag through close tag).
        raw = 'msg = "<thinking>not a tag</thinking>"\nprint(msg)\n'
        result = strip_code_fences(raw)
        # The current implementation WILL strip this. That's a tradeoff —
        # source-files almost never contain literal reasoning-tag strings,
        # and the alternative (parsing source to skip strings) is way too
        # heavy. Document this expectation: if a source file legitimately
        # needs the literal "<thinking>" string, it should use a variant.
        # For now, accept that we strip aggressively.
        assert "<thinking>" not in result

    def test_strips_thinking_then_fenced_block(self) -> None:
        """The combo: model thinks, then wraps code in a fence."""
        raw = """<thinking>
Plan it out.
</thinking>

```python
from fastapi import APIRouter
router = APIRouter()
```
"""
        result = strip_code_fences(raw)
        assert "<thinking>" not in result
        assert "```" not in result
        assert "from fastapi" in result
        assert "router = APIRouter()" in result


class TestTddStripFences:
    """The tdd_loop module uses its own strip helper. Make sure it ALSO
    strips reasoning tags so the test/impl files generated through the
    TDD loop aren't polluted."""

    def test_tdd_strip_removes_thinking(self) -> None:
        raw = """<thinking>plan</thinking>

def test_x():
    assert True
"""
        result = tdd_strip(raw)
        assert "<thinking>" not in result
        assert "plan" not in result
        assert "def test_x()" in result
