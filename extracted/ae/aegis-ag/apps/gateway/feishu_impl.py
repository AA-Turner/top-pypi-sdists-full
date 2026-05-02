"""Feishu gateway implementation assembled from support and store modules."""


from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
import importlib.util
import json
import logging
import os
import queue
import threading
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

from packages.gateway_core import (
    DEFAULT_GATEWAY_ACCOUNT_ID,
    GatewayExchange,
    GatewayInboundMessage,
    GatewayOutboundMessage,
)

from apps.provider_runtime import EnvironmentSecretStore, secret_reference_from_payload
from apps.runtime_layout import default_cli_state_dir, default_profile_dir
from packages.auth import AuthProfile, ProfileCredentialResolver, SecretReference

from .cli_control import (
    CliRuntimeFactory,
    FeishuCliBindingStore,
    FeishuCliControlService,
    load_feishu_cli_control_config,
)
from .plugins import GatewayManagedRuntime, GatewayPluginRegistry, default_gateway_runtime_path
from .runtime import FEISHU_ADAPTER_ID, FeishuMessagingAdapter, GatewayApp, build_gateway_app

DEFAULT_FEISHU_APP_ID_ENV = "AEGIS_FEISHU_APP_ID"
DEFAULT_FEISHU_APP_SECRET_ENV = "AEGIS_FEISHU_APP_SECRET"
LEGACY_FEISHU_APP_ID_ENV = "FEISHU_APP_ID"
LEGACY_FEISHU_APP_SECRET_ENV = "FEISHU_APP_SECRET"
DEFAULT_FEISHU_BASE_URL = "https://open.feishu.cn"
DEFAULT_FEISHU_EVENT_PATH = "/feishu/events"
DEFAULT_FEISHU_TOKEN_PATH = "/open-apis/auth/v3/tenant_access_token/internal"
SUPPORTED_FEISHU_TRANSPORTS = ("long-connection",)
FEISHU_SDK_PIP_SPEC = "lark-oapi>=1.5.3,<2"
DEFAULT_FEISHU_INBOUND_EVENT_RETENTION_SECONDS = 60 * 60 * 24 * 3
DEFAULT_FEISHU_INBOUND_EVENT_MAX_RECORDS = 4096
DEFAULT_FEISHU_ASYNC_JOB_RETENTION_SECONDS = DEFAULT_FEISHU_INBOUND_EVENT_RETENTION_SECONDS
DEFAULT_FEISHU_ASYNC_JOB_MAX_RECORDS = DEFAULT_FEISHU_INBOUND_EVENT_MAX_RECORDS
DEFAULT_FEISHU_ASYNC_WORKER_COUNT = 2
DEFAULT_FEISHU_ASYNC_FAILURE_HISTORY = 5
DEFAULT_FEISHU_PLACEHOLDER_BODY = "已收到，正在处理中..."
DEFAULT_FEISHU_FAILURE_BODY = "处理失败，请稍后重试。"

HttpJsonRequester = Callable[[str, str, Mapping[str, object], Mapping[str, str]], Mapping[str, object]]
FeishuWSClientFactory = Callable[[Any, str, str, object, object | None], object]

LOGGER = logging.getLogger(__name__)

from .feishu_accounts import *  # noqa: F401,F403
from .feishu_stores import *  # noqa: F401,F403
from .feishu_support import *  # noqa: F401,F403

@dataclass(slots=True)
class FeishuGatewayService:
    app: GatewayApp
    account_configs: tuple[FeishuGatewayAccountConfig, ...] = ()
    http_requester: HttpJsonRequester = _default_json_request
    environ: Mapping[str, str] = field(default_factory=lambda: dict(os.environ))
    adapter: FeishuMessagingAdapter | None = None
    cli_runtime_factory: CliRuntimeFactory | None = None
    cli_binding_store: FeishuCliBindingStore | None = None
    cli_control: FeishuCliControlService | None = None
    inbound_event_store: FeishuInboundEventStore | None = None
    async_job_store: FeishuAsyncJobStore | None = None
    default_cli_profile_dir: str | None = None
    default_cli_state_dir: str | None = None
    runtime_dependency_ensurer: Callable[..., object] | None = None
    respect_enabled: bool = True
    service_key: str = "feishu"
    async_worker_count: int = DEFAULT_FEISHU_ASYNC_WORKER_COUNT
    async_placeholder_body: str = DEFAULT_FEISHU_PLACEHOLDER_BODY
    async_failure_body: str = DEFAULT_FEISHU_FAILURE_BODY
    _token_cache: dict[str, _FeishuTokenCacheEntry] = field(
        init=False,
        default_factory=dict,
        repr=False,
    )
    _async_queue: queue.Queue[str | None] = field(
        init=False,
        default_factory=queue.Queue,
        repr=False,
    )
    _async_workers_started: bool = field(default=False, init=False, repr=False)
    _async_workers: list[threading.Thread] = field(default_factory=list, init=False, repr=False)
    _async_stop_event: threading.Event = field(
        default_factory=threading.Event,
        init=False,
        repr=False,
    )
    _async_worker_lock: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False,
    )
    _async_schedule_lock: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False,
    )
    _scheduled_job_keys: set[str] = field(default_factory=set, init=False, repr=False)
    _conversation_locks: dict[str, threading.Lock] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _conversation_locks_guard: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if not self.account_configs:
            self.account_configs = load_feishu_gateway_accounts(
                self.app,
                respect_enabled=self.respect_enabled,
            )
        if self.inbound_event_store is None:
            state_root = self.app.state_dir
            dedupe_path = (
                None
                if state_root is None
                else os.path.join(state_root, "feishu-inbound-events.json")
            )
            self.inbound_event_store = FeishuInboundEventStore(
                path=None if dedupe_path is None else Path(dedupe_path)
            )
        if self.async_job_store is None:
            state_root = self.app.state_dir
            async_jobs_path = (
                None if state_root is None else os.path.join(state_root, "feishu-async-jobs.json")
            )
            self.async_job_store = FeishuAsyncJobStore(
                path=None if async_jobs_path is None else Path(async_jobs_path)
            )
        if self.adapter is None:
            self.adapter = FeishuMessagingAdapter(app=self.app)
        if self.cli_control is None and self.app.loaded_profile is not None:
            config = load_feishu_cli_control_config(self.app.loaded_profile.manifest)
            if config is not None:
                binding_store = self.cli_binding_store
                if binding_store is None:
                    state_root = self.app.state_dir
                    binding_path = (
                        None
                        if state_root is None
                        else os.path.join(state_root, "feishu-cli-bindings.json")
                    )
                    binding_store = FeishuCliBindingStore(
                        path=None if binding_path is None else Path(binding_path)
                    )
                self.cli_control = FeishuCliControlService(
                    config=self._resolved_cli_control_config(config),
                    runtime_factory=self.cli_runtime_factory,
                    binding_store=binding_store,
                )

    def _resolved_cli_control_config(self, config):
        profile_dir = config.profile_dir or self.default_cli_profile_dir or self.app.profile_dir
        if profile_dir is None:
            profile_dir = str(default_profile_dir(environ=self.environ))
        state_dir = config.state_dir or self.default_cli_state_dir or self._inferred_cli_state_dir()
        if state_dir is None:
            state_dir = str(default_cli_state_dir(environ=self.environ))
        return type(config)(
            profile_dir=profile_dir,
            state_dir=state_dir,
            default_clone_id=config.default_clone_id,
            default_session_id=config.default_session_id,
            auto_create_clone=config.auto_create_clone,
            allow_group_chats=config.allow_group_chats,
        )

    def _inferred_cli_state_dir(self) -> str | None:
        if self.app.state_dir is None:
            return None
        state_dir = Path(self.app.state_dir)
        if state_dir.name == "gateway" and state_dir.parent != state_dir:
            return str(state_dir.parent)
        return str(state_dir)

    def _async_summary(self) -> Mapping[str, object]:
        if self.async_job_store is None:
            return {
                "queue_depth": 0,
                "running_jobs": 0,
                "recent_failures": (),
            }
        return self.async_job_store.summary()

    def _ensure_async_workers(self) -> None:
        with self._async_worker_lock:
            if self._async_workers_started:
                return
            worker_count = max(int(self.async_worker_count or 0), 1)
            self._async_stop_event.clear()
            self._async_workers = []
            for index in range(worker_count):
                worker = threading.Thread(
                    target=self._async_worker_loop,
                    name=f"feishu-async-worker-{index + 1}",
                    daemon=True,
                )
                worker.start()
                self._async_workers.append(worker)
            self._async_workers_started = True
            self._recover_async_jobs()

    def shutdown_async_processing(self, *, timeout: float = 1.0) -> None:
        with self._async_worker_lock:
            if not self._async_workers_started:
                return
            self._async_stop_event.set()
            for _ in self._async_workers:
                self._async_queue.put(None)
            for worker in self._async_workers:
                worker.join(timeout=timeout)
            self._async_workers = []
            self._async_workers_started = False
            with self._async_schedule_lock:
                self._scheduled_job_keys.clear()

    def _recover_async_jobs(self) -> None:
        assert self.async_job_store is not None
        for job_key, _ in self.async_job_store.incomplete_records():
            self._schedule_async_job(job_key)

    def _schedule_async_job(self, job_key: str) -> bool:
        with self._async_schedule_lock:
            if job_key in self._scheduled_job_keys:
                return False
            self._scheduled_job_keys.add(job_key)
        self._async_queue.put(job_key)
        return True

    def _conversation_lock(self, account_id: str, conversation_id: str) -> threading.Lock:
        key = f"{account_id}:{conversation_id}"
        with self._conversation_locks_guard:
            lock = self._conversation_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._conversation_locks[key] = lock
            return lock

    def _async_worker_loop(self) -> None:
        while not self._async_stop_event.is_set():
            job_key = self._async_queue.get()
            if job_key is None:
                self._async_queue.task_done()
                break
            try:
                self._run_async_job(job_key)
            except Exception:
                LOGGER.exception("Feishu async worker crashed for job=%s", job_key)
            finally:
                with self._async_schedule_lock:
                    self._scheduled_job_keys.discard(job_key)
                self._async_queue.task_done()

    def _run_async_job(self, job_key: str) -> None:
        assert self.async_job_store is not None
        record = self.async_job_store.get(job_key)
        if record is None or record.status in {"completed", "failed"}:
            return
        try:
            account = self._match_account(record.payload, account_id=record.account_id)
            assert self.adapter is not None
            inbound = self.adapter.normalize_event(
                record.payload,
                account_id=record.account_id,
                transport=record.transport,
            )
        except Exception as exc:
            failure_summary = str(exc).strip() or exc.__class__.__name__
            LOGGER.exception(
                "Feishu async job could not be reconstructed for account=%s conversation=%s",
                record.account_id,
                record.conversation_id,
            )
            self.async_job_store.fail(
                job_key,
                failure_summary=failure_summary,
                response_body={
                    **self._base_response_body(transport=record.transport),
                    "account_id": record.account_id,
                    "conversation_id": record.conversation_id,
                    "delivery_outcome": "failed",
                    "async_job_status": "failed",
                    "summary": failure_summary,
                },
            )
            return
        if self.async_job_store.has_earlier_incomplete_for_conversation(job_key):
            self._async_queue.put(job_key)
            return
        running_record = self.async_job_store.mark_running(job_key)
        if running_record is not None:
            record = running_record
        if not record.placeholder_sent and not inbound.sender.is_bot:
            try:
                self._send_placeholder_notice(job_key, account=account, inbound=inbound)
            except Exception:
                LOGGER.exception(
                    "Feishu async placeholder send failed for account=%s conversation=%s",
                    inbound.account_id,
                    inbound.conversation_id,
                )
        conversation_lock = self._conversation_lock(record.account_id, record.conversation_id)
        with conversation_lock:
            try:
                self.process_accepted_event(job_key, account=account, inbound=inbound)
            except Exception as exc:
                self._handle_async_job_failure(job_key, account=account, inbound=inbound, exc=exc)

    def _handle_async_job_failure(
        self,
        job_key: str,
        *,
        account: FeishuResolvedAccount,
        inbound: GatewayInboundMessage,
        exc: Exception,
    ) -> None:
        assert self.async_job_store is not None
        failure_summary = str(exc).strip() or exc.__class__.__name__
        LOGGER.exception(
            "Feishu async job failed for account=%s conversation=%s message=%s",
            inbound.account_id,
            inbound.conversation_id,
            inbound.event_id,
        )
        failure_response = {
            **self._base_response_body(transport="long-connection"),
            "account_id": inbound.account_id,
            "conversation_id": inbound.conversation_id,
            "delivery_outcome": "failed",
            "async_job_status": "failed",
            "summary": failure_summary,
        }
        try:
            self._send_failure_notice(account=account, inbound=inbound)
        except Exception:
            LOGGER.exception(
                "Feishu async failure notice send failed for account=%s conversation=%s",
                inbound.account_id,
                inbound.conversation_id,
            )
        self.async_job_store.fail(
            job_key,
            failure_summary=failure_summary,
            response_body=failure_response,
        )

    def _build_async_notice_outbound(
        self,
        inbound: GatewayInboundMessage,
        *,
        body: str,
        kind: str,
    ) -> GatewayOutboundMessage:
        return GatewayOutboundMessage(
            message_id=f"feishu-{kind}:{inbound.conversation_id}:{uuid4().hex[:12]}",
            account=inbound.account,
            conversation=inbound.conversation,
            session_id=f"{kind}:{inbound.conversation_id}",
            body=body,
            reply_to_message_id=inbound.event_id,
            attachment_refs=(),
            metadata={
                **dict(inbound.metadata),
                "delivery_surface": inbound.account.surface or f"feishu-{kind}",
                "runtime_surface": kind,
            },
        )

    def _send_placeholder_notice(
        self,
        job_key: str,
        *,
        account: FeishuResolvedAccount,
        inbound: GatewayInboundMessage,
    ) -> None:
        assert self.adapter is not None
        assert self.async_job_store is not None
        outbound = self._build_async_notice_outbound(
            inbound,
            body=self.async_placeholder_body,
            kind="async-placeholder",
        )
        delivery_request = self.adapter.build_reply_request(outbound)
        delivery_response = self._send_outbound(account, outbound, delivery_request)
        self.async_job_store.mark_placeholder_sent(
            job_key,
            placeholder_message_id=self._external_message_id(delivery_response),
        )

    def _send_failure_notice(
        self,
        *,
        account: FeishuResolvedAccount,
        inbound: GatewayInboundMessage,
    ) -> None:
        assert self.adapter is not None
        outbound = self._build_async_notice_outbound(
            inbound,
            body=self.async_failure_body,
            kind="async-failure",
        )
        delivery_request = self.adapter.build_reply_request(outbound)
        self._send_outbound(account, outbound, delivery_request)

    @property
    def event_paths(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(config.event_path for config in self.account_configs))

    @property
    def http_paths(self) -> tuple[str, ...]:
        return self.event_paths

    def handle_http_event(
        self,
        payload: Mapping[str, object],
        *,
        path: str,
    ) -> tuple[str, Mapping[str, object]]:
        try:
            result = self.dispatch_event(payload, transport="webhook")
        except LookupError as exc:
            return "503 Service Unavailable", {"ok": False, "error": str(exc)}
        except ValueError as exc:
            return "400 Bad Request", {"ok": False, "error": str(exc)}
        except RuntimeError as exc:
            return "502 Bad Gateway", {"ok": False, "error": str(exc)}
        payload_body = dict(result.response_body)
        if result.delivery_request is not None:
            payload_body["delivery_request_path"] = result.delivery_request.get("path", "")
        return "200 OK", payload_body

    def describe(self) -> Mapping[str, object]:
        async_summary = self._async_summary()
        accounts: list[dict[str, object]] = []
        for config in self.account_configs:
            status = "configured"
            resolved_app_id: str | None = None
            try:
                resolved = resolve_feishu_account(config, environ=self.environ)
                resolved_app_id = resolved.app_id
            except LookupError:
                status = "missing_credentials"
            accounts.append(
                {
                    "account_id": config.account_id,
                    "surface": config.surface,
                    "event_path": config.event_path,
                    "app_id_env_var": config.app_id_env_var,
                    "app_secret_env_var": config.app_secret_env_var,
                    "credential_env_vars": _credential_env_vars(config),
                    "secret_reference_ids": tuple(
                        reference.reference_id for reference in config.secret_references
                    ),
                    "credentials_source": (
                        "secret_references" if config.secret_references else "environment"
                    ),
                    "credentials_status": status,
                    "resolved_app_id": resolved_app_id,
                }
            )
        configured_transport: str | None = None
        configured_transport_error: str | None = None
        try:
            configured_transport = self.configured_transport()
        except (LookupError, ValueError) as exc:
            configured_transport_error = str(exc)
        return {
            "adapter_id": FEISHU_ADAPTER_ID,
            "profile_id": self.app.profile_id,
            "workspace_id": self.app.workspace_id,
            "preferred_transport": "long-connection",
            "implemented_transports": (
                "python-sdk-long-connection",
            ),
            "configured_transport": configured_transport,
            "configured_transport_error": configured_transport_error,
            "sdk_dependency_status": _lark_sdk_dependency_status(),
            "event_paths": self.event_paths,
            "accounts": tuple(accounts),
            "async_delivery_enabled": True,
            "queue_depth": async_summary.get("queue_depth", 0),
            "running_jobs": async_summary.get("running_jobs", 0),
            "worker_count": max(int(self.async_worker_count or 0), 1),
            "recent_failures": async_summary.get("recent_failures", ()),
            "control": (
                self.cli_control.describe()
                if self.cli_control is not None
                else {"enabled": True, "runtime": "cli-runtime", "runtime_status": "unavailable"}
            ),
        }

    def configured_transport(self) -> str:
        if not self.account_configs:
            return "long-connection"
        transports = tuple(
            dict.fromkeys(_normalize_transport(config.surface) for config in self.account_configs)
        )
        if len(transports) == 1:
            return transports[0]
        raise LookupError(
            "configured Feishu accounts use multiple transport surfaces; align their configured surfaces before starting the provider"
        )

    def configured_runtime_target(self) -> str:
        return self.configured_transport()

    def managed_runtime(
        self,
        *,
        args: Any,
        target: str,
    ) -> GatewayManagedRuntime:
        normalized_target = _normalize_configured_transport(target)
        state_dir = Path(args.state_dir)
        return GatewayManagedRuntime(
            service_key=self.service_key,
            runtime_id=f"{self.service_key}:{normalized_target}",
            target=normalized_target,
            label=f"Feishu {normalized_target} transport",
            pid_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="pid",
            ),
            log_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="log",
            ),
            record_path=default_gateway_runtime_path(
                state_dir,
                service_key=self.service_key,
                target=normalized_target,
                suffix="runtime.json",
            ),
        )

    def build_detached_runtime_command(
        self,
        *,
        args: Any,
        target: str,
    ) -> tuple[str, ...]:
        command = [
            os.sys.executable,
            "-m",
            "apps.launcher",
            "im",
            "feishu",
            "start",
        ]
        if args.account_id:
            command.append(str(args.account_id))
        command.extend(
            [
                "--transport",
                _normalize_configured_transport(target),
                "--profile-dir",
                str(args.profile_dir),
                "--state-dir",
                str(args.state_dir),
                "--cli-profile-dir",
                str(args.cli_profile_dir),
                "--cli-state-dir",
                str(args.cli_state_dir),
                "--workspace-id",
                str(args.workspace_id),
                "--host",
                str(args.host),
                "--port",
                str(args.port),
            ]
        )
        return tuple(command)

    def prepare_managed_runtime(self, *, action: str, target: str) -> None:
        if _normalize_configured_transport(target) != "long-connection":
            return
        if self.runtime_dependency_ensurer is None:
            return
        self.runtime_dependency_ensurer(
            reason=f"Feishu long-connection {action}",
        )

    def managed_runtime_log_hint(self, *, target: str) -> str:
        return "aegis gateway feishu logs <account-id> --follow"

    def accept_long_connection_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str | None = None,
    ) -> FeishuGatewayEventResult:
        challenge = payload.get("challenge")
        if challenge is not None and payload.get("event") is None:
            return FeishuGatewayEventResult(
                exchange=None,
                response_body={"ok": True, "challenge": str(challenge)},
            )

        account = self._match_account(payload, account_id=account_id)
        transport = "long-connection"
        response_body = self._base_response_body(transport=transport)
        assert self.adapter is not None
        assert self.async_job_store is not None
        inbound = self.adapter.normalize_event(
            payload,
            account_id=account.account_id,
            transport=transport,
        )
        raw_event_id, raw_message_id = _feishu_event_identifiers(payload)
        job_key, record, created = self.async_job_store.create_or_get(
            account_id=inbound.account_id,
            conversation_id=inbound.conversation_id,
            event_id=raw_event_id or inbound.metadata.get("event_id") or inbound.event_id,
            message_id=raw_message_id or _optional_text(inbound.metadata.get("message_id")),
            payload=payload,
            transport=transport,
        )
        if not created:
            if record.status == "completed" and record.response_body is not None:
                return self._duplicate_event_result(
                    inbound,
                    transport=transport,
                    response_body=record.response_body,
                )
            if record.status == "failed":
                return self._failed_duplicate_event_result(
                    inbound,
                    transport=transport,
                    failure_summary=record.failure_summary,
                )
            self._ensure_async_workers()
            self._schedule_async_job(job_key)
            return self._async_duplicate_event_result(
                inbound,
                transport=transport,
                status=record.status,
            )
        self._ensure_async_workers()
        self._schedule_async_job(job_key)
        response_body.update(
            {
                "account_id": inbound.account_id,
                "conversation_id": inbound.conversation_id,
                "delivery_outcome": "queued",
                "async_job_status": "queued",
                "summary": "Feishu event accepted and queued for async processing.",
            }
        )
        return FeishuGatewayEventResult(exchange=None, response_body=response_body)

    def process_accepted_event(
        self,
        job_key: str,
        *,
        account: FeishuResolvedAccount | None = None,
        inbound: GatewayInboundMessage | None = None,
    ) -> FeishuGatewayEventResult:
        assert self.async_job_store is not None
        assert self.inbound_event_store is not None
        record = self.async_job_store.get(job_key)
        if record is None:
            raise LookupError(f"unknown Feishu async job: {job_key}")
        if record.status == "completed" and record.response_body is not None:
            return FeishuGatewayEventResult(exchange=None, response_body=record.response_body)
        account = account or self._match_account(record.payload, account_id=record.account_id)
        assert self.adapter is not None
        inbound = inbound or self.adapter.normalize_event(
            record.payload,
            account_id=record.account_id,
            transport=record.transport,
        )
        response_body = self._base_response_body(transport=record.transport)
        if self.cli_control is not None:
            result = self._dispatch_cli_control(
                inbound,
                account=account,
                transport=record.transport,
                response_body=response_body,
                raise_on_error=True,
            )
        else:
            result = self._dispatch_shared_runtime(
                inbound,
                account=account,
                transport=record.transport,
                response_body=response_body,
            )
        external_message_id = _optional_text(result.response_body.get("external_message_id"))
        self.async_job_store.complete(
            job_key,
            response_body=result.response_body,
            external_message_id=external_message_id,
        )
        self.inbound_event_store.commit(
            account_id=inbound.account_id,
            event_id=record.event_id or inbound.event_id,
            message_id=record.message_id or _optional_text(inbound.metadata.get("message_id")),
            response_body=result.response_body,
        )
        return result

    def dispatch_event(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str | None = None,
        transport: str | None = None,
    ) -> FeishuGatewayEventResult:
        challenge = payload.get("challenge")
        if challenge is not None and payload.get("event") is None:
            return FeishuGatewayEventResult(
                exchange=None,
                response_body={"ok": True, "challenge": str(challenge)},
            )

        account = self._match_account(payload, account_id=account_id)
        resolved_transport = _normalize_transport(transport or account.config.surface)
        response_body = self._base_response_body(transport=resolved_transport)
        assert self.adapter is not None
        assert self.inbound_event_store is not None
        inbound = self.adapter.normalize_event(
            payload,
            account_id=account.account_id,
            transport=resolved_transport,
        )
        raw_event_id, raw_message_id = _feishu_event_identifiers(payload)
        dedupe_status, prior_record = self.inbound_event_store.begin(
            account_id=inbound.account_id,
            event_id=raw_event_id or inbound.event_id,
            message_id=raw_message_id or _optional_text(inbound.metadata.get("message_id")),
        )
        if dedupe_status == "duplicate" and prior_record is not None:
            return self._duplicate_event_result(
                inbound,
                transport=resolved_transport,
                response_body=prior_record.response_body,
            )
        if dedupe_status == "inflight":
            return self._inflight_duplicate_event_result(
                inbound,
                transport=resolved_transport,
            )
        try:
            if self.cli_control is not None:
                result = self._dispatch_cli_control(
                    inbound,
                    account=account,
                    transport=resolved_transport,
                    response_body=response_body,
                )
            else:
                result = self._dispatch_shared_runtime(
                    inbound,
                    account=account,
                    transport=resolved_transport,
                    response_body=response_body,
                )
        except Exception:
            self.inbound_event_store.abort(
                account_id=inbound.account_id,
                event_id=raw_event_id or inbound.event_id,
                message_id=raw_message_id or _optional_text(inbound.metadata.get("message_id")),
            )
            raise
        self.inbound_event_store.commit(
            account_id=inbound.account_id,
            event_id=raw_event_id or inbound.event_id,
            message_id=raw_message_id or _optional_text(inbound.metadata.get("message_id")),
            response_body=result.response_body,
        )
        return result

    def _base_response_body(self, *, transport: str) -> dict[str, object]:
        return {
            "ok": True,
            "adapter_id": FEISHU_ADAPTER_ID,
            "transport": transport,
        }

    def _dispatch_cli_control(
        self,
        inbound: GatewayInboundMessage,
        *,
        account: FeishuResolvedAccount,
        transport: str,
        response_body: Mapping[str, object],
        raise_on_error: bool = False,
    ) -> FeishuGatewayEventResult:
        assert self.cli_control is not None
        result = self.cli_control.handle_message(inbound)
        if raise_on_error and result.summary == "control error":
            raise RuntimeError(result.body or "cli control error")
        enriched_response = {
            **dict(response_body),
            "account_id": inbound.account_id,
            "conversation_id": inbound.conversation_id,
            "control_mode": "cli-runtime",
            "delivery_outcome": "ignored" if result.body is None else "delivered",
            "summary": result.summary or "",
        }
        if result.clone_id is not None:
            enriched_response["clone_id"] = result.clone_id
        if result.session_id is not None:
            enriched_response["session_id"] = result.session_id
        if result.body is None:
            return FeishuGatewayEventResult(exchange=None, response_body=enriched_response)
        outbound = self._build_control_outbound(inbound, body=result.body, session_id=result.session_id)
        return self._deliver_outbound_result(
            account,
            outbound,
            exchange=None,
            response_body=enriched_response,
        )

    def _dispatch_shared_runtime(
        self,
        inbound: GatewayInboundMessage,
        *,
        account: FeishuResolvedAccount,
        transport: str,
        response_body: Mapping[str, object],
    ) -> FeishuGatewayEventResult:
        exchange = self.app.handle_message(
            inbound,
            reply_to_message_id=inbound.event_id,
            attachment_refs=inbound.attachment_refs,
            metadata={
                **dict(inbound.metadata),
                "delivery_surface": inbound.account.surface or f"feishu-{transport}",
            },
        )
        enriched_response = {
            **dict(response_body),
            "account_id": exchange.route.inbound.account_id,
            "conversation_id": exchange.route.inbound.conversation_id,
            "session_id": exchange.route.session.session_id,
            "policy_decision": str(exchange.delivery.policy_result.decision),
            "delivery_outcome": exchange.delivery.outcome,
        }
        if exchange.delivery.outbound is None:
            enriched_response["summary"] = exchange.delivery.summary
            return FeishuGatewayEventResult(exchange=exchange, response_body=enriched_response)
        return self._deliver_outbound_result(
            account,
            exchange.delivery.outbound,
            exchange=exchange,
            response_body=enriched_response,
        )

    def _deliver_outbound_result(
        self,
        account: FeishuResolvedAccount,
        outbound: GatewayOutboundMessage,
        *,
        exchange: GatewayExchange | None,
        response_body: Mapping[str, object],
    ) -> FeishuGatewayEventResult:
        assert self.adapter is not None
        delivery_request = self.adapter.build_reply_request(outbound)
        delivery_response = self._send_outbound(account, outbound, delivery_request)
        enriched_response = {
            **dict(response_body),
            "external_message_id": self._external_message_id(delivery_response),
        }
        return FeishuGatewayEventResult(
            exchange=exchange,
            response_body=enriched_response,
            delivery_request=delivery_request,
            delivery_response=delivery_response,
        )

    def _duplicate_event_result(
        self,
        inbound: GatewayInboundMessage,
        *,
        transport: str,
        response_body: Mapping[str, object],
    ) -> FeishuGatewayEventResult:
        duplicate_response = dict(response_body)
        previous_outcome = _optional_text(duplicate_response.get("delivery_outcome"))
        if previous_outcome is not None:
            duplicate_response["initial_delivery_outcome"] = previous_outcome
        duplicate_response["ok"] = True
        duplicate_response["adapter_id"] = FEISHU_ADAPTER_ID
        duplicate_response["transport"] = transport
        duplicate_response["account_id"] = inbound.account_id
        duplicate_response["conversation_id"] = inbound.conversation_id
        duplicate_response["delivery_outcome"] = "deduplicated"
        duplicate_response["duplicate_event"] = True
        duplicate_response["duplicate_handling"] = "replayed-no-delivery"
        duplicate_response["summary"] = (
            "Duplicate Feishu event ignored; the original event was already processed."
        )
        return FeishuGatewayEventResult(exchange=None, response_body=duplicate_response)

    def _inflight_duplicate_event_result(
        self,
        inbound: GatewayInboundMessage,
        *,
        transport: str,
    ) -> FeishuGatewayEventResult:
        response_body = self._base_response_body(transport=transport)
        response_body.update(
            {
                "account_id": inbound.account_id,
                "conversation_id": inbound.conversation_id,
                "delivery_outcome": "deduplicating",
                "duplicate_event": True,
                "duplicate_handling": "inflight",
                "summary": "Duplicate Feishu event is already being processed.",
            }
        )
        return FeishuGatewayEventResult(exchange=None, response_body=response_body)

    def _async_duplicate_event_result(
        self,
        inbound: GatewayInboundMessage,
        *,
        transport: str,
        status: str,
    ) -> FeishuGatewayEventResult:
        response_body = self._base_response_body(transport=transport)
        summary = {
            "queued": "Duplicate Feishu event is queued for async processing.",
            "running": "Duplicate Feishu event is already being processed asynchronously.",
        }.get(status, "Duplicate Feishu event is already being handled asynchronously.")
        delivery_outcome = "processing" if status == "running" else "queued"
        response_body.update(
            {
                "account_id": inbound.account_id,
                "conversation_id": inbound.conversation_id,
                "delivery_outcome": delivery_outcome,
                "async_job_status": status,
                "duplicate_event": True,
                "duplicate_handling": status,
                "summary": summary,
            }
        )
        return FeishuGatewayEventResult(exchange=None, response_body=response_body)

    def _failed_duplicate_event_result(
        self,
        inbound: GatewayInboundMessage,
        *,
        transport: str,
        failure_summary: str | None,
    ) -> FeishuGatewayEventResult:
        response_body = self._base_response_body(transport=transport)
        response_body.update(
            {
                "account_id": inbound.account_id,
                "conversation_id": inbound.conversation_id,
                "delivery_outcome": "failed",
                "async_job_status": "failed",
                "duplicate_event": True,
                "duplicate_handling": "failed",
                "summary": failure_summary or "Feishu event previously failed and will not auto-retry.",
            }
        )
        return FeishuGatewayEventResult(exchange=None, response_body=response_body)

    def _external_message_id(self, response: Mapping[str, object]) -> str:
        data = _mapping(response.get("data")) or {}
        return str(data.get("message_id") or "")

    def build_long_connection_client(
        self,
        *,
        account_id: str | None = None,
        lark_module: Any | None = None,
        client_factory: FeishuWSClientFactory = _default_ws_client_factory,
        log_level: str = "INFO",
    ) -> object:
        if account_id is None and len(self.account_configs) != 1:
            raise LookupError(
                "long-connection mode requires an explicit account id when multiple Feishu accounts are configured"
            )
        account = self._match_account({}, account_id=account_id)
        self._ensure_async_workers()
        lark = _load_lark_sdk(lark_module)
        handler = self._build_long_connection_handler(
            account=account,
            lark_module=lark,
            log_level=log_level,
        )
        return client_factory(
            lark,
            account.app_id,
            account.app_secret,
            handler,
            _lark_log_level(lark, log_level),
        )

    def start_long_connection(
        self,
        *,
        account_id: str | None = None,
        lark_module: Any | None = None,
        client_factory: FeishuWSClientFactory = _default_ws_client_factory,
        log_level: str = "INFO",
    ) -> object:
        client = self.build_long_connection_client(
            account_id=account_id,
            lark_module=lark_module,
            client_factory=client_factory,
            log_level=log_level,
        )
        start = getattr(client, "start", None)
        if not callable(start):
            raise RuntimeError("feishu long-connection client does not expose start()")
        start()
        return client

    def _build_control_outbound(
        self,
        inbound: GatewayInboundMessage,
        *,
        body: str,
        session_id: str | None,
    ) -> GatewayOutboundMessage:
        return GatewayOutboundMessage(
            message_id=f"feishu-control:{session_id or inbound.conversation_id}:{uuid4().hex[:12]}",
            account=inbound.account,
            conversation=inbound.conversation,
            session_id=session_id or f"control:{inbound.conversation_id}",
            body=body,
            reply_to_message_id=inbound.event_id,
            attachment_refs=(),
            metadata={
                **dict(inbound.metadata),
                "delivery_surface": inbound.account.surface or "feishu-control",
                "runtime_surface": "cli-runtime",
            },
        )

    def _build_long_connection_handler(
        self,
        *,
        account: FeishuResolvedAccount,
        lark_module: Any,
        log_level: str,
    ) -> object:
        dispatcher = getattr(lark_module, "EventDispatcherHandler", None)
        if dispatcher is None or not hasattr(dispatcher, "builder"):
            raise RuntimeError("lark_oapi EventDispatcherHandler builder is unavailable")

        def _handle_message(event: object) -> None:
            payload = _lark_event_payload(event, lark_module=lark_module)
            self.accept_long_connection_event(
                payload,
                account_id=account.account_id,
            )

        builder = dispatcher.builder("", "", _lark_log_level(lark_module, log_level))
        builder = builder.register_p2_im_message_receive_v1(_handle_message)
        return builder.build()

    def _match_account(
        self,
        payload: Mapping[str, object],
        *,
        account_id: str | None = None,
    ) -> FeishuResolvedAccount:
        if not self.account_configs:
            raise LookupError("no Feishu gateway accounts are configured")
        if account_id is not None:
            for config in self.account_configs:
                if config.account_id == account_id:
                    return resolve_feishu_account(config, environ=self.environ)
            raise LookupError(f"unknown Feishu gateway account: {account_id}")

        header_payload = _mapping(payload.get("header")) or {}
        event_app_id = str(header_payload.get("app_id") or "")
        if event_app_id:
            matches: list[FeishuResolvedAccount] = []
            for config in self.account_configs:
                try:
                    resolved = resolve_feishu_account(config, environ=self.environ)
                except LookupError:
                    continue
                if resolved.app_id == event_app_id:
                    matches.append(resolved)
            if len(matches) == 1:
                return matches[0]

        if len(self.account_configs) == 1:
            return resolve_feishu_account(self.account_configs[0], environ=self.environ)
        raise LookupError("could not match Feishu event to a configured gateway account")

    def _tenant_access_token(self, account: FeishuResolvedAccount) -> str:
        cached = self._token_cache.get(account.account_id)
        now = time.time()
        if cached is not None and cached.expires_at - 60 > now:
            return cached.token
        response = self.http_requester(
            "POST",
            f"{account.config.base_url}{account.config.token_path}",
            {
                "app_id": account.app_id,
                "app_secret": account.app_secret,
            },
            {},
        )
        token = str(response.get("tenant_access_token") or "")
        if not token:
            raise RuntimeError("feishu token response did not include tenant_access_token")
        expires_in = int(response.get("expire", 7200) or 7200)
        self._token_cache[account.account_id] = _FeishuTokenCacheEntry(
            token=token,
            expires_at=now + expires_in,
        )
        return token

    def _send_outbound(
        self,
        account: FeishuResolvedAccount,
        outbound: GatewayOutboundMessage,
        delivery_request: Mapping[str, object],
    ) -> Mapping[str, object]:
        path = str(delivery_request.get("path") or "")
        method = str(delivery_request.get("method") or "POST")
        body = _mapping(delivery_request.get("body"))
        if not path or body is None:
            raise RuntimeError("feishu delivery request is missing a path or body payload")
        token = self._tenant_access_token(account)
        return self.http_requester(
            method,
            f"{account.config.base_url}{path}",
            body,
            {"Authorization": f"Bearer {token}"},
        )

def register_feishu_gateway_service(registry: GatewayPluginRegistry) -> GatewayPluginRegistry:
    registry.register_service(
        "feishu",
        factory=lambda app, **kwargs: FeishuGatewayService(app=app, **kwargs),
        enabled_by_default=True,
    )
    return registry

def build_feishu_gateway_service(
    *,
    profile_id: str = "profile:default",
    workspace_id: str | None = None,
    provider_profile: Mapping[str, Any] | None = None,
    profile_dir: str | None = None,
    state_dir: str | None = None,
    default_cli_profile_dir: str | Path | None = None,
    default_cli_state_dir: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
    http_requester: HttpJsonRequester = _default_json_request,
    plugin_registry: GatewayPluginRegistry | None = None,
) -> FeishuGatewayService:
    app, _, _ = build_gateway_app(
        profile_id=profile_id,
        workspace_id=workspace_id,
        provider_profile=provider_profile,
        profile_dir=profile_dir,
        state_dir=state_dir,
        plugin_registry=plugin_registry,
    )
    return FeishuGatewayService(
        app=app,
        http_requester=http_requester,
        environ=dict(environ or os.environ),
        default_cli_profile_dir=(
            None if default_cli_profile_dir is None else str(Path(default_cli_profile_dir))
        ),
        default_cli_state_dir=(
            None if default_cli_state_dir is None else str(Path(default_cli_state_dir))
        ),
    )

def create_gateway_web_app(service: FeishuGatewayService):
    return create_gateway_http_app(service, app=service.app)



__all__ = [
    "DEFAULT_FEISHU_APP_ID_ENV",
    "DEFAULT_FEISHU_APP_SECRET_ENV",
    "LEGACY_FEISHU_APP_ID_ENV",
    "LEGACY_FEISHU_APP_SECRET_ENV",
    "DEFAULT_FEISHU_EVENT_PATH",
    "DEFAULT_FEISHU_BASE_URL",
    "DEFAULT_FEISHU_TOKEN_PATH",
    "SUPPORTED_FEISHU_TRANSPORTS",
    "FeishuGatewayAccountConfig",
    "FeishuGatewayEventResult",
    "FeishuGatewayService",
    "FeishuResolvedAccount",
    "build_feishu_gateway_service",
    "create_gateway_web_app",
    "load_feishu_gateway_accounts",
    "register_feishu_gateway_service",
    "resolve_feishu_account",
]
