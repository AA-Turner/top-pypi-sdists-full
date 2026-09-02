"""Module containing helper functions related to eumdac configuration files"""

import os
from pathlib import Path


def get_config_dir() -> Path:
    """Path to the configuration directory of eumdac"""
    return Path(os.getenv("EUMDAC_CONFIG_DIR", (Path.home() / ".eumdac")))


def get_credentials_path() -> Path:
    """Path to the credentials of eumdac"""
    return get_config_dir() / "credentials"


def get_url_path() -> Path:
    """Path to the tailor configurations of eumdac"""
    r = get_config_dir() / "url"
    r.mkdir(parents=True, exist_ok=True)
    return r


# Configuration for download_app.py
download_app_max_chunk_download_attempts = 5

# Configuration for tailor_app.py
tailor_app_quota_percentage_warning = 90
tailor_app_max_retries = 5
