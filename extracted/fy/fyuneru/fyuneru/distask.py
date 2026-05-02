import datetime
from enum import Enum
from dataclasses import dataclass, field

from .lib import get_uuid

# 分布式任务支持


class TaskStatus(Enum):
    FAILED = -1  # 失败
    SUCCEEDED = 0  # 成功
    PENDING = 1  # 等待
    RUNNING = 2  # 运行
    CANCELLED = 3  # 取消
    RETRYING = 4  # 重试
    TIMEOUT = 5  # 超时


@dataclass
class TaskId:
    tid: str = field(default_factory=get_uuid())
    timestamp: int = field(default=int(datetime.datetime.now().timestamp()))
    status: int = field(default=1)
    excute_id: str | None = field(default=None)
    args: dict = field(default_factory=dict)
