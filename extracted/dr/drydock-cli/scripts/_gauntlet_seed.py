"""Pre-seed a realistic mid-size Python project for the gauntlet.

Drops a working markdown→HTML converter (`mdparse`) into the workspace
with a pytest suite. ONE test is intentionally broken by a subtle
parser bug — that's L1 of the gauntlet: find and fix it.

Why a real-ish project: the prior gauntlet asked the model to scaffold
a 1-file Fibonacci CLI, which never exercised drydock's failure
modes (search_replace cascades, truncated_history, multi-file refactor
loops). Real bugs only surface when there's enough surface area to
collide with.

Footprint after seeding:
  mdparse/__init__.py        (~10 lines)
  mdparse/__main__.py        (~5 lines)
  mdparse/cli.py             (~30 lines)
  mdparse/lexer.py           (~70 lines)
  mdparse/parser.py          (~95 lines) ← planted bug
  mdparse/renderer.py        (~70 lines)
  mdparse/inline.py          (~55 lines)
  tests/test_lexer.py        (~35 lines)
  tests/test_parser.py       (~50 lines)
  tests/test_renderer.py     (~45 lines)
  tests/test_inline.py       (~35 lines)
  tests/test_e2e.py          (~25 lines)
  pytest.ini                 (~3 lines)
  README.md                  (~30 lines)
Total ~13 files, ~560 LOC.

Planted bug: parser._parse_blockquote() strips the leading "> " but
also drops the FIRST CHARACTER of the actual content (off-by-one on
the slice). test_parser_blockquote_text expects "hello world" but
gets "ello world", so the test fails. A grep-and-stare debugger would
find it in 30 seconds; for drydock the multi-step debugging cycle is
the point.
"""
from __future__ import annotations

from pathlib import Path

# ── source files ─────────────────────────────────────────────────────

_INIT_PY = '''"""mdparse — minimal markdown→HTML converter.

Public API:
    from mdparse import render_html, parse
"""
from mdparse.parser import parse
from mdparse.renderer import render_html

__all__ = ["parse", "render_html"]
__version__ = "0.1.0"
'''

_MAIN_PY = '''from mdparse.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
'''

_CLI_PY = '''"""CLI entry point for mdparse."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mdparse.parser import parse
from mdparse.renderer import render_html


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="mdparse",
                                description="Convert markdown to HTML.")
    p.add_argument("input", help="markdown file (or - for stdin)")
    p.add_argument("-o", "--output", default="-",
                   help="output path (default: stdout)")
    args = p.parse_args(argv)

    if args.input == "-":
        src = sys.stdin.read()
    else:
        src = Path(args.input).read_text(encoding="utf-8")

    ast = parse(src)
    html = render_html(ast)

    if args.output == "-":
        sys.stdout.write(html)
    else:
        Path(args.output).write_text(html, encoding="utf-8")
    return 0
'''

_LEXER_PY = '''"""Markdown lexer — splits source text into block tokens."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Token:
    kind: str        # "heading", "paragraph", "blockquote", "blank", "list_item", "code_fence"
    text: str = ""
    level: int = 0   # for headings
    lang: str = ""   # for code fences


def tokenize(source: str) -> list[Token]:
    lines = source.splitlines()
    tokens: list[Token] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped:
            tokens.append(Token(kind="blank"))
            i += 1
            continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            tokens.append(Token(kind="heading", text=text, level=level))
            i += 1
            continue
        if stripped.startswith(">"):
            text = stripped[1:].lstrip()
            tokens.append(Token(kind="blockquote", text=text))
            i += 1
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            tokens.append(Token(kind="list_item", text=stripped[2:]))
            i += 1
            continue
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            tokens.append(Token(kind="code_fence", text="\\n".join(buf), lang=lang))
            continue
        # Default: paragraph — coalesce following non-blank lines
        buf2 = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("#", ">", "- ", "* ", "```")):
            buf2.append(lines[i].strip())
            i += 1
        tokens.append(Token(kind="paragraph", text=" ".join(buf2)))
    return tokens
'''

_PARSER_PY = '''"""Markdown parser — converts the token stream into an AST.

AST nodes are tuples: (kind, payload).
  ("doc", [child, ...])
  ("heading", level, text)
  ("paragraph", text)
  ("blockquote", text)
  ("list", [item_text, ...])
  ("code", lang, text)
"""
from __future__ import annotations

from typing import Any

from mdparse.lexer import Token, tokenize


def parse(source: str) -> tuple[str, list[Any]]:
    tokens = tokenize(source)
    children: list[Any] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.kind == "blank":
            i += 1
            continue
        if tok.kind == "heading":
            children.append(("heading", tok.level, tok.text))
            i += 1
            continue
        if tok.kind == "paragraph":
            children.append(("paragraph", tok.text))
            i += 1
            continue
        if tok.kind == "blockquote":
            children.append(_parse_blockquote(tokens, i))
            # advance over all consecutive blockquote tokens
            while i < len(tokens) and tokens[i].kind == "blockquote":
                i += 1
            continue
        if tok.kind == "list_item":
            items: list[str] = []
            while i < len(tokens) and tokens[i].kind == "list_item":
                items.append(tokens[i].text)
                i += 1
            children.append(("list", items))
            continue
        if tok.kind == "code_fence":
            children.append(("code", tok.lang, tok.text))
            i += 1
            continue
        i += 1
    return ("doc", children)


def _parse_blockquote(tokens: list[Token], start: int) -> tuple[str, str]:
    """Collect consecutive blockquote tokens and join their text.

    NOTE: there is a deliberate off-by-one bug in this function. The
    test_parser_blockquote_text test will catch it.
    """
    parts: list[str] = []
    i = start
    while i < len(tokens) and tokens[i].kind == "blockquote":
        # BUG: should be tokens[i].text, but slicing [1:] drops the
        # first character of the legitimate content. Fix this.
        parts.append(tokens[i].text[1:])
        i += 1
    return ("blockquote", " ".join(parts))
'''

_RENDERER_PY = '''"""AST → HTML renderer."""
from __future__ import annotations

from typing import Any

from mdparse.inline import render_inline


def render_html(ast: tuple[str, list[Any]]) -> str:
    assert ast[0] == "doc"
    out: list[str] = []
    for node in ast[1]:
        out.append(_render_node(node))
    return "\\n".join(out) + "\\n"


def _render_node(node: tuple) -> str:
    kind = node[0]
    if kind == "heading":
        _, level, text = node
        return f"<h{level}>{render_inline(text)}</h{level}>"
    if kind == "paragraph":
        return f"<p>{render_inline(node[1])}</p>"
    if kind == "blockquote":
        return f"<blockquote>{render_inline(node[1])}</blockquote>"
    if kind == "list":
        items = "".join(f"<li>{render_inline(t)}</li>" for t in node[1])
        return f"<ul>{items}</ul>"
    if kind == "code":
        _, lang, text = node
        cls = f' class="lang-{lang}"' if lang else ""
        return f"<pre><code{cls}>{_escape(text)}</code></pre>"
    return ""


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))
'''

_INLINE_PY = '''"""Inline-element handling (bold, italic).

Note: inline-code (`code`) is intentionally NOT yet supported — adding
it is one of the gauntlet's level prompts.
"""
from __future__ import annotations

import re

_BOLD = re.compile(r"\\*\\*([^*]+)\\*\\*")
_ITALIC = re.compile(r"(?<!\\*)\\*([^*]+)\\*(?!\\*)")
_LINK = re.compile(r"\\[([^\\]]+)\\]\\(([^)]+)\\)")


def render_inline(text: str) -> str:
    text = _escape(text)
    text = _BOLD.sub(r"<strong>\\1</strong>", text)
    text = _ITALIC.sub(r"<em>\\1</em>", text)
    text = _LINK.sub(r'<a href="\\2">\\1</a>', text)
    return text


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))
'''

# ── tests ────────────────────────────────────────────────────────────

_TEST_LEXER = '''from mdparse.lexer import tokenize


def test_heading_h1():
    toks = tokenize("# Title")
    assert len(toks) == 1
    assert toks[0].kind == "heading"
    assert toks[0].level == 1
    assert toks[0].text == "Title"


def test_heading_h3():
    toks = tokenize("### Subsub")
    assert toks[0].level == 3


def test_paragraph_single():
    toks = tokenize("hello world")
    assert toks[0].kind == "paragraph"
    assert toks[0].text == "hello world"


def test_paragraph_multiline():
    toks = tokenize("foo\\nbar")
    assert toks[0].kind == "paragraph"
    assert toks[0].text == "foo bar"


def test_blockquote():
    toks = tokenize("> quoted")
    assert toks[0].kind == "blockquote"
    assert toks[0].text == "quoted"


def test_code_fence():
    src = "```python\\nx = 1\\n```"
    toks = tokenize(src)
    assert toks[0].kind == "code_fence"
    assert toks[0].lang == "python"
    assert "x = 1" in toks[0].text
'''

_TEST_PARSER = '''from mdparse.parser import parse


def test_doc_root():
    ast = parse("# Title")
    assert ast[0] == "doc"
    assert isinstance(ast[1], list)


def test_heading_node():
    _, kids = parse("## Subtitle")
    assert kids == [("heading", 2, "Subtitle")]


def test_paragraph_node():
    _, kids = parse("hello world")
    assert kids == [("paragraph", "hello world")]


def test_blockquote_text():
    """This one CATCHES the planted off-by-one bug in
    parser._parse_blockquote. Until that bug is fixed, this test
    fails with 'ello world' (missing leading 'h').
    """
    _, kids = parse("> hello world")
    assert kids == [("blockquote", "hello world")]


def test_list_basic():
    _, kids = parse("- one\\n- two\\n- three")
    assert kids == [("list", ["one", "two", "three"])]


def test_code_fence_node():
    _, kids = parse("```python\\nprint(1)\\n```")
    assert kids == [("code", "python", "print(1)")]


def test_mixed_document():
    src = "# Title\\n\\nA paragraph.\\n\\n- item 1\\n- item 2"
    _, kids = parse(src)
    assert kids[0] == ("heading", 1, "Title")
    assert kids[1] == ("paragraph", "A paragraph.")
    assert kids[2] == ("list", ["item 1", "item 2"])
'''

_TEST_RENDERER = '''from mdparse.parser import parse
from mdparse.renderer import render_html


def test_heading_render():
    out = render_html(parse("# Hello"))
    assert "<h1>Hello</h1>" in out


def test_paragraph_render():
    out = render_html(parse("hello world"))
    assert "<p>hello world</p>" in out


def test_bold_italic_render():
    out = render_html(parse("**bold** and *italic*"))
    assert "<strong>bold</strong>" in out
    assert "<em>italic</em>" in out


def test_link_render():
    out = render_html(parse("[click](https://example.com)"))
    assert '<a href="https://example.com">click</a>' in out


def test_blockquote_render():
    out = render_html(parse("> a quote"))
    assert "<blockquote>a quote</blockquote>" in out


def test_list_render():
    out = render_html(parse("- one\\n- two"))
    assert "<ul><li>one</li><li>two</li></ul>" in out


def test_code_fence_render():
    out = render_html(parse("```py\\nx = 1\\n```"))
    assert "<pre><code" in out
    assert 'class="lang-py"' in out
    assert "x = 1" in out
'''

_TEST_INLINE = '''from mdparse.inline import render_inline


def test_plain_text_escaped():
    assert render_inline("a < b") == "a &lt; b"


def test_bold():
    assert render_inline("**x**") == "<strong>x</strong>"


def test_italic():
    assert render_inline("*y*") == "<em>y</em>"


def test_link():
    out = render_inline("[here](http://x)")
    assert out == '<a href="http://x">here</a>'


def test_bold_and_italic_mixed():
    out = render_inline("**a** and *b*")
    assert "<strong>a</strong>" in out
    assert "<em>b</em>" in out
'''

_TEST_E2E = '''from mdparse import parse, render_html


def test_full_document_render():
    md = "# Hello\\n\\nThis is *fun*.\\n\\n- a\\n- b\\n"
    out = render_html(parse(md))
    assert "<h1>Hello</h1>" in out
    assert "<em>fun</em>" in out
    assert "<ul><li>a</li><li>b</li></ul>" in out


def test_blockquote_full_pipeline():
    """End-to-end version of the parser blockquote test — catches the
    same bug from the renderer side."""
    out = render_html(parse("> deep thoughts"))
    assert "<blockquote>deep thoughts</blockquote>" in out
'''

_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_README = '''# mdparse

A minimal markdown→HTML converter, ~500 lines of pure-stdlib Python.

## Usage

```
python3 -m mdparse README.md         # → stdout
python3 -m mdparse README.md -o x.html
```

## Layout

- `mdparse/lexer.py`     tokenizer (block-level)
- `mdparse/parser.py`    token stream → AST
- `mdparse/renderer.py`  AST → HTML
- `mdparse/inline.py`    inline elements (bold, italic, links)
- `mdparse/cli.py`       command-line entry point

## Tests

```
pytest -q
```
'''


_FILES: dict[str, str] = {
    "mdparse/__init__.py": _INIT_PY,
    "mdparse/__main__.py": _MAIN_PY,
    "mdparse/cli.py": _CLI_PY,
    "mdparse/lexer.py": _LEXER_PY,
    "mdparse/parser.py": _PARSER_PY,
    "mdparse/renderer.py": _RENDERER_PY,
    "mdparse/inline.py": _INLINE_PY,
    "tests/test_lexer.py": _TEST_LEXER,
    "tests/test_parser.py": _TEST_PARSER,
    "tests/test_renderer.py": _TEST_RENDERER,
    "tests/test_inline.py": _TEST_INLINE,
    "tests/test_e2e.py": _TEST_E2E,
    "pytest.ini": _PYTEST_INI,
    "README.md": _README,
}


def seed_mdparse(cwd: Path) -> None:
    """Write the markdown-parser seed project into `cwd`.

    Idempotent: overwrites any pre-existing files at these paths.
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
