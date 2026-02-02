"""
Hover Provider for the CSSL Language Server.

Provides hover information (documentation) for CSSL code elements including:
- Built-in functions and types
- Keywords and modifiers
- User-defined functions and classes
- Local variables
- Namespace members
"""

import logging
from typing import Optional
from lsprotocol.types import (
    Hover,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
)

from ..analysis.document_manager import DocumentAnalysis
from ..utils.cssl_registry import get_registry
from ..utils.symbol_table import SymbolKind, Symbol
from ..utils.position_utils import get_word_at_position

logger = logging.getLogger('cssl-lsp.hover')



class HoverProvider:
    """
    Provides hover information for CSSL code elements.

    Shows documentation on hover for:
    - Built-in functions
    - Keywords
    - Types
    - Modifiers
    - User-defined symbols
    """

    def __init__(self):
        pass

    def get_hover(
        self,
        document: DocumentAnalysis,
        position: Position
    ) -> Optional[Hover]:
        """
        Get hover information at the given position.

        Args:
            document: The analyzed document
            position: Cursor position

        Returns:
            Hover with documentation, or None if no hover available
        """
        try:
            if document is None:
                logger.warning("Hover called with None document")
                return None

            text = document.text
            if not text:
                logger.debug("Document has no text")
                return None

            line = position.line
            column = position.character

            logger.debug(f"Getting hover at line {line}, column {column}")

            # Get the word at position
            word_info = get_word_at_position(text, line, column)

            if not word_info:
                logger.debug(f"No word found at position {line}:{column}")
                return None

            word, start_col, end_col = word_info
            logger.debug(f"Found word: '{word}' at {start_col}-{end_col}")

            # Check for special prefixes
            if word.startswith('?'):
                return self._hover_pointer_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('@'):
                return self._hover_global_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('$'):
                return self._hover_shared_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('%'):
                return self._hover_snapshot_reference(document, word[1:], line, start_col, end_col)

            # Create range for the word
            word_range = Range(
                start=Position(line=line, character=start_col),
                end=Position(line=line, character=end_col)
            )

            registry = get_registry()

            # Check builtins first
            func_info = registry.get_function_info(word)
            if func_info:
                return self._format_builtin_hover(word, func_info, word_range)

            # Check keywords
            if word in registry.keywords:
                return self._format_keyword_hover(word, word_range)

            # Check types
            type_info = registry.get_type_info(word)
            if type_info:
                return self._format_type_hover(word, type_info, word_range)

            # Check modifiers
            if word in registry.modifiers:
                return self._format_modifier_hover(word, word_range)

            # Check GUI classes
            gui_info = registry.get_gui_class_info(word)
            if gui_info:
                return self._format_gui_class_hover(word, gui_info, word_range)

            # Check user-defined symbols
            if document.symbol_table:
                symbol = document.symbol_table.get_symbol(word)
                if symbol:
                    return self._format_symbol_hover(symbol, word_range)

            logger.debug(f"No hover info for '{word}'")
            return None

        except Exception as e:
            logger.error(f"Error in get_hover: {e}", exc_info=True)
            return None

    def _format_builtin_hover(self, name: str, info, range: Range) -> Hover:
        """Format hover for a builtin function."""
        sig = info.signature or f'{name}()'
        doc = info.doc or f'Built-in function: {name}'
        ret = info.return_type or 'dynamic'

        lines = [
            f"```cssl",
            f"{sig} -> {ret}",
            f"```",
            "",
            doc,
        ]

        if info.params:
            lines.append("")
            lines.append("**Parameters:**")
            for p in info.params:
                type_hint = f" ({p.type_hint})" if p.type_hint else ""
                lines.append(f"- `{p.name}`{type_hint}")

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value="\n".join(lines)
            ),
            range=range
        )

    def _format_keyword_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a keyword."""
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**{name}** (keyword)\n\nCSSL keyword: {name}"
            ),
            range=range
        )

    def _format_type_hover(self, name: str, info, range: Range) -> Hover:
        """Format hover for a type."""
        generic = info.generic_syntax
        display = f"{name}{generic}" if generic else name
        doc = info.doc or f'CSSL type: {display}'

        lines = [f"**{display}** (type)", "", doc]

        if info.methods:
            lines.append("")
            lines.append("**Methods:**")
            for m in info.methods[:15]:  # Limit to 15 to avoid huge hovers
                lines.append(f"- `{m.signature or m.name + '()'}`")
            if len(info.methods) > 15:
                lines.append(f"- ... and {len(info.methods) - 15} more")

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value="\n".join(lines)
            ),
            range=range
        )

    def _format_modifier_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a modifier."""
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**{name}** (modifier)\n\nFunction modifier: {name}"
            ),
            range=range
        )

    def _format_gui_class_hover(self, name: str, info, range: Range) -> Hover:
        """Format hover for a GUI widget class."""
        doc = info.doc or f'CSSL GUI widget: {name}'

        lines = [f"**{info.cssl_name or name}** (GUI widget)", "", doc]

        if info.methods:
            lines.append("")
            lines.append("**Methods:**")
            for m in info.methods[:15]:
                lines.append(f"- `{m.signature or m.name + '()'}`")
            if len(info.methods) > 15:
                lines.append(f"- ... and {len(info.methods) - 15} more")

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value="\n".join(lines)
            ),
            range=range
        )

    def _format_symbol_hover(self, symbol: Symbol, range: Range) -> Hover:
        """Format hover for a user-defined symbol."""
        kind_name = symbol.kind.name.lower()

        if symbol.kind == SymbolKind.FUNCTION:
            # Build function signature
            params = []
            for p in symbol.parameters or []:
                if p.type_info:
                    params.append(f"{p.type_info} {p.name}")
                else:
                    params.append(p.name)
            param_str = ", ".join(params)
            return_type = symbol.return_type or "void"

            modifiers = " ".join(symbol.modifiers) + " " if symbol.modifiers else ""

            lines = [
                f"```cssl",
                f"{modifiers}define {symbol.name}({param_str}) -> {return_type}",
                f"```",
                "",
                f"User-defined function" + (f" at line {symbol.line}" if symbol.line > 0 else "")
            ]

            if symbol.documentation:
                lines.append("")
                lines.append(symbol.documentation)

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(lines)
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.CLASS:
            lines = [
                f"```cssl",
                f"class {symbol.name}",
                f"```",
                "",
                f"User-defined class" + (f" at line {symbol.line}" if symbol.line > 0 else "")
            ]

            if symbol.documentation:
                lines.append("")
                lines.append(symbol.documentation)

            # Show class members if available
            if symbol.children:
                lines.append("")
                lines.append("**Members:**")
                for name, child in symbol.children.items():
                    if child.kind == SymbolKind.METHOD:
                        doc_hint = f" - {child.documentation}" if child.documentation else ""
                        lines.append(f"- `{name}()`{doc_hint}")
                    elif child.kind == SymbolKind.PROPERTY:
                        lines.append(f"- `{name}` (property)")
                    else:
                        lines.append(f"- `{name}`")

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(lines)
                ),
                range=range
            )

        elif symbol.kind in (SymbolKind.VARIABLE, SymbolKind.PARAMETER):
            type_info = symbol.type_info or "dynamic"
            location = f" defined at line {symbol.line}" if symbol.line > 0 else ""

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\n{type_info} {symbol.name}\n```\n\n{kind_name.capitalize()}{location}"
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.GLOBAL:
            location = f" defined at line {symbol.line}" if symbol.line > 0 else ""
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\nglobal {symbol.name}\n```\n\nGlobal variable{location}"
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.SHARED:
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\nshared {symbol.name}\n```\n\nShared variable"
                ),
                range=range
            )

        else:
            location = f"\n\nDefined at line {symbol.line}" if symbol.line > 0 else ""
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{symbol.name}** ({kind_name}){location}"
                ),
                range=range
            )

    def _hover_pointer_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for pointer reference (?var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        # Try to find the referenced variable
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(var_name)
            if symbol:
                type_info = symbol.type_info or "dynamic"
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"**Pointer Reference**\n\n```cssl\n?{var_name}  // pointer to {type_info} {var_name}\n```\n\nReferences variable `{var_name}` defined at line {symbol.line}"
                    ),
                    range=word_range
                )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Pointer Reference**\n\n`?{var_name}` - pointer to variable `{var_name}`\n\n⚠️ Variable `{var_name}` not found"
            ),
            range=word_range
        )

    def _hover_global_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for global reference (@var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Global Reference**\n\n`@{var_name}` - reference to global variable `{var_name}`"
            ),
            range=word_range
        )

    def _hover_shared_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for shared reference ($var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Shared Reference**\n\n`${var_name}` - reference to shared variable `{var_name}`\n\nShared variables are accessible across modules."
            ),
            range=word_range
        )

    def _hover_snapshot_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for snapshot reference (%var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Snapshot Reference**\n\n`%{var_name}` - reference to snapshot of `{var_name}`\n\nAccess the value from when `snapshot({var_name})` was called."
            ),
            range=word_range
        )
