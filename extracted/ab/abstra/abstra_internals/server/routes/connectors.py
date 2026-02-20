import flask
import requests as req

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorConnectorsSchemaResponseItem,
    CloudApiCliConnectorsConnectionsResponseItem,
)
from abstra_internals.credentials import resolve_headers
from abstra_internals.environment import (
    CLOUD_API_CLI_URL,
    CLOUD_API_ENDPOINT,
    REQUEST_TIMEOUT,
)


def get_editor_bp() -> flask.Blueprint:
    bp = flask.Blueprint("connectors", __name__)

    @bp.get("/schema")
    def _connectors_schema():
        try:
            url = f"{CLOUD_API_ENDPOINT}/public/connectors/schema"
            res = req.get(url, timeout=REQUEST_TIMEOUT)
            res.raise_for_status()
            items = [
                AbstraLibApiEditorConnectorsSchemaResponseItem.from_dict(item)
                for item in res.json()
            ]
            return flask.jsonify([item.to_dict() for item in items])
        except Exception:
            return flask.jsonify([])

    @bp.get("/connections")
    def _list_connections():
        try:
            url = f"{CLOUD_API_CLI_URL}/connectors/connections"
            headers = resolve_headers()
            res = req.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            res.raise_for_status()
            items = [
                CloudApiCliConnectorsConnectionsResponseItem.from_dict(item)
                for item in res.json()
            ]
            return flask.jsonify([item.to_dict() for item in items])
        except Exception:
            return flask.jsonify([])

    @bp.get("/connection/<connection_name>/actions")
    def _list_connection_actions(connection_name: str):
        try:
            url = f"{CLOUD_API_CLI_URL}/connectors/connection/{connection_name}/actions"
            headers = resolve_headers()
            params = {
                "page": flask.request.args.get("page", "0"),
                "pageSize": flask.request.args.get("pageSize", "10000"),
                "search": flask.request.args.get("search", ""),
            }
            res = req.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            res.raise_for_status()
            return flask.jsonify(res.json())
        except Exception:
            return flask.jsonify({"data": [], "pageSize": 0, "page": 0})

    @bp.get("/connection/<connection_name>/action/<action_name>")
    def _get_action_details(connection_name: str, action_name: str):
        try:
            url = f"{CLOUD_API_CLI_URL}/connectors/connection/{connection_name}/action/{action_name}"
            headers = resolve_headers()
            res = req.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            res.raise_for_status()
            return flask.jsonify(res.json())
        except Exception:
            return flask.jsonify({}), 404

    return bp
