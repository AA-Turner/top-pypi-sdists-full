import flask

from abstra_internals.controllers.file_locks import FileLockController
from abstra_internals.repositories.factory import Repositories
from abstra_internals.server.guards.file_lock_guard import (
    current_editor_user as _current_user,
)


def get_editor_bp(repos: Repositories):
    bp = flask.Blueprint("editor_locks", __name__)
    del repos

    @bp.get("")
    def _list_locks():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        locks = [s.to_dict() for s in FileLockController.get_all_locks()]
        return flask.jsonify({"locks": locks})

    @bp.post("/acquire")
    def _acquire_lock():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        email, name = identity

        body = flask.request.get_json(silent=True) or {}
        file_path = body.get("filePath")
        session_id = body.get("sessionId")
        if not isinstance(file_path, str) or not isinstance(session_id, str):
            return flask.make_response(
                {"error": "filePath and sessionId are required"}, 400
            )

        granted, holder = FileLockController.acquire(
            file_path=file_path,
            session_id=session_id,
            email=email,
            name=name,
        )
        return flask.jsonify(
            {
                "granted": granted,
                "holder": holder.to_dict() if holder is not None else None,
            }
        )

    @bp.post("/release")
    def _release_lock():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        email, _ = identity

        body = flask.request.get_json(silent=True) or {}
        file_path = body.get("filePath")
        session_id = body.get("sessionId")
        if not isinstance(file_path, str) or not isinstance(session_id, str):
            return flask.make_response(
                {"error": "filePath and sessionId are required"}, 400
            )

        released = FileLockController.release(
            file_path=file_path,
            session_id=session_id,
            email=email,
        )
        return flask.jsonify({"released": released})

    @bp.post("/heartbeat")
    def _heartbeat_lock():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        email, _ = identity

        body = flask.request.get_json(silent=True) or {}
        file_path = body.get("filePath")
        session_id = body.get("sessionId")
        if not isinstance(file_path, str) or not isinstance(session_id, str):
            return flask.make_response(
                {"error": "filePath and sessionId are required"}, 400
            )

        still_held, lock = FileLockController.heartbeat_lock(
            file_path=file_path,
            session_id=session_id,
            email=email,
        )
        return flask.jsonify(
            {
                "stillHeld": still_held,
                "lock": lock.to_dict() if lock is not None else None,
            }
        )

    @bp.get("/presence")
    def _list_presence():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        users = [s.to_dict() for s in FileLockController.get_all_presence()]
        return flask.jsonify({"users": users})

    @bp.post("/presence/heartbeat")
    def _heartbeat_presence():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)
        email, name = identity

        body = flask.request.get_json(silent=True) or {}
        session_id = body.get("sessionId")
        current_file_path = body.get("currentFilePath")
        if not isinstance(session_id, str):
            return flask.make_response({"error": "sessionId is required"}, 400)
        if current_file_path is not None and not isinstance(current_file_path, str):
            return flask.make_response(
                {"error": "currentFilePath must be a string or null"}, 400
            )

        FileLockController.update_presence(
            session_id=session_id,
            email=email,
            name=name,
            current_file_path=current_file_path,
        )
        return flask.jsonify({"ok": True})

    @bp.post("/presence/leave")
    def _leave_presence():
        identity = _current_user()
        if identity is None:
            return flask.make_response({"error": "Unauthorized"}, 401)

        body = flask.request.get_json(silent=True) or {}
        session_id = body.get("sessionId")
        if not isinstance(session_id, str):
            return flask.make_response({"error": "sessionId is required"}, 400)

        FileLockController.remove_presence(session_id)
        return flask.jsonify({"ok": True})

    return bp
