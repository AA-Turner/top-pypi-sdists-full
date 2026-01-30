"""
Document Manager for the CSSL Language Server.

Handles document tracking, parsing, and caching of analysis results.
"""

import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Import CSSL parser components
try:
    from includecpp.core.cssl.cssl_parser import (
        CSSLLexer, CSSLParser, CSSLSyntaxError, Token, ASTNode
    )
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False
    CSSLLexer = None
    CSSLParser = None
    CSSLSyntaxError = Exception
    Token = None
    ASTNode = None

from ..utils.symbol_table import SymbolTable, Symbol, SymbolKind


@dataclass
class SyntaxError:
    """Represents a syntax error in the document."""
    line: int
    column: int
    message: str
    token: str = ""
    source_line: str = ""


@dataclass
class DocumentAnalysis:
    """
    Contains the complete analysis of a CSSL document.

    Includes tokens, AST, symbol table, and any errors found.
    """
    uri: str
    source: str
    version: int = 0
    tokens: List[Any] = field(default_factory=list)
    ast: Optional[Any] = None
    syntax_errors: List[SyntaxError] = field(default_factory=list)
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    source_lines: List[str] = field(default_factory=list)
    is_valid: bool = False

    def __post_init__(self):
        self.source_lines = self.source.splitlines()

    @property
    def text(self) -> str:
        """Alias for source - returns the document text."""
        return self.source

    def get_line(self, line: int) -> str:
        """Get the text of a specific line (0-based)."""
        if 0 <= line < len(self.source_lines):
            return self.source_lines[line]
        return ""

    def get_token_at(self, line: int, column: int) -> Optional[Any]:
        """Find the token at the given position."""
        for token in self.tokens:
            if hasattr(token, 'line') and hasattr(token, 'column'):
                token_line = token.line - 1  # Convert to 0-based
                token_col = token.column - 1
                token_value = str(token.value) if hasattr(token, 'value') else ''
                token_end = token_col + len(token_value)

                if token_line == line and token_col <= column < token_end:
                    return token
        return None


class DocumentManager:
    """
    Manages all open CSSL documents and their analysis state.

    Thread-safe for concurrent access from the language server.
    """

    def __init__(self):
        self._documents: Dict[str, DocumentAnalysis] = {}
        self._lock = threading.RLock()

    def open_document(self, uri: str, text: str, version: int = 0) -> DocumentAnalysis:
        """
        Open a new document and perform initial analysis.

        Args:
            uri: Document URI
            text: Document content
            version: Document version

        Returns:
            The analysis result
        """
        with self._lock:
            analysis = self._analyze_document(uri, text, version)
            self._documents[uri] = analysis
            return analysis

    def update_document(self, uri: str, text: str, version: int = 0) -> DocumentAnalysis:
        """
        Update an existing document and re-analyze.

        Args:
            uri: Document URI
            text: New document content
            version: New document version

        Returns:
            The updated analysis result
        """
        with self._lock:
            analysis = self._analyze_document(uri, text, version)
            self._documents[uri] = analysis
            return analysis

    def close_document(self, uri: str) -> None:
        """Close a document and remove from cache."""
        with self._lock:
            if uri in self._documents:
                del self._documents[uri]

    def get_document(self, uri: str) -> Optional[DocumentAnalysis]:
        """Get the analysis for a document."""
        with self._lock:
            return self._documents.get(uri)

    def _analyze_document(self, uri: str, text: str, version: int) -> DocumentAnalysis:
        """
        Perform full analysis of a CSSL document.

        Includes tokenization, parsing, and symbol extraction.
        """
        analysis = DocumentAnalysis(uri=uri, source=text, version=version)

        if not PARSER_AVAILABLE:
            analysis.syntax_errors.append(SyntaxError(
                line=1,
                column=1,
                message="CSSL parser not available - install includecpp package"
            ))
            return analysis

        # Step 1: Tokenize
        try:
            lexer = CSSLLexer(text)
            analysis.tokens = lexer.tokenize()
        except Exception as e:
            analysis.syntax_errors.append(SyntaxError(
                line=1,
                column=1,
                message=f"Tokenization error: {str(e)}"
            ))
            return analysis

        # Step 2: Parse
        try:
            parser = CSSLParser(analysis.tokens, analysis.source_lines, text)

            # Auto-detect format
            stripped = text.lstrip()
            if stripped.startswith('{') or stripped.startswith('service-'):
                analysis.ast = parser.parse()
            else:
                analysis.ast = parser.parse_program()

            analysis.is_valid = True

        except CSSLSyntaxError as e:
            analysis.syntax_errors.append(SyntaxError(
                line=getattr(e, 'line', 1),
                column=getattr(e, 'column', 1),
                message=str(e),
                source_line=getattr(e, 'source_line', '')
            ))
            # Still try to use partial tokens for analysis
            analysis.is_valid = False

        except Exception as e:
            analysis.syntax_errors.append(SyntaxError(
                line=1,
                column=1,
                message=f"Parse error: {str(e)}"
            ))
            analysis.is_valid = False

        # Step 3: Build symbol table from AST
        if analysis.ast:
            self._build_symbol_table(analysis)

        return analysis

    def _build_symbol_table(self, analysis: DocumentAnalysis) -> None:
        """Build the symbol table from the AST."""
        from .semantic_analyzer import SemanticAnalyzer

        analyzer = SemanticAnalyzer()
        analysis.symbol_table = analyzer.analyze(analysis.ast, analysis.tokens)

    def get_all_documents(self) -> List[DocumentAnalysis]:
        """Get all open documents."""
        with self._lock:
            return list(self._documents.values())
