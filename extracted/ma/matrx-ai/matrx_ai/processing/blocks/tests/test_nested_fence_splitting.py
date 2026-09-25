"""FORCING FUNCTION: a ```markdown fence that carries its own ```bash block
stays ONE markdown block — in the static detector and while streaming.

The break this catches: strict-CommonMark closing, where the first inner bare
``` ends the markdown block mid-document, the rest of the document leaks out
as prose, and the outer closing ``` opens a phantom code block that swallows
the assistant's closing sentence. The rule is shared with the frontend's
splitters (matrx-frontend components/markdown-core/fence-nesting.ts); the
spec lives once in common-docs/systems/content-ir-system/NESTED-FENCES.md.

Use case: a recycling company's operations lead asks the assistant for a
README for their pickup-scheduling repository; the answer is a ```markdown
document containing a route table and a ```bash setup block.
"""

from __future__ import annotations

import pytest

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks
from matrx_ai.processing.blocks.fence_nesting import classify_inner_fence_line
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor

F = "```"

README_DOC = f"""# Pickup Scheduler

| Route | Day | Driver |
|---|---|---|
| North Industrial | Tuesday | D. Alvarez |
| Harbor Commercial | Thursday | K. Osei |

## Setup

{F}bash
pnpm install
pnpm db:seed --routes north,harbor
{F}

Run `pnpm dev` and open the route board."""

MESSAGE = f"""Here is the README for the pickup scheduler:

{F}markdown
{README_DOC}
{F}

Want me to add the driver onboarding section too?"""

# A different expected shape: a longer ````md fence already nested correctly
# under strict CommonMark and must keep doing so.
LONG_FENCE_MESSAGE = f"""Draft:

````md
{README_DOC}
````

Done."""

# A non-markdown fence keeps strict CommonMark: a ```bash heredoc whose body
# happens to contain a ```python line is closed by the first bare ```.
BASH_MESSAGE = f"""Script:

{F}bash
cat <<EOF
{F}python
print("hi")
{F}
EOF
{F}

End."""


def _shape(blocks):
    return [(b.type, b.language) for b in blocks]


class TestStaticDetector:
    def test_markdown_fence_with_inner_bash_block_is_one_block(self):
        blocks = split_content_into_blocks(MESSAGE)
        assert _shape(blocks) == [
            ("text", None),
            ("code", "markdown"),
            ("text", None),
        ]
        assert blocks[1].content == README_DOC
        assert blocks[2].content.strip() == (
            "Want me to add the driver onboarding section too?"
        )

    def test_longer_outer_fence_still_nests(self):
        blocks = split_content_into_blocks(LONG_FENCE_MESSAGE)
        assert _shape(blocks) == [("text", None), ("code", "md"), ("text", None)]
        assert blocks[1].content == README_DOC

    def test_non_markdown_fence_keeps_strict_commonmark(self):
        blocks = split_content_into_blocks(BASH_MESSAGE)
        code = [b for b in blocks if b.type == "code"]
        # The inner bare ``` closes the bash fence (strict), so the body stops
        # at the ```python line — unchanged behavior for non-document fences.
        assert code[0].language == "bash"
        assert code[0].content == f'cat <<EOF\n{F}python\nprint("hi")'

    def test_unclosed_nested_fence_falls_back_to_strict(self):
        # The inner ```bash never closes (the model forgot its closer before
        # starting a ```python block); the text ends with a nested fence still
        # open, so the extraction is redone strictly: the first bare ```
        # closes the OUTER fence rather than eating the rest of the message.
        msg = (
            f"{F}markdown\n# Doc\n\n{F}bash\npnpm install\n\n"
            f"{F}python\nprint(1)\n{F}\n\nAfter."
        )
        blocks = split_content_into_blocks(msg)
        assert blocks[0].type == "code" and blocks[0].language == "markdown"
        assert blocks[0].content == (
            f"# Doc\n\n{F}bash\npnpm install\n\n{F}python\nprint(1)"
        )
        assert blocks[-1].type == "text" and blocks[-1].content.strip() == "After."


class TestStreaming:
    @pytest.mark.parametrize("chunk", [1, 7, 64])
    def test_streamed_markdown_fence_is_one_block(self, chunk):
        proc = StreamBlockProcessor()
        events = []
        for start in range(0, len(MESSAGE), chunk):
            events.extend(proc.process_chunk(MESSAGE[start : start + chunk]))
        events.extend(proc.finalize())
        latest: dict[str, object] = {}
        order: list[str] = []
        for e in events:
            if e.block_id not in latest:
                order.append(e.block_id)
            latest[e.block_id] = e
        final = [latest[b] for b in order]
        code = [e for e in final if e.type == "code"]
        assert len(code) == 1, [(e.type, (e.content or "")[:40]) for e in final]
        assert code[0].content == README_DOC
        tail = [e for e in final if e.type == "text"][-1]
        assert "driver onboarding" in (tail.content or "")


class TestClassifier:
    @pytest.mark.parametrize(
        ("line", "open_ticks", "nests", "depth", "expected"),
        [
            ("```bash", 3, True, 0, "open-nested"),
            ("```", 3, True, 1, "close-nested"),
            ("```", 3, True, 0, "close-outer"),
            ("```bash", 3, False, 0, "content"),
            ("```", 4, True, 0, "content"),
            ("```python", 4, True, 0, "content"),
            ("``", 3, True, 0, "content"),
            ("plain text", 3, True, 1, "content"),
        ],
    )
    def test_matches_the_frontend_rule(self, line, open_ticks, nests, depth, expected):
        assert classify_inner_fence_line(line, open_ticks, nests, depth) == expected
