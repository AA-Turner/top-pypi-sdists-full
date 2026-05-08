#!/usr/bin/env python3
"""
Mock Monte Carlo server for airflow-mcd e2e testing.

Captures GraphQL callbacks from airflow-mcd and exposes verification endpoints:
  GET /health           - liveness probe
  GET /callbacks        - all captured payloads (JSON)
  GET /verify           - structured pass/fail report with expected DAG run URLs
  DELETE /callbacks     - reset captured state between test runs
"""

import json
import threading
from urllib.parse import quote
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_captured: list[dict] = []
_lock = threading.Lock()


# ---------------------------------------------------------------------------
# URL-generation logic — mirrors monolith's AirflowService._is_airflow_3()
# and _get_urls() dag_run_url branch.  Keep in sync with service.py.
# ---------------------------------------------------------------------------

def _is_airflow_3(version: str | None) -> bool:
    """
    Returns True only when version is a dot-separated semver whose major is ≥ 3.
    A bare integer like "3" (GCP Composer MAJOR_VERSION) returns False — conservative.
    """
    if not version:
        return False
    parts = version.split(".")
    try:
        return int(parts[0]) >= 3 and len(parts) > 1
    except (ValueError, IndexError):
        return False


def _expected_dag_run_url_path(dag_id: str, run_id: str, version: str | None) -> str:
    if _is_airflow_3(version):
        return f"/dags/{dag_id}/runs/{run_id}"
    else:
        return f"/dags/{dag_id}/graph?run_id={quote(run_id, safe='')}"


# ---------------------------------------------------------------------------
# Payload extraction helpers
# ---------------------------------------------------------------------------

def _extract_gql_operation(query: str) -> str | None:
    """Best-effort: find the MC operation name inside the GQL mutation string."""
    for snake, camel in (
        ("upload_airflow_dag_result", "uploadAirflowDagResult"),
        ("upload_airflow_task_result", "uploadAirflowTaskResult"),
        ("upload_airflow_sla_misses", "uploadAirflowSlaMisses"),
    ):
        if camel in query or snake in query:
            return snake
    return None


def _parse_gql_body(data: dict) -> dict:
    """
    pycarlo sends GraphQL with the full result in variables.payload.
    The env (including version) lives in variables.payload.env.
    """
    variables = data.get("variables") or {}
    payload = variables.get("payload") or {}
    return {
        "operation": _extract_gql_operation(data.get("query", "")),
        "dag_id": payload.get("dag_id"),
        "run_id": payload.get("run_id"),
        "env": payload.get("env") or {},
        "success": payload.get("success"),
        "raw_payload": payload,
    }


def _parse_igw_body(data: dict) -> dict:
    """
    Integration-gateway path sends a flat JSON body with airflow_payload nested.
    """
    airflow_payload = data.get("airflow_payload") or {}
    return {
        "operation": data.get("airflow_operation"),
        "dag_id": airflow_payload.get("dag_id"),
        "run_id": airflow_payload.get("run_id"),
        "env": airflow_payload.get("env") or {},
        "success": airflow_payload.get("success"),
        "raw_payload": airflow_payload,
    }


# ---------------------------------------------------------------------------
# Verification logic
# ---------------------------------------------------------------------------

def _verify() -> dict:
    with _lock:
        callbacks = list(_captured)

    if not callbacks:
        return {
            "passed": False,
            "error": "No callbacks captured yet — has a DAG run completed?",
            "results": [],
            "total_callbacks": 0,
        }

    # Prefer dag-result callbacks; supplement with task-result callbacks for any Airflow
    # version not already represented.  This handles the Airflow 3.0 upstream bug where
    # dag-processor passes an empty context (TODO in dag_processing/processor.py) so
    # dag-level on_success/on_failure callbacks never fire — task callbacks carry the same
    # env/version payload and are sufficient for verification.
    dag_results = [c for c in callbacks if c.get("operation") == "upload_airflow_dag_result"]
    task_results = [c for c in callbacks if c.get("operation") == "upload_airflow_task_result"]

    # Collect the set of (major) versions already covered by dag results.
    dag_result_versions = {(c.get("env") or {}).get("version") for c in dag_results}

    # Supplement: add task-result callbacks whose version is not yet represented.
    combined = list(dag_results)
    for cb in task_results:
        if (cb.get("env") or {}).get("version") not in dag_result_versions:
            combined.append(cb)

    if not combined:
        return {
            "passed": False,
            "error": "No DAG-result or task-result callbacks captured yet.",
            "all_operations": [c.get("operation") for c in callbacks],
            "results": [],
            "total_callbacks": len(callbacks),
        }

    # De-duplicate by (dag_id, run_id, version) — task callbacks fire multiple times per run.
    seen: set[tuple] = set()
    deduped: list[dict] = []
    for cb in combined:
        key = (cb.get("dag_id"), cb.get("run_id"), (cb.get("env") or {}).get("version"))
        if key not in seen:
            seen.add(key)
            deduped.append(cb)
    dag_callbacks = deduped

    results = []
    for cb in dag_callbacks:
        env = cb.get("env") or {}
        version = env.get("version")
        dag_id = cb.get("dag_id") or "unknown"
        run_id = cb.get("run_id") or "unknown"
        is_v3 = _is_airflow_3(version)
        expected_path = _expected_dag_run_url_path(dag_id, run_id, version)

        results.append({
            "dag_id": dag_id,
            "run_id": run_id,
            "version_received": version,
            "is_airflow_3": is_v3,
            "expected_dag_run_url_path": expected_path,
            "url_format": "Airflow 3 (runs/)" if is_v3 else "Airflow 2 (graph?run_id=)",
        })

    v2 = [r for r in results if not r["is_airflow_3"]]
    v3 = [r for r in results if r["is_airflow_3"]]

    checks = {
        "airflow2_callback_received": bool(v2),
        "airflow3_callback_received": bool(v3),
        "airflow2_uses_graph_url": all("/graph?run_id=" in r["expected_dag_run_url_path"] for r in v2) if v2 else False,
        "airflow3_uses_runs_url": all("/runs/" in r["expected_dag_run_url_path"] for r in v3) if v3 else False,
    }
    passed = all(checks.values())

    return {
        "passed": passed,
        "checks": checks,
        "results": results,
        "total_callbacks": len(callbacks),
        "dag_callbacks": len(dag_callbacks),
    }


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class MockMCHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter logs
        ts = datetime.now(tz=timezone.utc).strftime("%H:%M:%S")
        print(f"[mock {ts}] {fmt % args}", flush=True)

    # ---- GET ---------------------------------------------------------------

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "ok", "captured": len(_captured)})
        elif self.path == "/callbacks":
            with _lock:
                self._json(200, _captured)
        elif self.path == "/verify":
            result = _verify()
            self._json(200 if result["passed"] else 206, result)
        else:
            self._json(404, {"error": "not found"})

    def do_DELETE(self):
        if self.path == "/callbacks":
            with _lock:
                _captured.clear()
            self._json(200, {"cleared": True})
        else:
            self._json(404, {"error": "not found"})

    # ---- POST --------------------------------------------------------------

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}

        # Determine which callback path this is
        if self.path == "/airflow/callbacks":
            entry = _parse_igw_body(data)
            response = {"success": True, "resource_ids": ["e2e-mock-resource-id"]}
        else:
            # /graphql or any other path — assume GQL
            entry = _parse_gql_body(data)
            response = {"data": {
                "uploadAirflowDagResult": {"ok": True},
                "uploadAirflowTaskResult": {"ok": True},
                "uploadAirflowSlaMisses": {"ok": True},
            }}

        entry["path"] = self.path
        entry["timestamp"] = datetime.now(tz=timezone.utc).isoformat()

        with _lock:
            _captured.append(entry)

        version = (entry.get("env") or {}).get("version", "<none>")
        print(
            f"[mock] captured operation={entry.get('operation')} "
            f"dag_id={entry.get('dag_id')} version={version}",
            flush=True,
        )

        self._json(200, response)

    # ---- helpers -----------------------------------------------------------

    def _json(self, status: int, body):
        encoded = json.dumps(body, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    addr = ("0.0.0.0", 8080)
    server = ThreadingHTTPServer(addr, MockMCHandler)
    print(f"[mock] Listening on {addr[0]}:{addr[1]}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[mock] Shutting down", flush=True)
