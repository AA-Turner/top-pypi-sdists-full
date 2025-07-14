# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Utility code for rendering.
"""

from __future__ import annotations

import io
import os
import typing as t
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from docutils import nodes
from docutils.core import Publisher, publish_parts
from docutils.io import StringInput
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.roles import register_local_role
from docutils.utils import Reporter as DocutilsReporter
from docutils.utils import SystemMessage

if t.TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner  # pragma: no cover

    RSTRole = t.Callable[  # pragma: no cover
        [str, str, str, int, Inliner, Mapping[str, t.Any], Sequence[str]],
        tuple[Sequence[nodes.Node], Sequence[SystemMessage]],
    ]

SupportedParser = t.Union[t.Literal["restructuredtext"], t.Literal["markdown"]]


_DOCUTILS_PUBLISH_SETTINGS = {
    "input_encoding": "unicode",
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "_disable_config": True,
    "report_level": DocutilsReporter.ERROR_LEVEL,
}


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


def get_document_structure(
    source: str, /, parser_name: SupportedParser
) -> RenderResult:
    """
    Render the document as its internal docutils structure.
    """
    warnings_stream = io.StringIO()
    parts = publish_parts(
        source=source,
        parser_name=parser_name,
        settings_overrides=get_docutils_publish_settings(
            warnings_stream=warnings_stream
        ),
    )
    whole = parts["whole"]
    return RenderResult(
        whole.decode("utf-8") if isinstance(whole, bytes) else whole,
        set(),
        warnings_stream.getvalue().splitlines(),
    )


def ensure_newline_after_last_content(lines: list[str]) -> None:
    """
    Ensure that if ``lines`` is not empty, the last entry is ``""``.
    """
    if lines and lines[-1] != "":
        lines.append("")


def parse_document(  # pylint: disable=too-many-arguments
    content: str,
    *,
    parser_name: SupportedParser,
    path: str | os.PathLike[str] | None = None,
    root_prefix: str | os.PathLike[str] | None = None,
    rst_directives: Mapping[str, t.Type[Directive]] | None = None,
    rst_local_roles: Mapping[str, RSTRole] | None = None,
) -> nodes.document:
    """
    Parse an already loaded document with the given parser.
    """

    if rst_directives:
        # pylint: disable-next=fixme
        # TODO: figure out how to register a directive only temporarily
        for directive_name, directive_class in rst_directives.items():
            register_directive(directive_name, directive_class)

    if rst_local_roles:
        # pylint: disable-next=fixme
        # TODO: figure out how to register a local role only temporarily
        for role_name, role in rst_local_roles.items():
            # The docutils types for register_local_role seem to be broken:
            # the return value expects two sequences of nodes.reference,
            # which is definitely wrong.
            register_local_role(role_name, role)  # type: ignore

    # We create a Publisher only to have a mechanism which gives us the settings object.
    # Doing this more explicit is a bad idea since the classes used are deprecated and will
    # eventually get replaced. Publisher.get_settings() looks like a stable enough API that
    # we can 'just use'.
    publisher = Publisher(source_class=StringInput)
    reader_name = "standalone"
    writer_name = "pseudoxml"  # doesn't matter, since we just need the parsed document
    publisher.set_components(reader_name, parser_name, writer_name)
    override = get_docutils_publish_settings(warnings_stream=io.StringIO())
    override.update(
        {
            "root_prefix": str(root_prefix),
        }
    )
    publisher.process_programmatic_settings(None, override, None)
    publisher.set_source(content, str(path))

    # Parse the document
    try:
        # mypy gives errors for the next line, but this is literally what docutils itself
        # is also doing. So we're going to ignore this error...
        return publisher.reader.read(
            publisher.source,
            publisher.parser,
            publisher.settings,  # type: ignore
        )
    except SystemMessage as exc:
        raise ValueError(f"Cannot parse document: {exc}") from exc
    except Exception as exc:  # pragma: no cover
        raise ValueError(
            f"Unexpected error while parsing document: {exc}"
        ) from exc  # pragma: no cover


__all__ = (
    "SupportedParser",
    "RenderResult",
    "get_docutils_publish_settings",
    "get_document_structure",
    "ensure_newline_after_last_content",
    "parse_document",
)
