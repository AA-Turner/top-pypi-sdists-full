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
import argparse
from typing import Optional

from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_REFERENCES,
    INITIALIZE,
    INITIALIZED,
    SHUTDOWN,
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
    InitializeParams,
    InitializeResult,
    Location,
    MessageType,
    Position,
    PublishDiagnosticsParams,
    ReferenceParams,
    ServerCapabilities,
    TextDocumentSyncKind,
    TextDocumentSyncOptions,
)

from pygls.lsp.server import LanguageServer

from .analysis.document_manager import DocumentManager
from .analysis.diagnostic_provider import DiagnosticProvider
from .providers.completion_provider import CompletionProvider
from .providers.hover_provider import HoverProvider
from .providers.definition_provider import DefinitionProvider


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

    def __init__(self):
        super().__init__(
            name='cssl-language-server',
            version='2.0.0'
        )

        # Initialize components
        self.document_manager = DocumentManager()
        self.diagnostic_provider = DiagnosticProvider()
        self.completion_provider = CompletionProvider()
        self.hover_provider = HoverProvider()
        self.definition_provider = DefinitionProvider()

        # Configuration
        self.diagnostics_enabled = True
        self.max_problems = 100

        logger.info("CSSL Language Server initialized")


# Create server instance
server = CSSLLanguageServer()


def _verify_feature_registration():
    """Debug function to verify features are registered correctly."""
    debug_log("_verify_feature_registration called")
    try:
        # Access the feature manager through the server's lsp protocol
        if hasattr(server, 'lsp') and hasattr(server.lsp, 'fm'):
            features = list(server.lsp.fm.features.keys())
            debug_log(f"Features registered: {features}")
            sys.stderr.write(f"[DEBUG] User features registered: {features}\n")
            sys.stderr.flush()

            # Specifically check for did_change
            if TEXT_DOCUMENT_DID_CHANGE in server.lsp.fm.features:
                debug_log("TEXT_DOCUMENT_DID_CHANGE IS registered!")
                sys.stderr.write(f"[DEBUG] TEXT_DOCUMENT_DID_CHANGE IS registered!\n")
            else:
                debug_log("WARNING: TEXT_DOCUMENT_DID_CHANGE is NOT registered!")
                sys.stderr.write(f"[DEBUG] WARNING: TEXT_DOCUMENT_DID_CHANGE is NOT registered!\n")
            sys.stderr.flush()
        else:
            debug_log("Cannot access feature manager")
            sys.stderr.write("[DEBUG] Cannot access feature manager (server not fully initialized)\n")
            sys.stderr.flush()
    except Exception as e:
        debug_log(f"Error checking features: {e}")
        sys.stderr.write(f"[DEBUG] Error checking features: {e}\n")
        sys.stderr.flush()


@server.feature(INITIALIZE)
def lsp_initialize(params: InitializeParams) -> InitializeResult:
    """Handle initialize request."""
    logger.info(f"Initializing CSSL Language Server for workspace: {params.root_uri}")

    # Read client configuration if provided
    if params.initialization_options:
        opts = params.initialization_options
        if isinstance(opts, dict):
            server.diagnostics_enabled = opts.get('diagnostics', {}).get('enabled', True)
            server.max_problems = opts.get('diagnostics', {}).get('maxProblems', 100)

    return InitializeResult(
        capabilities=ServerCapabilities(
            # Text document sync
            text_document_sync=TextDocumentSyncOptions(
                open_close=True,
                change=TextDocumentSyncKind.Full,
                save=True
            ),
            # Completion
            completion_provider=CompletionOptions(
                trigger_characters=['.', ':', '?', '@', '$', '%'],
                resolve_provider=False
            ),
            # Hover
            hover_provider=True,
            # Definition
            definition_provider=True,
            # References
            references_provider=True,
        ),
        server_info={
            'name': 'CSSL Language Server',
            'version': '2.0.0'
        }
    )


@server.feature(INITIALIZED)
def lsp_initialized(params):
    """Handle initialized notification."""
    logger.info("CSSL Language Server fully initialized")
    # Verify feature registration at runtime
    _verify_feature_registration()
    sys.stderr.write("[DEBUG] Server fully initialized, ready for document events\n")
    sys.stderr.flush()


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams):
    """Handle document open."""
    debug_log("=== DID_OPEN HANDLER CALLED ===")
    try:
        uri = params.text_document.uri
        text = params.text_document.text
        version = params.text_document.version

        debug_log(f"did_open: uri={uri}, version={version}, len={len(text)}")
        logger.info(f"Document opened: {uri}")

        # Update document in manager
        server.document_manager.update_document(uri, text, version)

        # Publish diagnostics
        _publish_diagnostics(uri)
    except Exception as e:
        logger.error(f"Error in did_open: {e}", exc_info=True)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams):
    """Handle document change - triggers live diagnostics."""
    # Write to debug log file (bypasses stdio completely)
    debug_log("=== DID_CHANGE HANDLER CALLED ===")

    # Use sys.stderr.write directly to bypass any logging issues
    sys.stderr.write("\n=== DID_CHANGE HANDLER REACHED ===\n")
    sys.stderr.flush()
    logger.info("=== did_change CALLED ===")
    try:
        uri = params.text_document.uri
        version = params.text_document.version
        logger.info(f"URI: {uri}, version: {version}")

        # Get the new text (full sync mode)
        if params.content_changes:
            text = params.content_changes[0].text
            logger.info(f"Got text content: {len(text)} chars")
        else:
            logger.warning(f"No content changes in did_change for {uri}")
            return

        logger.info(f"Document changed: {uri} (version {version}, {len(text)} chars)")

        # Update document in manager
        logger.info("Updating document in manager...")
        server.document_manager.update_document(uri, text, version)
        logger.info("Document updated successfully")

        # Publish diagnostics immediately for live updates
        logger.info("Calling _publish_diagnostics...")
        _publish_diagnostics(uri)
        logger.info("=== did_change COMPLETE ===")
    except Exception as e:
        logger.error(f"Error in did_change: {e}", exc_info=True)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(params: DidSaveTextDocumentParams):
    """Handle document save."""
    uri = params.text_document.uri

    logger.debug(f"Document saved: {uri}")

    # Re-publish diagnostics on save
    _publish_diagnostics(uri)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: DidCloseTextDocumentParams):
    """Handle document close."""
    uri = params.text_document.uri

    logger.debug(f"Document closed: {uri}")

    # Remove document from manager
    server.document_manager.close_document(uri)

    # Clear diagnostics
    server.text_document_publish_diagnostics(
        PublishDiagnosticsParams(uri=uri, diagnostics=[])
    )


@server.feature(TEXT_DOCUMENT_COMPLETION)
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
    uri = params.text_document.uri
    position = params.position

    logger.debug(f"Definition requested at {uri}:{position.line}:{position.character}")

    # Get document analysis
    document = server.document_manager.get_document(uri)
    if not document:
        return None

    # Get definition
    return server.definition_provider.get_definition(document, position)


@server.feature(TEXT_DOCUMENT_REFERENCES)
def references(params: ReferenceParams) -> list:
    """Handle find references request."""
    uri = params.text_document.uri
    position = params.position
    include_declaration = params.context.include_declaration if params.context else True

    logger.debug(f"References requested at {uri}:{position.line}:{position.character}")

    # Get document analysis
    document = server.document_manager.get_document(uri)
    if not document:
        return []

    # Get references
    return server.definition_provider.find_references(document, position, include_declaration)


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

    if args.tcp:
        logger.info(f"Listening on TCP {args.host}:{args.port}")
        server.start_tcp(args.host, args.port)
    else:
        logger.info("Using stdio communication")
        server.start_io()


if __name__ == '__main__':
    main()
