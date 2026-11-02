"""DatasetName 解析 Adapter:唯一入口委托给已安装的 InstanceRepo SDK。

AP CLI 不维护第三套 dataset 名解析:``instance_repo.paths.DatasetName`` 是客户端
路径契约的唯一事实源(单段 ``A`` / 两段 ``A/B`` / 多段树形 ``A/B/C``,与
apiserver 的 namespace guard 及 conformance 契约对齐)。SDK 缺失或过旧(没有
``DatasetName.parse`` 能力)时,给出明确的升级提示,不静默降级、不本地重写解析规则。
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

__all__ = [
    "DatasetNameError",
    "DatasetNameUpgradeRequired",
    "parse_dataset_name",
]

#: SDK 缺失/无 DatasetName 能力时的升级提示(与 irepo_sdk 的 SdkMissing 同范式)。
_UPGRADE_HINT = (
    "The installed instance-repo SDK does not provide DatasetName parsing "
    "(single-segment L1 dataset names need it).\n"
    "Install it with: pip install 'ap-client[dataset]' --upgrade"
)

#: 多段(3+)名能力的首个 SDK 版本。旧 SDK(如 1.4.0)有 parse 但只认 1-2 段,
#: 对多段名会抛"one or two canonical segments"——此时应提示升级而非报名称非法。
_MULTI_LEVEL_SDK_VERSION = (1, 4, 1)


def _sdk_supports_multi_level() -> bool:
    """已安装 instance-repo 是否支持多段数据集名(>= 1.4.1)。版本不可读时保守视为不支持。"""
    try:
        from importlib.metadata import version

        installed = version("instance-repo")
    except Exception:  # noqa: BLE001 - 元数据缺失与旧 SDK 同等对待
        return False
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", str(installed))
    if not match:
        return False
    return tuple(int(part) for part in match.groups()) >= _MULTI_LEVEL_SDK_VERSION


def _is_structurally_valid_multi_level(value: str) -> bool:
    """值是否为"新 SDK 会接受"的 3+ 段名——即每个段都合法。

    旧 SDK 对非法名(空段 a//b、非法字符 a*b)与多段名报同一文案,不能只按
    段数判断:升级 SDK 也修不好空段/非法字符,必须保留原始校验错误。
    这里保守复刻 SDK 的非法段规则作为 gate,只放行结构上合法的多段名。
    """
    parts = value.split("/")
    if len(parts) < 3 or any(not part for part in parts):
        return False
    for part in parts:
        if (
            part in {".", ".."}
            or "\\" in part
            or "*" in part
            or "?" in part
            or any(unicodedata.category(char) == "Cc" for char in part)
        ):
            return False
    return True


class DatasetNameUpgradeRequired(RuntimeError):
    """已安装的 instance-repo SDK 缺少 DatasetName 能力,必须升级。"""


class DatasetNameError(ValueError):
    """Dataset 名不符合 IR DatasetName 契约(单段或两段、无非法段)。"""


def parse_dataset_name(value: str) -> Any:
    """Parse ``value`` through the installed IR ``DatasetName`` capability.

    Returns the SDK ``DatasetName`` (``canonical`` / ``l1`` / ``l2`` /
    ``segments`` / ``leaf``)。Raises :class:`DatasetNameUpgradeRequired` when the
    installed SDK lacks the capability (包括只认 1-2 段的旧 SDK 拒绝多段名);
    raises :class:`DatasetNameError` when the value is not a valid name.
    """
    try:
        from instance_repo.paths import DatasetName
    except ImportError as exc:
        raise DatasetNameUpgradeRequired(_UPGRADE_HINT) from exc
    parse = getattr(DatasetName, "parse", None)
    if not callable(parse):
        raise DatasetNameUpgradeRequired(_UPGRADE_HINT)
    try:
        return parse(value)
    except Exception as exc:  # noqa: BLE001 - SDK 校验失败统一转成 CLI 契约
        # 旧 SDK(1.4.0 及更早)只认 1-2 段:结构上合法的多段名被拒时给出
        # 升级提示。非法名(空段/非法字符)无论新旧 SDK 都拒绝,保留原始
        # 校验错误为 DatasetNameError——升级修不好这类名称。
        if (
            isinstance(value, str)
            and _is_structurally_valid_multi_level(value)
            and not _sdk_supports_multi_level()
        ):
            raise DatasetNameUpgradeRequired(_UPGRADE_HINT) from exc
        raise DatasetNameError(str(exc)) from exc
