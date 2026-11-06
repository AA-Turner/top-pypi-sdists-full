"""errors.py — InstanceRepo SDK 错误码与异常。

与 Go SDK 对等（同码值 ErrLayout/ErrImmutable/...）。所有异常携带稳定 ``code``
供跨语言对齐与日志对账。
"""
from __future__ import annotations


class InstanceRepoError(Exception):
    """SDK 异常基类；``code`` 为稳定错误码（与 Go 对齐）。

    ``data`` 为服务端错误响应里**可选结构化负载**（如 grant miss 的
    ``reason``/``apply_url``）。旧服务不带 data 时为空 dict（兼容默认），
    调用方 ``getattr(e, "data", {})`` 或直接 ``e.data`` 均安全。
    注意：``data`` 只作结构化读取，绝不拼进 message/repr（凭据等秘密值
    不因异常日志而泄漏），SDK 也不自动消费其中的 URL。
    """

    code = "E_UNKNOWN"

    def __init__(self, message: str = "", *, cause: BaseException | None = None,
                 data: dict | None = None) -> None:
        super().__init__(message or self.code)
        self.message = message or self.code
        self.__cause__ = cause
        # 非 dict（含 None/缺省）一律回退空 dict：旧服务无 data、data=null、
        # data 为字符串等场景都拿到稳定类型，免调用方逐处判空。
        self.data = data if isinstance(data, dict) else {}


class LayoutError(InstanceRepoError):
    code = "E_LAYOUT"


class SchemaError(InstanceRepoError):
    code = "E_SCHEMA"


class OwnerRefMissing(InstanceRepoError):
    code = "E_OWNER_REF_MISSING"


class ImageMissing(InstanceRepoError):
    code = "E_IMAGE_MISSING"


class Immutable(InstanceRepoError):
    code = "E_IMMUTABLE"


class DigestMismatch(InstanceRepoError):
    code = "E_DIGEST_MISMATCH"


class Forbidden(InstanceRepoError):
    code = "E_FORBIDDEN"


class NotVisible(InstanceRepoError):
    code = "E_NOT_VISIBLE"


class TargetNotAllowed(InstanceRepoError):
    code = "E_TARGET_NOT_ALLOWED"


class NetworkDenied(InstanceRepoError):
    code = "E_NETWORK_DENIED"


class CredExpired(InstanceRepoError):
    code = "E_CRED_EXPIRED"


class PrivateNetworkRequired(InstanceRepoError):
    code = "E_PRIVATE_NETWORK_REQUIRED"


class WriteOutcomeUnknown(InstanceRepoError):
    code = "E_WRITE_OUTCOME_UNKNOWN"


class BizCodeError(InstanceRepoError):
    """携带 apiserver 数字业务码的异常基类（Dataset RBAC 等数字码场景）。"""

    def __init__(self, message: str = "", *, status: int | None = None,
                 biz_code: int | None = None,
                 data: dict | None = None) -> None:
        super().__init__(message, data=data)
        self.status = status
        # 未显式传入时继承类属性里的数字业务码（如 DatasetAccessDenied.biz_code=94016）。
        self.biz_code = biz_code if biz_code is not None else getattr(self, "biz_code", None)


class DatasetAccessDenied(BizCodeError):
    code = "E_DATASET_ACCESS_DENIED"
    biz_code = 94016


class DatasetClaimRequired(BizCodeError):
    code = "E_DATASET_CLAIM_REQUIRED"
    biz_code = 94017


class DatasetWriteDenied(BizCodeError):
    code = "E_DATASET_WRITE_DENIED"
    biz_code = 94018


class DatasetIdentifierConflict(BizCodeError):
    code = "E_DATASET_IDENTIFIER_CONFLICT"
    biz_code = 94019


class DatasetIdentifierRequired(BizCodeError):
    code = "E_DATASET_IDENTIFIER_REQUIRED"
    biz_code = 94020


class DatasetNotFound(BizCodeError):
    code = "E_DATASET_NOT_FOUND"
    biz_code = 94021


class TransportError(InstanceRepoError):
    """apiserver HTTP 非预期响应。

    ``status`` 为 HTTP 状态码（若由 HTTP 层抛出）；契约破坏等非 HTTP 场景为 None。
    重试逻辑据此区分 5xx（瞬时可重试）与 4xx（永不重试）。
    ``biz_code`` 为 apiserver 的**数字业务码**（如 92001 dataset not found、
    92003 dataset instance not found）——两者同为 HTTP 404 但语义不同：调用方需据此
    区分"实例不存在"（可返回 None）与"数据集不存在"（应报错，避免吞掉拼错的名字）。
    """

    code = "E_TRANSPORT"

    def __init__(self, message: str = "", *, status: int | None = None,
                 biz_code: int | None = None, report=None,
                 cause: BaseException | None = None,
                 data: dict | None = None) -> None:
        super().__init__(message, cause=cause, data=data)
        self.status = status
        self.biz_code = biz_code
        self.report = report
        # data 由基类归一化（非 dict → {}），不在此重复处理。


class RequestDeadlineExceeded(TransportError):
    """调用方显式给定的总预算（deadline）耗尽——**本地**信号（非服务器
    响应，不携带任何远端数据；retry/transport 层共享的 safe 异常形态）。

    与超时类传输错误的区别：这是**编排预算**（请求发出前/后判定），
    不是单次 socket 超时；调用方可据此区分"预算用尽"与"网络慢"。
    transport/retry 层使用；**禁止** import client 层模块（依赖方向：
    errors ← retry/transport ← clients）。"""
    code = "E_REQUEST_DEADLINE"


class JobFailed(InstanceRepoError):
    """远端异步作业到达失败终态（dataset-ingest 或 benchmark-release workflow）。

    ``status`` 为终态字符串（如 ``failed``/``canceled``）；``job`` 为最后一次拉到的
    原始作业/工作流 dict，供诊断。ingest/publish 轮询到失败终态时抛出，避免"调用返回
    正常、实际未成功"的静默失败。
    """

    code = "E_JOB_FAILED"

    def __init__(self, message: str = "", *, status: str | None = None,
                 job: dict | None = None, report=None) -> None:
        super().__init__(message)
        self.status = status
        self.job = job
        self.report = report


class RegistrationFailed(InstanceRepoError):
    """Incremental registration stopped with a cumulative diagnostic report."""

    code = "E_REGISTRATION_FAILED"

    def __init__(self, message: str = "", *, report=None,
                 cause: BaseException | None = None) -> None:
        super().__init__(message, cause=cause)
        self.report = report


# apiserver 业务错误码 → SDK 异常类映射（transport 层用）。
CODE_TO_EXC: dict[str, type[InstanceRepoError]] = {
    e.code: e
    for e in (
        LayoutError, SchemaError, OwnerRefMissing, ImageMissing, Immutable,
        DigestMismatch, Forbidden, NotVisible, TargetNotAllowed, NetworkDenied,
        CredExpired, PrivateNetworkRequired, WriteOutcomeUnknown,
        DatasetAccessDenied, DatasetClaimRequired, DatasetWriteDenied,
        DatasetIdentifierConflict, DatasetIdentifierRequired, DatasetNotFound,
    )
}

# apiserver 数字业务码 → SDK 异常类映射（Dataset RBAC 等仅返回数字码的场景）。
BIZ_CODE_TO_EXC: dict[int, type[BizCodeError]] = {
    e.biz_code: e
    for e in (
        DatasetAccessDenied, DatasetClaimRequired, DatasetWriteDenied,
        DatasetIdentifierConflict, DatasetIdentifierRequired, DatasetNotFound,
    )
}


def exc_for_code(code: str, message: str = "",
                 data: dict | None = None) -> InstanceRepoError:
    """按 apiserver 返回的 code 构造对应异常；未知 code 回退 TransportError。

    ``data`` 为错误响应可选结构化负载（非 dict 安全回退 {}）。
    **不设 status**（R1返修①）：base 语义中字符串码路径的异常从不携带 status
    （重试策略 is_transient 依赖这一点——一旦补 status，503 等会误触发
    retry_transient 重试，改变调用次数语义）。数字业务码请走 exc_for_biz_code。
    """
    cls = CODE_TO_EXC.get(code, TransportError)
    return cls(message, data=data)


def exc_for_biz_code(code: int, message: str = "", *,
                     status: int | None = None,
                     data: dict | None = None) -> InstanceRepoError:
    """按 apiserver 返回的数字业务码构造对应异常；未知码回退 TransportError。"""
    cls = BIZ_CODE_TO_EXC.get(code, TransportError)
    return cls(message, status=status, biz_code=code, data=data)
