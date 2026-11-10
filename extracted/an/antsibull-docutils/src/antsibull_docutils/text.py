# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Code for conversion to (formatted) plain text.
"""

from __future__ import annotations

import math
import typing as t

from docutils import nodes, writers

from ._collector import ANSIState as _ANSIState
from ._collector import EmptyState as _EmptyState
from ._collector import Formatting as _Formatting
from ._collector import State as _State
from ._string import ASCIIStringProcessor as _ASCIIStringProcessor
from ._string import StringProcessor as _StringProcessor
from ._string import UnicodeStringProcessor as _UnicodeStringProcessor
from ._string import has_unicode_string_processor as _has_unicode_string_processor
from ._text_context import ConstEnumerator as _ConstEnumerator
from ._text_context import Context as _Context
from ._text_context import IndentContext as _IndentContext
from ._text_context import ListContext as _ListContext
from ._text_context import VariableEnumerator as _VariableEnumerator
from ._text_context import arabic as _arabic
from ._text_table import BaseTranslator as _BaseTranslator
from ._text_table import TableRenderer as _TableRenderer
from ._utils import DocumentContextBase as _DocumentContextBase
from ._utils import add_skip as _add_skip
from ._utils import add_unsupported_classes as _add_unsupported_classes
from ._utils import render as _render
from .utils import RenderResult, SupportedParser

_Class = t.TypeVar("_Class")


UseAnsiFormattingType = t.Literal["always", "never"]
UseUnicodeSplittingType = t.Literal["always", "never", "auto"]


class GlobalContext:  # pylint: disable=too-few-public-methods
    """
    The global conversion context.
    """

    title_headings: str = """═━─┉┅┈┄-~.+`'"_"""
    column_width: int = 80
    use_ansi_formatting: UseAnsiFormattingType = "always"
    use_unicode_splitting: UseUnicodeSplittingType = "auto"


def _get_formatting_state(global_context: GlobalContext) -> _State:
    """
    Get formatting state for the given global context.
    """
    return (
        _ANSIState()
        if global_context.use_ansi_formatting == "always"
        else _EmptyState()
    )


def _get_string_proc(global_context: GlobalContext) -> _StringProcessor:
    """
    Get string processor for the given global context.
    """
    if (
        global_context.use_unicode_splitting == "auto"
        and _has_unicode_string_processor()
    ):
        return _UnicodeStringProcessor()
    if global_context.use_unicode_splitting == "always":
        return _UnicodeStringProcessor()
    return _ASCIIStringProcessor()


class _DocumentContext(_DocumentContextBase[GlobalContext, _Context]):
    """
    Conversion context for a document.
    """

    def __init__(
        self, *, global_context: GlobalContext, string_proc: _StringProcessor
    ) -> None:
        super().__init__(global_context)
        self._contexts.append(
            _Context(
                has_top=True,
                remaining_width=global_context.column_width,
                state=_get_formatting_state(global_context),
                string_proc=string_proc,
            )
        )


def _get_generic_visit(
    value: _Formatting | tuple[str, str] | None,
) -> t.Callable[[t.Any, nodes.Node], None]:
    # pylint: disable-next=unused-argument
    def visit(self: t.Any, node: nodes.Node) -> None:
        # pylint: disable=protected-access
        if isinstance(value, tuple):
            self._context.top.main.append(text=value[0])
        elif value is not None:
            self._context.top.state.push_formatting(value)
            self._context.top.main.update_state()

    return visit


def _get_generic_depart(
    value: _Formatting | tuple[str, str] | None,
) -> t.Callable[[t.Any, nodes.Node], None]:
    # pylint: disable-next=unused-argument
    def depart(self: t.Any, node: nodes.Node) -> None:
        # pylint: disable=protected-access
        if isinstance(value, tuple):
            self._context.top.main.append(text=value[1])
        elif value is not None:
            self._context.top.state.pop_formatting(value)
            self._context.top.main.update_state()

    return depart


def _add_simple(
    definitions: dict[str, _Formatting | tuple[str, str] | None],
) -> t.Callable[[_Class], _Class]:
    def decorator(clazz: _Class) -> _Class:
        for class_name, value in definitions.items():
            setattr(clazz, f"visit_{class_name}", _get_generic_visit(value))
            setattr(clazz, f"depart_{class_name}", _get_generic_depart(value))
        return clazz

    return decorator


def _add_admonitions(
    definitions: dict[str, str],
) -> t.Callable[[_Class], _Class]:
    def decorator(clazz: _Class) -> _Class:
        def get_visit(first_indent: str):
            # pylint: disable-next=unused-argument
            def visit(self: t.Any, node: nodes.Node) -> None:
                # pylint: disable=protected-access
                self._context.top.main.new_par()
                self._context.push_context(
                    _IndentContext(
                        remaining_width=self._context.top.remaining_width,
                        state=self._context.top.state,
                        string_proc=self._context.top.string_proc,
                        first_indent=first_indent,
                        at_least_one_line=True,
                    )
                )

            return visit

        def get_depart():
            # pylint: disable-next=unused-argument
            def depart(self: t.Any, node: nodes.Node) -> None:
                # pylint: disable=protected-access
                self._context.pop_context()

            return depart

        for class_name, first_indent in definitions.items():
            setattr(clazz, f"visit_{class_name}", get_visit(first_indent))
            setattr(clazz, f"depart_{class_name}", get_depart())
        return clazz

    return decorator


# pylint: disable=duplicate-code
@_add_unsupported_classes
@_add_simple(
    {
        "document": None,
        "inline": None,
        "generated": None,
        "entry": None,
        "literal": ("`", "`"),
        "emphasis": _Formatting.ITALICS,
        "strong": _Formatting.BOLD,
        "subscript": ("<sub>", "</sub>"),
        "superscript": ("<sup>", "</sup>"),
    }
)
@_add_admonitions(
    {
        "attention": "⚠️ ",
        "caution": "⚠️ ",
        "danger": "⚠️ ",
        "error": "❌ ",
        "important": "!\u20dd ",
        "note": "!\u20dd ",
        "tip": "ℹ️ ",
        "hint": "ℹ️ ",
        "warning": "⚠️ ",
    }
)
@_add_skip(
    [
        "comment",
    ]
)
class _Translator(
    _BaseTranslator[_DocumentContext]
):  # pylint: disable=too-many-public-methods
    """
    Translates a docutils node tree to text in a ``_DocumentContext``.
    """

    def get_text(self) -> str:
        """
        Return the result as a text.

        Must only be called after processing the document, and at most once.
        """
        context = self._context.top
        context.close()
        return context.get_text().lstrip("\n").rstrip("\n")

    # Node: paragraph

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_paragraph(self, node: nodes.paragraph) -> None:
        self._context.top.main.new_par()

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_paragraph(self, node: nodes.paragraph) -> None:
        self._context.top.main.new_par()

    # Node: title

    # pylint: disable-next=missing-function-docstring
    def visit_title(self, node: nodes.title) -> None:
        level = self._context.section_depth + 1
        title = node.astext()
        sep = self._context.global_context.title_headings[level - 1]
        underline = sep * math.ceil(
            self._context.top.string_proc.get_column_count(text=title)
            / self._context.top.string_proc.get_column_count(text=sep)
        )
        if self._context.section_depth == 0:
            self._context.top.top_state.push_formatting(_Formatting.BOLD)
            self._context.top.top.update_state()
            self._context.top.top.append(text=title)
            self._context.top.top.new_line()
            self._context.top.top.append(text=underline)
            self._context.top.top_state.push_formatting(_Formatting.BOLD)
            self._context.top.top.update_state()
            self._context.top.top.new_line()
            # Make sure there is an empty line
            self._context.top.top.new_line(force=True)
        else:
            self._context.top.main.new_par()
            self._context.top.state.push_formatting(_Formatting.BOLD)
            self._context.top.main.update_state()
            self._context.top.main.append(text=title)
            self._context.top.main.new_line()
            self._context.top.main.append(text=underline)
            self._context.top.state.pop_formatting(_Formatting.BOLD)
            self._context.top.main.update_state()
            self._context.top.main.new_par()
        raise nodes.SkipNode

    # Node: section

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_section(self, node: nodes.section) -> None:
        self._context.top.main.new_par()
        self._context.section_depth += 1

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_section(self, node: nodes.section) -> None:
        self._context.section_depth -= 1

    # Node: text

    # pylint: disable-next=missing-function-docstring,invalid-name
    def visit_Text(self, node: nodes.Text) -> None:
        text = node.astext()
        self._context.top.main.append(text=text)

    # pylint: disable-next=missing-function-docstring,invalid-name
    def depart_Text(self, node: nodes.Text) -> None:
        pass

    # Node: target

    # pylint: disable-next=missing-function-docstring
    def visit_target(self, node: nodes.target) -> None:
        pass

    # pylint: disable-next=missing-function-docstring
    def depart_target(self, node: nodes.target) -> None:
        pass

    # Node: reference

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_reference(self, node: nodes.reference) -> None:
        self._context.top.state.push_formatting(_Formatting.UNDERLINE)
        self._context.top.main.update_state()

    # pylint: disable-next=missing-function-docstring
    def depart_reference(self, node: nodes.reference) -> None:
        self._context.top.state.pop_formatting(_Formatting.UNDERLINE)
        self._context.top.main.update_state()
        if "refuri" in node.attributes:
            url: str = node.attributes["refuri"]
        elif "refid" in node.attributes:
            return
        else:
            # docutils fails an assertion at this point
            raise ValueError(  # pragma: no cover
                f"Do not know how to handle reference with attributes {node.attributes!r}"
            )
        if node.astext() == url:
            return
        self._context.top.main.append(text=" (")
        self._context.top.state.push_formatting(_Formatting.UNDERLINE)
        self._context.top.main.update_state()
        self._context.top.main.append(text=url)
        self._context.top.state.pop_formatting(_Formatting.UNDERLINE)
        self._context.top.main.update_state()
        self._context.top.main.append(text=")")

    # Node: bullet_list

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        self._context.top.main.new_par()
        self._context.push_context(
            _ListContext(
                enumerator=_ConstEnumerator(
                    prefix="- ", string_proc=self._context.top.string_proc
                ),
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        self._context.pop_context()

    # Node: enumerated_list

    # pylint: disable-next=missing-function-docstring
    def visit_enumerated_list(self, node: nodes.enumerated_list) -> None:
        self._context.top.main.new_par()
        self._context.push_context(
            _ListContext(
                enumerator=_VariableEnumerator(
                    generator=_arabic,
                    count=len(node),
                    string_proc=self._context.top.string_proc,
                ),
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_enumerated_list(self, node: nodes.enumerated_list) -> None:
        self._context.pop_context()

    # Node: list_item

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_list_item(self, node: nodes.list_item) -> None:
        list_context = t.cast(_ListContext, self._context.top)
        first_indent, next_indent = list_context.get_next_item_indents()
        self._context.push_context(
            _IndentContext(
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
                first_indent=first_indent,
                next_indent=next_indent,
                at_least_one_line=True,
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_list_item(self, node: nodes.list_item) -> None:
        self._context.pop_context()

    # Node: literal_block

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_literal_block(self, node: nodes.literal_block) -> None:
        self._context.top.main.new_par()
        self._context.push_context(
            _IndentContext(
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
                ignore_newlines=False,
                first_indent="  ",
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_literal_block(self, node: nodes.literal_block) -> None:
        self._context.pop_context()

    # Node: block_quote

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_block_quote(self, node: nodes.block_quote) -> None:
        self._context.push_context(
            _IndentContext(
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
                first_indent="  ",
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_block_quote(self, node: nodes.block_quote) -> None:
        self._context.pop_context()

    # Node: system_message

    # pylint: disable-next=missing-function-docstring
    def visit_system_message(self, node: nodes.system_message) -> None:
        message_type = node["type"]
        message_level = node["level"]
        source = node["source"]
        if node.hasattr("line"):
            source = f'{source}, line {node["line"]}'
        self._context.top.main.new_par()
        self._context.top.state.push_formatting(_Formatting.BOLD)
        self._context.top.main.update_state()
        self._context.top.main.append(
            text=f"⚠️ {message_type}/{message_level} ⚠️ ({source})"
        )
        self._context.top.state.pop_formatting(_Formatting.BOLD)
        self._context.top.main.update_state()
        self._context.top.main.new_par()
        self._context.push_context(
            _IndentContext(
                first_indent="  ",
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_system_message(self, node: nodes.system_message) -> None:
        self._context.pop_context()
        self._context.top.main.new_par()

    # Node: topic

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_topic(self, node: nodes.topic) -> None:
        # The main use of <topic> elements is for Table of Contents
        class _TopicContext(_Context):
            """
            Context for a topic.
            """

        self._context.section_depth += 1
        self._context.push_context(
            _TopicContext(
                remaining_width=self._context.top.remaining_width,
                state=self._context.top.state,
                string_proc=self._context.top.string_proc,
            )
        )

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_topic(self, node: nodes.topic) -> None:
        self._context.pop_context()
        self._context.section_depth -= 1

    # Node: image

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_image(self, node: nodes.image) -> None:
        self._context.top.main.new_par()
        raise nodes.SkipNode

    # Node: transition

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_transition(self, node: nodes.transition) -> None:
        self._context.top.main.new_par()
        elt = "─"
        self._context.top.main.append(
            text=elt
            * (
                self._context.top.remaining_width
                // self._context.top.string_proc.get_column_count(text=elt)
            )
        )
        self._context.top.main.new_par()
        raise nodes.SkipNode

    # Node: title_reference

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_title_reference(self, node: nodes.title_reference) -> None:
        # This usually happens if someone uses single backticks instead of double backticks
        self._context.top.state.push_formatting(_Formatting.ITALICS)
        self._context.top.main.update_state()

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_title_reference(self, node: nodes.title_reference) -> None:
        self._context.top.state.pop_formatting(_Formatting.ITALICS)
        self._context.top.main.update_state()

    # Node: problematic

    # pylint: disable-next=missing-function-docstring,unused-argument
    def visit_problematic(self, node: nodes.problematic) -> None:
        self._context.top.main.append(text="⚠️ ")

    # pylint: disable-next=missing-function-docstring,unused-argument
    def depart_problematic(self, node: nodes.problematic) -> None:
        self._context.top.main.append(text=" ⚠️")

    # Node: problematic

    # pylint: disable-next=missing-function-docstring
    def visit_table(self, node: nodes.table) -> None:
        renderer = _TableRenderer(
            table=node, destination=self._context.top, visitor=self
        )
        renderer.render()
        raise nodes.SkipNode


class _TextWriter(writers.Writer):
    """
    Create a text document from a docutils node tree.
    """

    def __init__(self, document_context: _DocumentContext):
        writers.Writer.__init__(self)
        self.document_context = document_context
        self.translator_class = _Translator

    def translate(self) -> None:
        """
        Translate the document node tree to text.
        """
        translator = self.translator_class(self.document, self.document_context)
        if self.document:
            self.document.walkabout(translator)
        self.output = translator.get_text()


def get_column_count(text: str, *, global_context: GlobalContext) -> int:
    """
    Compute the column count of a text without newlines.
    """
    string_proc = _get_string_proc(global_context)
    return string_proc.get_column_count(text=text)


def render_bold(line: str, *, global_context: GlobalContext) -> str:
    """
    Render a line in bold.
    """
    # Get formatting prefix/suffix
    state = _get_formatting_state(global_context)
    state.push_formatting(_Formatting.BOLD)
    s = state.get_state()
    prefix = state.get_start_of_line(s)
    suffix = state.get_end_of_line(s)

    # Compose result
    return f"{prefix}{line}{suffix}"


def render_title(title: str, *, level: int, global_context: GlobalContext) -> list[str]:
    """
    Render a title.

    ``level`` must be 1 or larger.
    """
    assert level >= 1

    # Get formatting prefix/suffix
    state = _get_formatting_state(global_context)
    state.push_formatting(_Formatting.BOLD)
    s = state.get_state()
    prefix = state.get_start_of_line(s)
    suffix = state.get_end_of_line(s)

    # Compute underline
    string_proc = _get_string_proc(global_context)
    sep = global_context.title_headings[level - 1]
    underline = sep * math.ceil(
        string_proc.get_column_count(text=title)
        / string_proc.get_column_count(text=sep)
    )

    # Compose result
    return [
        f"{prefix}{title}{suffix}",
        f"{prefix}{underline}{suffix}",
    ]


def render_as_text(
    source: str,
    /,
    parser_name: SupportedParser,
    global_context: GlobalContext | None = None,
    source_path: str | None = None,
    destination_path: str | None = None,
) -> RenderResult:
    """
    Render the document as text.

    :arg source: The document.
    :kwarg parser_name: The parser to use for ``source``.
    :kwarg global_context: An optional ``GlobalContext`` object.
    :kwarg source_path: An optional path for ``source``, to be used in error
        messages.
    :kwarg destination_path: An optional path for where the destination will
        be stored, to be used in error messages.
    :return: A ``RenderResult`` object containing the output and further
        information.
    """
    if global_context is None:
        global_context = GlobalContext()
    document_context = _DocumentContext(
        global_context=global_context, string_proc=_get_string_proc(global_context)
    )
    return _render(
        source,
        writer=_TextWriter(document_context),
        get_unknown_node_types=lambda: document_context.unknown_node_types,
        parser_name=parser_name,
        source_path=source_path,
        destination_path=destination_path,
    )


__all__ = (
    "GlobalContext",
    "UseAnsiFormattingType",
    "UseUnicodeSplittingType",
    "get_column_count",
    "render_as_text",
    "render_bold",
    "render_title",
)
