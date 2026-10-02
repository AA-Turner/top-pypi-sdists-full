"""front runtime 保存 API（/api/mp/runtime/v1/executions/{id}）の in-memory fake（httpx.MockTransport）。

chatboardfront `routes/mpRuntime.js` / `services/Project/mp/completion.js` の契約を写す:
context / artifacts/{id}/content / audit（accepted, duplicates）/ artifacts（multipart, 201 or 200 existing）/
completion（CAS: 同じ completion_id+digest は 200 existing、異なる terminal 候補は 409 terminal）、
terminal 後の非 completion write は 409 terminal、期限後の write は 409 deadline_exceeded。
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from email.parser import BytesParser
from email.policy import default as email_policy
from typing import Any, Optional

import httpx

from agenticstar_platform.workflow.canonical import digest_json

EXECUTION_ID = "0d5c6a9e-1b2c-4d3e-8f90-123456789abc"
TOKEN = "test-token"


def contract() -> dict[str, Any]:
    return {
        "contract_digest": "c" * 64, "image_digest": "sha256:" + "b" * 64,
        "files": [
            {"name": "instructions", "path": "instructions.md", "format": "markdown", "editable": True, "required": True},
            {"name": "settings", "path": "settings/agent.yaml", "format": "yaml", "from_parameters": True},
        ],
        "outputs": [{"name": "reply", "path": "reply.md", "format": "markdown", "required": True}],
        "effect_mode": "read_only",
        "limits": {"execution_timeout_seconds": 600},
    }


class FakeRuntime:
    def __init__(self, *, effect_mode: str = "read_only", deadline_seconds: Optional[int] = 600, instructions: bytes = b"# do it\n"):
        self.artifact_in = str(uuid.uuid4())
        self.instructions = instructions
        self.contract = contract()
        self.contract["effect_mode"] = effect_mode
        self.state = "running"
        self.cancel_requested_at: Optional[str] = None
        self.execution_deadline: Optional[datetime] = (datetime.now(timezone.utc) + timedelta(seconds=deadline_seconds)
                                                       if deadline_seconds is not None else None)
        self.input_format_override: Optional[str] = None      # manifest 側の format を契約と食い違わせる
        self.persist_then_500: dict[str, int] = {}            # event_type -> 保存してから 500 を返す回数（再送で duplicates）
        self.audit_events: list[dict[str, Any]] = []
        self.audit_ids: set[str] = set()
        self.artifacts: dict[str, dict[str, Any]] = {}
        self.completion: Optional[dict[str, Any]] = None
        self.calls: list[str] = []
        self.fail_audit_types: set[str] = set()      # これらの event_type の保存を 503 にする
        self.fail_completion_times = 0               # completion を N 回 503 にする
        self.fail_upload_times = 0
        self.fail_download_times = 0                 # 入力 artifact の取得を N 回 503 にする
        self.download_reject: Optional[tuple[int, str]] = None   # 入力 artifact の取得を (status, code) で拒否（live 読み取りの 409）
        self.fail_context: Optional[tuple[int, str]] = None   # /context を (status, code) で失敗させる（token 失効 / 消えた execution）
        self.completion_body_not_json = False        # completion は保存するが応答本文が JSON でない（proxy が差し替えた）
        self.completion_redirect = False             # ingress / SSO が 302 + HTML を返す（保存はされていない）
        self.completion_raises: Optional[BaseException] = None   # 送信経路が再送対象外の例外を出す（本文の decode 失敗 等）
        self.context_protocol_override: Optional[str] = None   # /context の protocol を契約外にする
        self.fail_invoked_500_times = 0
        self.reject_all_writes = False
        # 接続 slot の token 取り直し (executer-marketplace #55)。slot -> (access_token, expires_at)
        self.connection_tokens: dict[str, tuple[str, Optional[str]]] = {
            "gitlab": ("tok-1", (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat())}
        self.connection_token_calls: list[str] = []
        self.transport = httpx.MockTransport(self.handle)

    # ----- helpers -----
    def _ctx(self) -> dict[str, Any]:
        lr = {"protocol": "mp-workflow/1", "requested_execution_id": EXECUTION_ID, "project_id": str(uuid.uuid4()),
              "run_id": str(uuid.uuid4()), "run_step_id": 7, "step_id": str(uuid.uuid4()), "project_agent_id": str(uuid.uuid4()),
              "agent_id": str(uuid.uuid4()), "marketplace_agent_id": "mp-agent-1", "attempt": 1,
              "root_execution_id": EXECUTION_ID, "entry_ref": "start:cmd-1", "operation_key": "a" * 64,
              "execution_principal": "user:alice", "conversation_id": None, "message_id": None, "config_revision": 1,
              "input_manifest": self._input_manifest(), "contract_digest": "c" * 64, "image_digest": "sha256:" + "b" * 64}
        params = {"product_code": "P-100", "language": "ja"}
        return {
            "execution_id": EXECUTION_ID, "protocol": self.context_protocol_override or "mp-workflow/1", "state": self.state,
            "cancel_requested_at": self.cancel_requested_at, "launch_request": lr, "input_manifest": self._input_manifest(),
            "parameters": params, "parameters_digest": digest_json(params),
            "env": {"PRODUCT_CODE": "P-100", "REPLY_LANGUAGE": "ja"}, "connections": {},
            "contract": self.contract,
            "deadlines": {"launch": None,
                          "execution": self.execution_deadline.isoformat() if self.execution_deadline else None,
                          "collection": (self.execution_deadline + timedelta(seconds=300)).isoformat() if self.execution_deadline else None},
            "operation_key": "a" * 64, "entry_ref": "start:cmd-1", "root_execution_id": EXECUTION_ID, "config_revision": 1,
            "artifact_limits": {"file_bytes": 20 * 1024 * 1024, "execution_bytes": 100 * 1024 * 1024, "execution_files": 100},
        }

    def _input_manifest(self) -> list[dict[str, Any]]:
        return [{"artifact_id": self.artifact_in, "sha256": hashlib.sha256(self.instructions).hexdigest(),
                 "size": len(self.instructions), "target_path": "instructions.md",
                 "format": self.input_format_override or "markdown"}]

    @staticmethod
    def _err(status: int, code: str, message: str = "") -> httpx.Response:
        return httpx.Response(status, json={"code": code, "message": message, "ref": EXECUTION_ID})

    # ----- dispatch -----
    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        prefix = f"/api/mp/runtime/v1/executions/{EXECUTION_ID}"
        self.calls.append(f"{request.method} {path}")
        if request.headers.get("authorization") != f"Bearer {TOKEN}":
            return self._err(401, "unauthorized")
        if not path.startswith(prefix):
            return self._err(403, "forbidden")
        sub = path[len(prefix):]
        is_write = request.method not in ("GET", "HEAD")
        if self.state == "terminal" and not sub.endswith("/completion"):
            return self._err(409, "terminal", "execution is terminal")
        if is_write and self.state != "terminal" and self.execution_deadline is not None \
                and datetime.now(timezone.utc) > self.execution_deadline + timedelta(seconds=300):
            return self._err(409, "deadline_exceeded")
        if is_write and self.reject_all_writes:
            return self._err(503, "runtime_unavailable")
        if sub == "/context":
            if self.fail_context is not None:
                return self._err(*self.fail_context)
            return httpx.Response(200, json=self._ctx())
        if sub.startswith("/connections/") and sub.endswith("/token") and request.method == "GET":
            slot = sub[len("/connections/"):-len("/token")]
            self.connection_token_calls.append(slot)
            if self.cancel_requested_at:
                return self._err(409, "cancelled")
            if slot not in self.connection_tokens:
                return self._err(404, "connection_not_bound")
            token, expires_at = self.connection_tokens[slot]
            return httpx.Response(200, json={"access_token": token, "token_type": "Bearer", "expires_at": expires_at})
        if sub.startswith("/artifacts/") and sub.endswith("/content"):
            aid = sub[len("/artifacts/"):-len("/content")]
            if aid != self.artifact_in:
                return self._err(403, "forbidden", "artifact not in input manifest")
            if self.fail_download_times > 0:
                self.fail_download_times -= 1
                return self._err(503, "storage_unavailable")
            if self.download_reject is not None:
                return self._err(*self.download_reject)
            return httpx.Response(200, content=self.instructions, headers={"Content-Type": "text/markdown"})
        if sub == "/audit":
            return self._audit(json.loads(request.content))
        if sub == "/artifacts":
            return self._upload(request)
        if sub == "/completion":
            return self._completion(json.loads(request.content))
        return self._err(404, "not_found")

    def _audit(self, body: dict[str, Any]) -> httpx.Response:
        events = body.get("events") or []
        if not events or len(events) > 100:
            return self._err(400, "invalid_request")
        accepted, duplicates = [], []
        for e in events:
            if e.get("event_type") not in ("context.manifest", "tool.invoked", "tool.effect", "tool.denied"):
                return self._err(400, "event_not_allowed")
            if e.get("event_type") in self.fail_audit_types:
                return self._err(503, "runtime_unavailable")
            if e.get("event_type") == "tool.invoked" and self.fail_invoked_500_times > 0:
                self.fail_invoked_500_times -= 1
                return self._err(500, "internal_error")
            if e["event_id"] in self.audit_ids:
                duplicates.append(e["event_id"])
                continue
            self.audit_ids.add(e["event_id"])
            self.audit_events.append(e)
            accepted.append(e["event_id"])
        for e in events:  # front は batch を 1 transaction で保存する: 保存後に応答が落ちるのは batch 全体
            if self.persist_then_500.get(e.get("event_type"), 0) > 0:
                self.persist_then_500[e["event_type"]] -= 1
                return self._err(500, "internal_error")
        return httpx.Response(200, json={"accepted": accepted, "duplicates": duplicates})

    def _upload(self, request: httpx.Request) -> httpx.Response:
        if self.fail_upload_times > 0:
            self.fail_upload_times -= 1
            return self._err(503, "storage_unavailable")
        ctype = request.headers.get("content-type", "")
        msg = BytesParser(policy=email_policy).parsebytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + request.content)
        fields: dict[str, Any] = {}
        content: Optional[bytes] = None
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            payload = part.get_payload(decode=True)
            if name == "file":
                content = payload
            else:
                fields[name] = payload.decode("utf-8")
        if content is None or not fields.get("artifact_id") or not fields.get("logical_name"):
            return self._err(400, "invalid_request")
        out = next((o for o in self.contract["outputs"] if o["name"] == fields["logical_name"]), None)
        if out is None:
            return self._err(400, "output_not_declared")  # front: outputs に宣言された名前だけ
        expected_source = out.get("source") or "output"
        if fields.get("source", "output") != expected_source:
            return self._err(400, "output_source_mismatch")
        if fields.get("path") and fields["path"] != out["path"]:
            return self._err(400, "output_path_mismatch")
        sha = hashlib.sha256(content).hexdigest()
        if fields.get("sha256") and fields["sha256"] != sha:
            return self._err(400, "digest_mismatch")
        existing = self.artifacts.get(fields["artifact_id"])
        rec = {"id": fields["artifact_id"], "logical_name": fields["logical_name"], "sha256": sha, "size_bytes": len(content),
               "format": fields.get("format"), "state": "ready", "path": fields.get("path"), "source": expected_source}
        self.artifacts[fields["artifact_id"]] = rec
        return httpx.Response(200 if existing else 201, json=rec)

    def _completion(self, body: dict[str, Any]) -> httpx.Response:
        if self.completion_raises is not None:   # httpx が retry / status で扱えない例外（DecodingError 等）
            raise self.completion_raises
        if self.completion_redirect:   # front は redirect を返さない: 保存せずに 302 + HTML（ingress / SSO の割り込み）
            return httpx.Response(302, content=b"<html>login</html>",
                                  headers={"Content-Type": "text/html", "Location": "https://sso.test/login"})
        if self.fail_completion_times > 0:
            self.fail_completion_times -= 1
            return self._err(503, "runtime_unavailable")
        cid = body.get("completion_id")
        env = body.get("completion_envelope") or {}
        ids = sorted(body.get("output_artifact_ids") or [])
        if env.get("version") != 2 or env.get("had_mutating_success") not in (True, False, None) or env.get("resumed") is not False:
            return self._err(400, "invalid_envelope")
        if env["outcome"] == "completed":
            names = {self.artifacts[i]["logical_name"] for i in ids if i in self.artifacts}
            missing = [o["name"] for o in self.contract["outputs"] if o.get("required") and o["name"] not in names]
            if missing:
                return self._err(400, "required_output_missing")
        if self.contract["effect_mode"] == "read_only" and env["had_mutating_success"]:
            return self._err(400, "instrumentation_mismatch")
        digest = digest_json({"completion_id": cid, "completion_envelope": env, "output_artifact_ids": ids})
        if self.state == "terminal":
            if self.completion and self.completion["completion_id"] == cid and self.completion["digest"] == digest:
                return httpx.Response(200, json={"execution_id": EXECUTION_ID, "state": "terminal", "existing": True,
                                                 "output_manifest": []})
            return self._err(409, "terminal")
        self.state = "terminal"
        self.completion = {"completion_id": cid, "digest": digest, "envelope": env, "output_artifact_ids": ids}
        if self.completion_body_not_json:
            return httpx.Response(200, content=b"<html>gateway</html>", headers={"Content-Type": "text/html"})
        return httpx.Response(200, json={"execution_id": EXECUTION_ID, "state": "terminal", "existing": False,
                                         "output_manifest": [{"artifact_id": i} for i in ids]})
