"""Grail phase #2 STEP 3 — the repoint: CLI brain-write goes to the unified brain via the bearer route
(_brain_route_push → POST /api/brain/cli-write with the device-flow token), off the retired tiyon token.

Run: python3 nx/cli/tests/test_brain_repoint.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli
import requests

_VALID = ("concept", "source", "returning_question", "decision", "contradiction", "current_edge", "pattern")


class _Resp:
    def __init__(self, status, body):
        self.status_code = status
        self._body = body

    def json(self):
        return self._body


def _patch(fn):
    orig = requests.post
    requests.post = fn
    return orig


def test_success_posts_mapped_body_with_device_token():
    calls = []

    def ok_post(url, json=None, headers=None, timeout=None):
        calls.append((url, json, headers))
        return _Resp(200, {"ok": True, "node": {"id": "n1"}})

    orig = _patch(ok_post)
    try:
        r = nx_cli._brain_route_push(
            {"token": "dev-tok"}, "Acme signed the pilot", "Acme pilot", "sales", "nx_brain", {"deal": "d1"})
    finally:
        requests.post = orig
    assert r is True
    url, body, hdr = calls[-1]
    assert url.endswith("/api/brain/cli-write")               # the unified-brain route on the baked backend base
    assert hdr["Authorization"] == "Bearer dev-tok"           # DEVICE-flow token, not the retired tiyon nx_token
    assert body["label"] == "Acme pilot"
    assert body["payload"]["content"] == "Acme signed the pilot"
    assert body["payload"]["world"] == "sales"
    assert body["sourceAttribution"]["sourceKind"] == "nx-cli"
    assert "sourceWorld" not in body                          # route defaults source_world='cli' (CLI provenance)
    assert body["nodeType"] in _VALID


def test_not_signed_in_never_posts():
    calls = []
    orig = _patch(lambda *a, **k: (calls.append(1), _Resp(200, {"ok": True}))[1])
    try:
        assert nx_cli._brain_route_push({}, "x", "x", "", "nx_brain", {}) is False   # no token
    finally:
        requests.post = orig
    assert not calls


def test_server_not_ok_and_non_200_return_false():
    orig = _patch(lambda *a, **k: _Resp(200, {"ok": False, "blocked": True}))   # sealed / blocked
    try:
        assert nx_cli._brain_route_push({"token": "t"}, "x", "x", "", "nx_brain", {}) is False
    finally:
        requests.post = orig
    orig = _patch(lambda *a, **k: _Resp(503, {}))                                # server down
    try:
        assert nx_cli._brain_route_push({"token": "t"}, "x", "x", "", "nx_brain", {}) is False
    finally:
        requests.post = orig


if __name__ == "__main__":
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        fn(); print(f"  ✓ {name}")
    print("ALL BRAIN-REPOINT PROOFS PASS")
