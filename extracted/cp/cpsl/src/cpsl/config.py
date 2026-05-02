import configparser
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import MutableMapping, Optional, Union

DEFAULT_CONTEXT_NAME = "default"
DEFAULT_GATEWAY_HOST = "gateway.capsule.new"
DEFAULT_GATEWAY_PORT = 443


def _parse_gateway_url(raw: str) -> tuple[str, int]:
    """Parse a host:port string, defaulting port to 443 if omitted."""
    raw = raw.strip()
    if ":" in raw:
        host, port_s = raw.rsplit(":", 1)
        return host, int(port_s)
    return raw, DEFAULT_GATEWAY_PORT


@dataclass
class SDKSettings:
    name: str = "Capsule"
    gateway_host: str = DEFAULT_GATEWAY_HOST
    gateway_port: int = DEFAULT_GATEWAY_PORT
    gateway_http_port: Optional[int] = None
    config_path: Path = Path("~/.capsule/config.ini").expanduser()
    api_token: Optional[str] = os.getenv("CAPSULE_TOKEN")

    def __post_init__(self):
        if p := os.getenv("CONFIG_PATH"):
            self.config_path = Path(p).expanduser()

        if url := os.getenv("CAPSULE_GATEWAY_URL"):
            self.gateway_host, self.gateway_port = _parse_gateway_url(url)

        if hp := os.getenv("CAPSULE_HTTP_PORT"):
            self.gateway_http_port = int(hp)


@dataclass
class ConfigContext:
    token: Optional[str] = None
    gateway_host: Optional[str] = None
    gateway_port: Optional[int] = None
    gateway_http_port: Optional[int] = None

    @property
    def http_port(self) -> Optional[int]:
        """HTTP API port. Falls back to gateway_port (works when both sit behind the same LB)."""
        return self.gateway_http_port or self.gateway_port

    def to_dict(self) -> dict:
        return {k: ("" if not v else v) for k, v in asdict(self).items()}

    def is_valid(self) -> bool:
        return all([self.token, self.gateway_host, self.gateway_port])


_SETTINGS: Optional[SDKSettings] = None


def get_settings() -> SDKSettings:
    global _SETTINGS
    if not _SETTINGS:
        _SETTINGS = SDKSettings()
    return _SETTINGS


def set_settings(s: SDKSettings) -> None:
    global _SETTINGS
    _SETTINGS = s


def load_config(path: Optional[Union[str, Path]] = None) -> MutableMapping[str, ConfigContext]:
    if path is None:
        path = get_settings().config_path

    path = Path(path)
    if not path.exists():
        return {}

    parser = configparser.ConfigParser(default_section=DEFAULT_CONTEXT_NAME)
    parser.read(path)

    contexts: MutableMapping[str, ConfigContext] = {}
    for name, section in parser.items():
        port = section.get("gateway_port")
        http_port = section.get("gateway_http_port")
        contexts[name] = ConfigContext(
            token=section.get("token"),
            gateway_host=section.get("gateway_host"),
            gateway_port=int(port) if port else None,
            gateway_http_port=int(http_port) if http_port else None,
        )

    return contexts


def save_config(
    contexts: MutableMapping[str, ConfigContext],
    path: Optional[Union[Path, str]] = None,
) -> None:
    if not contexts:
        return

    if path is None:
        path = get_settings().config_path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    parser = configparser.ConfigParser(default_section=DEFAULT_CONTEXT_NAME)
    parser.read_dict({k: v.to_dict() for k, v in contexts.items()})

    with open(path, "w") as f:
        parser.write(f)


def is_config_empty(path: Optional[Union[Path, str]] = None) -> bool:
    if path is None:
        path = get_settings().config_path

    path = Path(path)
    return not path.exists()


def app_url(hostname: str) -> str:
    """Build the full URL for an app hostname based on the current gateway context."""
    ctx = get_config_context()
    if ctx and ctx.gateway_port not in (443, None):
        http_port = ctx.gateway_http_port or (ctx.gateway_port + 1)
        return f"http://{hostname}.localhost:{http_port}"
    return f"https://{hostname}.capsule.new"


def get_config_context(name: str = DEFAULT_CONTEXT_NAME) -> Optional[ConfigContext]:
    contexts = load_config()
    if name in contexts:
        return contexts[name]

    settings = get_settings()
    token = os.getenv("CAPSULE_TOKEN", settings.api_token)
    if token:
        return ConfigContext(
            token=token,
            gateway_host=settings.gateway_host,
            gateway_port=settings.gateway_port,
            gateway_http_port=settings.gateway_http_port,
        )

    return None
