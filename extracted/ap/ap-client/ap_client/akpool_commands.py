"""``ap akpool`` 命令族 —— Account Pool(托管 AK)观测操作。

* ``akpool rpm get`` → apiserver ``GET /apis/v1/model-api-keys/rpm-usage``
  (中心侧,走 ``APIClient._get_central``),按 AK + 模型查询当前 RPM 用量与上限。

AK 的两种指定方式互斥且必填其一:``--ak-id``(uak-xxx,仅平台托管 AK)或
``--masked-ak``(掩码后 6 位,未托管 AK 走这条路)。服务端同口径(都缺或都给 →
400),CLI 侧先拦一道,不发请求。``--time-range`` 是 Go duration 风格
(``30s``/``5m``/``1h``);显式 ``--from``/``--to``(RFC3339)时覆盖
``--time-range``。

响应是嵌套结构(无信封):``usage.current_rpm``/``usage.sampled_at``、
``rpm.limit``/``rpm.limit_state``/``rpm.synced_at``、``usage_status``、
``time_range``、``ak_id``/``masked_api_key``/``model_id``。json/yaml 原样透传;
plain/table 摊平成单行 key=value 展示。
"""

from __future__ import annotations

import re
from typing import Any, Optional

import typer
from ap_client import get_client

__all__ = ["akpool_app", "register"]

akpool_app = typer.Typer(help="Account Pool operations (managed API keys)")
rpm_app = typer.Typer(help="Account Pool RPM usage operations")

akpool_app.add_typer(rpm_app, name="rpm")


def register(app: typer.Typer) -> None:
    """把 ``akpool`` 挂到 ``ap`` 根命令上。"""
    app.add_typer(akpool_app, name="akpool")


_FORMAT_HELP = "Output format: plain/table/json/yaml (default: AP_FORMAT or command default)"
_TIME_RANGE_HELP = "Lookback window for the RPM reading (Go duration, e.g. 30s/5m/1h)"
_ISO_TIME_HELP = "RFC3339 timestamp, e.g. 2026-09-21T12:00:00+08:00"

_TIME_RANGE_RE = re.compile(r"^\d+[smh]$")

#: plain/table 输出的字段顺序,取值自嵌套响应(见 _flatten_rpm)。
_RPM_KEYS = (
    "current_rpm",
    "rpm_limit",
    "model",
    "sampled_at",
    "time_range",
    "ak_id",
    "usage_status",
)


def _fmt(output_format: Optional[str]) -> str:
    from .cli import _normalize_output_format

    return _normalize_output_format(output_format, keep_table=True)


def _check_time_range(value: str) -> str:
    normalized = str(value or "").strip().lower()
    if not _TIME_RANGE_RE.fullmatch(normalized):
        raise typer.BadParameter(f"--time-range must be a duration like 30s/5m/1h, got {value!r}")
    return normalized


def _flatten_rpm(payload: dict) -> dict:
    """把嵌套的 rpm-usage 响应摊平成 plain/table 展示用的扁平 dict。

    null 值渲染为 ``-``(如未托管 AK 的 ``ak_id``、未知限额的 ``rpm.limit``)。
    """
    rpm = payload.get("rpm")
    usage = payload.get("usage")
    flat = {
        "current_rpm": usage.get("current_rpm") if isinstance(usage, dict) else None,
        "rpm_limit": rpm.get("limit") if isinstance(rpm, dict) else None,
        "model": payload.get("model_id"),
        "sampled_at": usage.get("sampled_at") if isinstance(usage, dict) else None,
        "time_range": payload.get("time_range"),
        "ak_id": payload.get("ak_id"),
        "usage_status": payload.get("usage_status"),
    }
    return {key: (value if value is not None else "-") for key, value in flat.items()}


def _emit_rpm(payload: Any, output_format: str) -> None:
    from .cli import _print_formatted, _print_rich_table

    if not isinstance(payload, dict):
        payload = {"value": payload}
    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
        return
    flat = _flatten_rpm(payload)
    keys = [key for key in _RPM_KEYS if key in flat]
    keys += [key for key in flat if key not in keys]
    if output_format == "table":
        _print_rich_table([flat], [(key, key) for key in keys])
        return
    _print_rpm_plain(payload)


def _print_rpm_plain(payload: dict) -> None:
    """plain 输出：标题行(usage_status) + 对齐 key/value，与 _print_job_get_plain 同风格。

    current_rpm 在限额已知时附利用率百分比；rpm_limit 未知/不限时展示 limit_state。
    ak_id / masked_api_key 为 null(未托管 AK)时整行省略。
    """
    from .cli import _print_key_values

    rpm = payload.get("rpm")
    usage = payload.get("usage")
    rpm = rpm if isinstance(rpm, dict) else {}
    usage = usage if isinstance(usage, dict) else {}

    current = usage.get("current_rpm")
    limit = rpm.get("limit")
    limit_state = rpm.get("limit_state") or "unknown"

    if isinstance(current, (int, float)) and isinstance(limit, (int, float)) and limit > 0:
        current_text = f"{current} ({current / limit * 100:.1f}% of limit)"
    else:
        current_text = current
    limit_text = f"{limit} ({limit_state})" if limit is not None else limit_state

    typer.echo(f"AK RPM Usage ({payload.get('usage_status') or 'unknown'})")
    _print_key_values(
        [
            ("current_rpm", current_text),
            ("rpm_limit", limit_text),
            ("model", payload.get("model_id")),
            ("ak_id", payload.get("ak_id")),
            ("masked_api_key", payload.get("masked_api_key")),
            ("sampled_at", usage.get("sampled_at")),
            ("time_range", payload.get("time_range")),
        ]
    )


@rpm_app.command("get")
def rpm_get(
    ak_id: Optional[str] = typer.Option(
        None, "--ak-id", help="Managed AK ID (uak-xxx); mutually exclusive with --masked-ak"
    ),
    masked_ak: Optional[str] = typer.Option(
        None, "--masked-ak", help="Last 6 characters of the AK; mutually exclusive with --ak-id"
    ),
    model: str = typer.Option(..., "--model", help="Model the RPM reading applies to"),
    time_range: str = typer.Option("5m", "--time-range", help=_TIME_RANGE_HELP),
    from_time: Optional[str] = typer.Option(
        None, "--from", help=f"Window start ({_ISO_TIME_HELP}); overrides --time-range"
    ),
    to_time: Optional[str] = typer.Option(
        None, "--to", help=f"Window end ({_ISO_TIME_HELP}); overrides --time-range"
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Show the current RPM usage and limit of a managed AK for one model."""
    resolved_ak_id = (ak_id or "").strip()
    resolved_masked_ak = (masked_ak or "").strip()
    if bool(resolved_ak_id) == bool(resolved_masked_ak):
        raise typer.BadParameter("exactly one of --ak-id or --masked-ak is required")
    if not model.strip():
        raise typer.BadParameter("--model must not be empty")
    normalized_range = _check_time_range(time_range)
    output_format = _fmt(output_format)

    result = get_client().get_akpool_rpm(
        model=model.strip(),
        ak_id=resolved_ak_id or None,
        masked_ak=resolved_masked_ak or None,
        time_range=normalized_range,
        from_time=from_time,
        to_time=to_time,
    )
    _emit_rpm(result, output_format)
