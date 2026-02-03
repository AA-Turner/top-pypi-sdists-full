"""
Document Manager for the CSSL Language Server.

Handles document tracking, parsing, and caching of analysis results.
"""

import logging
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger('cssl-lsp.document_manager')

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
        # Run expensive analysis WITHOUT holding the lock
        analysis = self._analyze_document(uri, text, version)
        # Only hold lock for the quick dict update
        with self._lock:
            self._documents[uri] = analysis
        return analysis

    def update_document_fast(self, uri: str, text: str, version: int = 0) -> DocumentAnalysis:
        """
        Fast update: tokenize only (no parsing/symbol table).

        Used for immediate responsiveness during typing.
        Completions can work from tokens alone.
        """
        with self._lock:
            analysis = DocumentAnalysis(uri=uri, source=text, version=version)

            if PARSER_AVAILABLE:
                try:
                    lexer = CSSLLexer(text)
                    analysis.tokens = lexer.tokenize()
                except Exception:
                    pass  # Tokens from previous analysis will be used

            # Preserve AST and symbol table from previous analysis if available
            prev = self._documents.get(uri)
            if prev:
                analysis.ast = prev.ast
                analysis.symbol_table = prev.symbol_table
                analysis.is_valid = prev.is_valid
                if not analysis.tokens and prev.tokens:
                    analysis.tokens = prev.tokens

            self._documents[uri] = analysis
            return analysis

    def update_document(self, uri: str, text: str, version: int = 0) -> DocumentAnalysis:
        """
        Full update: tokenize, parse, and build symbol table.

        This is the expensive operation - should be run in a background thread.
        Lock is NOT held during analysis to avoid blocking the event loop.
        """
        # Run expensive analysis WITHOUT holding the lock
        analysis = self._analyze_document(uri, text, version)
        # Only hold lock for the quick dict update
        with self._lock:
            # Only update if no newer version has been stored while we were parsing
            existing = self._documents.get(uri)
            if existing is None or existing.version <= version:
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
        Uses a timeout to prevent parser hangs from blocking the server.
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
            logger.debug(f"Step 1: Tokenizing {uri}")
            lexer = CSSLLexer(text)
            analysis.tokens = lexer.tokenize()
            logger.debug(f"Tokenized: {len(analysis.tokens)} tokens")
        except Exception as e:
            analysis.syntax_errors.append(SyntaxError(
                line=1,
                column=1,
                message=f"Tokenization error: {str(e)}"
            ))
            return analysis

        # Step 2: Parse (with timeout to prevent hangs)
        try:
            logger.debug(f"Step 2: Parsing {uri}")
            ast_result = self._parse_with_timeout(analysis.tokens, analysis.source_lines, text, timeout=1)
            if ast_result is not None:
                analysis.ast = ast_result
                analysis.is_valid = True
                logger.debug(f"Parsed successfully")
            else:
                analysis.syntax_errors.append(SyntaxError(
                    line=1, column=1,
                    message="Parser timed out"
                ))
                analysis.is_valid = False

        except CSSLSyntaxError as e:
            analysis.syntax_errors.append(SyntaxError(
                line=getattr(e, 'line', 1),
                column=getattr(e, 'column', 1),
                message=str(e),
                source_line=getattr(e, 'source_line', '')
            ))
            analysis.is_valid = False

        except Exception as e:
            analysis.syntax_errors.append(SyntaxError(
                line=1,
                column=1,
                message=f"Parse error: {str(e)}"
            ))
            analysis.is_valid = False

        # Step 3: Build symbol table from AST (with timeout)
        if analysis.ast:
            try:
                logger.debug(f"Step 3: Building symbol table for {uri}")
                self._build_symbol_table_with_timeout(analysis, timeout=1)
                logger.debug(f"Symbol table built")
            except Exception as e:
                logger.warning(f"Symbol table build failed: {e}")

        return analysis

    def _parse_with_timeout(self, tokens, source_lines, text, timeout=3):
        """Run the parser in a thread with a timeout to prevent hangs."""
        result = [None]
        error = [None]

        def do_parse():
            try:
                parser = CSSLParser(tokens, source_lines, text)
                stripped = text.lstrip()
                if stripped.startswith('{') or stripped.startswith('service-'):
                    result[0] = parser.parse()
                else:
                    result[0] = parser.parse_program()
            except Exception as e:
                error[0] = e

        thread = threading.Thread(target=do_parse, daemon=True)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            logger.warning(f"Parser timed out after {timeout}s")
            return None

        if error[0]:
            raise error[0]

        return result[0]

    def _build_symbol_table_with_timeout(self, analysis, timeout=3):
        """Build symbol table with a timeout to prevent hangs."""
        error = [None]

        def do_build():
            try:
                self._build_symbol_table(analysis)
            except Exception as e:
                error[0] = e

        thread = threading.Thread(target=do_build, daemon=True)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            logger.warning(f"Symbol table build timed out after {timeout}s")
            return

        if error[0]:
            raise error[0]

    def _build_symbol_table(self, analysis: DocumentAnalysis) -> None:
        """Build the symbol table from the AST."""
        from .semantic_analyzer import SemanticAnalyzer

        analyzer = SemanticAnalyzer()
        analysis.symbol_table = analyzer.analyze(analysis.ast, analysis.tokens)
        logger.debug(f"Symbol table has {len(analysis.symbol_table.get_all_symbols_flat())} symbols")

        # Extract /d docstrings from source text and attach to symbols
        self._extract_docstrings(analysis)

    def _extract_docstrings(self, analysis: DocumentAnalysis) -> None:
        """Extract /d docstring comments and attach to nearest symbols.

        Scans source text for /d lines and associates them with the
        class, constructor, or function that contains them.

        Supports:
            /d This is a docstring for the enclosing construct.
            /d Multiple /d lines are joined together.
        """
        if not analysis.text or not analysis.symbol_table:
            return

        try:
            self._do_extract_docstrings(analysis)
        except Exception as e:
            logger.debug(f"Docstring extraction error: {e}")

    def _do_extract_docstrings(self, analysis: DocumentAnalysis) -> None:
        """Internal docstring extraction implementation."""
        lines = analysis.text.splitlines()
        all_symbols = analysis.symbol_table.get_all_symbols_flat()
        if not all_symbols:
            return

        from ..utils.symbol_table import SymbolKind
        target_kinds = {SymbolKind.CLASS, SymbolKind.FUNCTION, SymbolKind.METHOD, SymbolKind.CONSTRUCTOR}
        declared_symbols = [s for s in all_symbols if s.kind in target_kinds and s.line > 0]

        # Collect consecutive /d lines and their line numbers (1-indexed)
        docstring_blocks = []  # [(start_line_1indexed, end_line_1indexed, text)]
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped.startswith('/d ') or stripped == '/d':
                doc_lines = []
                start = i
                while i < len(lines):
                    s = lines[i].strip()
                    if s.startswith('/d '):
                        doc_lines.append(s[3:].strip())
                    elif s == '/d':
                        doc_lines.append('')
                    else:
                        break
                    i += 1
                docstring_blocks.append((start + 1, i, '\n'.join(doc_lines)))
            else:
                i += 1

        if not docstring_blocks:
            return

        # For each docstring block, find the enclosing symbol
        # The /d is inside a construct's body, so find the symbol whose
        # declaration line is the closest BEFORE the /d line
        for doc_start_line, doc_end_line, doc_text in docstring_blocks:
            best_symbol = None
            best_dist = float('inf')
            for sym in declared_symbols:
                # Symbol must be declared before or at the docstring
                if sym.line <= doc_start_line:
                    dist = doc_start_line - sym.line
                    if dist < best_dist:
                        best_dist = dist
                        best_symbol = sym
            if best_symbol and not best_symbol.documentation:
                best_symbol.documentation = doc_text
            elif best_symbol and best_symbol.documentation:
                best_symbol.documentation += '\n\n' + doc_text

        # Also infer return types for define functions from return statements
        self._infer_return_types(analysis, lines, declared_symbols)

    def _infer_return_types(self, analysis: DocumentAnalysis, lines, declared_symbols) -> None:
        """Infer return types for functions from return statements.

        Rules:
        - No return statement found → void
        - return <expr> with inferrable type → int, float, string, bool
        - return <expr> with unknown type → dynamic
        - No explicit return type and no return → void
        """
        from ..utils.symbol_table import SymbolKind
        for sym in declared_symbols:
            if sym.kind != SymbolKind.FUNCTION:
                continue
            if sym.line <= 0:
                continue
            # Scan lines after function declaration for return statements
            start = sym.line  # 1-indexed
            found_return = False
            brace_depth = 0
            started = False
            for j in range(start - 1, min(start + 100, len(lines))):
                line_text = lines[j]
                stripped = line_text.strip()
                # Track brace depth to stay within this function's body
                brace_depth += stripped.count('{') - stripped.count('}')
                if '{' in stripped:
                    started = True
                if started and brace_depth <= 0:
                    break  # Left the function body
                if stripped.startswith('return ') or stripped.startswith('return;'):
                    expr = stripped[7:].rstrip(';').strip() if stripped.startswith('return ') else ''
                    if not expr or expr == 'null' or expr == 'None':
                        found_return = True
                        continue  # return; or return null → void-like
                    found_return = True
                    # Simple type inference from the expression
                    inferred = None
                    try:
                        int(expr)
                        inferred = 'int'
                    except ValueError:
                        pass
                    if not inferred:
                        try:
                            float(expr)
                            inferred = 'float'
                        except ValueError:
                            pass
                    if not inferred:
                        if (expr.startswith('"') and expr.endswith('"')) or \
                           (expr.startswith("'") and expr.endswith("'")):
                            inferred = 'string'
                    if not inferred:
                        if expr in ('true', 'false', 'True', 'False'):
                            inferred = 'bool'
                    if not inferred:
                        inferred = 'dynamic'
                    sym.return_type = inferred
                    break
            if not found_return and not sym.return_type:
                sym.return_type = 'void'

    def get_all_documents(self) -> List[DocumentAnalysis]:
        """Get all open documents."""
        with self._lock:
            return list(self._documents.values())
