"""A fake platform runtime for testing workflow agents without ASTER (`mp-workflow/1`, SDK >= 3.2.1).

`FakeRuntime` answers the runtime API the runner talks to (`/api/mp/runtime/v1/executions/{id}/...`) in memory, through an
`httpx.MockTransport`. Pass its transport and env to the runner, then read what the runner saved::

    from agenticstar_platform.workflow import arun
    from agenticstar_platform.workflow.testing import FakeRuntime

    fake = FakeRuntime(contract=CONTRACT, parameters={"product_code": "P-100", "language": "en"},
                       inputs={"instructions": b"# Answer the customer\\n"})
    result = await arun("my_agent.main:run", env=fake.runner_env(), workspace=str(tmp_path), transport=fake.transport)
    assert result.outcome == "completed"
    reply = fake.saved_artifacts()["reply"]["content"]

The runner starts your entrypoint in a child process with the current directory set to the work directory, so the
module of the entrypoint must be importable from `PYTHONPATH` (or installed).

It copies the current behaviour of the platform's runtime API and nothing more:

- `GET context`: the run's context (`parameters`, the contract's `files` / `outputs` / `effect_mode` / `limits`, deadlines,
  connections, `gate_decision`, `start_input`); `cancel_requested_at` is also set once the run has ended
- `GET artifacts/{id}/content`: the input artifacts of the input manifest (others are `403`)
- `GET connections/{slot}/token`: the token of a bound slot (`404 connection_not_bound` otherwise)
- `POST audit`: `accepted` / `duplicates` by `event_id`; only `context.manifest` / `tool.invoked` / `tool.effect` /
  `tool.denied`
- `POST artifacts`: only outputs the contract declares, with the declared `source` and `path`; `201`, or `200` for an
  `artifact_id` already saved
- `POST completion`: `version` 2, the `completed` outcome needs the required outputs, a `read_only` contract cannot report
  `had_mutating_success: true`, `error_class` is at most 128 characters; the first completion makes the execution terminal,
  the same `completion_id` and content again is `200 existing`, anything else afterwards is `409 terminal`
- before terminal, writes and the live reads (input artifacts, connection tokens) are refused with `409 deadline_exceeded`
  after the deadline, `409 cancelled` after cancellation and `409 run_closed` after the run ended (in this order). An audit
  batch made only of `tool.effect` / `tool.denied` events is still accepted then: it records what the agent already did

**It does not check the parameters or the contract.** `parameters` are passed to the agent as given (not checked against
`parameters_schema`, no defaults filled in), and the contract is not validated. The platform checks both before a run (the
admin console's pre-registration check and the executor); use those to check a contract. Audit events and the completion
are kept as the runner sent them (the platform keeps only the fields it knows).

**Supported surface**: the constructor arguments, `runner_env()`, `transport`, `saved_artifacts()` /
`saved_audit_events()` / `saved_completion()`, `sample_contract()` / `sample_parameters()`, the constants `EXECUTION_ID` /
`TOKEN` / `BASE_URL`, and these attributes, which you can change before or during a step to simulate the platform:

- `contract`: the contract the fake serves (a copy of the one you passed); later requests see your changes
- `cancel_requested_at`: an ISO time = cancellation was requested
- `run_closed`: the run has ended (`409 run_closed`)
- `deadline_passed`: the deadline has passed (`409 deadline_exceeded`) without waiting for it
- `gate_decision` / `start_input`: the values of the context (see `WorkflowContext`)
- `fail_audit_types`: a set of event types whose audit batches get `503`
- `fail_upload_times` / `fail_completion_times` / `fail_download_times`: the next N output uploads / completions /
  input downloads get `503`

Everything else (other attributes and methods) is internal and may change without notice.
"""
from __future__ import annotations

import copy
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from email.parser import BytesParser
from email.policy import default as email_policy
from typing import Any, Mapping, Optional, Union

import httpx

from .canonical import CanonicalizationError, canonical_json, digest_json

__all__ = ["EXECUTION_ID", "TOKEN", "BASE_URL", "FakeRuntime", "sample_contract", "sample_parameters"]

EXECUTION_ID = "0d5c6a9e-1b2c-4d3e-8f90-123456789abc"
TOKEN = "test-token"
BASE_URL = "http://aster.test/api/mp/runtime/v1/executions"
_PREFIX = f"/api/mp/runtime/v1/executions/{EXECUTION_ID}"
_IMAGE_DIGEST = "sha256:" + "b" * 64
_AUDIT_EVENT_TYPES = ("context.manifest", "tool.invoked", "tool.effect", "tool.denied")
# records of what the agent already did: accepted after cancellation / the end of the run / the deadline until terminal
_LATE_RECORD_EVENTS = ("tool.effect", "tool.denied")

ConnectionToken = Union[str, tuple[str, Union[str, datetime, None]]]


def sample_contract() -> dict[str, Any]:
    """The contract of the sample `docs/examples/workflow_reply_agent.py` (drafting a reply, `read_only`)."""
    return {
        "contract_digest": "c" * 64,
        "image_digest": _IMAGE_DIGEST,
        "runtime_protocol": "mp-workflow/1",
        "effect_mode": "read_only",
        "parameters_schema": {"type": "object", "additionalProperties": False,
                              "properties": {"product_code": {"type": "string"},
                                             "language": {"type": "string", "enum": ["ja", "en"]}},
                              "required": ["product_code", "language"]},
        "env_bindings": {"PRODUCT_CODE": "product_code", "REPLY_LANGUAGE": "language"},
        "files": [
            {"name": "instructions", "path": "instructions.md", "format": "markdown", "editable": True, "required": True},
            {"name": "settings", "path": "settings/agent.yaml", "format": "yaml", "from_parameters": True},
        ],
        "outputs": [{"name": "reply", "path": "reply.md", "format": "markdown", "required": True}],
        "limits": {"execution_timeout_seconds": 600},
    }


def sample_parameters() -> dict[str, Any]:
    """The parameters used with `sample_contract()`."""
    return {"product_code": "P-100", "language": "ja"}


def _env_from_parameters(contract: Mapping[str, Any], parameters: Mapping[str, Any]) -> dict[str, str]:
    """The `env` of the context: `env_bindings` filled from the parameters (scalars only, as the platform does; numbers are
    written as JavaScript writes them, so `5.0` is `"5"`)."""
    env: dict[str, str] = {}
    for name, param in (contract.get("env_bindings") or {}).items():
        value = parameters.get(param)
        if isinstance(value, bool):
            env[name] = "true" if value else "false"
        elif isinstance(value, str):
            env[name] = value
        elif isinstance(value, (int, float)):
            try:
                env[name] = canonical_json(value)
            except CanonicalizationError:   # NaN / Infinity: the platform has no value for it either
                continue
    return env


class FakeRuntime:
    """In-memory platform runtime API for one execution (`EXECUTION_ID`).

    Args:
        contract: the agent's contract (`files`, `outputs`, `effect_mode`, `limits`, `env_bindings`, ...). Defaults to
            `sample_contract()`. Copied; change `fake.contract` to change what later requests see
        parameters: the resolved parameters of the step, passed as given. Defaults to `sample_parameters()` when
            `contract` is omitted, otherwise `{}`
        inputs: the input artifacts by the name of a contract file (`{"instructions": b"..."}`); each is staged at that
            file's `path` with its `format`. Defaults to `{"instructions": instructions}` when the contract has a file
            named `instructions`, otherwise none
        connections: the connection slots bound to the run, `{slot: access_token}` or `{slot: (access_token, expires_at)}`
            (`expires_at`: an ISO time, a `datetime` or `None` = unknown)
        effect_mode: overrides the contract's `effect_mode` (`read_only` / `idempotent_write` / `non_idempotent_write`)
        deadline_seconds: the execution deadline from now (the collection deadline is 300 seconds later); `None` = the
            platform has not set one yet (the runner uses the contract's `limits.execution_timeout_seconds`)
        instructions: the content of the `instructions` input when `inputs` is omitted
    """

    def __init__(self, *, contract: Optional[Mapping[str, Any]] = None, parameters: Optional[Mapping[str, Any]] = None,
                 inputs: Optional[Mapping[str, Union[bytes, str]]] = None,
                 connections: Optional[Mapping[str, ConnectionToken]] = None, effect_mode: Optional[str] = None,
                 deadline_seconds: Optional[int] = 600, instructions: bytes = b"# do it\n"):
        self.contract: dict[str, Any] = copy.deepcopy(dict(contract)) if contract is not None else sample_contract()
        if effect_mode is not None:
            self.contract["effect_mode"] = effect_mode
        self.parameters: dict[str, Any] = (copy.deepcopy(dict(parameters)) if parameters is not None
                                           else sample_parameters() if contract is None else {})
        self.contract_digest = str(self.contract.get("contract_digest") or digest_json(self.contract))
        self.image_digest = str(self.contract.get("image_digest") or _IMAGE_DIGEST)
        files = {f.get("name"): f for f in self.contract.get("files") or [] if isinstance(f, Mapping)}
        if inputs is None:
            inputs = {"instructions": instructions} if "instructions" in files else {}
        # artifact_id -> {name, target_path, format, content}。保存済みの artifact と同じく、形式は作った時の契約の値で固定する
        self.input_artifacts: dict[str, dict[str, Any]] = {}
        for name, content in inputs.items():
            fdef = files.get(name)
            if fdef is None or not fdef.get("path"):
                raise ValueError(f"input {name!r} is not a file of the contract")
            data = content.encode("utf-8") if isinstance(content, str) else bytes(content)
            self.input_artifacts[str(uuid.uuid4())] = {"name": name, "target_path": str(fdef["path"]),
                                                       "format": str(fdef.get("format") or "text"), "content": data}
        self.connection_tokens: dict[str, tuple[str, Optional[str]]] = {}
        for slot, tok in (connections or {}).items():
            token, expires_at = (tok, None) if isinstance(tok, str) else tok
            self.connection_tokens[str(slot)] = (
                token, expires_at.isoformat() if isinstance(expires_at, datetime) else expires_at)
        self.state = "running"
        self.cancel_requested_at: Optional[str] = None
        self.execution_deadline: Optional[datetime] = (datetime.now(timezone.utc) + timedelta(seconds=deadline_seconds)
                                                       if deadline_seconds is not None else None)
        self.input_format_override: Optional[str] = None      # internal: the manifest format differs from the contract
        self.persist_then_500: dict[str, int] = {}            # internal: event_type -> N saves answered with 500 afterwards
        self.audit_events: list[dict[str, Any]] = []
        self.audit_ids: set[str] = set()
        self.artifacts: dict[str, dict[str, Any]] = {}        # internal: artifact_id -> the record the save answered
        self.artifact_contents: dict[str, bytes] = {}         # internal: artifact_id -> the saved content
        self.completion: Optional[dict[str, Any]] = None
        self.calls: list[str] = []
        self.fail_audit_types: set[str] = set()      # audit batches with these event types get 503
        self.fail_completion_times = 0               # the next N completions get 503
        self.fail_upload_times = 0                   # the next N output uploads get 503
        self.fail_download_times = 0                 # the next N input downloads get 503
        self.download_reject: Optional[tuple[int, str]] = None   # internal: input downloads get (status, code)
        self.fail_context: Optional[tuple[int, str]] = None   # internal: /context gets (status, code)
        self.completion_body_not_json = False        # internal: the completion is saved but the answer is not JSON
        self.completion_redirect = False             # internal: a 302 + HTML in front of the API (not saved)
        self.completion_raises: Optional[BaseException] = None   # internal: the transport raises this on completion
        self.context_protocol_override: Optional[str] = None   # internal: /context answers another protocol
        self.fail_invoked_500_times = 0              # internal
        self.reject_all_writes = False               # internal
        self.run_closed = False                      # the run has ended (or was cancelled): 409 run_closed
        self.deadline_passed = False                 # the deadline has passed, without waiting for it
        self.connection_token_calls: list[str] = []
        self.gate_decision: Any = None   # /context gate_decision (a run started by a review decision)
        self.start_input: Any = None     # /context start_input (the first step of a run started from outside)
        self.transport = httpx.MockTransport(self.handle)

    # ----- what the runner needs and what it saved -----
    @staticmethod
    def runner_env() -> dict[str, str]:
        """The env the platform's executor injects into the agent's Pod, pointing at this fake (pass it as `env=`)."""
        return {"ASTER_RUNTIME_PROTOCOL": "mp-workflow/1", "ASTER_RUNTIME_BASE_URL": BASE_URL,
                "ASTER_RUNTIME_TOKEN": TOKEN, "EXECUTION_ID": EXECUTION_ID}

    def saved_artifacts(self) -> dict[str, dict[str, Any]]:
        """The output artifacts the runner saved, by logical name:
        `{name: {artifact_id, logical_name, path, source, format, sha256, size_bytes, content}}` (`content` is bytes)."""
        return {rec["logical_name"]: {"artifact_id": aid, **copy.deepcopy(rec), "content": self.artifact_contents[aid]}
                for aid, rec in self.artifacts.items()}

    def saved_audit_events(self) -> list[dict[str, Any]]:
        """The audit events saved, in order (`event_id`, `event_type`, `decision`, `reason`, `metadata`, `occurred_at`).
        The first two are the runner's `context.manifest` events."""
        return copy.deepcopy(self.audit_events)

    def saved_completion(self) -> Optional[dict[str, Any]]:
        """The saved completion `{completion_id, envelope, output_artifact_ids}`, or `None` before the runner saved one."""
        if self.completion is None:
            return None
        return {"completion_id": self.completion["completion_id"], "envelope": copy.deepcopy(self.completion["envelope"]),
                "output_artifact_ids": list(self.completion["output_artifact_ids"])}

    # ----- helpers -----
    def _ctx(self) -> dict[str, Any]:
        params = copy.deepcopy(self.parameters)
        lr = {"protocol": "mp-workflow/1", "requested_execution_id": EXECUTION_ID, "project_id": str(uuid.uuid4()),
              "run_id": str(uuid.uuid4()), "run_step_id": 7, "step_id": str(uuid.uuid4()), "project_agent_id": str(uuid.uuid4()),
              "agent_id": str(uuid.uuid4()), "marketplace_agent_id": "mp-agent-1", "attempt": 1,
              "root_execution_id": EXECUTION_ID, "entry_ref": "start:cmd-1", "operation_key": "a" * 64,
              "execution_principal": "user:alice", "conversation_id": None, "message_id": None, "config_revision": 1,
              "input_manifest": self._input_manifest(), "contract_digest": self.contract_digest,
              "image_digest": self.image_digest}
        return {
            "execution_id": EXECUTION_ID, "protocol": self.context_protocol_override or "mp-workflow/1", "state": self.state,
            # like the platform, the end of the run is also reported here (the run's end time)
            "cancel_requested_at": self.cancel_requested_at or (datetime.now(timezone.utc).isoformat() if self.run_closed else None),
            "launch_request": lr, "input_manifest": self._input_manifest(),
            "parameters": params, "parameters_digest": digest_json(params),
            "env": _env_from_parameters(self.contract, params),
            "connections": {slot: f"provider-{slot}" for slot in self.connection_tokens},
            # the platform passes this part of the contract (not the whole registered contract)
            "contract": {"contract_digest": self.contract_digest, "image_digest": self.image_digest,
                         "parameters_schema": self.contract.get("parameters_schema"),
                         "files": self.contract.get("files") or [], "outputs": self.contract.get("outputs") or [],
                         "effect_mode": self.contract.get("effect_mode"), "limits": self.contract.get("limits") or {}},
            "deadlines": {"launch": None,
                          "execution": self.execution_deadline.isoformat() if self.execution_deadline else None,
                          "collection": (self.execution_deadline + timedelta(seconds=300)).isoformat() if self.execution_deadline else None},
            "operation_key": "a" * 64, "entry_ref": "start:cmd-1", "root_execution_id": EXECUTION_ID, "config_revision": 1,
            "gate_decision": self.gate_decision,
            "start_input": self.start_input,
            "artifact_limits": {"file_bytes": 20 * 1024 * 1024, "execution_bytes": 100 * 1024 * 1024, "execution_files": 100},
        }

    def _input_manifest(self) -> list[dict[str, Any]]:
        manifest = [{"artifact_id": aid, "sha256": hashlib.sha256(a["content"]).hexdigest(), "size": len(a["content"]),
                     "target_path": a["target_path"], "format": self.input_format_override or a["format"]}
                    for aid, a in self.input_artifacts.items()]
        return sorted(manifest, key=lambda m: m["target_path"])

    def _outputs(self) -> list[dict[str, Any]]:
        return list(self.contract.get("outputs") or [])

    def _closed_reason(self) -> Optional[str]:
        """After the deadline / cancellation / the end of the run, the code (in the platform's order); otherwise None."""
        if self.deadline_passed or (self.execution_deadline is not None
                                    and datetime.now(timezone.utc) > self.execution_deadline + timedelta(seconds=300)):
            return "deadline_exceeded"
        if self.cancel_requested_at:
            return "cancelled"
        if self.run_closed:
            return "run_closed"
        return None

    @staticmethod
    def _only_late_records(request: httpx.Request) -> bool:
        """An audit batch made only of records of what the agent already did (accepted until terminal, like the platform)."""
        try:
            events = json.loads(request.content).get("events")
        except (ValueError, AttributeError):
            return False
        return (isinstance(events, list) and bool(events)
                and all(isinstance(e, dict) and e.get("event_type") in _LATE_RECORD_EVENTS for e in events))

    @staticmethod
    def _err(status: int, code: str, message: str = "") -> httpx.Response:
        return httpx.Response(status, json={"code": code, "message": message, "ref": EXECUTION_ID})

    # ----- dispatch -----
    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        self.calls.append(f"{request.method} {path}")
        if request.headers.get("authorization") != f"Bearer {TOKEN}":
            return self._err(401, "unauthorized")
        if not path.startswith(_PREFIX):
            return self._err(403, "forbidden")
        sub = path[len(_PREFIX):]
        is_write = request.method not in ("GET", "HEAD")
        if self.state == "terminal" and not sub.endswith("/completion"):
            return self._err(409, "terminal", "execution is terminal")
        live = (sub.startswith("/artifacts/") and sub.endswith("/content")) \
            or (sub.startswith("/connections/") and sub.endswith("/token"))
        if (is_write or live) and self.state != "terminal":
            closed = self._closed_reason()
            if closed and not (sub == "/audit" and is_write and self._only_late_records(request)):
                return self._err(409, closed)
        if is_write and self.reject_all_writes:
            return self._err(503, "runtime_unavailable")
        if sub == "/context":
            if self.fail_context is not None:
                return self._err(*self.fail_context)
            return httpx.Response(200, json=self._ctx())
        if sub.startswith("/connections/") and sub.endswith("/token") and request.method == "GET":
            slot = sub[len("/connections/"):-len("/token")]
            self.connection_token_calls.append(slot)
            if slot not in self.connection_tokens:
                return self._err(404, "connection_not_bound")
            token, expires_at = self.connection_tokens[slot]
            return httpx.Response(200, json={"slot": slot, "access_token": token, "token_type": "Bearer",
                                             "expires_at": expires_at})
        if sub.startswith("/artifacts/") and sub.endswith("/content"):
            aid = sub[len("/artifacts/"):-len("/content")]
            if aid not in self.input_artifacts:
                return self._err(403, "forbidden", "artifact not in input manifest")
            if self.fail_download_times > 0:
                self.fail_download_times -= 1
                return self._err(503, "storage_unavailable")
            if self.download_reject is not None:
                status, code = self.download_reject
                if status == 409:   # 拒んだ理由は以後の要求にも効く（本物の front は保存行の現在値で判定する）
                    self.cancel_requested_at = self.cancel_requested_at or (
                        datetime.now(timezone.utc).isoformat() if code == "cancelled" else None)
                    self.run_closed = self.run_closed or code == "run_closed"
                    self.deadline_passed = self.deadline_passed or code == "deadline_exceeded"
                return self._err(status, code)
            return httpx.Response(200, content=self.input_artifacts[aid]["content"],
                                  headers={"Content-Type": "application/octet-stream"})
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
            if e.get("event_type") not in _AUDIT_EVENT_TYPES:
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
        out = next((o for o in self._outputs() if o.get("name") == fields["logical_name"]), None)
        if out is None:
            return self._err(400, "output_not_declared")  # front: outputs に宣言された名前だけ
        expected_source = out.get("source") or "output"
        if fields.get("source", "output") != expected_source:
            return self._err(400, "output_source_mismatch")
        if fields.get("path") and fields["path"] != out.get("path"):
            return self._err(400, "output_path_mismatch")
        sha = hashlib.sha256(content).hexdigest()
        if fields.get("sha256") and fields["sha256"] != sha:
            return self._err(400, "digest_mismatch")
        existing = self.artifacts.get(fields["artifact_id"])
        rec = {"id": fields["artifact_id"], "logical_name": fields["logical_name"], "sha256": sha, "size_bytes": len(content),
               "format": fields.get("format"), "state": "ready", "path": fields.get("path"), "source": expected_source}
        self.artifacts[fields["artifact_id"]] = rec
        self.artifact_contents[fields["artifact_id"]] = content
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
        ec = env.get("error_class")   # JS の length（UTF-16 の単位）で数える
        if ec is not None and (not isinstance(ec, str) or len(ec.encode("utf-16-le", "surrogatepass")) > 256):
            return self._err(400, "invalid_envelope")   # front completion.js の optionalString(error_class, 128)
        if env.get("outcome") == "completed":
            names = {self.artifacts[i]["logical_name"] for i in ids if i in self.artifacts}
            missing = [o.get("name") for o in self._outputs() if o.get("required") and o.get("name") not in names]
            if missing:
                return self._err(400, "required_output_missing")
        if self.contract.get("effect_mode") == "read_only" and env.get("had_mutating_success"):
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
