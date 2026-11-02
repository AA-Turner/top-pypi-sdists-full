"""Dataset registry commands.

Metadata queries and split release workflows use APIClient. Version creation
uses the optional InstanceRepo SDK to calculate its storage path. Split release
is implemented in split_publish.py and never publishes a whole version.
"""

from __future__ import annotations

import dataclasses
import json
import os
import re
from typing import TYPE_CHECKING, Any, List, Optional

import typer

from .repo_read_guard import STORAGE_SIDES as _STORAGE_SIDES
from .repo_read_guard import oss_fallback_kwargs

if TYPE_CHECKING:  # pragma: no cover - 仅用于类型标注,运行时不 import
    from datetime import datetime

    from instance_repo import Repo

__all__ = [
    "dataset_version_app",
    "dataset_split_app",
    "dataset_access_app",
    "register",
]

dataset_version_app = typer.Typer(help="Dataset version operations")
dataset_split_app = typer.Typer(help="Dataset split operations (splits live inside a version)")
dataset_access_app = typer.Typer(help="Dataset access control (dataset role bindings)")


def register(dataset_app: typer.Typer) -> None:
    """把 version/split/access 子命令组与 dataset 级命令挂到 ``ap dataset`` 上。

    ``dataset_app`` 由 ``ap_client.cli`` 拥有(它还带着 §6 保留下来的
    ``versions`` / ``instances`` 两个弃用命令),因此 dataset 级命令只能在这里
    命令式挂载,不能用模块作用域的装饰器。
    """
    dataset_app.add_typer(dataset_version_app, name="version")
    dataset_app.add_typer(dataset_split_app, name="split")
    dataset_app.add_typer(dataset_access_app, name="access")
    from .split_publish import dataset_split_publish, dataset_split_publish_status

    dataset_split_app.command("publish")(dataset_split_publish)
    dataset_split_app.command("publish-status")(dataset_split_publish_status)
    _register_dataset_commands(dataset_app)


def _register_dataset_commands(dataset_app: typer.Typer) -> None:
    """挂载 dataset 级命令。"""
    from .dataset_register import dataset_register

    dataset_app.command("list")(dataset_list)
    dataset_app.command("get")(dataset_get)
    dataset_app.command("create")(dataset_create)
    dataset_app.command("update")(dataset_update)
    dataset_app.command("claim")(dataset_claim)
    dataset_app.command("register")(dataset_register)


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

#: 上游 §6.1 的默认列,顺序不可改(设计 §5)。
_DATASET_COLUMNS: tuple[tuple[str, str], ...] = (
    ("dataset", "DATASET"),
    ("benchmark", "BENCHMARK"),
    ("visibility", "VISIBILITY"),
    ("status", "STATUS"),
    ("owner", "OWNER"),
    ("versions", "VERSIONS"),
    ("updated_at", "UPDATED_AT"),
)

#: 上游 §7.2 的默认列(设计 §5)。
_VERSION_COLUMNS: tuple[tuple[str, str], ...] = (
    ("version", "VERSION"),
    ("status", "STATUS"),
    ("splits", "SPLITS"),
    ("instances", "INSTANCES"),
    ("updated_at", "UPDATED_AT"),
    ("registered", "REGISTERED"),
)

#: 上游 §8.2 的默认列(设计 §5)。
_SPLIT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("split", "SPLIT"),
    ("run_type", "RUN_TYPE"),
    ("instances", "INSTANCES"),
    ("updated_at", "UPDATED_AT"),
    ("registered", "REGISTERED"),
)

_ACCESS_COLUMNS: tuple[tuple[str, str], ...] = (
    ("principal_type", "PRINCIPAL_TYPE"),
    ("principal_id", "PRINCIPAL_ID"),
    ("role", "ROLE"),
)

#: 语义角色名 → apiserver 内置 dataset 角色 id(``model/role.go:70-72``)。
_ROLES = ("reader", "writer", "admin")
_ROLE_IDS = {role: f"built-in:dataset-{role}" for role in _ROLES}
_ROLE_BY_ID = {value: key for key, value in _ROLE_IDS.items()}

_PRINCIPAL_TYPES = ("user", "user_group")
_VISIBILITIES = ("private", "public")
#: 服务端 version 枚举(设计 §9:上游的 publishing/failed 是 ingest 任务状态,不在此列)。
_VERSION_STATUSES = ("draft", "published", "deprecated", "archived")
_RUN_TYPES = ("train", "eval")
#: ``dataset list`` 的服务端排序键与方向(``GET /apis/v1/datasets/series``)。
_SORT_KEYS = ("updated_at", "dataset_name")
_SORT_ORDERS = ("asc", "desc")
#: 服务端 ``benchmark_id`` 的特殊取值:未绑定 benchmark 的治理查询。
_NO_BENCHMARK = "none"

_FORMAT_HELP = "Output format: plain/table/json/yaml (default: AP_FORMAT or command default)"

_METADATA_MODELS = ("version_first", "split_first")
# IR SDK >= 1.4.0.dev3 的业务入口固定 split_first：business_metadata_model 拒绝
# version_first（仅保留给低层 legacy 读）。带 version 的 split 查询在两种模型下
# 结果一致（实测），显式 split_first 与 SDK 归一值一致且新旧 SDK 均接受。
_VERSION_SPLIT_METADATA_MODEL = "split_first"

#: CLI **不替 SDK 决定元数据模型**:不下发 ``metadata_model``,由 SDK 按 profile 归一
#: (当前为 ``split_first``)。
#:
#: 早期实现缺省下发 ``version_first``(服务端缺省值),结果是"省略 --version"的无版本空间
#: 请求也会被服务端按 version_first 解析,直接报 ``version is required``——split_first 的
#: dataset/split 寻址根本走不到。带 version 的读在两种模型下结果一致(实测),所以缺省不
#: 下发既修好了无版本路径,也不改变有版本路径。

_ENVIRONMENT_HELP = (
    "Metadata environment: online / pre / auto. Defaults to online, or to "
    "AP_DATASET_ENVIRONMENT when set. Writes inherit the cluster-bound storage "
    "and must match its side (pre needs a dev-storage cluster); auto follows "
    "the cluster binding entirely."
)

_METADATA_MODEL_HELP = (
    "Metadata projection: version_first / split_first. Omit to let the SDK decide "
    "(it derives split_first, which is what makes a version-less dataset/split "
    "addressable). Only split_first exposes split-parented metadata."
)

_VERSION_HELP = (
    "Dataset version. Omitting it means the version-less space "
    "(split_first) - it never implies 'latest'."
)

#: 空 version 的固定说明(设计 §4.3 要求报错文案显式点出这一点)。
_NO_VERSION_NOTE = "Omitting --version means the version-less space (split_first); latest is never picked implicitly"


# ---------------------------------------------------------------------------
# 共用 helper
# ---------------------------------------------------------------------------


def _fmt(output_format: Optional[str], *, default: str = "plain") -> str:
    from .cli import _normalize_output_format

    return _normalize_output_format(output_format, default=default, keep_table=True)


def _fail(message: str, hint: str, exit_code: int = 1) -> "typer.Exit":
    """打设计 §5 的固定两行文案到 stderr 并返回待 raise 的 ``typer.Exit``。"""
    typer.echo(f"error: {message}", err=True)
    typer.echo(f"hint: {hint}", err=True)
    return typer.Exit(exit_code)


def _describe(exc: BaseException) -> str:
    message = getattr(exc, "message", None)
    text = str(message or "").strip() or str(exc).strip()
    return text or type(exc).__name__


def _print_table(rows: list[dict], columns, output_format: str) -> None:
    from .cli import _print_plain_table, _print_rich_table

    if output_format == "table":
        _print_rich_table(rows, list(columns))
    else:
        _print_plain_table(rows, list(columns))


def _emit(payload, rows, columns, output_format: str) -> None:
    """``json``/``yaml`` 打 payload;``plain``/``table`` 打固定列表格。"""
    from .cli import _print_formatted

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
        return
    _print_table(rows, columns, output_format)


#: `dataset list` 缺省页大小:只取一页,不自动翻页(见 §7.1)。
_DEFAULT_PAGE_SIZE = 100

#: 显式给了 `--page` 而未给 `--page-size` 时的页大小(迁移前的旧默认)。
_PAGE_SIZE_WITH_PAGE = 20

#: dataset 详情的 plain/table 字段顺序:取 SDK 化之前的服务端 JSON 顺序,并把
#: `status` 插在 `visibility` 之后(未列出的字段按原顺序追加在末尾)。
_DATASET_DETAIL_ORDER: tuple[str, ...] = (
    "dataset_id",
    "dataset_name",
    "dataset_l1",
    "dataset_l2",
    "display_name",
    "owner",
    "visibility",
    "status",
    "benchmark_id",
    "description",
    "created_at",
    "updated_at",
    "version_count",
    "split_count",
    "latest_version",
    "available_envs",
    "stats",
)

#: version 详情的 plain/table 字段顺序(同上)。
_VERSION_DETAIL_ORDER: tuple[str, ...] = (
    "dataset_version_id",
    "version",
    "dataset",
    "status",
    "run_type",
    "storage_type",
    "storage_path",
    "created_by",
    "created_at",
    "updated_at",
    "published_at",
    "last_ingested_at",
    "splits",
    "manifest",
)


def _emit_detail(
    payload: dict,
    output_format: str,
    *,
    order: tuple[str, ...] = (),
    always: tuple[str, ...] = (),
) -> None:
    """打详情。

    ``order`` / ``always`` 只作用于 plain/table(给人看的视图):按 ``order`` 排列字段,
    ``always`` 里的字段即使服务端 `omitempty` 没返回也补空串显示。**`json`/`yaml` 恒为
    服务端原样**,键集与顺序都不动。
    """
    from .cli import _print_detail, _print_formatted

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
        return

    rendered: dict = {}
    for key in order:
        if key in payload:
            rendered[key] = payload[key]
        elif key in always:
            rendered[key] = ""
    for key, value in payload.items():
        if key not in rendered:
            rendered[key] = value
    _print_detail(rendered)


def _version_value(version: Optional[str]) -> str:
    """省略 ``--version`` 就是**无版本空间**(空串),绝不隐式取 latest(设计 §4.3)。"""
    return (version or "").strip()


def _version_label(version: str) -> str:
    return version or "<no version space>"


def _check_choice(value: str, choices: tuple[str, ...], option: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in choices:
        raise _fail(
            f"{option} invalid value: {value!r}",
            f"{option} accepts only: {', '.join(choices)}",
            exit_code=2,
        )
    return normalized


def _environment(value: Optional[str]) -> str:
    """``--environment`` 归一:显式参数 > ``AP_DATASET_ENVIRONMENT`` > 固定缺省 online。

    缺省**固定 online**,与集群无关——可预期性的底线。``auto`` 表示跟随集群绑定
    (读省略下发,写继承集群桶,天然无冲突),是唯一在两种集群上都合法的取值,
    供共享脚本与"不想选环境"的用户使用。
    """
    from .irepo_sdk import DATASET_ENVIRONMENTS

    text = str(value or "").strip()
    if text:
        return _check_choice(text, DATASET_ENVIRONMENTS, "--environment")
    configured = os.environ.get("AP_DATASET_ENVIRONMENT", "").strip()
    if configured:
        return _check_choice(configured, DATASET_ENVIRONMENTS, "AP_DATASET_ENVIRONMENT")
    return "online"


def _env_kwargs(environment: str) -> dict:
    """``environment`` 的调用参数:``auto`` 省略下发(跟随集群绑定),其余显式下发。"""
    return {"environment": environment} if environment and environment != "auto" else {}


def _read_env_kwargs(repo: Any, client: Any, method: str, environment: str) -> dict:
    return {**_env_kwargs(environment), **oss_fallback_kwargs(repo, client, method, environment)}


def _check_storage_side(repo: Any, environment: str) -> None:
    """写数据面前置:集群绑定存储与请求环境同侧校验(设计 §4.2)。

    字节只能从本地集群的桶进出(网络可达性与 STS 签发都是集群域内的),所以写
    不存在"跨集群存储"的形态;异侧写只能报错——静默写到另一边的桶就是历史上
    读写撕裂缺陷的原样复刻。``auto`` 跟随集群绑定,天然无冲突,直接放行。
    """
    if environment == "auto":
        return
    profile = getattr(repo, "profile", None)
    storage_env = str(getattr(profile, "storage_env", "") or "").strip().lower()
    side = _STORAGE_SIDES.get(storage_env, "")
    if side == environment:
        return
    cluster = str(getattr(profile, "cluster", "") or "").strip() or "current cluster"
    if not side:
        raise _fail(
            f"Cluster {cluster} has no data storage configured; cannot upload as {environment}",
            "Ask the platform to configure storage for this cluster, or switch to a cluster with storage configured (ap cluster list --all)",
        )
    bound = "dev storage" if side == "pre" else "prod storage"
    if environment == "pre":
        hint = "For data production, switch to a cluster bound to dev storage (e.g. hk-benchmark-dev); to upload to online, use --environment online"
    else:
        hint = (
            "To upload online data, switch to a cluster bound to prod storage (e.g. hz-prod-1); "
            "for data production, set export AP_DATASET_ENVIRONMENT=pre"
        )
    raise _fail(f"Cluster {cluster} is bound to {bound}; cannot upload as {environment}", hint)


def _pagination_envelope(result: Any) -> dict:
    """把 SDK ``PagedResult`` 还原成**服务端原样**的分页信封。

    服务端回的是 ``{total,page,pageSize}``(驼峰),而 CLI 历史上就是原样透出这个 dict;
    换成 SDK 归一化后的 ``page_size`` 会改掉既有 JSON 契约。``PagedResult.raw`` 保留
    了原始信封,优先用它;老 SDK 没有该字段时回退到归一化字段。
    """
    raw = getattr(result, "raw", None)
    if isinstance(raw, dict) and raw:
        return dict(raw)
    total = getattr(result, "total", None)
    page = getattr(result, "page", None)
    page_size = getattr(result, "page_size", None)
    envelope = {}
    if isinstance(total, int) and total >= 0:
        envelope["total"] = total
    if isinstance(page, int):
        envelope["page"] = page
    if isinstance(page_size, int) and page_size:
        envelope["pageSize"] = page_size
    return envelope


def _metadata_model(value: Optional[str]) -> str:
    """``--metadata-model`` 归一;**没给就是空串**(CLI 不下发,交给 SDK/服务端)。

    显式传了才下发——那是调用方自己的选择,CLI 不做拦截也不改写成服务端缺省值。
    """
    text = str(value or "").strip()
    if not text:
        return ""
    return _check_choice(text, _METADATA_MODELS, "--metadata-model")


def _model_dict(record: Any) -> dict:
    """SDK 模型 → 输出用的 dict。

    空值一律丢掉:服务端 Go 结构体基本都带 ``omitempty``(``false`` / ``""`` / ``[]`` /
    ``{}`` / 缺省都不会出现在响应里),而 SDK 模型会把它们补成默认值;留着这些默认值会让
    JSON 凭空多出字段(迁移前是原样透出服务端响应,契约必须一致)。

    ``registered`` 是显式注册状态，必须保留 ``false``。
    只清洗**顶层**:嵌套结构(如 version 详情里的 ``splits[].is_default``)按模型原样输出,
    服务端在那里确实是显式返回 ``false``。
    """
    to_dict = getattr(record, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif dataclasses.is_dataclass(record):
        payload = dataclasses.asdict(record)
    elif isinstance(record, dict):
        payload = record
    else:
        return {}
    if not isinstance(payload, dict):
        return {}
    registered = getattr(record, "registered", None)
    if isinstance(registered, bool):
        payload = {**payload, "registered": registered}
    return {
        key: value
        for key, value in payload.items()
        if value is not None
        and (
            key == "registered" or not (value is False or value == "" or value == [] or value == {})
        )
    }


def _registered_dict(record: Any) -> dict:
    """Preserve SDK registration state; older metadata-only SDK reads imply true."""
    payload = _model_dict(record)
    payload.setdefault("registered", True)
    return payload


def _api_biz_code(exc: BaseException) -> Optional[int]:
    """从 ``APIError`` 里取 apiserver 业务码(设计 §5.1),不 import 数值异常类。

    ``api._response_error_detail`` 把 ``detail`` 填成 ``resp.text``,所以业务码要么在
    ``exc.response.json()["code"]``,要么得把 ``detail`` 当 JSON 再解一次。
    """
    payload: Any = None
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            payload = response.json()
        except Exception:  # noqa: BLE001 - 非 JSON 响应就退回 detail
            payload = None
    if not isinstance(payload, dict):
        detail = getattr(exc, "detail", None)
        if isinstance(detail, dict):
            payload = detail
        elif isinstance(detail, str) and detail.strip().startswith("{"):
            try:
                payload = json.loads(detail)
            except (TypeError, ValueError):
                payload = None
    if isinstance(payload, dict):
        try:
            return int(payload.get("code"))
        except (TypeError, ValueError):
            return None
    return None


def _business_code(exc: BaseException) -> Optional[int]:
    code = getattr(exc, "biz_code", None)
    if isinstance(code, int) and not isinstance(code, bool):
        return code
    return _api_biz_code(exc)


def _last_admin_hint(dataset: str) -> str:
    return (
        "Cannot revoke or demote the last admin of a dataset; grant admin to another user first: "
        f"ap dataset access grant {dataset} --user <another-uid> --role admin, "
        "then retry this command after it succeeds"
    )


#: apiserver dataset 控制面业务码 → 固定 hint(设计 §5.1)。
_DATASET_CODE_HINTS: dict[int, str] = {
    92008: "Dataset capability is not enabled in this environment; contact the admin",
    92011: "Grant another admin before revoking the current one",
    92014: "Retry later; per-user claim count is limited",
    92015: "Wait for the current ingest/ACL operation to finish, then retry",
    92016: "claim can only bind a benchmark and cannot be re-bound; contact the admin to change it",
}


def _resolve_benchmark_id(repo: "Repo", value: str) -> str:
    """``--benchmark`` 接受名称或 ``source_id``,统一解析成 ``source_id``(设计 §9)。

    走 SDK ``benchmarks``:先按 source_id 点查,再按名称模糊搜一遍精确比对
    (服务端 ``q`` 是 name 的不区分大小写子串,所以本地还要做等值判定)。
    解析不到 → 退出码 2(使用错误),不静默把名称当 id 下发。
    """
    target = str(value or "").strip()
    if not target:
        return ""
    record: Any = None
    try:
        record = repo.benchmarks.get(target)
    except Exception:  # noqa: BLE001 - 404 / 网络问题都退回搜索
        record = None
    if record is not None:
        resolved = str(getattr(record, "source_id", "") or "").strip()
        if resolved:
            return resolved
    try:
        page = repo.benchmarks.list(q=target, page_size=100)
        items = list(getattr(page, "items", None) or [])
    except Exception:  # noqa: BLE001
        items = []
    for item in items:
        source_id = str(getattr(item, "source_id", "") or "").strip()
        name = str(getattr(item, "name", "") or "").strip()
        if target in (source_id, name) and source_id:
            return source_id
    raise _fail(
        f"Failed to resolve benchmark {target}: no benchmark with that name or source_id",
        "Use ap benchmark list to see available benchmarks, then pass a name or source_id",
        exit_code=2,
    )


def _visibility_values(values: Optional[List[str]]) -> list[str]:
    """``--visibility`` 归一成服务端的逗号分隔多值形式(同维 OR)。

    既支持重复给(``--visibility public --visibility private``),也支持逗号分隔
    (``--visibility public,private``);逐项校验枚举,非法值 exit 2,不等到服务端 400。
    """
    resolved: list[str] = []
    for raw in values or []:
        for part in str(raw).split(","):
            part = part.strip()
            if not part:
                continue
            checked = _check_choice(part, _VISIBILITIES, "--visibility")
            if checked not in resolved:
                resolved.append(checked)
    return resolved


#: ``--updated-from/--updated-to`` 的 RFC3339 形状:日期 + 分隔符 + 时间 + 可选小数秒 + 带
#: 偏移的时区(与 ``time.Parse(time.RFC3339, ...)`` 的接受面基本一致)。
_UPDATED_AT_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2})[Tt ](\d{2}:\d{2}:\d{2})(\.\d+)?([Zz]|[+-]\d{2}:?\d{2})$"
)


def _parse_updated_at(option: str, raw: str) -> "datetime":
    """把 ``--updated-from/--updated-to`` 解析成带时区的 ``datetime``;形状不对则 exit 2。

    只做前置校验,下发给服务端的仍是用户原样输入的字符串——服务端的
    ``datasetUpdatedRangeFromQuery`` 才是最终解释方(它会把入参归一到 UTC 并做同样的
    区间倒挂检查)。小数秒超过 6 位时截断,避免 Python <3.11 的 ``fromisoformat`` 把
    服务端能接受的纳秒时间戳误判成非法。
    """
    from datetime import datetime

    match = _UPDATED_AT_PATTERN.match(raw)
    if match is None:
        raise _fail(
            f"{option} invalid value: {raw!r}",
            "Use an RFC3339 timestamp with timezone, e.g. 2026-03-01T00:00:00Z or 2026-03-02T12:30:00+08:00",
            exit_code=2,
        )
    date, clock, fraction, zone = match.groups()
    fraction = (fraction or "")[:7]  # ".123456789" → ".123456"
    zone = "+00:00" if zone in ("Z", "z") else zone
    if len(zone) == 5:  # "+0800" → "+08:00"
        zone = f"{zone[:3]}:{zone[3:]}"
    return datetime.fromisoformat(f"{date}T{clock}{fraction}{zone}")


def _updated_range(from_value: Optional[str], to_value: Optional[str]) -> tuple[str, str]:
    """校验 ``--updated-from/--updated-to``(闭区间,可只给一侧),原样返回待下发字符串。"""
    lower = str(from_value or "").strip()
    upper = str(to_value or "").strip()
    parsed_lower = _parse_updated_at("--updated-from", lower) if lower else None
    parsed_upper = _parse_updated_at("--updated-to", upper) if upper else None
    if parsed_lower is not None and parsed_upper is not None and parsed_lower > parsed_upper:
        raise _fail(
            "--updated-from must not be later than --updated-to",
            "The range is a closed interval; swap the two timestamps, or give only one side",
            exit_code=2,
        )
    return lower, upper


def _fetch_version(
    dataset: str,
    version: str,
    *,
    stage: str,
    environment: Optional[str] = None,
    metadata_model: str = "",
) -> dict:
    """读 version 详情(含内嵌 ``splits[]``);空 version 的报错必须点明"无版本空间"语义。

    走 SDK ``versions.get``——它返回的详情带同样的内嵌 ``splits[]``(split 不是独立资源),
    但**必须显式带 environment**,否则 SDK 会按 profile 派生(见 :func:`_environment`)。
    """
    from .irepo_sdk import _reason

    # 归一/构造必须在 try 之外:它们内部会 raise typer.Exit(2)(用法错 / 缺 SDK),
    # 被 except Exception 接住会降级成退出码 1。
    env = _environment(environment)
    repo = _dataset_repo()
    try:
        detail = repo.versions.get(
            dataset,
            version,
            **_read_env_kwargs(repo, repo.versions, "get", env),
            **({"metadata_model": metadata_model} if metadata_model else {}),
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        if version:
            hint = (
                f"Check the version name: ap dataset version list --dataset {dataset}"
                "; the version may live in another metadata environment, retry with --environment online/pre"
            )
        else:
            hint = f"{_NO_VERSION_NOTE}; add --version <version> to operate on a specific version"
        raise _fail(
            f"dataset {dataset} version {_version_label(version)}: {stage} failed: {_reason(exc)}",
            hint,
        ) from exc
    return _model_dict(detail)


#: recordsvc 的 split 列表服务端上限(``GET /datasets/splits``)。
_SPLIT_PAGE_SIZE = 200


def _unversioned_splits(
    dataset: str, *, stage: str, environment: Optional[str] = None
) -> list[dict]:
    """读**无版本空间**的 split(split_first)——走 SDK ``repo.splits``(recordsvc)。

    为什么不能像有版本时那样读 ``versions.get`` + 内嵌 ``splits[]``:``GET/PATCH
    /datasets/versions/detail`` **必须**带非空 version(apiserver 400 92005
    "version is required",SDK 也在客户端前置拒绝),无版本空间表达不出来。真正承载它的是
    recordsvc 的 ``/datasets/splits``(``version_scope=unversioned``)。
    """
    from .irepo_sdk import _reason

    env = _environment(environment)
    repo = _dataset_repo()
    try:
        records: list[dict] = []
        page = 1
        while True:
            result = repo.splits.list(
                dataset,
                version_scope="unversioned",
                page_size=_SPLIT_PAGE_SIZE,
                **({"page": page} if page > 1 else {}),
                **_read_env_kwargs(repo, repo.splits, "list", env),
            )
            items = getattr(result, "items", None) or []
            for item in items:
                record = _model_dict(item)
                if not _version_value(record.get("version")):
                    records.append(record)
            if not items or getattr(result, "has_more", False) is not True:
                break
            page += 1
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"dataset {dataset} (no version space): {stage} failed: {_reason(exc)}",
            f"Check the dataset name and permission: ap dataset get {dataset}",
        ) from exc
    return records


def _unversioned_split(
    dataset: str, split: str, *, environment: Optional[str] = None
) -> Optional[dict]:
    """取无版本空间里的单个 split 记录;不存在返回 ``None``(不当作错误)。"""
    from .irepo_sdk import _reason

    env = _environment(environment)
    repo = _dataset_repo()
    try:
        record = repo.splits.get(dataset, split, **_read_env_kwargs(repo, repo.splits, "get", env))
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"dataset {dataset} (no version space) split {split}: query failed: {_reason(exc)}",
            f"Check the dataset name and permission: ap dataset get {dataset}",
        ) from exc
    detail = _model_dict(record) if record is not None else None
    return detail if detail is not None and not _version_value(detail.get("version")) else None


def _versioned_split(
    dataset: str, version: str, split: str, *, environment: Optional[str] = None
) -> Optional[dict]:
    """取指定 version 里的单个 split 记录;不存在返回 ``None``(不当作错误)。

    与 ``_unversioned_split`` 同源,走 recordsvc 的 ``splits.get``(SDK 自带
    version_first 内嵌投影的 legacy 回退)。
    """
    from .irepo_sdk import _reason

    env = _environment(environment)
    repo = _dataset_repo()
    try:
        record = repo.splits.get(
            dataset, split, version=version, **_read_env_kwargs(repo, repo.splits, "get", env)
        )
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"dataset {dataset} version {version} split {split}: query failed: {_reason(exc)}",
            f"Check the dataset name and permission: ap dataset get {dataset}",
        ) from exc
    detail = _model_dict(record) if record is not None else None
    return detail if detail is not None and _version_value(detail.get("version")) == version else None


def _versioned_splits(
    dataset: str, version: str, *, stage: str, environment: Optional[str] = None
) -> list[dict]:
    """读**指定 version**的 split——走 SDK ``repo.splits``(recordsvc)。

    与 ``_unversioned_splits`` 同源:version 文档不内嵌 ``splits[]``(服务端只给
    ``split_count`` 聚合,split 记录由 recordsvc 的 ``/datasets/splits`` 承载),
    SDK ``splits.list(version=...)`` 是唯一正确读法,且自带存量 version_first
    内嵌投影的 legacy 回退。
    """
    from .irepo_sdk import _reason

    env = _environment(environment)
    repo = _dataset_repo()
    try:
        records: list[dict] = []
        page = 1
        while True:
            result = repo.splits.list(
                dataset,
                version=version,
                page_size=_SPLIT_PAGE_SIZE,
                **({"page": page} if page > 1 else {}),
                **_read_env_kwargs(repo, repo.splits, "list", env),
            )
            items = getattr(result, "items", None) or []
            for item in items:
                record = _model_dict(item)
                # 与 ``_versioned_split`` 同口径:只收 version 匹配的记录(服务端
                # exact scope 保证;legacy 投影与 OSS 发现也会带 version)。
                if _version_value(record.get("version")) == version:
                    records.append(record)
            if not items or getattr(result, "has_more", False) is not True:
                break
            page += 1
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"dataset {dataset} version {version}: {stage} failed: {_reason(exc)}",
            f"Check the version name: ap dataset version get {version} --dataset {dataset}",
        ) from exc
    return records


def _split_records(detail: dict) -> list[dict]:
    """version 文档内嵌的 ``splits[]``(设计 §4.3:split 没有独立资源)。"""
    splits = detail.get("splits")
    if not isinstance(splits, list):
        return []
    records: list[dict] = []
    for item in splits:
        if isinstance(item, dict):
            records.append(item)
        elif item:
            records.append({"name": str(item)})
    return records


def _split_names_of(records: list[dict]) -> list[str]:
    """recordsvc split 记录里的名字(去重)。"""
    names: list[str] = []
    for record in records:
        name = str(record.get("name") or "").strip()
        if name and name not in names:
            names.append(name)
    return names


def _split_names(detail: dict) -> list[str]:
    names: list[str] = []
    for record in _split_records(detail):
        name = str(record.get("name") or "").strip()
        if name and name not in names:
            names.append(name)
    return names


def _dataset_repo(*, request_timeout: float | None = None) -> "Repo":
    """dataset 写路径统一走 InstanceRepo SDK;未装 ``dataset`` extra 时退出 2。"""
    from .irepo_sdk import SdkMissing, load_repo

    try:
        return load_repo(request_timeout=request_timeout)
    except SdkMissing as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc


def _patch_version(
    dataset: str,
    version: str,
    body: dict,
    *,
    stage: str,
    fallback_hint: str = "",
    environment: Optional[str] = None,
    metadata_model: str = "",
) -> None:
    """split 写操作统一走 SDK;body 为 splits/split_run_types 单键。

    ``environment`` 必须与读路径同口径(缺省 ``online``):SDK 的 ``versions.update``
    会按 profile 派生(dev 集群→``pre``),而版本在 ``online``,于是"能查到却 PATCH 404"。
    见 :func:`ap_client.irepo_sdk.update_version_detail`。
    """
    from .irepo_sdk import _reason, update_version_detail

    repo = _dataset_repo()
    try:
        update_version_detail(
            repo,
            dataset,
            version,
            body,
            environment=_environment(environment),
            metadata_model=metadata_model,
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        code = getattr(exc, "biz_code", None)
        if code == 94018:
            hint = f"Writer role required: ap dataset access grant {dataset} --user <you> --role writer"
        elif code == 94016:
            hint = (
                f"Ask an admin to run ap dataset access grant {dataset} --user <you> --role writer"
            )
        else:
            shown = version if version else '""'
            hint = fallback_hint or (
                f"Check the version status: ap dataset version get {shown} --dataset {dataset}"
            )
        raise _fail(
            f"dataset {dataset} version {_version_label(version)}: {stage} failed: {_reason(exc)}",
            hint,
        ) from exc


# ---- 行投影 ---------------------------------------------------------------


def _dataset_row(record: dict) -> dict:
    return {
        "dataset": record.get("dataset_name") or record.get("dataset") or "",
        "benchmark": record.get("benchmark_id") or "",
        "visibility": record.get("visibility") or "",
        # 服务端只在 series status 非空时返回(omitempty):正常态显示空,deprecated 显示 deprecated
        "status": record.get("status") or "",
        "owner": record.get("owner") or "",
        "versions": record.get("version_count", ""),
        "updated_at": record.get("updated_at") or "",
    }


def _legacy_dataset_record(record: dict) -> dict:
    """JSON 输出的记录附带主干旧字段 ``name``(``ap dataset list --format json``
    的脚本依赖 ``.datasets[].name`` 与顶层 ``.total``)。
    """
    name = str(record.get("dataset_name") or record.get("dataset") or "").strip()
    if not name:
        return record
    merged = dict(record)
    merged.setdefault("name", name)
    return merged


def _pagination_total(pagination: dict, *, fallback: int | None = None) -> int | None:
    """顶层 ``total`` 的取值:pagination.total,fallback 兜底。"""
    raw = pagination.get("total") if isinstance(pagination, dict) else None
    try:
        total = int(raw)
    except (TypeError, ValueError):
        return fallback
    return total


def _version_row(record: dict) -> dict:
    """version 列表项投影。

    列只取服务端 ``DatasetVersionListItem`` **确实返回**的字段(``version`` / ``status``
    / ``split_count`` / ``instance_count`` / ``updated_at``):它不带 ``created_at`` /
    ``published_at``,那两列以前恒为空(表头 6 列、行里只有 4 个值),现已去掉——
    要这两个时间用 ``version get``(详情文档才有)。
    """
    splits = record.get("split_count")
    if splits is None:
        splits = len(_split_records(record)) or ""
    return {
        "version": record.get("version") or "",
        "status": record.get("status") or "",
        "splits": splits,
        "instances": record.get("instance_count", ""),
        "updated_at": record.get("updated_at") or "",
        "registered": record.get("registered", True),
    }


def _split_row(record: dict, detail: dict) -> dict:
    """split 行投影。

    两种记录形状:version 文档内嵌的 ``splits[]``(``instance_count`` 在顶层)与 recordsvc
    的 split 记录(``manifest.instance_count``)。``detail`` 为所属 version,缺自己的时间戳
    时退回它的(无版本空间没有 version,传空 dict)。
    """
    manifest = record.get("manifest") if isinstance(record.get("manifest"), dict) else {}
    instances = record.get("instance_count")
    if instances in (None, ""):
        instances = manifest.get("instance_count", "")
    return {
        "split": record.get("name") or "",
        "run_type": record.get("run_type") or detail.get("run_type") or "",
        "instances": "" if instances is None else instances,
        "updated_at": record.get("updated_at") or detail.get("updated_at") or "",
        "registered": record.get("registered", detail.get("registered", True)),
    }


#: ``datasets.list_access`` 的分页大小:一次多拿一点,再把所有页取满。
_ACCESS_PAGE_SIZE = 100


def _binding_row(binding: Any) -> dict:
    """SDK ``RoleBinding``(或原始 dict)→ ``{principal_type, principal_id, role}``。"""
    if isinstance(binding, dict):
        data = binding
    else:
        data = {
            "principal_type": getattr(binding, "principal_type", "") or "",
            "principal_id": getattr(binding, "principal_id", "") or "",
            "role_id": getattr(binding, "role_id", "") or "",
        }
    role_id = str(data.get("role_id") or "").strip()
    role = str(data.get("role") or "").strip() or _ROLE_BY_ID.get(role_id, role_id)
    return {
        "principal_type": str(data.get("principal_type") or ""),
        "principal_id": str(data.get("principal_id") or ""),
        "role": role,
    }


def _bindings(repo, dataset: str) -> list[dict]:
    """列出某 dataset 的全部绑定。

    SDK 的 ``list_access`` 是**单页**语义(默认 20 条),这里按 ``has_more`` 取满:
    迁移前是控制面一次性列全,不能因为 SDK 分页而把后面的绑定吞掉。
    """
    collected: list[dict] = []
    page = 1
    while True:
        result = repo.datasets.list_access(dataset, page=page, page_size=_ACCESS_PAGE_SIZE)
        items = list(getattr(result, "items", None) or [])
        collected.extend(_binding_row(item) for item in items)
        if not items or not getattr(result, "has_more", False):
            return collected
        page += 1


def _bindings_of(repo, dataset: str, principal_id: str, principal_type: str) -> list[dict]:
    """某 principal 在此 dataset 上的现存绑定;读失败时停止变更。"""
    from .irepo_sdk import _reason

    try:
        rows = _bindings(repo, dataset)
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"dataset {dataset}: failed to query existing grants: {_reason(exc)}",
            "Check dataset-admin permission and the current cluster, then retry",
        ) from exc
    return [
        row
        for row in rows
        if row["principal_id"] == principal_id and row["principal_type"] == principal_type
    ]


# ---------------------------------------------------------------------------
# ap dataset
# ---------------------------------------------------------------------------


def dataset_list(
    search: Optional[str] = typer.Argument(
        None, help="Search keyword (legacy positional form of --query)"
    ),
    query: Optional[str] = typer.Option(
        None, "--query", help="Fuzzy match on dataset name / description"
    ),
    benchmark: Optional[str] = typer.Option(
        None,
        "--benchmark",
        help=f"Benchmark name or source_id; '{_NO_BENCHMARK}' selects datasets with no binding",
    ),
    visibility: Optional[List[str]] = typer.Option(
        None,
        "--visibility",
        help=f"Filter by visibility: {'/'.join(_VISIBILITIES)}; repeat or comma-separate for OR",
    ),
    mine: bool = typer.Option(
        False,
        "--mine",
        help="Only datasets owned by the caller (server-side owned_by_me=true)",
    ),
    include_deprecated: bool = typer.Option(
        False,
        "--include-deprecated",
        help="Include deprecated datasets (the server excludes them by default)",
    ),
    updated_from: Optional[str] = typer.Option(
        None,
        "--updated-from",
        help="Inclusive RFC3339 lower bound on updated_at (metadata edits only)",
    ),
    updated_to: Optional[str] = typer.Option(
        None, "--updated-to", help="Inclusive RFC3339 upper bound on updated_at"
    ),
    sort_by: Optional[str] = typer.Option(
        None, "--sort-by", help=f"Sort key: {'/'.join(_SORT_KEYS)} (server default: updated_at)"
    ),
    order: Optional[str] = typer.Option(
        None, "--order", help=f"Sort direction: {'/'.join(_SORT_ORDERS)} (server default: desc)"
    ),
    page: Optional[int] = typer.Option(
        None,
        "--page",
        help=f"Page number (default: page 1, {_DEFAULT_PAGE_SIZE} rows)",
    ),
    page_size: Optional[int] = typer.Option(
        None,
        "--page-size",
        help=(
            f"Page size (default: {_DEFAULT_PAGE_SIZE} rows without --page, "
            f"{_PAGE_SIZE_WITH_PAGE} rows with it)"
        ),
    ),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    legacy: bool = typer.Option(
        False,
        "--legacy",
        help="Use the previous data source and output (the datasets ap job create --dataset consumes)",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List datasets from the registry. Defaults to JSON; use --format table for a table."""
    from .cli import _print_formatted, get_client

    output_format = _fmt(output_format, default="json")
    resolved_query = str(query or "").strip()
    legacy_search = str(search or "").strip()
    if legacy_search:
        # 主干旧用法是位置参数搜索(`ap dataset list <keyword>`),这里兼容为
        # --query 的等价形式,而不是让旧脚本直接报"unexpected extra argument"。
        if resolved_query and resolved_query != legacy_search:
            raise _fail(
                "The positional argument and --query must not carry different values",
                f"Keep only one: ap dataset list {legacy_search} "
                f"or ap dataset list --query {query}",
                exit_code=2,
            )
        resolved_query = legacy_search

    if legacy:
        # 旧口径:ossdata 数据源自动翻页拉全量,只支持关键词搜索;registry 独有的
        # 筛选/分页参数在这里不存在,静默忽略会让用户误以为筛选生效,直接退出 2。
        unsupported = [
            name
            for name, value in (
                ("--benchmark", benchmark),
                ("--visibility", visibility),
                ("--mine", mine),
                ("--include-deprecated", include_deprecated),
                ("--updated-from", updated_from),
                ("--updated-to", updated_to),
                ("--sort-by", sort_by),
                ("--order", order),
                ("--environment", environment),
                ("--metadata-model", metadata_model),
                ("--page", page),
                ("--page-size", page_size),
            )
            if value
        ]
        if unsupported:
            raise _fail(
                f"--legacy does not support {' / '.join(unsupported)}: the legacy datasource only supports keyword search",
                "Drop these options, or drop --legacy to use the dataset registry",
                exit_code=2,
            )
        result = get_client().list_all_datasets(resolved_query or None)
        if output_format == "table":
            from .cli import _print_records_table

            _print_records_table(result)
        else:
            _print_formatted(result, output_format)
        return

    resolved_visibility = _visibility_values(visibility)
    resolved_sort_by = _check_choice(sort_by, _SORT_KEYS, "--sort-by") if sort_by else ""
    resolved_order = _check_choice(order, _SORT_ORDERS, "--order") if order else ""
    resolved_from, resolved_to = _updated_range(updated_from, updated_to)

    repo = _dataset_repo()
    env = _environment(environment)
    model = _metadata_model(metadata_model)
    if str(benchmark or "").strip() == _NO_BENCHMARK:
        # 服务端的治理查询:benchmark_id=none 表示"未绑定 benchmark",不经过名称解析。
        benchmark_id = _NO_BENCHMARK
    else:
        benchmark_id = _resolve_benchmark_id(repo, benchmark) if benchmark else ""

    # 服务端在分页前完成筛选/排序,所以这些条件对每一页都成立。
    filters: dict[str, Any] = {
        "q": resolved_query or None,
        "visibility": ",".join(resolved_visibility) or None,
        "benchmark_id": benchmark_id or None,
        "owned_by_me": mine,
        "updated_from": resolved_from or None,
        "updated_to": resolved_to or None,
        "sort_by": resolved_sort_by or None,
        "order": resolved_order or None,
        "include_deprecated": include_deprecated,
    }
    if env:
        filters["environment"] = env
    if model:
        filters["metadata_model"] = model

    resolved_page = page or 1
    # 缺省只取**一页**(100 条):registry 全库 4000+ 条,拉全量要 20+ 次请求、数秒,
    # 而列表命令绝大多数用法只是看一眼或按关键词找一条。要全量走 --legacy(见下)。
    # 显式给了 --page 时沿用旧默认 20 条/页。
    resolved_page_size = page_size or (_DEFAULT_PAGE_SIZE if page is None else _PAGE_SIZE_WITH_PAGE)

    def fetch(current_page: int):
        try:
            result = repo.datasets.list_paged(
                page=current_page, page_size=resolved_page_size, **filters
            )
        except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
            from .irepo_sdk import _reason

            raise _fail(
                f"Failed to list datasets: {_reason(exc)}",
                "Check the filter options and permission, then retry: ap dataset list --format table",
            ) from exc
        return (
            [_model_dict(item) for item in (getattr(result, "items", None) or [])],
            result,
        )

    records, result = fetch(resolved_page)
    pagination = _pagination_envelope(result)

    payload: dict[str, Any] = {}
    if mine:
        payload["owned_by_me"] = True

    rows = [_dataset_row(record) for record in records]
    payload["datasets"] = [_legacy_dataset_record(record) for record in records]
    payload["total"] = _pagination_total(pagination, fallback=len(records))
    payload["pagination"] = pagination
    _emit(payload, rows, _DATASET_COLUMNS, output_format)


#: ``dataset get`` 尾部 environment 摘要表的列。
_ENVIRONMENT_SUMMARY_COLUMNS: tuple[tuple[str, str], ...] = (
    ("environment", "ENVIRONMENT"),
    ("versions", "VERSIONS"),
    ("splits", "SPLITS"),
    ("latest_version", "LATEST_VERSION"),
)


def _print_dataset_environments(repo: "Repo", dataset: str, detail: dict) -> None:
    """``dataset get`` 尾部按 environment 汇总 version/split,告诉用户该去哪个 env 指定。

    仅人读视图(plain/table)追加;``json``/``yaml`` 恒为服务端原样。单个 env 读失败
    (旧 SDK 不接受 environment、权限差异)显示 ``?``,不影响主输出。
    """
    envs = [str(env).strip() for env in detail.get("available_envs") or [] if str(env).strip()]
    if not envs:
        return
    rows: list[dict] = []
    for env in envs:
        try:
            env_detail = _model_dict(
                repo.datasets.get_detail(
                    dataset, **_read_env_kwargs(repo, repo.datasets, "get_detail", env)
                )
            )
        except Exception:  # noqa: BLE001 - 摘要尽力而为
            rows.append({"environment": env, "versions": "?", "splits": "?", "latest_version": "?"})
            continue
        rows.append(
            {
                "environment": env,
                "versions": env_detail.get("version_count", ""),
                "splits": env_detail.get("split_count", ""),
                "latest_version": env_detail.get("latest_version") or "",
            }
        )
    typer.echo("\nEnvironments (add --environment <env> to target one)")
    _print_table(rows, _ENVIRONMENT_SUMMARY_COLUMNS, "plain")


def dataset_get(
    dataset: str = typer.Argument(..., help="Dataset name"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Show dataset detail, including version / split summary stats."""
    from .irepo_sdk import _reason

    dataset = dataset.strip()
    if not dataset:
        raise _fail(
            "Failed to query dataset: name is empty",
            "Pass a non-empty dataset name, e.g. ap dataset get alibaba/a",
            exit_code=2,
        )
    output_format = _fmt(output_format)
    env = _environment(environment)
    repo = _dataset_repo()
    try:
        detail = repo.datasets.get_detail(
            dataset, **_read_env_kwargs(repo, repo.datasets, "get_detail", env)
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        if _business_code(exc) not in (92001, 94021):
            raise _fail(
                f"Failed to query dataset {dataset}: {_reason(exc)}",
                f"Check the dataset name: ap dataset list --query {dataset}",
            ) from exc
        detail = None
    if detail is None:
        rendered = {
            "dataset_name": dataset,
            "registered": False,
        }
        from .dataset_name import (
            DatasetNameError,
            DatasetNameUpgradeRequired,
            parse_dataset_name,
        )

        try:
            name = parse_dataset_name(dataset)
        except DatasetNameUpgradeRequired as exc:
            raise _fail(
                f"Failed to query dataset {dataset}: {exc}",
                "pip install 'ap-client[dataset]' --upgrade",
                exit_code=2,
            ) from exc
        except DatasetNameError:
            # 非规范名:不凭空发明 level 字段(与历史行为一致)。
            pass
        else:
            rendered["dataset_l1"] = name.l1
            rendered["dataset_l2"] = name.l2
    else:
        rendered = _registered_dict(detail)
    _emit_detail(rendered, output_format, order=_DATASET_DETAIL_ORDER, always=("status",))
    if output_format not in ("json", "yaml"):
        _print_dataset_environments(repo, dataset, rendered)


def dataset_create(
    dataset: str = typer.Argument(
        ..., help="Dataset name: L1, L1/L2, or a deeper path "
        "(e.g. my-bench, alibaba/my-bench, or gdpval/synthetic/my-bench)"
    ),
    benchmark: str = typer.Option(..., "--benchmark", help="Benchmark name or source_id"),
    description: Optional[str] = typer.Option(None, "--description", help="Dataset description"),
    visibility: str = typer.Option(
        "private", "--visibility", help=f"Visibility: {'/'.join(_VISIBILITIES)} (default: private)"
    ),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", help="Owning workspace / queue id (optional; server may infer it)"
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Create a dataset. Owner is taken from the caller identity by the server."""
    output_format = _fmt(output_format)
    resolved_visibility = _check_choice(visibility, _VISIBILITIES, "--visibility")
    repo = _dataset_repo()
    benchmark_id = _resolve_benchmark_id(repo, benchmark)

    from instance_repo.models import DatasetSeries

    from .dataset_name import (
        DatasetNameError,
        DatasetNameUpgradeRequired,
        parse_dataset_name,
    )
    from .irepo_sdk import _reason

    try:
        name = parse_dataset_name(dataset)
    except DatasetNameUpgradeRequired as exc:
        raise _fail(
            f"Failed to create dataset {dataset}: {exc}",
            "pip install 'ap-client[dataset]' --upgrade",
            exit_code=2,
        ) from exc
    except DatasetNameError:
        raise _fail(
            f"Failed to create dataset {dataset}: the name must be one or more "
            "canonical path segments",
            "e.g. my-bench, your-team/my-bench, or gdpval/synthetic/my-bench",
            exit_code=2,
        )
    series = DatasetSeries(
        dataset_name=dataset,
        dataset_l1=name.l1,
        dataset_l2=name.l2,
        benchmark_id=benchmark_id,
        visibility=resolved_visibility,
        description=description or None,
        workspace_id=(workspace or "").strip() or None,
    )
    try:
        record = repo.datasets.create(series)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to create dataset {dataset}: {_reason(exc)}",
            f"On a name conflict, rename or use the existing dataset: ap dataset get {dataset}",
        ) from exc
    _emit_detail(
        record.to_dict() if hasattr(record, "to_dict") else {"dataset": dataset},
        output_format,
    )


def dataset_update(
    dataset: str = typer.Argument(..., help="Dataset name"),
    description: Optional[str] = typer.Option(None, "--description", help="New description"),
    visibility: Optional[str] = typer.Option(
        None,
        "--visibility",
        help=f"New visibility ({'/'.join(_VISIBILITIES)}); needs dataset-admin",
    ),
    display_name: Optional[str] = typer.Option(None, "--display-name", help="New display name"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Update dataset metadata. At least one field is required."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    body: dict[str, Any] = {}
    if description is not None:
        body["description"] = description
    if visibility is not None:
        body["visibility"] = _check_choice(visibility, _VISIBILITIES, "--visibility")
    if display_name is not None:
        body["display_name"] = display_name
    if not body:
        raise _fail(
            f"Failed to update dataset {dataset}: no field to change was given",
            "Provide at least one: --description / --visibility / --display-name",
            exit_code=2,
        )

    repo = _dataset_repo()
    try:
        record = repo.datasets.update(dataset, **body)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        if getattr(exc, "status", None) == 403:
            raise _fail(
                f"Failed to update dataset {dataset}: {_reason(exc)}",
                f"Governance fields like visibility require dataset-admin: ask an admin to run "
                f"ap dataset access grant {dataset} --user <you> --role admin",
            ) from exc
        raise _fail(
            f"Failed to update dataset {dataset}: {_reason(exc)}",
            f"Check the field values and retry: ap dataset get {dataset}",
        ) from exc
    _emit_detail(_model_dict(record) or {"dataset": dataset}, output_format)


def dataset_claim(
    dataset: str = typer.Argument(..., help="Dataset name"),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", help="Workspace (queue) id to claim into; required by the server"
    ),
    benchmark: Optional[str] = typer.Option(
        None, "--benchmark", help="Benchmark name or source_id to bind while claiming"
    ),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Claim an unclaimed dataset. The caller becomes its dataset admin."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    env = _environment(environment)
    repo = _dataset_repo()
    try:
        detail = _model_dict(
            repo.datasets.get_detail(
                dataset, **_read_env_kwargs(repo, repo.datasets, "get_detail", env)
            )
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"dataset {dataset}: pre-claim query failed: {_reason(exc)}",
            f"Check the dataset name: ap dataset list --query {dataset}",
        ) from exc
    dataset_id = str(detail.get("dataset_id") or "").strip()
    if not dataset_id:
        raise _fail(
            f"dataset {dataset}: pre-claim query failed: the server returned no dataset_id",
            "The dataset may be a placeholder shell; confirm with ap dataset get, then retry",
        )

    if not detail.get("claimable", False):
        # 幂等:已认领就不是错误(设计 §4.1),stdout 仍按 --format 输出现状。
        owner = str(detail.get("owner") or "").strip() or "<unknown>"
        _emit_detail(
            {
                "dataset": dataset,
                "dataset_id": dataset_id,
                "owner": owner,
                "workspace_id": detail.get("workspace_id") or "",
                "claimed": True,
                "claimable": False,
            },
            output_format,
        )
        return

    if not (workspace or "").strip():
        candidates: list[Any] = []
        candidate_error = ""
        try:
            candidates = repo.datasets.list_claim_workspaces() or []
        except Exception as exc:  # noqa: BLE001 - 列不出来不影响报用法错
            candidate_error = _reason(exc)
        choices: list[str] = []
        for item in candidates:
            queue_id = str(getattr(item, "queue_id", "") or getattr(item, "id", "") or "").strip()
            name = str(getattr(item, "name", "") or "").strip()
            if not queue_id and isinstance(item, dict):
                queue_id = str(item.get("queue_id") or item.get("id") or "")
                name = str(item.get("name") or "")
            if queue_id:
                choices.append(f"{queue_id} ({name})" if name else queue_id)
        if choices:
            hint = f"Available workspaces: {', '.join(choices)}; "
        elif candidate_error:
            hint = f"Failed to list available workspaces: {candidate_error}; "
        else:
            hint = ""
        hint += f"Run ap dataset claim {dataset} --workspace <queue-id> --benchmark <benchmark>"
        raise _fail(
            f"Failed to claim dataset {dataset}: the server requires workspace_id, but --workspace was not given",
            hint,
            exit_code=2,
        )

    benchmark_id = _resolve_benchmark_id(repo, benchmark) if benchmark else ""

    from .irepo_sdk import _reason

    try:
        # 认领走 SDK(POST /series/{id}/claim);未给 benchmark 时不做本地强制,
        # 由服务端决定是否要求绑定(与旧直连行为一致)。
        record = repo.datasets.claim(
            dataset_id,
            workspace.strip(),
            benchmark_id,
            require_benchmark=bool(benchmark_id),
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        code = _business_code(exc)
        if code == 92010:
            # 已被认领:以服务端 92010 为准(不本地推断),幂等 exit 0。
            owner = str(detail.get("owner") or "").strip()
            if not owner:
                try:
                    fresh = _model_dict(
                        repo.datasets.get_detail(
                            dataset, **_read_env_kwargs(repo, repo.datasets, "get_detail", env)
                        )
                    )
                    owner = str(fresh.get("owner") or "").strip()
                except Exception:  # noqa: BLE001 - 取不到 owner 不影响幂等退出
                    owner = ""
            owner = owner or "<unknown>"
            _emit_detail(
                {
                    "dataset": dataset,
                    "dataset_id": dataset_id,
                    "owner": owner,
                    "claimed": True,
                    "claimable": False,
                },
                output_format,
            )
            return
        hint = (
            _DATASET_CODE_HINTS.get(code)
            or "Make sure you have workspace-admin permission in that workspace, or use another --workspace"
        )
        raise _fail(
            f"Failed to claim dataset {dataset}: {_reason(exc)}",
            hint,
        ) from exc
    _emit_detail(record if isinstance(record, dict) else {"dataset": dataset}, output_format)


# ---------------------------------------------------------------------------
# ap dataset access
# ---------------------------------------------------------------------------


@dataset_access_app.command("list")
def dataset_access_list(
    dataset: str = typer.Argument(..., help="Dataset name"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List the dataset-level role bindings (who can read / write this dataset)."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    repo = _dataset_repo()

    try:
        series = repo.datasets.get(dataset)
        dataset_id = str(getattr(series, "dataset_id", "") or "")
        rows = _bindings(repo, dataset)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"dataset {dataset}: failed to list grants: {_reason(exc)}",
            "dataset-admin is required to view bindings; or make sure dataset RBAC is enabled in this environment",
        ) from exc
    _emit(
        {"dataset": dataset, "dataset_id": dataset_id, "access": rows},
        rows,
        _ACCESS_COLUMNS,
        output_format,
    )


@dataset_access_app.command("grant")
def dataset_access_grant(
    dataset: str = typer.Argument(..., help="Dataset name"),
    user: str = typer.Option(..., "--user", help="Grantee uid (or user_group id)"),
    role: str = typer.Option(..., "--role", help=f"Role to grant: {'/'.join(_ROLES)}"),
    principal_type: str = typer.Option(
        "user", "--principal-type", help=f"Principal type: {'/'.join(_PRINCIPAL_TYPES)}"
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Grant a dataset role to a user or user group (repeat = change the role)."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    resolved_role = _check_choice(role, _ROLES, "--role")
    resolved_type = _check_choice(principal_type, _PRINCIPAL_TYPES, "--principal-type")
    principal_id = user.strip()

    repo = _dataset_repo()
    try:
        series = repo.datasets.get(dataset)
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"dataset {dataset}: pre-grant query failed: {_reason(exc)}",
            f"Check the dataset name: ap dataset list --query {dataset}",
        ) from exc
    dataset_id = str(getattr(series, "dataset_id", "") or "")
    if not dataset_id:
        raise _fail(
            f"dataset {dataset}: pre-grant query failed: the server returned no dataset_id",
            "The dataset may be a placeholder shell; confirm with ap dataset get, then retry",
        )

    # 重复 grant 视为"更新角色":先撤掉该 principal 的其它角色,再授新角色(设计 §4.1)。
    replaced: list[str] = []
    for existing in _bindings_of(repo, dataset, principal_id, resolved_type):
        stale = existing["role"]
        if stale == resolved_role or stale not in _ROLE_IDS:
            continue
        try:
            repo.datasets.revoke(dataset, principal_id, stale, principal_type=resolved_type)
        except Exception as exc:  # noqa: BLE001
            code = _business_code(exc)
            if code == 92011:
                raise _fail(
                    f"dataset {dataset}: failed to revoke old role {stale}: {_reason(exc)}",
                    _last_admin_hint(dataset),
                ) from exc
            if code != 24401:
                raise _fail(
                    f"dataset {dataset}: failed to revoke old role {stale}: {_reason(exc)}",
                    f"Revoke it manually first: ap dataset access revoke {dataset} "
                    f"--user {principal_id} --role {stale}",
                ) from exc
        else:
            replaced.append(stale)

    already = False
    try:
        repo.datasets.grant(dataset, principal_id, resolved_role, principal_type=resolved_type)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        code = _business_code(exc)
        if code == 24404:
            already = True
        elif code == 24402:
            raise _fail(
                f"dataset {dataset}: grant failed: invalid arguments ({_reason(exc)})",
                "Check that the uid/user-group id matches --principal-type",
                exit_code=2,
            ) from exc
        else:
            hint = "Granting requires dataset-admin; if the dataset is not claimed, run ap dataset claim first"
            if replaced:
                # 撤旧授新不是原子操作:grant 失败时旧角色已没了,必须把恢复命令交给用户。
                hint = (
                    f"Old roles {', '.join(replaced)} were revoked but granting the new role failed; "
                    f"restore access first: ap dataset access grant {dataset} "
                    f"--user {principal_id} --role <{'/'.join(replaced)}>"
                )
            raise _fail(
                f"dataset {dataset}: grant failed: {_reason(exc)}",
                hint,
            ) from exc

    _emit_detail(
        {
            "dataset": dataset,
            "dataset_id": dataset_id,
            "principal_type": resolved_type,
            "principal_id": principal_id,
            "role": resolved_role,
            "already_granted": already,
            "replaced_roles": replaced,
        },
        output_format,
    )


@dataset_access_app.command("revoke")
def dataset_access_revoke(
    dataset: str = typer.Argument(..., help="Dataset name"),
    user: str = typer.Option(..., "--user", help="Grantee uid (or user_group id)"),
    role: Optional[str] = typer.Option(
        None, "--role", help=f"Role to revoke ({'/'.join(_ROLES)}); omit to revoke every role"
    ),
    principal_type: str = typer.Option(
        "user", "--principal-type", help=f"Principal type: {'/'.join(_PRINCIPAL_TYPES)}"
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Revoke a dataset role (or every role) from a user or user group."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    resolved_role = _check_choice(role, _ROLES, "--role") if role else ""
    resolved_type = _check_choice(principal_type, _PRINCIPAL_TYPES, "--principal-type")
    principal_id = user.strip()

    repo = _dataset_repo()
    try:
        series = repo.datasets.get(dataset)
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"dataset {dataset}: pre-revoke query failed: {_reason(exc)}",
            f"Check the dataset name: ap dataset list --query {dataset}",
        ) from exc
    dataset_id = str(getattr(series, "dataset_id", "") or "")

    if resolved_role:
        targets = [resolved_role]
    else:
        targets = [
            row["role"]
            for row in _bindings_of(repo, dataset, principal_id, resolved_type)
            if row["role"] in _ROLE_IDS
        ]
        if not targets:
            _emit_detail(
                {
                    "dataset": dataset,
                    "dataset_id": dataset_id,
                    "principal_type": resolved_type,
                    "principal_id": principal_id,
                    "revoked_roles": [],
                    "missing_roles": [],
                },
                output_format,
            )
            return

    revoked: list[str] = []
    missing: list[str] = []
    for target in targets:
        try:
            repo.datasets.revoke(dataset, principal_id, target, principal_type=resolved_type)
        except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
            code = _business_code(exc)
            if code == 24401:
                missing.append(target)
                continue
            if code == 24402:
                raise _fail(
                    f"dataset {dataset}: revoke failed: invalid arguments ({_reason(exc)})",
                    "Check that the uid/user-group id matches --principal-type",
                    exit_code=2,
                ) from exc
            if code == 92011:
                raise _fail(
                    f"dataset {dataset}: failed to revoke {target}: {_reason(exc)}",
                    _last_admin_hint(dataset),
                ) from exc
            raise _fail(
                f"dataset {dataset}: failed to revoke {target}: {_reason(exc)}",
                "Revoking requires dataset-admin; make sure dataset RBAC is enabled in this environment",
            ) from exc
        else:
            revoked.append(target)

    _emit_detail(
        {
            "dataset": dataset,
            "dataset_id": dataset_id,
            "principal_type": resolved_type,
            "principal_id": principal_id,
            "revoked_roles": revoked,
            "missing_roles": missing,
        },
        output_format,
    )


# ---------------------------------------------------------------------------
# ap dataset version
# ---------------------------------------------------------------------------


@dataset_version_app.command("list")
def dataset_version_list(
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    status: Optional[str] = typer.Option(
        None, "--status", help=f"Filter by status: {'/'.join(_VERSION_STATUSES)}"
    ),
    page: int = typer.Option(1, "--page", help="Page number"),
    page_size: int = typer.Option(20, "--page-size", help="Page size"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List versions of a dataset."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    resolved_status = _check_choice(status, _VERSION_STATUSES, "--status") if status else ""
    env = _environment(environment)
    model = _metadata_model(metadata_model)

    repo = _dataset_repo()
    try:
        result = repo.versions.list_paged(
            dataset,
            status=resolved_status or None,
            page=page,
            page_size=page_size,
            **({"metadata_model": model} if model else {}),
            **_read_env_kwargs(repo, repo.versions, "list_paged", env),
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"dataset {dataset}: failed to list versions: {_reason(exc)}",
            f"Check the dataset name: ap dataset list --query {dataset}",
        ) from exc

    records = [_registered_dict(record) for record in (getattr(result, "items", None) or [])]
    rows = [_version_row(record) for record in records]
    _emit(
        {"dataset": dataset, "versions": records, "pagination": _pagination_envelope(result)},
        rows,
        _VERSION_COLUMNS,
        output_format,
    )


@dataset_version_app.command("get")
def dataset_version_get(
    version: str = typer.Argument(..., help="Dataset version"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Show version detail: status, splits, manifest stats and published_at."""
    output_format = _fmt(output_format)
    resolved = _version_value(version)
    detail = _fetch_version(dataset, resolved, stage="query", environment=environment)
    _emit_detail(_registered_dict(detail), output_format, order=_VERSION_DETAIL_ORDER)


@dataset_version_app.command("create")
def dataset_version_create(
    version: str = typer.Argument(..., help="Dataset version to create"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    storage_path: Optional[str] = typer.Option(
        None,
        "--storage-path",
        help="Explicit oss:// storage path (otherwise auto-computed from data-plane addressing)",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Create a draft version. storage_path is auto-computed from data-plane addressing."""
    from .irepo_sdk import SdkMissing, _is_addressing_failure, _reason, load_repo, sdk_error_exit

    output_format = _fmt(output_format)
    env = _environment(environment)
    resolved = _version_value(version)
    if not resolved:
        raise _fail(
            f"dataset {dataset}: version creation failed: version must not be empty",
            f"{_NO_VERSION_NOTE}; a non-empty version name is required to create a version",
            exit_code=2,
        )

    # 服务端(92005)要求 storage_path 必传;SDK versions.create 按 repo-config
    # 发现的 bucket/prefix 自动计算,CLI 不再自拼 OSS URL。存储永远继承集群绑定
    # 的桶(设计 §4.2):加载后先做同侧校验,异侧写直接教学式报错。
    try:
        repo = load_repo()
    except SdkMissing as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc
    except Exception as exc:  # noqa: BLE001 - SDK configuration errors use the CLI error contract
        sdk_error_exit(exc, what="storage config", stage="resolve")
    _check_storage_side(repo, env)
    create_kwargs = _env_kwargs(env)
    explicit_storage_path = str(storage_path or "").strip()
    if explicit_storage_path:
        create_kwargs["storage_path"] = explicit_storage_path
    try:
        record = repo.versions.create(dataset, resolved, **create_kwargs)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        if _is_addressing_failure(exc):
            raise _fail(
                f"dataset {dataset}: failed to create version {resolved}: {_reason(exc)}",
                "Set AP_CLUSTER, or use ap --cluster <cluster> before the command; "
                "you can also pass --storage-path oss://<bucket>/<prefix>/",
            ) from exc
        sdk_error_exit(exc, what=f"dataset {dataset} version {resolved}", stage="create")
    # 与 ``version get`` 同一个视图:同一个对象在两个命令里字段集、字段顺序、空值处理
    # 必须一致(``to_dict()`` 原样输出会把 SDK 补的 False/[]/{} 也打出来)。
    _emit_detail(
        _model_dict(record) or {"dataset": dataset, "version": resolved},
        output_format,
        order=_VERSION_DETAIL_ORDER,
    )


@dataset_version_app.command(
    "publish",
    hidden=True,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def dataset_version_publish(
    version: str = typer.Argument(..., help="Legacy version argument"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
):
    """Explain the migration to split-scoped publishing without submitting anything."""
    raise _fail(
        "Publishing is now split-scoped; pick a split explicitly",
        f"ap dataset split publish <split> --dataset {dataset} --version {version}",
        exit_code=2,
    )


# ---------------------------------------------------------------------------
# ap dataset split
# ---------------------------------------------------------------------------


@dataset_split_app.command("list")
def dataset_split_list(
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    run_type: Optional[str] = typer.Option(
        None, "--run-type", help=f"Filter by run type: {'/'.join(_RUN_TYPES)} (client-side)"
    ),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List the splits of a version, or of the version-less (split_first) space."""
    output_format = _fmt(output_format)
    resolved_version = _version_value(version)
    resolved_run_type = _check_choice(run_type, _RUN_TYPES, "--run-type") if run_type else ""

    if resolved_version:
        records = _versioned_splits(
            dataset, resolved_version, stage="split query", environment=environment
        )
        rows = [_split_row(record, {}) for record in records]
    else:
        records = _unversioned_splits(dataset, stage="split query", environment=environment)
        rows = [_split_row(record, {}) for record in records]
    if resolved_run_type:
        rows = [row for row in rows if str(row["run_type"]).lower() == resolved_run_type]
    _emit(
        {"dataset": dataset, "version": resolved_version, "splits": rows},
        rows,
        _SPLIT_COLUMNS,
        output_format,
    )


@dataset_split_app.command("get")
def dataset_split_get(
    split: str = typer.Argument(..., help="Split name"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Show one split of a version, or of the version-less (split_first) space."""
    output_format = _fmt(output_format)
    resolved_version = _version_value(version)

    if resolved_version:
        record = _versioned_split(
            dataset, resolved_version, split, environment=environment
        )
        if record is not None:
            payload = dict(record)
            payload.setdefault("dataset", dataset)
            payload.setdefault("version", resolved_version)
            payload.setdefault("registered", True)
            _emit_detail(payload, output_format)
            return
        known = (
            ", ".join(
                _split_names_of(
                    _versioned_splits(
                        dataset, resolved_version, stage="split query", environment=environment
                    )
                )
            )
            or "<none>"
        )
    else:
        record = _unversioned_split(dataset, split, environment=environment)
        if record is not None:
            payload = dict(record)
            payload.setdefault("dataset", dataset)
            payload.setdefault("version", "")
            payload.setdefault("registered", True)
            _emit_detail(payload, output_format)
            return
        known = (
            ", ".join(
                _split_names_of(
                    _unversioned_splits(dataset, stage="split query", environment=environment)
                )
            )
            or "<none>"
        )

    raise _fail(
        f"dataset {dataset} version {_version_label(resolved_version)} split {split}: query failed: not found",
        f"Existing splits in this {'version' if resolved_version else 'dataset (no version space)'}: {known}"
        + ("" if resolved_version else f"; {_NO_VERSION_NOTE}"),
    )


@dataset_split_app.command("create")
def dataset_split_create(
    split: str = typer.Argument(..., help="Split name to create"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    run_type: Optional[str] = typer.Option(
        None, "--run-type", help=f"Run type to tag the split with: {'/'.join(_RUN_TYPES)}"
    ),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Add a split to a version (PATCH version.splits; no split resource exists)."""
    output_format = _fmt(output_format)
    resolved_version = _version_value(version)
    resolved_run_type = _check_choice(run_type, _RUN_TYPES, "--run-type") if run_type else ""

    if not resolved_version:
        # 无版本空间**没有创建接口**:recordsvc 的 /datasets/splits 只有 GET/GET detail/
        # PATCH detail(仅 run_type),split 记录由 ingest 扫 OSS 时落库;而
        # PATCH /datasets/versions/detail 又不接受空 version。迁移前后都是如此,不是 SDK 限制。
        raise _fail(
            f"Failed to create split {split} of dataset {dataset}: the version-less space has no create API",
            f"Split records in the version-less space are produced by the data plane: instance files "
            f"must exist under {dataset}/{split}/ first, then run ingest (console, or SDK "
            f"versions.ingest(dataset, splits=['{split}'], "
            f'metadata_model="split_first")); the record appears afterwards, then use ap dataset split update '
            f"to set run_type; the server rejects an empty directory (split path has no instance files); "
            f"to create an empty split manually, pass --version <version>",
            exit_code=2,
        )

    # 版本化创建走独立 Split API（POST /datasets/splits），与 split-first 服务端
    # 契约对齐——旧 Version PATCH（splits 全量替换 / split_run_types）已被服务端
    # 拒绝（"split-first Version group updates are not supported"）。
    env = _environment(environment)
    existing = _versioned_split(dataset, resolved_version, split, environment=environment)
    if existing is not None:
        # 幂等:已存在同名 split(设计 §4.3)。
        payload = dict(existing)
        payload.setdefault("dataset", dataset)
        payload.setdefault("version", resolved_version)
        payload["created"] = False
        _emit_detail(payload, output_format)
        return

    from .instance_commands import _sdk_read_kwargs
    from .irepo_sdk import _reason

    repo = _dataset_repo()
    create_kwargs = _sdk_read_kwargs(repo.splits, "create", environment=env, metadata_model="")
    if resolved_run_type:
        create_kwargs["run_type"] = resolved_run_type
    try:
        record = repo.splits.create(dataset, split, version=resolved_version, **create_kwargs)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to create split {split} of dataset {dataset} version {resolved_version}: {_reason(exc)}",
            "Check the version name and write permission, then retry",
        ) from exc
    payload = _model_dict(record) if record is not None else {}
    payload.setdefault("dataset", dataset)
    payload.setdefault("version", resolved_version)
    payload.setdefault("split", split)
    payload["created"] = True
    _emit_detail(payload, output_format)


@dataset_split_app.command("update")
def dataset_split_update(
    split: str = typer.Argument(..., help="Split name"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    run_type: Optional[str] = typer.Option(
        None, "--run-type", help=f"New run type: {'/'.join(_RUN_TYPES)} (required)"
    ),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Retag a split's run type (PATCH version.split_run_types, or the split record)."""

    output_format = _fmt(output_format)
    resolved_version = _version_value(version)
    if not run_type:
        raise _fail(
            f"Failed to update split {split}: no field to change was given",
            "Only run_type can be changed on a split: --run-type " + "/".join(_RUN_TYPES),
            exit_code=2,
        )
    resolved_run_type = _check_choice(run_type, _RUN_TYPES, "--run-type")

    if not resolved_version:
        # 无版本空间改 run_type 走 recordsvc 的 split 记录(PATCH /datasets/splits/detail):
        # 写端点仅限 online——SDK 1.1.2 起派生/显式 pre 都会前置 SchemaError 拒绝,
        # 不再出现"存在性检查读 pre、写入默默落 online"的读写环境撕裂。
        env = _environment(environment)
        if env == "pre":
            raise _fail(
                f"Failed to update split {split} of dataset {dataset}: split records can only be changed in the online environment",
                "PATCH on version-less split records only supports online; drop --environment pre, "
                "or use a version-scoped run_type (--version <version>)",
                exit_code=2,
            )
        if _unversioned_split(dataset, split, environment=environment) is None:
            known = (
                ", ".join(
                    _split_names_of(
                        _unversioned_splits(
                            dataset, stage="split update precheck", environment=environment
                        )
                    )
                )
                or "<none>"
            )
            raise _fail(
                f"Failed to update split {split} of dataset {dataset} (no version space): not found",
                f"Existing splits in this dataset's version-less space: {known}; {_NO_VERSION_NOTE}",
            )
        from .instance_commands import _sdk_read_kwargs
        from .irepo_sdk import _reason

        repo = _dataset_repo()
        # 写请求与上面的存在性预检查同口径路由环境(缺省 online);auto 由
        # _sdk_read_kwargs 省略下发,跟随集群绑定。旧 SDK 不接受 environment 时
        # 按显式值报升级提示,不静默忽略。
        update_kwargs = _sdk_read_kwargs(repo.splits, "update", environment=env, metadata_model="")
        try:
            repo.splits.update(dataset, split, run_type=resolved_run_type, **update_kwargs)
        except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
            raise _fail(
                f"Failed to update split {split} of dataset {dataset} (no version space): {_reason(exc)}",
                "Write permission on this dataset is required; check the split name and the online environment, then retry",
            ) from exc
        _emit_detail(
            {
                "dataset": dataset,
                "version": "",
                "split": split,
                "run_type": resolved_run_type,
                "updated": True,
            },
            output_format,
        )
        return

    # 版本化更新走独立 Split API（PATCH /datasets/splits/detail），预检用精确
    # split 身份（splits.get with version）——旧实现查 Version 内嵌 splits 再
    # PATCH Version，与独立 Split 记录不匹配，导致"已存在却报 not found"。
    env = _environment(environment)
    if env == "pre":
        raise _fail(
            f"Failed to update split {split} of dataset {dataset}: split records can only be changed in the online environment",
            "PATCH on split records only supports online; drop --environment pre",
            exit_code=2,
        )
    record = _versioned_split(dataset, resolved_version, split, environment=environment)
    if record is None:
        known = (
            ", ".join(
                _split_names_of(
                    _versioned_splits(
                        dataset, resolved_version, stage="split update precheck",
                        environment=environment,
                    )
                )
            )
            or "<none>"
        )
        raise _fail(
            f"dataset {dataset} version {_version_label(resolved_version)} split {split}: "
            f"update failed: not found",
            f"Create it first: ap dataset split create {split} --dataset {dataset} "
            f"--version {resolved_version} (existing: {known})",
        )

    from .instance_commands import _sdk_read_kwargs
    from .irepo_sdk import _reason

    repo = _dataset_repo()
    update_kwargs = _sdk_read_kwargs(repo.splits, "update", environment=env, metadata_model="")
    try:
        repo.splits.update(dataset, split, version=resolved_version, run_type=resolved_run_type, **update_kwargs)
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to update split {split} of dataset {dataset} version {resolved_version}: {_reason(exc)}",
            "Write permission on this dataset is required; check the split name and the online environment, then retry",
        ) from exc
    _emit_detail(
        {
            "dataset": dataset,
            "version": resolved_version,
            "split": split,
            "run_type": resolved_run_type,
            "updated": True,
        },
        output_format,
    )
