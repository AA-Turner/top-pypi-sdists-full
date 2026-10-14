import os


def _resolve_downloads_dir() -> str:
    env_path = os.getenv("TESTMU_DOWNLOAD_PATH", "").strip()
    if env_path:
        return env_path
    return os.path.join(os.path.expanduser("~"), "Downloads")


def downloads_path(name: str) -> str:
    return os.path.join(_resolve_downloads_dir(), name)
