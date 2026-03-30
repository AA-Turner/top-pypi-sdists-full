import flask

from abstra_internals.controllers.language_server import (
    SEMANTIC_TOKEN_MODIFIERS,
    SEMANTIC_TOKEN_TYPES,
    TextDocumentContext,
    get_cached_diagnostics,
    get_completions,
    get_definition,
    get_diagnostics,
    get_document_highlights,
    get_hover,
    get_references,
    get_rename_edits,
    get_semantic_tokens,
    get_signature_help,
    get_status,
    read_external_file,
)


class RenameContext(TextDocumentContext):
    new_name: str = ""


def get_editor_bp():
    bp = flask.Blueprint("editor_language_server", __name__)

    @bp.post("/completion")
    def completion():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        items = get_completions(ctx.code, ctx.position.line, ctx.position.character)
        # Piggyback cached diagnostics — avoids separate /diagnostics call
        return {"items": items, "diagnostics": get_cached_diagnostics()}

    @bp.post("/hover")
    def hover():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        result = get_hover(ctx.code, ctx.position.line, ctx.position.character)
        return result or {}

    @bp.post("/definition")
    def definition():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        result = get_definition(ctx.code, ctx.position.line, ctx.position.character)
        return result or {}

    @bp.post("/references")
    def references():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        return get_references(ctx.code, ctx.position.line, ctx.position.character)

    @bp.post("/document-highlight")
    def document_highlight():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        return get_document_highlights(
            ctx.code, ctx.position.line, ctx.position.character
        )

    @bp.post("/signature-help")
    def signature_help():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        result = get_signature_help(ctx.code, ctx.position.line, ctx.position.character)
        return result or {}

    @bp.post("/rename")
    def rename():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = RenameContext(**flask.request.json)
        result = get_rename_edits(
            ctx.code, ctx.position.line, ctx.position.character, ctx.new_name
        )
        return result or {}

    @bp.post("/semantic-tokens")
    def semantic_tokens():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        result = get_semantic_tokens(ctx.code)
        return {
            "data": result.get("data", []) if result else [],
            "legend": {
                "tokenTypes": SEMANTIC_TOKEN_TYPES,
                "tokenModifiers": SEMANTIC_TOKEN_MODIFIERS,
            },
        }

    @bp.post("/read-file")
    def read_file():
        if flask.request.json is None:
            return flask.abort(400)
        uri = flask.request.json.get("uri", "")
        content = read_external_file(uri)
        if content is None:
            return flask.abort(404)
        return {"content": content}

    @bp.get("/status")
    def status():
        return get_status()

    @bp.post("/diagnostics")
    def diagnostics():
        if flask.request.json is None:
            return flask.abort(400)
        ctx = TextDocumentContext(**flask.request.json)
        return get_diagnostics(ctx.code)

    return bp
