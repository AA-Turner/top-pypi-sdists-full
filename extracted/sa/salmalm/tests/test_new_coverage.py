import os
import io
import json
import uuid
import zipfile

import pytest
from fastapi.testclient import TestClient

# Ensure writable test home before salmalm imports/constants resolution.
os.environ.setdefault("SALMALM_HOME", "/tmp/salmalm_new_cov_home")
os.environ.setdefault("SALMALM_VAULT_PW", "testpass")

from salmalm.web.app import app
from salmalm.web.auth import auth_manager

client = TestClient(app, raise_server_exceptions=False)


def _auth_headers(role: str = "user"):
    username = f"cov_{role}_{uuid.uuid4().hex[:10]}"
    user = auth_manager.create_user(username, "password123", role)
    token = auth_manager.create_token(user)
    return {"Authorization": f"Bearer {token}"}, user


# --- salmalm/web/routes/web_files.py ---

def test_web_files_uploads_not_found_404():
    r = client.get("/uploads/definitely_missing_file.xyz")
    assert r.status_code == 404


def test_web_files_uploads_happy_path_200(tmp_path, monkeypatch):
    from salmalm import constants

    monkeypatch.setattr(constants, "WORKSPACE_DIR", tmp_path)
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    f = upload_dir / "hello.txt"
    f.write_text("hello", encoding="utf-8")

    r = client.get("/uploads/hello.txt")
    assert r.status_code == 200
    assert r.text == "hello"
    assert "etag" in {k.lower(): v for k, v in r.headers.items()}


def test_web_files_agent_export_auth_and_role():
    r_unauth = client.get("/api/agent/export")
    assert r_unauth.status_code == 401

    user_headers, _ = _auth_headers("user")
    r_forbidden = client.get("/api/agent/export?vault=1", headers=user_headers)
    assert r_forbidden.status_code == 403

    r_ok = client.get("/api/agent/export", headers=user_headers)
    assert r_ok.status_code == 200
    assert r_ok.headers.get("content-type", "").startswith("application/zip")


def test_web_files_import_preview_invalid_inputs(user_headers=None):
    headers, _ = _auth_headers("user")

    r_bad_ct = client.post("/api/agent/import/preview", data=b"abc", headers=headers)
    assert r_bad_ct.status_code == 400

    boundary = "----covboundary"
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"bad.zip\"\r\n"
        f"Content-Type: application/zip\r\n\r\n"
    ).encode() + b"not a zip" + f"\r\n--{boundary}--\r\n".encode()
    headers2 = dict(headers)
    headers2["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    r_bad_zip = client.post("/api/agent/import/preview", content=body, headers=headers2)
    assert r_bad_zip.status_code == 400


def test_web_files_session_export_not_found_404():
    headers, _ = _auth_headers("user")
    r = client.get("/api/sessions/no_such_session/export", headers=headers)
    assert r.status_code == 404


# --- salmalm/web/routes/web_manage.py ---

def test_web_manage_backup_auth_and_admin():
    r_unauth = client.get("/api/backup")
    assert r_unauth.status_code == 401

    user_headers, _ = _auth_headers("user")
    r_user = client.get("/api/backup", headers=user_headers)
    assert r_user.status_code == 403

    r_presence_ok = client.post(
        "/api/presence",
        json={"instanceId": "cov-web", "mode": "web"},
        headers=user_headers,
    )
    assert r_presence_ok.status_code == 200


def test_web_manage_validation_errors_and_forbidden():
    user_headers, _ = _auth_headers("user")

    r_switch = client.post("/api/persona/switch", json={"session_id": "s1"}, headers=user_headers)
    assert r_switch.status_code == 400

    r_create = client.post("/api/persona/create", json={"name": ""}, headers=user_headers)
    assert r_create.status_code == 400

    r_presence = client.post("/api/presence", json={}, headers=user_headers)
    assert r_presence.status_code == 400

    r_node = client.post("/api/node/execute", json={}, headers=user_headers)
    assert r_node.status_code == 400

    r_hooks = client.post("/api/hooks", json={"action": "reload"}, headers=user_headers)
    assert r_hooks.status_code == 403


def test_web_manage_backup_restore_invalid_zip_400():
    admin_headers, _ = _auth_headers("admin")
    r = client.post("/api/backup/restore", content=b"notzip", headers=admin_headers)
    assert r.status_code == 400


# --- salmalm/web/routes/web_chat.py ---

def test_web_chat_auth_and_422_and_abort_200(monkeypatch):
    r_unauth = client.post("/api/chat", json={"message": "hi"})
    assert r_unauth.status_code == 401

    headers, _ = _auth_headers("user")

    # Body must be object for pydantic model
    r_422 = client.post("/api/chat", json=["not-an-object"], headers=headers)
    assert r_422.status_code == 422

    from salmalm.security import crypto as crypto_mod

    monkeypatch.setattr(crypto_mod.vault, "_password", "testpass", raising=False)

    async def _fake_process_message(*args, **kwargs):
        return "ok-response"

    monkeypatch.setattr("salmalm.core.engine.process_message", _fake_process_message)

    r_ok = client.post("/api/chat", json={"message": "hello", "session": "cov_chat"}, headers=headers)
    assert r_ok.status_code == 200
    assert r_ok.json().get("response") == "ok-response"

    r_abort = client.post("/api/chat/abort", json={"session": "cov_chat"}, headers=headers)
    assert r_abort.status_code == 200


def test_web_chat_message_validation_and_not_found(monkeypatch):
    headers, _ = _auth_headers("user")

    r_edit = client.post("/api/messages/edit", json={"session_id": "s"}, headers=headers)
    assert r_edit.status_code == 400

    r_regen = client.post("/api/chat/regenerate", json={"session_id": "s"}, headers=headers)
    assert r_regen.status_code == 400

    monkeypatch.setattr(
        "salmalm.features.edge_cases.conversation_fork.switch_alternative",
        lambda *args, **kwargs: None,
    )
    r_404 = client.post(
        "/api/alternatives/switch",
        json={"session_id": "s", "message_index": 0, "alt_id": 1},
        headers=headers,
    )
    assert r_404.status_code == 404


# --- salmalm/web/routes/web_sessions.py ---

def test_web_sessions_happy_auth_404_and_422():
    r_unauth = client.get("/api/sessions")
    assert r_unauth.status_code == 401

    headers, _ = _auth_headers("user")

    sid = f"cov_sess_{uuid.uuid4().hex[:8]}"
    r_create = client.post("/api/sessions/create", json={"session_id": sid}, headers=headers)
    assert r_create.status_code == 200

    r_list = client.get("/api/sessions", headers=headers)
    assert r_list.status_code == 200

    r_msgs = client.get(f"/api/sessions/{sid}/messages", headers=headers)
    assert r_msgs.status_code == 200

    r_not_found = client.get("/api/sessions/does_not_exist/messages", headers=headers)
    assert r_not_found.status_code == 404

    r_422 = client.get(f"/api/sessions/{sid}/alternatives?msg_index=bad", headers=headers)
    assert r_422.status_code == 422


# --- salmalm/web/routes/web_model.py ---

def test_web_model_endpoints(monkeypatch):
    r_unauth = client.get("/api/llm-router/current")
    assert r_unauth.status_code == 401

    headers, _ = _auth_headers("user")

    r_current = client.get("/api/llm-router/current", headers=headers)
    assert r_current.status_code == 200

    r_missing_model = client.post("/api/model/switch", json={}, headers=headers)
    assert r_missing_model.status_code == 400

    r_invalid_model = client.post("/api/model/switch", json={"model": "bad model !"}, headers=headers)
    assert r_invalid_model.status_code == 400

    monkeypatch.setattr("salmalm.core.llm_router.llm_router.switch_model", lambda m: "✅ switched")
    r_ok = client.post("/api/model/switch", json={"model": "auto"}, headers=headers)
    assert r_ok.status_code == 200
    assert r_ok.json().get("ok") is True


# --- salmalm/web/routes/web_gateway.py ---

def test_web_gateway_nodes_and_register_paths(monkeypatch):
    r_unauth = client.get("/api/gateway/nodes")
    assert r_unauth.status_code == 401

    headers_user, _ = _auth_headers("user")
    headers_admin, _ = _auth_headers("admin")

    r_forbidden = client.post(
        "/api/gateway/register", json={"node_id": "n1", "url": "https://example.com"}, headers=headers_user
    )
    assert r_forbidden.status_code == 403

    r_missing = client.post("/api/gateway/register", json={"node_id": ""}, headers=headers_admin)
    assert r_missing.status_code == 400

    r_heartbeat = client.post("/api/gateway/heartbeat", json={"node_id": "n1"})
    assert r_heartbeat.status_code == 200


def test_web_gateway_webhooks_503_and_403(monkeypatch):
    r_slack_503 = client.post("/webhook/slack", json={})
    assert r_slack_503.status_code == 503

    from salmalm.channels import slack_bot as slack_mod

    monkeypatch.setattr(slack_mod.slack_bot, "bot_token", "x", raising=False)
    monkeypatch.setattr(slack_mod.slack_bot, "verify_request", lambda *a, **k: False)
    r_slack_403 = client.post("/webhook/slack", json={"type": "event_callback"})
    assert r_slack_403.status_code == 403

    r_tg_503 = client.post("/webhook/telegram", json={})
    assert r_tg_503.status_code == 503


# --- salmalm/web/routes/web_cron.py ---

class _DummyCron:
    def __init__(self):
        self.jobs = [{"id": "j1", "enabled": True, "user_id": 1}]

    def list_jobs(self):
        return list(self.jobs)

    def add_job(self, name, schedule, prompt, user_id=None):
        job = {"id": f"j{len(self.jobs)+1}", "name": name, "schedule": schedule, "prompt": prompt, "user_id": user_id, "enabled": True}
        self.jobs.append(job)
        return job

    def remove_job(self, job_id):
        old = len(self.jobs)
        self.jobs = [j for j in self.jobs if j["id"] != job_id]
        return len(self.jobs) != old

    def save_jobs(self):
        return None

    def _execute_job(self, job):
        return None


def test_web_cron_auth_and_crud(monkeypatch):
    import salmalm.core as core_mod
    import salmalm.core.core as core_core_mod

    dummy = _DummyCron()
    monkeypatch.setattr(core_mod, "_llm_cron", dummy, raising=False)
    monkeypatch.setattr(core_core_mod, "_llm_cron", dummy, raising=False)

    r_unauth = client.get("/api/cron")
    assert r_unauth.status_code == 401

    headers_user, user = _auth_headers("user")
    headers_admin, _ = _auth_headers("admin")

    # move ownership to user for 200 paths
    dummy.jobs[0]["user_id"] = user["id"]

    r_list = client.get("/api/cron", headers=headers_user)
    assert r_list.status_code == 200

    r_add_bad = client.post("/api/cron/add", json={"name": "x"}, headers=headers_user)
    assert r_add_bad.status_code == 400

    r_add_ok = client.post("/api/cron/add", json={"name": "x", "prompt": "hello", "interval": 120}, headers=headers_user)
    assert r_add_ok.status_code == 200

    r_toggle_forbidden = client.post("/api/cron/toggle", json={"id": "j1"}, headers=headers_admin)
    assert r_toggle_forbidden.status_code == 200  # admin can toggle any job

    r_delete_404 = client.post("/api/cron/delete", json={"id": "missing"}, headers=headers_user)
    assert r_delete_404.status_code == 404

    r_run_404 = client.post("/api/cron/run", json={"id": "missing"}, headers=headers_user)
    assert r_run_404.status_code == 404


# --- salmalm/features/users.py ---

def test_users_manager_quota_and_settings(tmp_path, monkeypatch):
    from salmalm.features import users as users_mod

    monkeypatch.setattr(users_mod, "USERS_DB", tmp_path / "users.db")
    monkeypatch.setattr(users_mod, "_USERS_DIR", tmp_path / "users")

    um = users_mod.UserManager()
    um._initialized = False
    um._multi_tenant_enabled = None

    um._ensure_db()
    conn = users_mod.get_connection(users_mod.USERS_DB)
    conn.execute(
        "INSERT INTO users (id, username, password_hash, password_salt, role, enabled) VALUES (?,?,?,?,?,?)",
        (101, "quota_user", b"x", b"y", "user", 1),
    )
    conn.commit()
    conn.close()

    # default: single-tenant compatibility branch
    q = um.check_quota(101)
    assert q["ok"] is True and q.get("unlimited") is True

    um.enable_multi_tenant(True)
    um.ensure_quota(101)
    um.set_quota(101, daily_limit=0.1, monthly_limit=1.0)
    um.record_cost(101, 0.1)

    with pytest.raises(users_mod.QuotaExceeded):
        um.check_quota(101)

    um.set_user_settings(101, model_preference="auto", persona="default", tts_enabled=True, extra={"a": 1})
    s = um.get_user_settings(101)
    assert s["tts_enabled"] is True
    assert s["extra"]["a"] == 1


def test_users_manager_telegram_and_config(tmp_path, monkeypatch):
    from salmalm.features import users as users_mod

    monkeypatch.setattr(users_mod, "USERS_DB", tmp_path / "users2.db")
    monkeypatch.setattr(users_mod, "_USERS_DIR", tmp_path / "users2")

    um = users_mod.UserManager()
    um._initialized = False
    um._multi_tenant_enabled = None
    um._ensure_db()

    conn = users_mod.get_connection(users_mod.USERS_DB)
    conn.execute(
        "INSERT INTO users (id, username, password_hash, password_salt, role, enabled) VALUES (?,?,?,?,?,?)",
        (777, "tg_user", b"x", b"y", "user", 1),
    )
    conn.commit()
    conn.close()

    um.link_telegram("chat-1", 777, "tgname")
    linked = um.get_user_by_telegram("chat-1")
    assert linked and linked["id"] == 777

    um.unlink_telegram("chat-1")
    assert um.get_user_by_telegram("chat-1") is None

    assert um.get_registration_mode() == "admin_only"
    um.set_registration_mode("open")
    assert um.get_registration_mode() == "open"

    with pytest.raises(ValueError):
        um.set_registration_mode("invalid")
