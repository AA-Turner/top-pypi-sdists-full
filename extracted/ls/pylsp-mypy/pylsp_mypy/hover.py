# -*- coding: utf-8 -*-
"""
File to house the   class.

Created on Wed Jul 15 20:27:14 2026

@author: Richard Kellnberger
"""

import itertools
from typing import Any

from jedi.api.classes import Name
from pylsp import _utils
from pylsp.config.config import Config
from pylsp.plugins.hover import pylsp_hover
from pylsp.workspace import Document

from pylsp_mypy.backend import Backend, DmypyAPIBackend, DmypyCommandBackend
from pylsp_mypy.util import get_cmd

# Start from https://github.com/python-lsp/python-lsp-server/pull/452


def _find_docstring(definitions: list[Name]) -> str:
    if len(definitions) != 1:
        # Either no definitions or multiple definitions
        # If we have multiple definitions the element can be multiple things and we
        # do not know which one

        # TODO(Review)
        # We could also concatenate all docstrings we find in the definitions
        # I am against this because
        # - If just one definition has a docstring, it gives a false impression of the hover element
        # - If multiple definitions have a docstring, the user will probably not realize
        #   that he can scroll to see the other options
        return ""

    # The single true definition
    definition = definitions[0]
    docstring: str = definition.docstring(
        raw=True
    )  # raw docstring returns only doc, without signature
    if docstring != "":
        return docstring

    # If the definition has no docstring, try to infer the type
    types = definition.infer()

    if len(types) != 1:
        # If we have multiple types the element can be multiple things and we
        # do not know which one
        return ""

    # Use the docstring of the single true type (possibly empty)
    docstring = types[0].docstring(raw=True)
    return docstring


def _find_signatures_and_types(definitions: list[Name]) -> list[str]:
    def _line_number(definition: Name) -> int:
        """Helper for sorting definitions by line number (which might be None)."""
        return definition.line if definition.line is not None else 0

    def _get_signatures(definition: Name) -> list[str]:
        """Get the signatures of functions and classes."""
        return [
            signature.to_string()
            for signature in definition.get_signatures()
            if signature.type in ["class", "function"]
        ]

    definitions = sorted(definitions, key=_line_number)
    signatures_per_def = [_get_signatures(d) for d in definitions]
    types_per_def = [d.infer() for d in definitions]

    # a flat list with all signatures
    signatures = list(itertools.chain(*signatures_per_def))

    # We want to show the type if there is at least one type that does not
    # correspond to a signature
    if any(len(s) == 0 and len(t) > 0 for s, t in zip(signatures_per_def, types_per_def)):
        # Get all types (also the ones that correspond to a signature)
        types = set(itertools.chain(*types_per_def))
        type_names = [t.name for t in sorted(types, key=_line_number)]

        if len(type_names) == 1:
            return [*signatures, type_names[0]]
        elif len(type_names) > 1:
            return [*signatures, f"Union[{', '.join(type_names)}]"]
        return []

    else:
        # The type does not add any information because it is already in the signatures
        return signatures


# @hookimpl
def pylsp_hover_(config: Config, document: Document, position: dict[str, int]) -> dict[str, Any]:
    code_position = _utils.position_to_jedi_linecolumn(document, position)
    definitions = document.jedi_script(use_document_path=True).help(**code_position)

    hover_capabilities = config.capabilities.get("textDocument", {}).get("hover", {})
    supported_markup_kinds = hover_capabilities.get("contentFormat", ["markdown"])
    preferred_markup_kind = _utils.choose_markup_kind(supported_markup_kinds)

    return {
        "contents": _utils.format_docstring(
            _find_docstring(definitions),
            preferred_markup_kind,
            signatures=_find_signatures_and_types(definitions),
        )
    }


# End from https://github.com/python-lsp/python-lsp-server/pull/452


def hover(config: Config, document: Document, position: dict[str, int]) -> dict[str, str]:
    settings = config.plugin_settings("pylsp_mypy")
    hover = settings.get("hover", False)
    if not hover:
        result: dict[str, str] = pylsp_hover(config, document, position)  # current pylsp
        return result

    result = pylsp_hover_(config, document, position)  # pylsp PR 452

    dmypy = settings.get("dmypy", False)

    if dmypy:
        dmypy_status_file = settings.get("dmypy_status_file", ".dmypy.json")

        command = get_cmd(settings, "dmypy")

        args = [
            "--status-file",
            dmypy_status_file,
            "inspect",
            f"{document.path}:{position['line']+1}:{position['character']}",
            "--include-span",
        ]

        backend: Backend

        if command:
            # dmypy exists on PATH or was provided by settings
            # -> use this dmypy
            backend = DmypyCommandBackend()
        else:
            # dmypy does not exist on PATH and was not provided by settings,
            # but must exist in the env pylsp-mypy is installed in
            # -> use dmypy via api
            backend = DmypyAPIBackend()

        report, errors, exit_status = backend.hover(command, args)

        if exit_status != 0:  # TODO do not fail silently
            return result

        firstType = report.split("\n")[0]

        if "->" not in firstType:  # TODO do not fail silently
            return result

        mypyType = firstType.split("->")[1][2:-1]

        value = result["contents"]["value"]

        if "\n\n" in value:
            parts = value.split("\n\n")
            parts[0] += f"\n\nMypy type: {mypyType}"
            result["contents"]["value"] = "\n\n".join(parts)
        else:
            result["contents"]["value"] = f"Mypy type: {mypyType}\n\n" + value

    return result
