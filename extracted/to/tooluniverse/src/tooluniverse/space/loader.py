"""
ToolUniverse Space Configuration Loader

Simplified loader supporting HuggingFace, local files, and HTTP/HTTPS.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml
import requests
from huggingface_hub import hf_hub_download

from ..utils import get_user_cache_dir
from .validator import validate_space_config


class SpaceLoader:
    """Simplified loader for ToolUniverse Space configurations."""

    def __init__(self, cache_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the Space loader.

        Args:
            cache_dir: Directory for caching downloaded configurations
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(get_user_cache_dir()) / "spaces"

        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, uri: str) -> Dict[str, Any]:
        """
        Load Space configuration from URI.

        Args:
            uri: Space URI (e.g., "hf:user/repo", "./config.yaml", "https://example.com/config.yaml")

        Returns
            Loaded configuration dictionary

        Raises:
            ValueError: If URI is unsupported or configuration is invalid
        """
        # Use URI directly (no alias resolution)
        resolved_uri = uri

        # Detect URI type
        if resolved_uri.startswith("hf:"):
            config = self._load_from_hf(resolved_uri)
        elif resolved_uri.startswith(("http://", "https://")):
            config = self._load_from_url(resolved_uri)
        else:
            config = self._load_from_file(resolved_uri)

        # Validate configuration
        is_valid, errors = validate_space_config(config)
        if not is_valid:
            error_msg = "Configuration validation failed:\n" + "\n".join(
                f"  - {e}" for e in errors
            )
            raise ValueError(error_msg)

        return config

    def _load_from_hf(self, uri: str) -> Dict[str, Any]:
        """Load configuration from HuggingFace Hub."""
        repo_id = uri[3:]  # Remove 'hf:' prefix

        try:
            # Try to download the config file
            config_path = hf_hub_download(
                repo_id=repo_id,
                filename="space.yaml",
                cache_dir=self.cache_dir,
                local_files_only=False,
            )
            return self._load_from_file(config_path)
        except Exception as e:
            # Fallback: try space.json
            try:
                config_path = hf_hub_download(
                    repo_id=repo_id,
                    filename="space.json",
                    cache_dir=self.cache_dir,
                    local_files_only=False,
                )
                return self._load_from_file(config_path)
            except Exception:
                raise ValueError(
                    f"Failed to load Space from HuggingFace {repo_id}: {e}"
                )

    def _load_from_url(self, uri: str) -> Dict[str, Any]:
        """Load configuration from HTTP/HTTPS URL."""
        try:
            response = requests.get(uri, timeout=30)
            response.raise_for_status()

            # Try YAML first, then JSON
            try:
                return yaml.safe_load(response.text)
            except yaml.YAMLError:
                return response.json()
        except Exception as e:
            raise ValueError(f"Failed to load Space from URL {uri}: {e}")

    def _load_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from local file."""
        path = Path(file_path)

        if not path.exists():
            raise ValueError(f"Space file not found: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.suffix.lower() in [".yaml", ".yml"]:
                    return yaml.safe_load(f)
                elif path.suffix.lower() == ".json":
                    return json.load(f)
                else:
                    # Try YAML first, then JSON
                    try:
                        f.seek(0)
                        return yaml.safe_load(f)
                    except yaml.YAMLError:
                        f.seek(0)
                        return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load Space from file {file_path}: {e}")
