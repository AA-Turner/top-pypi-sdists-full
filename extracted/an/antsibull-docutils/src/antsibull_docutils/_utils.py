# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Utilities.
"""

from __future__ import annotations

import abc
import contextlib
import io
import typing as t
from dataclasses import dataclass

# docutils.__version_info__ exists since docutils 0.14, released in August 2017.
# Python 3.7 wasn't even out then. I think we can safely ignore versions before that.
from docutils import __version_info__, nodes, writers
from docutils.core import publish_parts
from docutils.utils import Reporter as DocutilsReporter

_Class = t.TypeVar("_Class")
_GlobalContext = t.TypeVar("_GlobalContext")

_PARSER_NAME_ARG = "parser" if __version_info__ >= (0, 22) else "parser_name"

_DOCUTILS_PUBLISH_SETTINGS = {
    "input_encoding": "unicode",
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "_disable_config": True,
    "report_level": DocutilsReporter.ERROR_LEVEL,
}

SupportedParser = t.Union[t.Literal["restructuredtext"], t.Literal["markdown"]]


@dataclass
class RenderResult:
    """
    A rendering result.
    """

    # The output of the renderer.
    output: str

    # The set of class names found that weren't supported by this renderer.
    unsupported_class_names: set[str]

    # List of warnings emitted
    warnings: list[str]


def get_docutils_publish_settings(
    *,
    warnings_stream: io.IOBase | None = None,
) -> dict[str, t.Any]:
    """
    Provide docutils publish settings.
    """
    settings = _DOCUTILS_PUBLISH_SETTINGS.copy()
    settings["warning_stream"] = warnings_stream or False
    return settings


def add_unsupported_classes(clazz: _Class) -> _Class:
    """
    Add unknown classes encountered in the node visitor to the ``unknown_node_types``
    set of the visitor's context.
    """

    def get_visit(class_name: str):
        # pylint: disable-next=unused-argument
        def visit_unsupported(self: t.Any, node: nodes.Node):
            # pylint: disable-next=protected-access
            self._context.unknown_node_types.add(class_name)
            raise nodes.SkipNode

        return visit_unsupported

    for class_name in nodes.node_class_names:
        function_name = f"visit_{class_name}"
        if not hasattr(clazz, function_name):
            setattr(clazz, function_name, get_visit(class_name))

    return clazz


def add_skip(class_names: list[str]) -> t.Callable[[_Class], _Class]:
    """
    Skip class names in the node visitor.
    """

    def decorator(clazz: _Class) -> _Class:
        def visit(self: t.Any, node: nodes.Node) -> None:
            raise nodes.SkipNode

        for class_name in class_names:
            setattr(clazz, f"visit_{class_name}", visit)
        return clazz

    return decorator


_ContextBase = t.TypeVar("_ContextBase")


class ContextBase(t.Generic[_ContextBase], metaclass=abc.ABCMeta):
    """
    Base context class for MarkDown conversion.
    """

    @abc.abstractmethod
    def append(
        self,
        context: _ContextBase,
    ) -> None:
        """
        Append another context to this context.
        """

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the context.

        Should be called before using its value / content, for example by
        passing it to ``append()`` or calling ``get_text()``.
        """


_Context = t.TypeVar("_Context", bound=ContextBase)


class DocumentContextBase(t.Generic[_GlobalContext, _Context]):
    """
    Conversion context for a document.
    """

    section_depth: int
    global_context: _GlobalContext
    unknown_node_types: set[str]
    created_labels: set[str]

    _contexts: list[_Context]

    def __init__(self, global_context: _GlobalContext) -> None:
        self.section_depth = 0
        self.global_context = global_context
        self.unknown_node_types = set()
        self.created_labels = set()
        self._contexts = []

    def push_context(self, context: _Context) -> None:
        """
        Add a new context on the context stack.
        """
        self._contexts.append(context)

    def pop_context(self) -> None:
        """
        Pop the top-most context from the context stack.

        The last context cannot be popped, trying to do so will result in a
        ``ValueError`` exception.
        """
        if len(self._contexts) < 2:
            raise ValueError("Cannot pop last element")
        context = self._contexts.pop()
        context.close()
        self._contexts[-1].append(context)

    @property
    def top(self) -> _Context:
        """
        Return the top-most context from the context stack.
        """
        return self._contexts[-1]

    @contextlib.contextmanager
    def with_fake_top(self, *, fake_top: _Context) -> t.Generator[None]:
        """
        Temporarily replace the document context's top with a "fake top" context.
        """
        self._contexts.append(fake_top)
        new_length = len(self._contexts)
        try:
            yield
        finally:
            if len(self._contexts) != new_length:
                raise RuntimeError(  # pragma: no cover
                    f"Internal error: context stack has wrong length {len(self._contexts)},"
                    f" expected {new_length}!"
                )
            self._contexts.pop()


def render(  # pylint: disable=too-many-positional-arguments
    source: str,
    /,
    parser_name: SupportedParser,
    writer: writers.Writer | None,
    get_unknown_node_types: t.Callable[[], set[str]],
    source_path: str | None,
    destination_path: str | None,
) -> RenderResult:
    """
    Render ``source`` with the given writer.
    """
    warnings_stream = io.StringIO()
    opts: dict[str, t.Any] = {
        _PARSER_NAME_ARG: parser_name,
    }
    parts = publish_parts(
        source=source,
        source_path=source_path,
        destination_path=destination_path,
        writer=writer,
        settings_overrides=get_docutils_publish_settings(
            warnings_stream=warnings_stream
        ),
        **opts,
    )
    whole = parts["whole"]
    return RenderResult(
        whole.decode("utf-8") if isinstance(whole, bytes) else whole,
        get_unknown_node_types(),
        warnings_stream.getvalue().splitlines(),
    )
