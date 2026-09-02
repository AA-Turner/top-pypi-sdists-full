"""
Configuration Schema for InnoDay Services

Defines the configuration structure for the unified service management system.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class APIConfig:
    """Configuration for the InnoDay API service."""

    enabled: bool = True
    host: str = "0.0.0.0"
    port: int = 8002
    reload: bool = False
    workers: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DatabaseConfig:
    """Configuration for database connections."""

    url: str = "sqlite:///innoday.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    console_enabled: bool = True
    max_file_size: str = "10MB"
    backup_count: int = 5

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InnoServiceConfig:
    """Main configuration for InnoDay platform services."""

    version: str = "0.10.0-beta"
    data_dir: str = "~/.innoday/data"

    # Service configurations
    api: APIConfig = None
    database: DatabaseConfig = None
    logging: LoggingConfig = None

    def __post_init__(self):
        """Initialize sub-configurations if not provided."""
        if self.api is None:
            self.api = APIConfig()
        if self.database is None:
            self.database = DatabaseConfig()
        if self.logging is None:
            self.logging = LoggingConfig()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for TOML serialization."""
        return {
            "innoday": {"version": self.version, "data_dir": self.data_dir},
            "api": self.api.to_dict(),
            "database": self.database.to_dict(),
            "logging": self.logging.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InnoServiceConfig":
        """Create configuration from dictionary."""
        innoday_config = data.get("innoday", {})

        return cls(
            version=innoday_config.get("version", "0.10.0-beta"),
            data_dir=innoday_config.get("data_dir", "~/.innoday/data"),
            api=APIConfig(**data.get("api", {})),
            database=DatabaseConfig(**data.get("database", {})),
            logging=LoggingConfig(**data.get("logging", {})),
        )

    def get_expanded_data_dir(self) -> Path:
        """Get data directory with home directory expansion."""
        return Path(self.data_dir).expanduser()


@dataclass
class ServiceStatus:
    """Status information for a service."""

    name: str
    display_name: str
    enabled: bool
    running: bool
    pid: Optional[int] = None
    port: Optional[int] = None
    uptime: Optional[float] = None  # seconds
    memory_usage: Optional[int] = None  # bytes
    cpu_percent: Optional[float] = None

    @property
    def status_text(self) -> str:
        """Get human-readable status text."""
        if not self.enabled:
            return "Disabled"
        elif self.running:
            return "Running"
        else:
            return "Stopped"

    @property
    def uptime_text(self) -> str:
        """Get human-readable uptime text."""
        if not self.uptime:
            return "N/A"

        hours, remainder = divmod(int(self.uptime), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    @property
    def memory_text(self) -> str:
        """Get human-readable memory usage text."""
        if not self.memory_usage:
            return "N/A"

        # Convert bytes to MB
        mb = self.memory_usage / (1024 * 1024)
        return f"{mb:.1f} MB"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "enabled": self.enabled,
            "running": self.running,
            "pid": self.pid,
            "port": self.port,
            "uptime": self.uptime,
            "uptime_text": self.uptime_text,
            "memory_usage": self.memory_usage,
            "memory_text": self.memory_text,
            "cpu_percent": self.cpu_percent,
            "status": self.status_text,
        }
