"""Markdown parser for converting to structured paragraphs."""

import re
from dataclasses import dataclass, field


@dataclass
class TextRun:
    """A piece of text with styling."""

    text: str
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    code: bool = False
    link: str | None = None


@dataclass
class Paragraph:
    """A paragraph with text runs."""

    runs: list[TextRun] = field(default_factory=list)
    heading_level: int = 0
    is_list_item: bool = False
    list_type: str = "BULLET"
    nesting_level: int = 0
    is_code_block: bool = False
    is_blockquote: bool = False


class MarkdownParser:
    """Parses markdown text into structured paragraphs."""

    # Pattern for inline formatting
    INLINE_PATTERN = (
        r"(\*\*\*(.+?)\*\*\*)|"  # bold italic
        r"(\*\*(.+?)\*\*)|"  # bold
        r"(__(.+?)__)|"  # bold alt
        r"(\*(.+?)\*)|"  # italic
        r"(_(.+?)_)|"  # italic alt
        r"(~~(.+?)~~)|"  # strikethrough
        r"(`(.+?)`)|"  # inline code
        r"(\[([^\]]+)\]\(([^)]+)\))"  # links
    )

    def __init__(self, markdown_text: str):
        self.markdown = markdown_text

    def parse(self) -> list[Paragraph]:
        """Parse markdown and return structured paragraphs."""
        lines = self.markdown.split("\n")
        paragraphs: list[Paragraph] = []
        i = 0
        in_code_block = False
        code_block_content: list[str] = []

        while i < len(lines):
            line = lines[i]

            # Code blocks
            if line.startswith("```"):
                if in_code_block:
                    para = Paragraph(is_code_block=True)
                    para.runs.append(TextRun("\n".join(code_block_content), code=True))
                    paragraphs.append(para)
                    code_block_content = []
                    in_code_block = False
                else:
                    in_code_block = True
                i += 1
                continue

            if in_code_block:
                code_block_content.append(line)
                i += 1
                continue

            if not line.strip():
                i += 1
                continue

            # Headers
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                content = header_match.group(2)
                para = Paragraph(heading_level=level)
                para.runs = self._parse_inline(content)
                paragraphs.append(para)
                i += 1
                continue

            # Unordered list
            ul_match = re.match(r"^(\s*)[-*+]\s+(.+)$", line)
            if ul_match:
                indent = len(ul_match.group(1))
                content = ul_match.group(2)
                para = Paragraph(
                    is_list_item=True,
                    list_type="BULLET",
                    nesting_level=indent // 2,
                )
                para.runs = self._parse_inline(content)
                paragraphs.append(para)
                i += 1
                continue

            # Ordered list
            ol_match = re.match(r"^(\s*)(\d+)\.\s+(.+)$", line)
            if ol_match:
                indent = len(ol_match.group(1))
                content = ol_match.group(3)
                para = Paragraph(
                    is_list_item=True,
                    list_type="NUMBER",
                    nesting_level=indent // 2,
                )
                para.runs = self._parse_inline(content)
                paragraphs.append(para)
                i += 1
                continue

            # Blockquote
            bq_match = re.match(r"^>\s*(.*)$", line)
            if bq_match:
                content = bq_match.group(1)
                para = Paragraph(is_blockquote=True)
                para.runs = self._parse_inline(content) if content else [TextRun("")]
                paragraphs.append(para)
                i += 1
                continue

            # Regular paragraph
            para = Paragraph()
            para.runs = self._parse_inline(line)
            paragraphs.append(para)
            i += 1

        return paragraphs

    def _parse_inline(self, text: str) -> list[TextRun]:
        """Parse inline formatting (bold, italic, code, links, etc.)."""
        runs: list[TextRun] = []

        last_end = 0
        for match in re.finditer(self.INLINE_PATTERN, text):
            if match.start() > last_end:
                plain = text[last_end : match.start()]
                if plain:
                    runs.append(TextRun(plain))

            if match.group(1):  # ***bold italic***
                runs.append(TextRun(match.group(2), bold=True, italic=True))
            elif match.group(3):  # **bold**
                runs.append(TextRun(match.group(4), bold=True))
            elif match.group(5):  # __bold__
                runs.append(TextRun(match.group(6), bold=True))
            elif match.group(7):  # *italic*
                runs.append(TextRun(match.group(8), italic=True))
            elif match.group(9):  # _italic_
                runs.append(TextRun(match.group(10), italic=True))
            elif match.group(11):  # ~~strikethrough~~
                runs.append(TextRun(match.group(12), strikethrough=True))
            elif match.group(13):  # `code`
                runs.append(TextRun(match.group(14), code=True))
            elif match.group(15):  # [text](url)
                runs.append(TextRun(match.group(16), link=match.group(17)))

            last_end = match.end()

        if last_end < len(text):
            remaining = text[last_end:]
            if remaining:
                runs.append(TextRun(remaining))

        if not runs:
            runs.append(TextRun(text))

        return runs
