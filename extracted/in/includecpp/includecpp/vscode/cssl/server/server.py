"""
CSSL Language Server

A complete Language Server Protocol (LSP) implementation for CSSL,
built with pygls. Provides:
- Real-time diagnostics (syntax errors, type errors, undefined variables)
- Autocomplete (builtins, keywords, types, user symbols)
- Hover documentation
- Go-to-definition
- Find references

Usage:
    python -m includecpp.vscode.cssl.server
"""

import logging
import sys
import asyncio
import argparse
from typing import Optional, Dict

from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_REFERENCES,
    TEXT_DOCUMENT_SIGNATURE_HELP,
    INITIALIZED,
    CompletionOptions,
    CompletionParams,
    CompletionList,
    DefinitionParams,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    Hover,
    HoverParams,
    Location,
    Position,
    PublishDiagnosticsParams,
    ReferenceParams,
    SignatureHelp,
    SignatureHelpOptions,
    SignatureHelpParams,
    TextDocumentSyncKind,
)

from pygls.lsp.server import LanguageServer

from .analysis.document_manager import DocumentManager
from .analysis.diagnostic_provider import DiagnosticProvider
from .providers.completion_provider import CompletionProvider
from .providers.hover_provider import HoverProvider
from .providers.definition_provider import DefinitionProvider
from .providers.signature_help_provider import SignatureHelpProvider


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('cssl-lsp')

# Debug file logging - writes to a file to bypass any stdio issues
import os
import tempfile
DEBUG_LOG_FILE = os.path.join(tempfile.gettempdir(), 'cssl_lsp_debug.log')

def debug_log(msg: str):
    """Write debug message to file for troubleshooting."""
    try:
        with open(DEBUG_LOG_FILE, 'a', encoding='utf-8') as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
            f.flush()
    except:
        pass

debug_log(f"=== CSSL LSP Server module loaded ===" )


class CSSLLanguageServer(LanguageServer):
    """
    CSSL Language Server implementation.

    Provides full LSP support for the CSSL scripting language.
    """

    DEBOUNCE_DELAY = 0.15  # seconds to wait after last keystroke before parsing

    def __init__(self):
        super().__init__(
            name='cssl-language-server',
            version='2.0.0',
            text_document_sync_kind=TextDocumentSyncKind.Full,
        )

        # Initialize components
        self.document_manager = DocumentManager()
        self.diagnostic_provider = DiagnosticProvider()
        self.completion_provider = CompletionProvider()
        self.hover_provider = HoverProvider()
        self.definition_provider = DefinitionProvider()
        self.signature_help_provider = SignatureHelpProvider()

        # Give providers access to document manager for cross-file lookups
        self.completion_provider.set_document_manager(self.document_manager)
        self.signature_help_provider.set_document_manager(self.document_manager)

        # Configuration
        self.diagnostics_enabled = True
        self.max_problems = 100

        # Debounce timers per document URI
        self._debounce_tasks: Dict[str, asyncio.Task] = {}
        # Pending text per URI (updated immediately, parsed after debounce)
        self._pending_texts: Dict[str, tuple] = {}  # uri -> (text, version)

        logger.info("CSSL Language Server initialized")

    async def schedule_analysis(self, uri: str, text: str, version: int):
        """Schedule a debounced analysis for a document.

        Updates the document text immediately (for completions) but
        defers the expensive parse+diagnostics until typing pauses.
        Must be called from an async context (the event loop).
        """
        # Store pending text immediately
        self._pending_texts[uri] = (text, version)

        # Update document with just tokens (fast) for immediate completions
        self.document_manager.update_document_fast(uri, text, version)

        # Cancel any existing debounce timer for this URI
        if uri in self._debounce_tasks:
            self._debounce_tasks[uri].cancel()

        # Schedule new debounced analysis on the running event loop
        self._debounce_tasks[uri] = asyncio.ensure_future(
            self._debounced_analyze(uri)
        )

    async def _debounced_analyze(self, uri: str):
        """Wait for typing to pause, then run full analysis in background."""
        try:
            await asyncio.sleep(self.DEBOUNCE_DELAY)
        except asyncio.CancelledError:
            return  # New keystroke came in, this analysis is superseded

        # Get the latest pending text
        pending = self._pending_texts.pop(uri, None)
        if not pending:
            return

        text, version = pending

        try:
            # Run the expensive parsing in a thread pool (non-blocking)
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                self.document_manager.update_document, uri, text, version
            )

            # Publish diagnostics after analysis completes
            _publish_diagnostics(uri)
        except Exception as e:
            logger.error(f"Error in debounced analysis: {e}", exc_info=True)


# Create server instance
server = CSSLLanguageServer()


def _verify_feature_registration():
    """Debug function to verify features are registered correctly."""
    debug_log("_verify_feature_registration called")
    try:
        if hasattr(server, 'protocol') and hasattr(server.protocol, 'fm'):
            features = list(server.protocol.fm.features.keys())
            debug_log(f"Features registered: {features}")
            sys.stderr.write(f"[DEBUG] User features registered: {features}\n")
            sys.stderr.flush()
        else:
            debug_log("Cannot access feature manager")
            sys.stderr.write("[DEBUG] Cannot access feature manager (server not fully initialized)\n")
            sys.stderr.flush()
    except Exception as e:
        debug_log(f"Error checking features: {e}")
        sys.stderr.write(f"[DEBUG] Error checking features: {e}\n")
        sys.stderr.flush()


@server.feature(INITIALIZED)
def lsp_initialized(params):
    """Handle initialized notification."""
    logger.info("CSSL Language Server fully initialized")

    # Read client configuration if provided via initialization options
    try:
        proto = getattr(server, 'protocol', None)
        init_params = getattr(proto, '_init_params', None) if proto else None
        if init_params and getattr(init_params, 'initialization_options', None):
            opts = init_params.initialization_options
            if isinstance(opts, dict):
                server.diagnostics_enabled = opts.get('diagnostics', {}).get('enabled', True)
                server.max_problems = opts.get('diagnostics', {}).get('maxProblems', 100)
                logger.info(f"Configuration: diagnostics={server.diagnostics_enabled}, max_problems={server.max_problems}")
    except Exception as e:
        logger.warning(f"Could not read initialization options: {e}")

    # Verify feature registration at runtime
    _verify_feature_registration()
    sys.stderr.write("[DEBUG] Server fully initialized, ready for document events\n")
    sys.stderr.flush()


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(params: DidOpenTextDocumentParams):
    """Handle document open - async to allow debounced background analysis."""
    try:
        uri = params.text_document.uri
        text = params.text_document.text
        version = params.text_document.version

        logger.info(f"Document opened: {uri} ({len(text)} chars)")

        # Schedule debounced analysis (non-blocking)
        await server.schedule_analysis(uri, text, version)
    except Exception as e:
        logger.error(f"Error in did_open: {e}", exc_info=True)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(params: DidChangeTextDocumentParams):
    """Handle document change - async with debounce to avoid blocking the event loop."""
    try:
        uri = params.text_document.uri
        version = params.text_document.version

        # Get the new text - handle both Full and Incremental sync
        if params.content_changes:
            if hasattr(params.content_changes[0], 'range') and params.content_changes[0].range is not None:
                # Incremental change - get full text from server workspace
                doc = server.workspace.get_text_document(uri)
                text = doc.source
            else:
                # Full sync - use the provided text
                text = params.content_changes[0].text
        else:
            return

        logger.info(f"Document changed: {uri} (version {version}, {len(text)} chars)")

        # Schedule debounced analysis (non-blocking)
        await server.schedule_analysis(uri, text, version)
    except Exception as e:
        logger.error(f"Error in did_change: {e}", exc_info=True)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(params: DidSaveTextDocumentParams):
    """Handle document save."""
    try:
        uri = params.text_document.uri
        logger.debug(f"Document saved: {uri}")
        # Re-publish diagnostics on save
        _publish_diagnostics(uri)
    except Exception as e:
        logger.error(f"Error in did_save: {e}", exc_info=True)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: DidCloseTextDocumentParams):
    """Handle document close."""
    try:
        uri = params.text_document.uri
        logger.debug(f"Document closed: {uri}")

        # Cancel any pending debounced analysis
        if uri in server._debounce_tasks:
            server._debounce_tasks[uri].cancel()
            del server._debounce_tasks[uri]
        server._pending_texts.pop(uri, None)

        # Remove document from manager
        server.document_manager.close_document(uri)

        # Clear diagnostics
        server.text_document_publish_diagnostics(
            PublishDiagnosticsParams(uri=uri, diagnostics=[])
        )
    except Exception as e:
        logger.error(f"Error in did_close: {e}", exc_info=True)


@server.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(
        trigger_characters=['.', ':', '?', '@', '$', '%', '>'],
        resolve_provider=False,
    ),
)
def completion(params: CompletionParams) -> CompletionList:
    """Handle completion request."""
    try:
        uri = params.text_document.uri
        position = params.position
        trigger = None

        # Get trigger character if available
        if params.context and params.context.trigger_character:
            trigger = params.context.trigger_character

        logger.debug(f"Completion requested at {uri}:{position.line}:{position.character}")

        # Get document analysis
        document = server.document_manager.get_document(uri)
        if not document:
            return CompletionList(is_incomplete=False, items=[])

        # Get completions
        return server.completion_provider.get_completions(document, position, trigger)
    except Exception as e:
        logger.error(f"Error in completion: {e}", exc_info=True)
        return CompletionList(is_incomplete=False, items=[])


@server.feature(
    TEXT_DOCUMENT_SIGNATURE_HELP,
    SignatureHelpOptions(
        trigger_characters=['(', ','],
        retrigger_characters=[','],
    ),
)
def signature_help(params: SignatureHelpParams) -> Optional[SignatureHelp]:
    """Handle signature help request."""
    try:
        uri = params.text_document.uri
        position = params.position
        trigger = None

        if params.context and params.context.trigger_character:
            trigger = params.context.trigger_character

        logger.debug(f"Signature help requested at {uri}:{position.line}:{position.character}")

        document = server.document_manager.get_document(uri)
        if not document:
            return None

        return server.signature_help_provider.get_signature_help(document, position, trigger)
    except Exception as e:
        logger.error(f"Error in signature_help: {e}", exc_info=True)
        return None


@server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: HoverParams) -> Optional[Hover]:
    """Handle hover request."""
    try:
        uri = params.text_document.uri
        position = params.position

        logger.debug(f"Hover requested at {uri}:{position.line}:{position.character}")

        # Get document analysis
        document = server.document_manager.get_document(uri)
        if not document:
            return None

        # Get hover info
        return server.hover_provider.get_hover(document, position)
    except Exception as e:
        logger.error(f"Error in hover: {e}", exc_info=True)
        return None


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(params: DefinitionParams) -> Optional[Location]:
    """Handle go-to-definition request."""
    try:
        uri = params.text_document.uri
        position = params.position

        logger.debug(f"Definition requested at {uri}:{position.line}:{position.character}")

        document = server.document_manager.get_document(uri)
        if not document:
            return None

        return server.definition_provider.get_definition(document, position)
    except Exception as e:
        logger.error(f"Error in definition: {e}", exc_info=True)
        return None


@server.feature(TEXT_DOCUMENT_REFERENCES)
def references(params: ReferenceParams) -> list:
    """Handle find references request."""
    try:
        uri = params.text_document.uri
        position = params.position
        include_declaration = params.context.include_declaration if params.context else True

        logger.debug(f"References requested at {uri}:{position.line}:{position.character}")

        document = server.document_manager.get_document(uri)
        if not document:
            return []

        return server.definition_provider.find_references(document, position, include_declaration)
    except Exception as e:
        logger.error(f"Error in references: {e}", exc_info=True)
        return []


def _publish_diagnostics(uri: str):
    """Publish diagnostics for a document."""
    try:
        logger.info(f"_publish_diagnostics called for {uri}")

        if not server.diagnostics_enabled:
            logger.info("Diagnostics are disabled")
            return

        # Get document analysis
        document = server.document_manager.get_document(uri)
        if not document:
            logger.warning(f"No document found for {uri}")
            return

        logger.info(f"Document found, version={document.version}, tokens={len(document.tokens)}")

        # Get diagnostics
        diagnostics = server.diagnostic_provider.get_diagnostics(document)
        logger.info(f"Generated {len(diagnostics)} diagnostics")

        # Limit number of problems
        if len(diagnostics) > server.max_problems:
            diagnostics = diagnostics[:server.max_problems]

        # Publish diagnostics using pygls method
        logger.info(f"Publishing {len(diagnostics)} diagnostics to client...")
        server.text_document_publish_diagnostics(
            PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics)
        )
        logger.info(f"Successfully published {len(diagnostics)} diagnostics for {uri}")
    except Exception as e:
        logger.error(f"Error publishing diagnostics: {e}", exc_info=True)


def main():
    """Main entry point for the CSSL Language Server."""
    parser = argparse.ArgumentParser(
        description='CSSL Language Server'
    )
    parser.add_argument(
        '--stdio',
        action='store_true',
        help='Use stdio for communication (default)'
    )
    parser.add_argument(
        '--tcp',
        action='store_true',
        help='Use TCP for communication'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='TCP host (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=2087,
        help='TCP port (default: 2087)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (verify setup and exit)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.test:
        # Test mode - verify everything works
        print("CSSL Language Server Test Mode")
        print("=" * 40)
        print("[OK] Server module loaded")
        print("[OK] Document manager initialized")
        print("[OK] Diagnostic provider initialized")
        print("[OK] Completion provider initialized")
        print("[OK] Hover provider initialized")
        print("[OK] Definition provider initialized")

        # Test parsing
        test_code = '''
int x = 42;
string name = "test";

define greet(string name) {
    printl("Hello, " + name);
}

greet(?name);
'''
        try:
            server.document_manager.update_document("test://test.cssl", test_code, 1)
            doc = server.document_manager.get_document("test://test.cssl")
            if doc:
                print("[OK] Document parsing works")

                # Test diagnostics
                diagnostics = server.diagnostic_provider.get_diagnostics(doc)
                print(f"[OK] Diagnostics: {len(diagnostics)} issues found")

                # Test completions
                from lsprotocol.types import Position
                completions = server.completion_provider.get_completions(
                    doc, Position(line=0, character=0), None
                )
                print(f"[OK] Completions: {len(completions.items)} items available")

                # Test hover
                hover_result = server.hover_provider.get_hover(
                    doc, Position(line=0, character=0)
                )
                print("[OK] Hover provider works")

                print("=" * 40)
                print("All tests passed! Server is ready.")
            else:
                print("[FAIL] Document parsing failed")
                sys.exit(1)
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        sys.exit(0)

    # Start server
    logger.info("Starting CSSL Language Server")
    sys.stderr.write("[DEBUG] Server starting - stderr output is working\n")
    sys.stderr.flush()

    # Verify feature registration before starting
    sys.stderr.write("[DEBUG] Checking feature registration before server start...\n")
    _verify_feature_registration()

    try:
        if args.tcp:
            logger.info(f"Listening on TCP {args.host}:{args.port}")
            server.start_tcp(args.host, args.port)
        else:
            logger.info("Using stdio communication")
            server.start_io()
    except Exception as e:
        debug_log(f"SERVER CRASHED: {e}")
        logger.error(f"Server crashed: {e}", exc_info=True)
        sys.stderr.write(f"[FATAL] Server crashed: {e}\n")
        import traceback
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()
        raise


if __name__ == '__main__':
    main()
