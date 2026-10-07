"""
AGENTICSTAR Platform SDK - Database Module
PostgreSQL接続とクエリ実行の機能を提供
"""

from .config import AzureADConfig, PostgreSQLConfig
from .manager import PostgreSQLManager
from .api_manager import ApiPostgreSQLManager
from .factory import create_postgresql_manager
from .data_access import DataAccess
from .config_access import ConfigAccess
from .execution_access import ExecutionAccess
from .pod_runtime import PodRuntime
from .telemetry_access import TelemetryAccess
# サイクル型の完遂報告（指示書 37）。会話 runner を使わない Agent からも呼べるよう公開する
from .completion_report import report_completion

__all__ = [
    "PostgreSQLManager",
    "ApiPostgreSQLManager",
    "create_postgresql_manager",
    "PostgreSQLConfig",
    "AzureADConfig",
    "DataAccess",
    "ConfigAccess",
    "ExecutionAccess",
    "PodRuntime",
    "TelemetryAccess",
    "report_completion",
]
