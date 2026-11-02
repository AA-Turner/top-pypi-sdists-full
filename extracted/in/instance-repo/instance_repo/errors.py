"""errors.py — InstanceRepo SDK 错误码与异常。

与 Go SDK 对等（同码值 ErrLayout/ErrImmutable/...）。所有异常携带稳定 ``code``
供跨语言对齐与日志对账。
"""
from __future__ import annotations


class InstanceRepoError(Exception):
    """SDK 异常基类；``code`` 为稳定错误码（与 Go 对齐）。"""

    code = "E_UNKNOWN"

    def __init__(self, message: str = "", *, cause: BaseException | None = None) -> None:
        super().__init__(message or self.code)
        self.message = message or self.code
        self.__cause__ = cause


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
                 biz_code: int | None = None) -> None:
        super().__init__(message)
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
                 cause: BaseException | None = None) -> None:
        super().__init__(message, cause=cause)
        self.status = status
        self.biz_code = biz_code
        self.report = report


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


def exc_for_code(code: str, message: str = "") -> InstanceRepoError:
    """按 apiserver 返回的 code 构造对应异常；未知 code 回退 TransportError。"""
    cls = CODE_TO_EXC.get(code, TransportError)
    return cls(message)


def exc_for_biz_code(code: int, message: str = "", *,
                     status: int | None = None) -> InstanceRepoError:
    """按 apiserver 返回的数字业务码构造对应异常；未知码回退 TransportError。"""
    cls = BIZ_CODE_TO_EXC.get(code, TransportError)
    return cls(message, status=status, biz_code=code)
