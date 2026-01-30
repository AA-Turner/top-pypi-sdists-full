"""
Symbol Table for CSSL Language Server.

Provides data structures for tracking symbols (variables, functions, classes)
in CSSL source code for semantic analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class SymbolKind(Enum):
    """Types of symbols that can be tracked."""
    VARIABLE = 1
    FUNCTION = 2
    CLASS = 3
    STRUCT = 4
    ENUM = 5
    NAMESPACE = 6
    PARAMETER = 7
    BUILTIN_FUNCTION = 8
    BUILTIN_TYPE = 9
    METHOD = 10
    PROPERTY = 11
    CONSTRUCTOR = 12
    GLOBAL = 13
    SHARED = 14
    SNAPSHOT = 15


@dataclass
class Symbol:
    """Represents a symbol in the CSSL source code."""
    name: str
    kind: SymbolKind
    type_info: Optional[str] = None
    line: int = 0
    column: int = 0
    end_line: int = 0
    end_column: int = 0
    documentation: str = ""
    parameters: List['Symbol'] = field(default_factory=list)
    return_type: Optional[str] = None
    modifiers: List[str] = field(default_factory=list)
    scope: str = ""
    children: Dict[str, 'Symbol'] = field(default_factory=dict)
    is_used: bool = False

    def __hash__(self):
        return hash((self.name, self.kind, self.line, self.column))


@dataclass
class SymbolTable:
    """
    Hierarchical symbol table for tracking all symbols in a CSSL document.

    Supports nested scopes for functions, classes, and blocks.
    """
    symbols: Dict[str, Symbol] = field(default_factory=dict)
    scopes: Dict[str, 'SymbolTable'] = field(default_factory=dict)
    parent: Optional['SymbolTable'] = None
    scope_name: str = ""

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to this scope."""
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Optional[Symbol]:
        """Get a symbol by name, searching parent scopes if needed."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.get_symbol(name)
        return None

    def has_symbol(self, name: str) -> bool:
        """Check if a symbol exists in this scope or parent scopes."""
        return self.get_symbol(name) is not None

    def has_symbol_local(self, name: str) -> bool:
        """Check if a symbol exists only in this scope (not parents)."""
        return name in self.symbols

    def create_child_scope(self, name: str) -> 'SymbolTable':
        """Create a new child scope."""
        child = SymbolTable(parent=self, scope_name=name)
        self.scopes[name] = child
        return child

    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols from this scope and all parent scopes."""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.symbols)
        return all_symbols

    def get_all_symbols_flat(self) -> List[Symbol]:
        """Get a flat list of all symbols including nested scopes."""
        result = list(self.symbols.values())
        for scope in self.scopes.values():
            result.extend(scope.get_all_symbols_flat())
        return result

    def find_symbol_by_position(self, line: int, column: int) -> Optional[Symbol]:
        """Find a symbol that contains the given position."""
        for symbol in self.symbols.values():
            if symbol.line == line:
                if symbol.column <= column <= symbol.column + len(symbol.name):
                    return symbol
        for scope in self.scopes.values():
            found = scope.find_symbol_by_position(line, column)
            if found:
                return found
        return None

    def get_functions(self) -> List[Symbol]:
        """Get all function symbols."""
        return [s for s in self.get_all_symbols_flat() if s.kind == SymbolKind.FUNCTION]

    def get_classes(self) -> List[Symbol]:
        """Get all class symbols."""
        return [s for s in self.get_all_symbols_flat() if s.kind == SymbolKind.CLASS]

    def get_variables(self) -> List[Symbol]:
        """Get all variable symbols."""
        return [s for s in self.get_all_symbols_flat() if s.kind == SymbolKind.VARIABLE]

    def get_globals(self) -> List[Symbol]:
        """Get all global symbols."""
        return [s for s in self.get_all_symbols_flat() if s.kind == SymbolKind.GLOBAL]

    def get_shared(self) -> List[Symbol]:
        """Get all shared symbols."""
        return [s for s in self.get_all_symbols_flat() if s.kind == SymbolKind.SHARED]

    def mark_symbol_used(self, name: str) -> None:
        """Mark a symbol as used."""
        symbol = self.get_symbol(name)
        if symbol:
            symbol.is_used = True

    def get_unused_symbols(self) -> List[Symbol]:
        """Get all symbols that were declared but never used."""
        return [
            s for s in self.get_all_symbols_flat()
            if not s.is_used
            and s.kind in (SymbolKind.VARIABLE, SymbolKind.PARAMETER)
            and not s.name.startswith('_')
        ]
