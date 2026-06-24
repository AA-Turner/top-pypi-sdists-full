import logging

import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiAiStreamRequest,
    CloudApiCliAiV2QueueClearRequest,
    CloudApiCliAiV2QueuePostRequest,
    CloudApiCliAiV2QueueRemoveRequest,
)
from abstra_internals.controllers.ai import AiController, InvalidUploadPathError
from abstra_internals.controllers.main import MainController
from abstra_internals.usage import editor_usage

MAX_AI_UPLOAD_SIZE = 300 * 1024 * 1024  # 300MB, matches cloud-api
MAX_AI_UPLOAD_LABEL = "300MB"

logger = logging.getLogger(__name__)


def get_editor_bp(main_controller: MainController):
    bp = flask.Blueprint("editor_ai", __name__)
    controller = AiController(main_controller)

    def _get_user_jwt():
        return flask.request.cookies.get("editor_auth")

    @bp.post("/stream")
    @editor_usage
    def _get_next_message():
        body = flask.request.json
        if not body:
            flask.abort(400)

        body = AbstraLibApiAiStreamRequest.from_dict(body)

        streamer = controller.send_ai_message(body, user_jwt=_get_user_jwt())

        if streamer is None:
            flask.abort(403)

        return flask.Response(streamer, mimetype="text/event-stream")

    @bp.post("/abort")
    @editor_usage
    def _abort():
        body = flask.request.json
        if not body:
            flask.abort(400)
        thread_id = body.get("langGraphThreadId")
        if not thread_id:
            flask.abort(400)
        controller.abort_thread(thread_id, user_jwt=_get_user_jwt())
        return {"success": True}

    @bp.get("/history")
    @editor_usage
    def _get_history():
        limit = flask.request.args.get("limit")
        limit = int(limit) if limit else 10
        offset = flask.request.args.get("offset")
        offset = int(offset) if offset else 0
        summary = flask.request.args.get("summary") == "true"
        conversation_id = flask.request.args.get("conversationId")
        threads = controller.get_history(
            limit,
            offset,
            summary=summary,
            conversation_id=conversation_id,
            user_jwt=_get_user_jwt(),
        )
        if threads is None:
            flask.abort(403)
        return threads

    @bp.post("/thread")
    @editor_usage
    def _create_thread():
        thread = controller.create_thread(user_jwt=_get_user_jwt())
        if not thread:
            flask.abort(403)
        return thread.to_dict()

    @bp.delete("/thread/<thread_id>")
    @editor_usage
    def _delete_thread(thread_id: str):
        """
        Delete a conversation thread.
        """
        controller.delete_thread(thread_id, user_jwt=_get_user_jwt())
        return {"success": True}

    @bp.post("/compact")
    @editor_usage
    def _compact_conversation():
        body = flask.request.json
        if not body:
            flask.abort(400)
        conversation_id = body.get("conversationId")
        if not conversation_id:
            flask.abort(400)
        result = controller.compact_conversation(
            conversation_id, user_jwt=_get_user_jwt()
        )
        if result is None:
            flask.abort(403)
        return flask.jsonify(result)

    @bp.post("/queue")
    @editor_usage
    def _queue_message():
        body = flask.request.json
        if not body:
            flask.abort(400)
        try:
            request = CloudApiCliAiV2QueuePostRequest.from_dict(body)
        except (KeyError, TypeError, ValueError):
            flask.abort(400)
        result = controller.queue_message(request, user_jwt=_get_user_jwt())
        if result is None:
            flask.abort(403)
        return flask.jsonify(result)

    @bp.get("/queue")
    @editor_usage
    def _list_queued_messages():
        conversation_id = flask.request.args.get("conversationId")
        if not conversation_id:
            flask.abort(400)
        result = controller.list_queued_messages(
            conversation_id, user_jwt=_get_user_jwt()
        )
        if result is None:
            flask.abort(403)
        return flask.jsonify(result)

    @bp.post("/queue/remove")
    @editor_usage
    def _remove_queued_message():
        body = flask.request.json
        if not body:
            flask.abort(400)
        try:
            request = CloudApiCliAiV2QueueRemoveRequest.from_dict(body)
        except (KeyError, TypeError, ValueError):
            flask.abort(400)
        result = controller.remove_queued_message(request, user_jwt=_get_user_jwt())
        if result is None:
            flask.abort(403)
        return "", 204

    @bp.post("/queue/clear")
    @editor_usage
    def _clear_queued_messages():
        body = flask.request.json
        if not body:
            flask.abort(400)
        try:
            request = CloudApiCliAiV2QueueClearRequest.from_dict(body)
        except (KeyError, TypeError, ValueError):
            flask.abort(400)
        result = controller.clear_queued_messages(request, user_jwt=_get_user_jwt())
        if result is None:
            flask.abort(403)
        return "", 204

    @bp.post("/start-conversation")
    def _start_conversation():
        """
        Start a new conversation with the AI.
        """
        conversation = controller.start_conversation(user_jwt=_get_user_jwt())
        if not conversation:
            flask.abort(403)
        return conversation

    @bp.post("/upload")
    @editor_usage
    def _upload_attachment():
        content_length = flask.request.content_length
        if content_length is not None and content_length > MAX_AI_UPLOAD_SIZE:
            return (
                flask.jsonify({"error": f"File too large (max {MAX_AI_UPLOAD_LABEL})"}),
                413,
            )
        file = flask.request.files.get("file")
        conversation_id = flask.request.form.get("conversationId")
        if file is None or not conversation_id:
            return (
                flask.jsonify({"error": "file and conversationId are required"}),
                400,
            )
        try:
            return controller.save_uploaded_file(file, conversation_id)
        except Exception:
            logger.exception("[ai/upload] Failed to save attachment")
            return flask.jsonify({"error": "Failed to save attachment"}), 500

    @bp.delete("/upload")
    @editor_usage
    def _delete_attachment():
        body = flask.request.json
        if not body:
            return flask.jsonify({"error": "filePath is required"}), 400
        file_path = body.get("filePath")
        if not file_path:
            return flask.jsonify({"error": "filePath is required"}), 400
        try:
            controller.delete_uploaded_file(file_path)
        except InvalidUploadPathError:
            return flask.jsonify({"error": "Invalid path"}), 400
        except Exception:
            logger.exception("[ai/upload] Failed to delete attachment")
            return flask.jsonify({"error": "Failed to delete attachment"}), 500
        return {"success": True}

    return bp
