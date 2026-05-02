"""HTTP client — registers, sends event batches, forces seal. Zero deps."""

import json
import ssl
import socket
import urllib.request
import urllib.error


API_URL = "https://api.ghostlogic.tech"


def _ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _post(url: str, body: dict, key: str = "") -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "GhostLogic-Demo/0.2.0")
    if key:
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("X-API-Key", key)
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"status": "error", "http_code": e.code, "detail": body_text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def register(base_url: str = API_URL) -> str:
    """Auto-register with Blackbox, return API key."""
    hostname = socket.gethostname()
    url = f"{base_url.rstrip('/')}/api/v1/register"
    resp = _post(url, {"name": f"demo:{hostname}", "agent_id": "ghostlogic-demo"})
    key = resp.get("api_key", "")
    if not key:
        detail = resp.get("detail", resp.get("error", "unknown"))
        raise RuntimeError(f"Registration failed: {detail}")
    return key


def send_batch(base_url: str, key: str, events: list[dict], source_id: str = "ghostlogic-demo") -> dict:
    """POST events to /api/v1/ingest."""
    url = f"{base_url.rstrip('/')}/api/v1/ingest"
    return _post(url, {
        "events": events,
        "source_id": source_id,
        "endpoint_name": "demo-breach-replay",
    }, key)


def force_seal(base_url: str, key: str) -> dict:
    """POST to /api/v1/seal — force immediate capsule seal."""
    url = f"{base_url.rstrip('/')}/api/v1/seal"
    return _post(url, {}, key)


def get_capsules(base_url: str, key: str) -> dict:
    """GET /api/v1/capsules — list all capsules."""
    url = f"{base_url.rstrip('/')}/api/v1/capsules"
    return _get(url, key)


def investigate(base_url: str, key: str, capsule_id: str) -> dict:
    """POST /api/v1/investigate — trigger investigation on a capsule."""
    url = f"{base_url.rstrip('/')}/api/v1/investigate"
    return _post(url, {"capsule_id": capsule_id}, key)


def get_investigation(base_url: str, key: str, capsule_id: str) -> dict:
    """GET /api/v1/investigate/{capsule_id} — poll investigation status."""
    url = f"{base_url.rstrip('/')}/api/v1/investigate/{capsule_id}"
    return _get(url, key)


def list_investigations(base_url: str, key: str) -> dict:
    """GET /api/v1/investigations — list all investigations."""
    url = f"{base_url.rstrip('/')}/api/v1/investigations"
    return _get(url, key)


def run_arbitrator(base_url: str, key: str, payload: dict) -> dict:
    """POST /api/v1/arbitrator/decide — run settlement engine."""
    url = f"{base_url.rstrip('/')}/api/v1/arbitrator/decide"
    return _post(url, payload, key)


def _get(url: str, key: str) -> dict:
    """Generic GET with auth."""
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "GhostLogic-Demo/1.0.0")
    if key:
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("X-API-Key", key)
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"status": "error", "http_code": e.code, "detail": body_text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
