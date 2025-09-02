from collections.abc import Iterator
from contextlib import suppress
from operator import itemgetter
from typing import NamedTuple

from more_itertools import chunked
from tree_sitter import Node

from fluidattacks_core.serializers.syntax import (
    TREE_SITTER_FUNCTION_DECLARATION_MAP,
    TREE_SITTER_FUNCTION_IDENTIFIER,
    TREE_SITTER_LANGUAGE_CONVERSION,
    InvalidFileType,
    extract_function_nodes,
    extract_hierarchical_nodes,
    get_language_from_path,
    get_node_content,
)

# Constants
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


class SnippetViewport(NamedTuple):
    line: int
    column: int | None = None

    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False
    show_line_numbers: bool = True
    highlight_line_number: bool = True


class Function(NamedTuple):
    name: str | None = None
    node_type: str | None = None
    field_identifier_name: str | None = None


class Snippet(NamedTuple):
    content: str
    offset: int
    line: int | None = None
    column: int | None = None
    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False
    show_line_numbers: bool = True
    highlight_line_number: bool = True
    start_point: tuple[int, int] | None = None
    end_point: tuple[int, int] | None = None
    is_function: bool = False
    function: Function | None = None

    def reshape(self, *, viewport: SnippetViewport) -> "Snippet":
        """Reshapes the given Snippet to the specified SnippetViewport.

        The original focus line cannot be changed, but the content will be
        adjusted to fit the viewport. The method calculates the vertical and
        horizontal center of the snippet, and then slices the content to fit
        the viewport. It also handles line numbers and highlighting as needed.

        Args:
            viewport (SnippetViewport | None, optional): The viewport to
            reshape the snippet to. Defaults to None.

        Returns:
            Snippet: The reshaped Snippet.

        """
        if not self.line:
            return self
        snippet = make_snippet(
            content=self.content,
            viewport=viewport._replace(line=self.line),
            offset=self.offset,
        )
        line_context = self.line_context - snippet.offset
        snippet = snippet._replace(
            offset=self.offset + snippet.offset,
            is_function=self.is_function
            if len(snippet.content.splitlines()) == len(self.content.splitlines())
            else False,
            function=self.function,
            line_context=line_context,
        )
        return snippet


def make_snippet(
    *,
    content: str,
    viewport: SnippetViewport | None = None,
    offset: int | None = None,
) -> Snippet:
    # Replace tab by spaces so 1 char renders as 1 symbol
    lines_raw: list[str] = content.replace("\t", " ").splitlines()
    offset = offset or 0
    # Build a list of line numbers to line contents, handling wrapping
    if viewport is not None:
        lines = _get_lines(lines_raw, viewport, offset=offset)
        # Find the vertical center of the snippet
        viewport_center = next(
            (index for index, (line_no, _) in enumerate(lines) if line_no == viewport.line),
            0,
        )

        # Find the horizontal left of the snippet
        # We'll place the center at 25% from the left border
        viewport_left: int = (
            max(viewport.column - viewport.columns_per_line // 4, 0)
            if viewport.column is not None
            else 0
        )

        if lines:
            # How many chars do we need to write the line number
            loc_width: int = len(str(lines[-1][0]))
            modify_lines(lines, viewport, viewport_left, loc_width)
            if viewport.line_context == -1:
                offset = 0
            elif viewport_center - viewport.line_context <= 0:
                offset = 0
                lines = lines[
                    slice(
                        0,
                        2 * viewport.line_context + 1,
                    )
                ]
            else:
                offset = (
                    max(viewport_center - viewport.line_context, 0)
                    if (viewport_center + viewport.line_context < len(lines))
                    else max(len(lines) - 2 * viewport.line_context - 1, 0)
                )
                lines = lines[
                    slice(
                        max(viewport_center - viewport.line_context, 0),
                        viewport_center + viewport.line_context + 1,
                    )
                    if (viewport_center + viewport.line_context < len(lines))
                    else slice(
                        max(len(lines) - 2 * viewport.line_context - 1, 0),
                        len(lines),
                    )
                ]

            # Highlight the column if requested

            if _must_highlight_line_number(viewport):
                lines.append((0, f"  {' ':>{loc_width}} ^ Col {viewport_left}"))

    if viewport:
        return Snippet(
            content="\n".join(map(itemgetter(1), lines)),
            offset=offset,
            line=viewport.line,
            column=viewport.column,
            columns_per_line=viewport.columns_per_line,
            line_context=viewport.line_context,
            highlight_line_number=viewport.highlight_line_number,
            show_line_numbers=viewport.show_line_numbers,
            wrap=viewport.wrap,
            start_point=None,
        )

    return Snippet(
        content="\n".join(map(itemgetter(1), enumerate(lines_raw))),
        offset=offset,
    )


def modify_lines(
    lines: list[tuple[int, str]],
    viewport: SnippetViewport,
    viewport_left: int,
    loc_width: int,
) -> None:
    if not lines:
        return

    line_no_last: int | None = lines[-2][0] if len(lines) >= 2 else None

    for index, (line_no, line) in enumerate(lines):
        mark_symbol = _get_mark_symbol(line_no, line_no_last, viewport._replace())
        line_no_str = "" if line_no == line_no_last else str(line_no)
        line_no_last = line_no

        # Apply horizontal viewport slicing
        n_line = line[viewport_left : viewport_left + viewport.columns_per_line + 1]
        line_prefix = f"{mark_symbol} {line_no_str:>{loc_width}} | "

        lines[index] = (
            line_no,
            _format_line(n_line, line_prefix, viewport, lines[index][1]),
        )


def _format_line(
    line: str,
    line_prefix: str,
    viewport: SnippetViewport,
    original_line: str,
) -> str:
    if not viewport.show_line_numbers:
        if original_line.startswith(line_prefix.rstrip()):
            line = line.replace(line_prefix, "").replace(line_prefix.rstrip(), "")
        return line

    if not line.startswith(line_prefix) and viewport.highlight_line_number:
        return f"{line_prefix}{line}".rstrip(" ")

    if original_line.startswith(line_prefix[0]):
        line = line.replace(line_prefix, "")
    return line


def _get_mark_symbol(
    line_no: int,
    line_no_last: int | None,
    viewport: SnippetViewport,
) -> str:
    if line_no == viewport.line and line_no != line_no_last:
        return ">"
    return " "


def _must_highlight_line_number(viewport: SnippetViewport) -> bool:
    return bool(
        viewport.column is not None
        and viewport.highlight_line_number
        and viewport.show_line_numbers,
    )


def _get_lines(
    lines_raw: list[str],
    viewport: SnippetViewport,
    offset: int | None = None,
) -> list[tuple[int, str]]:
    offset = offset or 0
    if viewport is not None and viewport.wrap:
        return [
            (line_no + offset, "".join(line_chunk))
            for line_no, line in enumerate(lines_raw, start=1)
            for line_chunk in _chunked(line, viewport.columns_per_line)
        ]

    return [(line_no + offset, line) for line_no, line in enumerate(lines_raw, start=1)]


def _chunked(line: str, chunk_size: int) -> Iterator[str]:
    if line:
        yield from chunked(list(line), n=chunk_size)  # type: ignore  # noqa: PGH003
    else:
        yield ""


def find_function_name(func_nodes: list[Node], language: str) -> tuple[Node, str] | None:
    for node in func_nodes:
        if (field_name := TREE_SITTER_FUNCTION_IDENTIFIER.get(language, {}).get(node.type)) and (
            (children := node.child_by_field_name(field_name))
            or (children := next((x for x in node.children if x.type == field_name), None))
        ):
            return children, node.type
    return None


def extract_snippet_function_from_nodes(
    file_bytes: bytes,
    func_nodes: list[Node],
    desired_line: int,
    *,
    language: str,
) -> Snippet | None:
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language

    try:
        result = file_bytes[func_nodes[0].start_byte : func_nodes[-1].end_byte].decode(
            encoding="utf-8",
        )
        identifier_ = find_function_name(func_nodes, language)
        function_: Function | None = None
        if identifier_:
            identifier_node, node_type = identifier_
            if identifier_node.text:
                function_ = Function(
                    name=identifier_node.text.decode("utf-8"),
                    node_type=node_type,
                    field_identifier_name=identifier_node.type,
                )

        offset = func_nodes[0].start_point[0]
        return Snippet(
            content=result,
            offset=offset,
            line=desired_line,
            show_line_numbers=False,
            start_point=(func_nodes[0].start_point[0], func_nodes[0].start_point[1]),
            end_point=(func_nodes[-1].end_point[0], func_nodes[-1].end_point[1]),
            highlight_line_number=False,
            line_context=(desired_line - offset) - 1,
            is_function=True,
            function=function_,
        )
    except IndexError:
        return None


def extract_function(
    file_content: str,
    desired_line: int,
    *,
    language: str,
) -> Snippet | None:
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language

    if language not in TREE_SITTER_FUNCTION_DECLARATION_MAP:
        raise InvalidFileType
    file_bytes = file_content.encode("utf-8")
    func_nodes = extract_function_nodes(file_bytes, desired_line, language=language)

    return extract_snippet_function_from_nodes(
        file_bytes,
        func_nodes,
        desired_line,
        language=language,
    )


def make_snippet_function(
    *,
    file_content: str,
    viewport: SnippetViewport,
    file_path: str | None = None,
    language: str | None = None,
) -> Snippet | None:
    if not language and file_path:
        language = get_language_from_path(file_path)
    if not language:
        return None

    vulnerability_snippet: Snippet | None = None
    with suppress(InvalidFileType, OSError, UnicodeEncodeError):
        vulnerability_snippet = extract_function(
            file_content,
            desired_line=viewport.line,
            language=language,
        )
        if vulnerability_snippet:
            vulnerability_snippet = vulnerability_snippet.reshape(
                viewport=viewport._replace(
                    line_context=-1,
                ),
            )
        if not vulnerability_snippet:
            return None

    return vulnerability_snippet


def make_hierarchical_snippets(
    source_code: str,
    language: str,
    vulnerability_line: int,
) -> list[Snippet]:
    """Generate hierarchical code snippets for source code context.

    It function is util for declarative languages like html, xml, json, etc.

    Returns:
        List of Snippet objects ordered by context specificity
        from most specific to most general

    """
    nodes = extract_hierarchical_nodes(
        source_code=source_code.encode("utf-8"),
        language=language,
        desired_line=vulnerability_line,
    )
    snippets = []
    for node in nodes:
        content = get_node_content(source_code=source_code.encode("utf-8"), node=node)

        offset = node.start_point[0] + 1  # Start of the node content

        snippet = Snippet(
            content=content,
            offset=offset,
            line=vulnerability_line,
            show_line_numbers=False,
            start_point=(node.start_point[0], node.start_point[1]),
            end_point=(node.end_point[0], node.end_point[1]),
            highlight_line_number=False,
            line_context=(vulnerability_line - offset) - 1,
            is_function=False,
            function=None,
        )
        snippets.append(snippet)
    return snippets
