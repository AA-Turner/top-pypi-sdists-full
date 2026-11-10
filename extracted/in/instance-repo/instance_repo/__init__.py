"""instance_repo — 评测 Instance 统一存储 SDK（Python）。

唯一入口：所有 OSS/ACR 操作经 SDK，先向 apiserver 换 STS 再直连。控制面
（鉴权/元数据/STS/审计/release）全在 apiserver。
"""
from .repo import Repo
from .loader import load_instances
from .content import compute_source_hash
from .models import (
    DatasetSeries, DatasetVersion, DatasetInstance, ManifestEntry,
    OwnerReference, Feedback, Identity, IngestReport, RegistrationReport,
    PushResult, PushManyReport, RolloutReport, RolloutJob, ScaffoldConfig,
    DatasetObjectDirectory, DatasetObjectFile, DatasetObjectListResult,
    canonical_json, parse_feedbacks, append_feedback,
)
from .errors import (
    InstanceRepoError, LayoutError, SchemaError, OwnerRefMissing, ImageMissing,
    Immutable, DigestMismatch, Forbidden, NotVisible, TargetNotAllowed,
    NetworkDenied, CredExpired, PrivateNetworkRequired, WriteOutcomeUnknown,
    RegistrationFailed, TransportError,
)

__version__ = "1.4.7"

__all__ = [
    "Repo", "load_instances",
    "DatasetSeries", "DatasetVersion", "DatasetInstance", "ManifestEntry",
    "OwnerReference", "Feedback", "Identity", "IngestReport",
    "RegistrationReport", "PushResult", "PushManyReport",
    "RolloutReport", "RolloutJob", "ScaffoldConfig",
    "DatasetObjectDirectory", "DatasetObjectFile", "DatasetObjectListResult",
    "canonical_json", "parse_feedbacks", "append_feedback",
    "compute_source_hash",
    "InstanceRepoError", "LayoutError", "SchemaError", "OwnerRefMissing",
    "ImageMissing", "Immutable", "DigestMismatch", "Forbidden", "NotVisible",
    "TargetNotAllowed", "NetworkDenied", "CredExpired",
    "PrivateNetworkRequired", "WriteOutcomeUnknown", "RegistrationFailed",
    "TransportError", "__version__",
]
