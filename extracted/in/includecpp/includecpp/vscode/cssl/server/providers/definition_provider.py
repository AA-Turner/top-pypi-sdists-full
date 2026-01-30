"""
Definition Provider for the CSSL Language Server.

Provides go-to-definition functionality for CSSL code elements including:
- User-defined functions
- User-defined classes and structs
- Variables and parameters
- Global and shared variables
"""

from typing import Optional, List
from lsprotocol.types import (
    Location,
    Position,
    Range,
)

from ..analysis.document_manager import DocumentAnalysis
from ..analysis.semantic_analyzer import CSSL_KEYWORDS, CSSL_TYPES, CSSL_BUILTINS, CSSL_MODIFIERS
from ..utils.symbol_table import SymbolKind, Symbol
from ..utils.position_utils import get_word_at_position


class DefinitionProvider:
    """
    Provides go-to-definition for CSSL code.

    Allows jumping to:
    - Function definitions
    - Class definitions
    - Variable declarations
    - Parameter definitions
    """

    def __init__(self):
        pass

    def get_definition(
        self,
        document: DocumentAnalysis,
        position: Position
    ) -> Optional[Location]:
        """
        Get the definition location for the symbol at position.

        Args:
            document: The analyzed document
            position: Cursor position

        Returns:
            Location of the definition, or None if not found
        """
        text = document.text
        line = position.line
        column = position.character

        # Get the word at position
        word_info = get_word_at_position(text, line, column)

        if not word_info:
            return None

        word, start_col, end_col = word_info

        # Handle special prefixes
        if word.startswith('?'):
            # Pointer reference - go to variable definition
            word = word[1:]
        elif word.startswith('@'):
            # Global reference - go to global definition
            word = word[1:]
        elif word.startswith('$'):
            # Shared reference - go to share() call
            word = word[1:]
        elif word.startswith('%'):
            # Snapshot reference - go to snapshot() call
            word = word[1:]

        # Skip builtins, keywords, types - they have no source location
        if word in CSSL_BUILTINS or word in CSSL_KEYWORDS or word in CSSL_TYPES or word in CSSL_MODIFIERS:
            return None

        # Search in symbol table
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(word)
            if symbol and symbol.line > 0:
                return self._create_location(document.uri, symbol)

        # Search in AST for definitions
        if document.ast:
            location = self._find_definition_in_ast(document, word)
            if location:
                return location

        return None

    def get_definitions(
        self,
        document: DocumentAnalysis,
        position: Position
    ) -> List[Location]:
        """
        Get all definition locations for the symbol at position.

        This handles cases where there might be multiple definitions
        (e.g., method overloads).

        Args:
            document: The analyzed document
            position: Cursor position

        Returns:
            List of definition locations
        """
        # For now, return single definition as a list
        definition = self.get_definition(document, position)
        if definition:
            return [definition]
        return []

    def _create_location(self, uri: str, symbol: Symbol) -> Location:
        """Create a Location from a Symbol."""
        # Calculate end position
        end_line = symbol.end_line if symbol.end_line > 0 else symbol.line
        end_column = symbol.end_column if symbol.end_column > 0 else symbol.column + len(symbol.name)

        return Location(
            uri=uri,
            range=Range(
                start=Position(line=symbol.line - 1, character=symbol.column - 1),
                end=Position(line=end_line - 1, character=end_column - 1)
            )
        )

    def _find_definition_in_ast(
        self,
        document: DocumentAnalysis,
        name: str
    ) -> Optional[Location]:
        """
        Search the AST for a definition of the given name.

        Args:
            document: The analyzed document
            name: Name to find

        Returns:
            Location if found, None otherwise
        """
        if not document.ast:
            return None

        # Walk the AST looking for definitions
        result = self._walk_ast_for_definition(document.ast, name)

        if result:
            line, column = result
            return Location(
                uri=document.uri,
                range=Range(
                    start=Position(line=line - 1, character=column - 1),
                    end=Position(line=line - 1, character=column - 1 + len(name))
                )
            )

        return None

    def _walk_ast_for_definition(
        self,
        node,
        name: str
    ) -> Optional[tuple]:
        """
        Recursively walk AST to find definition.

        Args:
            node: Current AST node
            name: Name to find

        Returns:
            Tuple of (line, column) if found, None otherwise
        """
        if node is None:
            return None

        if not hasattr(node, 'type'):
            return None

        node_type = node.type

        # Check function definitions
        if node_type == 'function':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                func_name = info.get('name', '')
            else:
                func_name = str(info)

            if func_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Check class definitions
        elif node_type == 'class':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                class_name = info.get('name', '')
            else:
                class_name = str(info)

            if class_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Check struct definitions
        elif node_type == 'struct':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                struct_name = info.get('name', '')
            else:
                struct_name = str(info)

            if struct_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Check enum definitions
        elif node_type == 'enum':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                enum_name = info.get('name', '')
            else:
                enum_name = str(info)

            if enum_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Check namespace definitions
        elif node_type == 'namespace':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                ns_name = info.get('name', '')
            else:
                ns_name = str(info)

            if ns_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Check typed declarations
        elif node_type == 'typed_declaration':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                var_name = info.get('name', '')
                if var_name == name:
                    line = getattr(node, 'line', 0)
                    column = getattr(node, 'column', 0)
                    if line > 0:
                        return (line, column)

        # Check assignments (first assignment is declaration in CSSL)
        elif node_type == 'assignment':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                var_name = info.get('name') or info.get('target')

                # Handle ASTNode targets
                if hasattr(var_name, 'type') and hasattr(var_name, 'value'):
                    if var_name.type == 'identifier':
                        var_name = var_name.value
                    else:
                        var_name = None

                if var_name == name:
                    line = getattr(node, 'line', 0)
                    column = getattr(node, 'column', 0)
                    if line > 0:
                        return (line, column)

        # Check global declarations
        elif node_type == 'global_declaration':
            info = node.value if hasattr(node, 'value') else {}
            if isinstance(info, dict):
                var_name = info.get('name', '')
            else:
                var_name = str(info)

            if var_name == name:
                line = getattr(node, 'line', 0)
                column = getattr(node, 'column', 0)
                if line > 0:
                    return (line, column)

        # Recursively check children
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                result = self._walk_ast_for_definition(child, name)
                if result:
                    return result

        return None

    def find_references(
        self,
        document: DocumentAnalysis,
        position: Position,
        include_declaration: bool = True
    ) -> List[Location]:
        """
        Find all references to the symbol at position.

        Args:
            document: The analyzed document
            position: Cursor position
            include_declaration: Whether to include the declaration itself

        Returns:
            List of locations where the symbol is referenced
        """
        text = document.text
        line = position.line
        column = position.character

        # Get the word at position
        word_info = get_word_at_position(text, line, column)

        if not word_info:
            return []

        word, _, _ = word_info

        # Handle special prefixes
        if word.startswith(('?', '@', '$', '%')):
            word = word[1:]

        # Skip builtins, keywords, types
        if word in CSSL_BUILTINS or word in CSSL_KEYWORDS or word in CSSL_TYPES or word in CSSL_MODIFIERS:
            return []

        references: List[Location] = []

        # Search through all tokens for the name
        if document.tokens:
            for token in document.tokens:
                if not hasattr(token, 'value') or not hasattr(token, 'type'):
                    continue

                token_value = token.value
                type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)

                # Check if this token is the word we're looking for
                if type_name == 'IDENTIFIER' and token_value == word:
                    token_line = getattr(token, 'line', 0)
                    token_column = getattr(token, 'column', 0)

                    if token_line > 0:
                        # Skip declaration if requested
                        if not include_declaration:
                            if document.symbol_table:
                                symbol = document.symbol_table.get_symbol(word)
                                if symbol and symbol.line == token_line and symbol.column == token_column:
                                    continue

                        references.append(Location(
                            uri=document.uri,
                            range=Range(
                                start=Position(line=token_line - 1, character=token_column - 1),
                                end=Position(line=token_line - 1, character=token_column - 1 + len(word))
                            )
                        ))

                # Also check pointer references (?word)
                elif type_name == 'POINTER_REF' and token_value[1:] == word:
                    token_line = getattr(token, 'line', 0)
                    token_column = getattr(token, 'column', 0)

                    if token_line > 0:
                        references.append(Location(
                            uri=document.uri,
                            range=Range(
                                start=Position(line=token_line - 1, character=token_column - 1),
                                end=Position(line=token_line - 1, character=token_column + len(token_value))
                            )
                        ))

                # Check global references (@word)
                elif type_name == 'GLOBAL_REF' and token_value[1:] == word:
                    token_line = getattr(token, 'line', 0)
                    token_column = getattr(token, 'column', 0)

                    if token_line > 0:
                        references.append(Location(
                            uri=document.uri,
                            range=Range(
                                start=Position(line=token_line - 1, character=token_column - 1),
                                end=Position(line=token_line - 1, character=token_column + len(token_value))
                            )
                        ))

                # Check shared references ($word)
                elif type_name == 'SHARED_REF' and token_value[1:] == word:
                    token_line = getattr(token, 'line', 0)
                    token_column = getattr(token, 'column', 0)

                    if token_line > 0:
                        references.append(Location(
                            uri=document.uri,
                            range=Range(
                                start=Position(line=token_line - 1, character=token_column - 1),
                                end=Position(line=token_line - 1, character=token_column + len(token_value))
                            )
                        ))

        return references
