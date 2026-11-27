import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from temporalio.service import TLSConfig

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.core.config.config_discovery import normalize_temporal_url  # noqa: F401
from mistralai.workflows.core.temporal.temporal_client import _get_proxy_basic_auth  # noqa: F401

# Import regression — fail at collection time if any internal path moves.
from mistralai.workflows.core.worker_client import get_worker_client  # noqa: F401
from mistralai.workflows.scripts.diagnose import (
    _check_connectivity,
    _check_mistral_api,
    _check_whoami,
    _env_vars_from_models,
    _print_activities,
    _print_config,
    _print_env_vars,
)

from .subprocess_helpers import run_python

_WORKFLOWS_MODULE = """
import os

from mistralai.workflows import workflow

os.environ.update(MODULE_ENVIRONMENT)

@workflow.define(name="inherited")
class InheritedWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"

@workflow.define(name="explicit", enforce_determinism=False)
class ExplicitWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"
"""

_DIAGNOSE_SCRIPT = """
import io
import json
import sys
from contextlib import redirect_stdout
from unittest.mock import AsyncMock, patch

from mistralai.workflows.scripts.diagnose import main

sys.argv = ["wf-diagnose", "diagnostic_workflows"]
output = io.StringIO()
with redirect_stdout(output), patch(
    "mistralai.workflows.scripts.diagnose._check_connectivity", new_callable=AsyncMock
):
    main()
report = output.getvalue()
section = report.split("REGISTERED WORKFLOWS", 1)[1].split("REGISTERED ACTIVITIES", 1)[0]
rows, _ = json.JSONDecoder().raw_decode(section[section.index("["):])
print(json.dumps({
    "failed": "Configuration failed to load" in section,
    "workflows": {row["name"]: row["enforce_determinism"] for row in rows},
}))
"""


def _diagnose(tmp_path: Path, env: dict[str, str], module_environment: dict[str, str] | None = None) -> dict:
    (tmp_path / "diagnostic_workflows.py").write_text(
        f"MODULE_ENVIRONMENT = {module_environment or {}!r}\n" + _WORKFLOWS_MODULE
    )
    base = {name: value for name, value in os.environ.items() if name not in {"WORKFLOW_NAME_PREFIX", "VERSIONING"}}
    result = run_python(_DIAGNOSE_SCRIPT, cwd=tmp_path, env={**base, **env})
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


class TestDiagnosticStartup:
    @pytest.mark.parametrize("default_determinism", [True, False])
    def test_reports_the_settings_a_worker_registers(self, tmp_path: Path, default_determinism: bool) -> None:
        report = _diagnose(
            tmp_path,
            {"WORKFLOW_NAME_PREFIX": "prod_", "DEFAULT_ENFORCE_DETERMINISM": str(default_determinism).lower()},
        )

        assert report == {
            "failed": False,
            "workflows": {"prod_inherited": default_determinism, "prod_explicit": False},
        }

    def test_reports_settings_the_user_module_sets(self, tmp_path: Path) -> None:
        report = _diagnose(tmp_path, {}, module_environment={"WORKFLOW_NAME_PREFIX": "loaded_"})

        assert report["workflows"] == {"loaded_inherited": True, "loaded_explicit": False}

    @pytest.mark.parametrize(
        ("name", "value"), [("BLOB_STORAGE_CONFIGS", "not-json"), ("WORKER_AUTO_REGISTER_AS_CURRENT", "notabool")]
    )
    def test_reports_sdk_defaults_when_configuration_fails(self, tmp_path: Path, name: str, value: str) -> None:
        report = _diagnose(tmp_path, {"WORKFLOW_NAME_PREFIX": "prod_", name: value})

        assert report == {"failed": True, "workflows": {"inherited": True, "explicit": False}}


class TestEnvVarsFromModels:
    def test_includes_all_critical_vars(self):
        vars_ = set(_env_vars_from_models())
        assert "MISTRAL_API_KEY" in vars_
        assert "MISTRAL_CLIENT_API_KEY" in vars_
        assert "SERVER_URL" in vars_
        assert "DEPLOYMENT_NAME" in vars_
        assert "CA_BUNDLE" in vars_
        assert "TEMPORAL_SERVER_URL" in vars_
        assert "KUBERNETES_SERVICE_HOST" in vars_
        assert "MAX_ACTIVITY_TASK_POLLERS" in vars_
        assert "MAX_CONCURRENT_ACTIVITIES" in vars_
        assert "MAX_WORKFLOW_TASK_POLLERS" in vars_
        assert "TEMPORAL_TASK_QUEUE" not in vars_


class TestPrintConfig:
    def test_includes_key_config_fields(self, capsys):
        from mistralai.workflows.core.config.config import AppConfig

        _print_config(AppConfig())
        output = capsys.readouterr().out
        assert "server_url" in output
        assert "deployment_name" in output
        assert "task_queue" not in output
        assert "max_concurrent_activities" in output

    def test_secret_values_are_redacted(self, capsys, monkeypatch):
        monkeypatch.setenv("MISTRAL_API_KEY", "super-secret-value")
        from mistralai.workflows.core.config.config import AppConfig

        _print_config(AppConfig())
        output = capsys.readouterr().out
        assert "super-secret-value" not in output
        assert "***" in output

    def test_proxy_credentials_are_redacted(self, capsys):
        from mistralai.workflows.core.config.config import AppConfig

        cfg = AppConfig()
        cfg.http.proxy = "http://user:S3cret@corp-proxy:3128"
        cfg.http.routes = {"all://*.eu.corp": {"proxy": "http://ruser:rpass@eu-proxy:3128"}}

        _print_config(cfg)
        output = capsys.readouterr().out
        assert "S3cret" not in output
        assert "rpass" not in output
        assert "http://***@corp-proxy:3128" in output


class TestPrintEnvVars:
    def test_masks_secret_vars(self, capsys, monkeypatch):
        monkeypatch.setenv("MISTRAL_API_KEY", "should-not-appear")
        _print_env_vars()
        output = capsys.readouterr().out
        assert "should-not-appear" not in output
        assert "*** (set)" in output


class TestPrintActivities:
    def test_uses_configured_poller_counts(self, capsys):
        from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import (
            set_activity_as_sticky_to_worker,
        )
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        async def first_rate_limited_activity():
            pass

        async def second_rate_limited_activity():
            pass

        async def sticky_activity():
            pass

        set_rate_limit(first_rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))
        set_rate_limit(second_rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=2, key="shared"))
        set_activity_as_sticky_to_worker(sticky_activity)

        config = MagicMock()
        config.get_effective_task_queue.return_value = "main-queue"
        config.worker.max_activity_task_pollers = 2
        config.worker.max_workflow_task_pollers = 5
        config.worker.connection_stream_limit = 100

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=[first_rate_limited_activity, second_rate_limited_activity, sticky_activity],
        ):
            _print_activities(config)

        output = capsys.readouterr().out
        assert "distinct rate-limit keys: 1  ['shared']" in output
        assert "rate-limit workers      : 2" in output
        assert "internal workers        : 4  (1 main + 1 sticky + 2 rate-limited)" in output
        assert (
            "min poll streams        : 13  (4 workers × 2 activity + 1 main × 5 workflow; "
            "respond/heartbeat streams not included)"
        ) in output
        assert "stream headroom         : 87 of 100" in output
        assert "namespace" not in output

    def test_warns_above_poll_stream_threshold(self, capsys):
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        rate_limited_activities = []
        for key in range(19):

            async def rate_limited_activity():
                pass

            set_rate_limit(rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key=f"key-{key}"))
            rate_limited_activities.append(rate_limited_activity)

        config = MagicMock()
        config.get_effective_task_queue.return_value = "main-queue"
        config.worker.max_activity_task_pollers = 5
        config.worker.max_workflow_task_pollers = 5
        config.worker.connection_stream_limit = 100

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=rate_limited_activities,
        ):
            _print_activities(config)

        output = capsys.readouterr().out
        assert "WARNING" in output
        # 5 workflow + 5 activity polls on the main worker + 19 rate-limited workers × 5 = 105
        assert "105" in output
        assert "rate-limit keys" in output
        assert "MAX_ACTIVITY_TASK_POLLERS" in output
        assert "poll streams only" in output
        assert "stream headroom         : -5 of 100" in output
        assert "namespace" not in output

    def test_does_not_warn_with_lower_activity_pollers(self, capsys):
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        rate_limited_activities = []
        for key in range(19):

            async def rate_limited_activity():
                pass

            set_rate_limit(rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key=f"key-{key}"))
            rate_limited_activities.append(rate_limited_activity)

        config = MagicMock()
        config.get_effective_task_queue.return_value = "main-queue"
        config.worker.max_activity_task_pollers = 2
        config.worker.max_workflow_task_pollers = 5
        config.worker.connection_stream_limit = 100

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=rate_limited_activities,
        ):
            _print_activities(config)

        output = capsys.readouterr().out
        # 5 + 2 polls on the main worker + 19 rate-limited workers × 2 = 45
        assert "min poll streams        : 45" in output
        assert "stream headroom         : 55 of 100" in output
        assert "WARNING" not in output
        assert "namespace" not in output

    def test_does_not_warn_when_no_connection_stream_limit_is_configured(self, capsys):
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        rate_limited_activities = []
        for key in range(19):

            async def rate_limited_activity():
                pass

            set_rate_limit(rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key=f"key-{key}"))
            rate_limited_activities.append(rate_limited_activity)

        config = MagicMock()
        config.get_effective_task_queue.return_value = "main-queue"
        config.worker.max_activity_task_pollers = 5
        config.worker.max_workflow_task_pollers = 5
        config.worker.connection_stream_limit = None

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=rate_limited_activities,
        ):
            _print_activities(config)

        output = capsys.readouterr().out
        assert "min poll streams        : 105" in output
        assert "stream headroom         : no connection stream limit configured" in output
        assert "WARNING" not in output

    def test_still_prints_the_summary_when_the_worker_config_is_unavailable(self, capsys):
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        async def rate_limited_activity():
            pass

        set_rate_limit(rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="only-key"))

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=[rate_limited_activity],
        ):
            _print_activities(RuntimeError("config failed to load"))

        output = capsys.readouterr().out
        assert "distinct rate-limit keys: 1  ['only-key']" in output
        assert "internal workers        : 2  (1 main + 0 sticky + 1 rate-limited)" in output
        assert "min poll streams        : unknown (worker config unavailable)" in output
        assert "ERROR" not in output

    def test_lists_a_key_shared_across_rates_once_and_hints_at_aligning_rates(self, capsys):
        from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit

        async def first_activity():
            pass

        async def second_activity():
            pass

        set_rate_limit(first_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))
        set_rate_limit(second_activity, RateLimit(time_window_in_sec=1, max_execution=2, key="shared"))

        config = MagicMock()
        config.get_effective_task_queue.return_value = "main-queue"
        config.worker.max_activity_task_pollers = 30
        config.worker.max_workflow_task_pollers = 5
        config.worker.connection_stream_limit = 100

        with patch(
            "mistralai.workflows.core.activity.get_all_temporal_activities",
            return_value=[first_activity, second_activity],
        ):
            _print_activities(config)

        output = capsys.readouterr().out
        assert "distinct rate-limit keys: 1  ['shared']" in output
        assert "rate-limit keys [shared]" in output
        assert "shared, shared" not in output
        assert "different rates" in output


class TestCheckMistralApi:
    @pytest.mark.asyncio
    async def test_reports_fail_on_network_error(self, capsys):
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=MISTRAL_HTTP.ConnectError("unreachable"))

        with patch.object(MISTRAL_HTTP, "AsyncClient", return_value=mock_client):
            await _check_mistral_api("https://api.mistral.ai", None)

        assert "[FAIL]" in capsys.readouterr().out


class TestCheckWhoami:
    @pytest.mark.asyncio
    async def test_returns_whoami_on_success(self):
        mock_whoami = MagicMock()
        mock_whoami.model_dump.return_value = {"worker_id": "w1", "tls": False}
        mock_wc = AsyncMock()
        mock_wc.__aenter__ = AsyncMock(return_value=mock_wc)
        mock_wc.__aexit__ = AsyncMock(return_value=None)
        mock_wc.whoami_async = AsyncMock(return_value=mock_whoami)

        with (
            patch("mistralai.workflows.core.worker_client.get_worker_client", return_value=mock_wc),
            patch("mistralai.workflows.client.translate_model", return_value=mock_whoami),
        ):
            result = await _check_whoami("https://api.mistral.ai", "key")

        assert result is mock_whoami

    @pytest.mark.asyncio
    async def test_returns_none_and_prints_fail_on_error(self, capsys):
        with patch(
            "mistralai.workflows.core.worker_client.get_worker_client", side_effect=Exception("connection failed")
        ):
            result = await _check_whoami("https://api.mistral.ai", None)

        assert result is None
        assert "[FAIL]" in capsys.readouterr().out


class TestCheckConnectivityTlsRootCa:
    @staticmethod
    async def _run(monkeypatch, ca_path: str, *, whoami_tls: bool, env_tls: str | None):
        from mistralai.workflows.core.config.config import AppConfig

        monkeypatch.setenv("TEMPORAL_TLS_SERVER_ROOT_CA_CERT_PATH", ca_path)
        if env_tls is None:
            monkeypatch.delenv("TEMPORAL_TLS", raising=False)
        else:
            monkeypatch.setenv("TEMPORAL_TLS", env_tls)

        whoami = MagicMock(scheduler_url="temporal.example.com:7233", tls=whoami_tls)
        check_temporal = AsyncMock()
        with (
            patch("mistralai.workflows.scripts.diagnose._check_mistral_api", AsyncMock()),
            patch("mistralai.workflows.scripts.diagnose._check_whoami", AsyncMock(return_value=whoami)),
            patch("mistralai.workflows.scripts.diagnose._check_temporal", check_temporal),
        ):
            await _check_connectivity(AppConfig())
        return check_temporal

    @pytest.mark.asyncio
    async def test_local_tls_setting_wins_over_whoami(self, monkeypatch, ca_file):
        # `adopt_remote_default` keeps an explicit TEMPORAL_TLS, so the worker pins the CA here;
        # diagnose must report on the same connection the worker would open.
        check_temporal = await self._run(monkeypatch, ca_file(), whoami_tls=False, env_tls="true")

        assert isinstance(check_temporal.await_args.args[1], TLSConfig)

    @pytest.mark.asyncio
    async def test_unusable_ca_skips_the_connection_check(self, monkeypatch, ca_file, capsys):
        check_temporal = await self._run(monkeypatch, ca_file(write=False), whoami_tls=True, env_tls=None)

        output = capsys.readouterr().out
        assert "[FAIL] Temporal TLS setup" in output
        assert "[SKIP]" in output
        check_temporal.assert_not_awaited()
