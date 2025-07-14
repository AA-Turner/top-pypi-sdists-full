# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Find code blocks in RST files.
"""

from __future__ import annotations

import os
import typing as t
from collections.abc import Mapping
from dataclasses import dataclass

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged as directive_param_unchanged

from .utils import parse_document

_SPECIAL_ATTRIBUTES = (
    "antsibull-code-language",
    "antsibull-code-block",
    "antsibull-code-content-offset",
    "antsibull-code-lineno",
)


class IgnoreDirective(Directive):
    """
    Directive that simply ignores its content.
    """

    has_content = True

    def run(self) -> list:
        return []


def mark_antsibull_code_block(
    node: nodes.literal_block,
    *,
    language: str | None,
    line: int | None = None,
    content_offset: int | None = None,
    other: dict[str, t.Any] | None = None,
) -> None:
    """
    Mark a literal block as an Antsibull code block with given language and line number.

    Everything in ``other`` will be available as ``antsibull-other-{key}`` for a key ``key``
    in ``other`` in the node's attributes.
    """
    if (line is None) == (content_offset is None):
        raise AssertionError(  # pragma: no cover
            "At least one of line and content_offset must be provided"
        )
    node["antsibull-code-language"] = language
    node["antsibull-code-block"] = True
    node["antsibull-code-lineno"] = line
    node["antsibull-code-content-offset"] = content_offset
    if other:
        for key, value in other.items():
            node[f"antsibull-other-{key}"] = value


class CodeBlockDirective(Directive):
    """
    Fake code block directive.

    Acts similar to Sphinx's code block directives, except that it calls
    ``mark_antsibull_code_block()`` on the generated literal blocks.
    """

    has_content = True
    optional_arguments = 1

    # These are all options Sphinx allows for code blocks.
    # We need to have them here so that docutils successfully parses this extension.
    option_spec = {
        "caption": directive_param_unchanged,
        "class": directive_param_unchanged,
        "dedent": directive_param_unchanged,
        "emphasize-lines": directive_param_unchanged,
        "name": directive_param_unchanged,
        "force": directive_param_unchanged,
        "linenos": directive_param_unchanged,
        "lineno-start": directive_param_unchanged,
    }

    def run(self) -> list[nodes.literal_block]:
        code = "\n".join(self.content)
        literal = nodes.literal_block(code, code)
        literal["classes"].append("code-block")
        mark_antsibull_code_block(
            literal,
            language=self.arguments[0] if self.arguments else None,
            content_offset=self.content_offset,
        )
        return [literal]


def _find_indent(content: str) -> int | None:
    """
    Given concatenated lines, find the minimum indent if possible.

    If all lines consist only out of whitespace (or are empty),
    ``None`` is returned.
    """
    min_indent = None
    for line in content.split("\n"):
        stripped_line = line.lstrip()
        if stripped_line:
            indent = len(line) - len(line.lstrip())
            if min_indent is None or min_indent > indent:
                min_indent = indent
    return min_indent


def _find_offset_from_content_offset(
    content_offset: int, content: str, *, document_content_lines: list[str]
) -> tuple[int, int, bool]:
    """
    Try to identify the row/col offset of the code in ``content`` in the document.

    ``content_offset`` is assumed to be the content_offset where the code-block's
    contents start.
    """
    content_lines = content.count("\n") + 1
    min_indent = None
    for line in document_content_lines[content_offset:]:
        if content_lines <= 0:
            break
        stripped_line = line.strip()
        if stripped_line:
            indent = len(line) - len(line.lstrip())
            if min_indent is None or min_indent > indent:
                min_indent = indent
        content_lines -= 1

    min_source_indent = _find_indent(content)
    col_offset = max(0, (min_indent or 0) - (min_source_indent or 0))
    return content_offset, col_offset, content_lines == 0


def _find_offset(
    lineno: int | None,
    content_offset: int | None,
    content: str,
    *,
    document_content_lines: list[str],
) -> tuple[int, int, bool]:
    """
    Try to identify the row/col offset of the code in ``content`` in the document.

    ``lineno`` is assumed to be the line where the code-block starts.
    This function looks for an empty line, followed by the right pattern of
    empty and non-empty lines.
    """
    if content_offset is not None:
        return _find_offset_from_content_offset(
            content_offset, content, document_content_lines=document_content_lines
        )

    assert lineno is not None
    row_offset = lineno
    found_empty_line = False
    found_content_lines = False
    content_lines = content.count("\n") + 1
    min_indent = None
    for offset, line in enumerate(document_content_lines[lineno:]):
        stripped_line = line.strip()
        if not stripped_line:
            if not found_empty_line:
                row_offset = lineno + offset + 1
                found_empty_line = True
        elif not found_content_lines:
            found_content_lines = True
            row_offset = lineno + offset

        if found_content_lines and content_lines > 0:
            if stripped_line:
                indent = len(line) - len(line.lstrip())
                if min_indent is None or min_indent > indent:
                    min_indent = indent
            content_lines -= 1
        elif not content_lines:
            break

    min_source_indent = _find_indent(content)
    col_offset = max(0, (min_indent or 0) - (min_source_indent or 0))
    return row_offset, col_offset, content_lines == 0


def _find_in_code(
    row_offset: int,
    col_offset: int,
    content: str,
    *,
    document_content_lines: list[str],
) -> bool:
    """
    Check whether the code can be found at the given row/col offset in a way
    that makes it easy to replace.

    That is, it is surrounded only by whitespace.
    """
    for index, line in enumerate(content.split("\n")):
        if row_offset + index >= len(document_content_lines):
            return False
        found_line = document_content_lines[row_offset + index]
        if found_line[:col_offset].strip():
            return False
        eol = found_line[col_offset:]
        if eol[: len(line)] != line:
            return False
        if eol[len(line) :].strip():
            return False
    return True


class CodeBlockVisitor(nodes.SparseNodeVisitor):
    """
    Visitor that calls callbacks for all code blocks.
    """

    def __init__(
        self,
        document: nodes.document,
        content: str,
        callback: t.Callable[
            [str, int, int, bool, bool, str, nodes.literal_block], None
        ],
        warn_unknown_block: t.Callable[
            [int | str, int, nodes.literal_block, bool], None
        ],
    ):
        super().__init__(document)
        self.__content_lines = content.splitlines()
        self.__callback = callback
        self.__warn_unknown_block = warn_unknown_block

    def visit_system_message(self, node: nodes.system_message) -> None:
        """
        Ignore system messages.
        """
        raise nodes.SkipNode

    def visit_error(self, node: nodes.error) -> None:
        """
        Ignore errors.
        """
        raise nodes.SkipNode

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        """
        Visit a code block.
        """
        if "antsibull-code-block" not in node.attributes:
            # This could be a `::` block, or something else (unknown)
            self.__warn_unknown_block(
                node.line or "unknown", 0, node, bool(node.attributes["classes"])
            )
            raise nodes.SkipNode

        language = node.attributes["antsibull-code-language"]
        lineno = node.attributes["antsibull-code-lineno"]
        content_offset = node.attributes["antsibull-code-content-offset"]
        row_offset, col_offset, position_exact = _find_offset(
            lineno,
            content_offset,
            node.rawsource,
            document_content_lines=self.__content_lines,
        )
        found_in_code = False
        if position_exact:
            # If we think we have the exact position, try to identify the code.
            # ``found_in_code`` indicates that it is easy to replace the code,
            # and at the same time it's easy to identify it.
            found_in_code = _find_in_code(
                row_offset,
                col_offset,
                node.rawsource,
                document_content_lines=self.__content_lines,
            )
            if not found_in_code:
                position_exact = False
        if not found_in_code:
            # We were not able to find the code 'the easy way'. This could be because
            # it is inside a table.

            # pylint: disable-next=fixme
            pass  # TODO search for the content, f.ex. in tables
        self.__callback(
            language,
            row_offset,
            col_offset,
            position_exact,
            found_in_code,
            node.rawsource.rstrip() + "\n",
            node,
        )
        raise nodes.SkipNode


_DIRECTIVES: dict[str, t.Type[Directive]] = {
    # Replace Sphinx code blocks with our code block directive:
    "code": CodeBlockDirective,
    "code-block": CodeBlockDirective,
    "sourcecode": CodeBlockDirective,
    # The following docutils directives should better be ignored:
    "parsed-literal": IgnoreDirective,
}


@dataclass
class CodeBlockInfo:
    """
    Information on a code block
    """

    # The code block's language (if known)
    language: str | None

    # The code block's line and column offset
    row_offset: int
    col_offset: int

    # Whether the position (row/col_offset) is exact.
    # If set to ``False``, the position is approximate and col_offset is often 0.
    position_exact: bool

    # Whether the code block's contents can be found as-is in the RST file,
    # only indented by whitespace, and with potentially trailing whitespace
    directly_replacable_in_content: bool

    # The code block's contents
    content: str

    # The code block's attributes that start with ``antsibull-``.
    # Special attributes used by ``find_code_blocks()`` to keep track of
    # certain properties are not present.
    attributes: dict[str, t.Any]


def get_code_block_directives(
    *,
    extra_directives: Mapping[str, t.Type[Directive]] | None = None,
) -> Mapping[str, t.Type[Directive]]:
    """
    Return directives needed to find all code blocks.

    You can pass an optional mapping with directives that will be added
    to the result.
    """
    directives = _DIRECTIVES.copy()
    if extra_directives:
        directives.update(extra_directives)
    return directives


def find_code_blocks_in_document(
    *,
    document: nodes.document,
    content: str,
    warn_unknown_block: t.Callable[[int | str, int, str], None] | None = None,
    warn_unknown_block_w_unknown_info: (
        t.Callable[[int | str, int, str, bool], None] | None
    ) = None,
) -> t.Generator[CodeBlockInfo]:
    """
    Given a parsed RST document, finds all code blocks.

    All code blocks must be parsed with special directives
    (see ``get_code_block_directives()``) that have appropriate metadata
    registered with ``mark_antsibull_code_block()``.

    You can provide callbacks:
    * ``warn_unknown_block()`` will be called for every literal block
      that's of unknown origin.
    * ``warn_unknown_block_w_unknown_info()`` will be called for every
      literal block that's of known or unknown origin.
    """
    # If someone can figure out how to yield from a sub-function, we can avoid
    # using this ugly list
    results = []

    def callback(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        language: str,
        row_offset: int,
        col_offset: int,
        position_exact: bool,
        directly_replacable_in_content: bool,
        content: str,
        node: nodes.literal_block,
    ) -> None:
        results.append(
            CodeBlockInfo(
                language=language,
                row_offset=row_offset,
                col_offset=col_offset,
                position_exact=position_exact,
                directly_replacable_in_content=directly_replacable_in_content,
                content=content,
                attributes={
                    key: value
                    for key, value in node.attributes.items()
                    if key not in _SPECIAL_ATTRIBUTES and key.startswith("antsibull-")
                },
            )
        )

    def warn_unknown_block_cb(
        line: int | str,
        col: int,
        node: nodes.literal_block,
        unknown_directive: bool,
    ) -> None:
        if warn_unknown_block and unknown_directive:
            warn_unknown_block(line, col, node.rawsource)
        if warn_unknown_block_w_unknown_info:
            warn_unknown_block_w_unknown_info(
                line, col, node.rawsource, unknown_directive
            )

    # Process the document
    try:
        visitor = CodeBlockVisitor(document, content, callback, warn_unknown_block_cb)
        document.walk(visitor)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Cannot process document: {exc}") from exc  # pragma: no cover
    finally:
        yield from results


def find_code_blocks(  # pylint: disable=too-many-arguments
    content: str,
    *,
    path: str | os.PathLike[str] | None = None,
    root_prefix: str | os.PathLike[str] | None = None,
    extra_directives: Mapping[str, t.Type[Directive]] | None = None,
    warn_unknown_block: t.Callable[[int | str, int, str], None] | None = None,
    warn_unknown_block_w_unknown_info: (
        t.Callable[[int | str, int, str, bool], None] | None
    ) = None,
) -> t.Generator[CodeBlockInfo]:
    """
    Given a RST document, finds all code blocks.

    To add support for own types of code blocks, you can pass these
    as ``extra_directives``. Use ``mark_antsibull_code_block()`` to
    mark them to be found by ``find_code_blocks()``.

    You can provide callbacks:
    * ``warn_unknown_block()`` will be called for every literal block
      that's of unknown origin.
    * ``warn_unknown_block_w_unknown_info()`` will be called for every
      literal block that's of known or unknown origin.
    """
    directives = get_code_block_directives(extra_directives=extra_directives)

    doc = parse_document(
        content,
        parser_name="restructuredtext",
        path=path,
        root_prefix=root_prefix,
        rst_directives=directives,
    )

    yield from find_code_blocks_in_document(
        document=doc,
        content=content,
        warn_unknown_block=warn_unknown_block,
        warn_unknown_block_w_unknown_info=warn_unknown_block_w_unknown_info,
    )


__all__ = ("CodeBlockInfo", "mark_antsibull_code_block", "find_code_blocks")
